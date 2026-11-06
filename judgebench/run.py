"""CLI: build datasets, run baselines and judges, write per-item results.

  python -m judgebench.run build
  python -m judgebench.run baseline
  python -m judgebench.run judge <ollama-model | claude_haiku | gemini_flash> [task ...]
"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor

from . import baselines, datasets, judges
from .common import ROOT, read_jsonl, write_jsonl

RESULTS = ROOT / "results"
CLAUDE_WORKERS = 6
LATENCY_PROBE = 20


def run_baseline():
    meta = {}
    for task in datasets.TASKS:
        items = datasets.load(task)
        flagged, stats = baselines.run(task, items)
        rows = [{"id": it["id"], "verdict": "YES" if flagged[it["id"]] else "NO", "p_yes": None} for it in items]
        write_jsonl(RESULTS / f"baseline__{task}.jsonl", rows)
        meta[task] = {**stats, "items": len(items)}
    (RESULTS / "baseline__meta.json").write_text(json.dumps(meta, indent=2))


def _one(judge, task, it):
    try:
        if getattr(judge, "decisions", False):
            return {"id": it["id"], **judge.decide(datasets.PROMPT_TASK.get(task, task), it["text"])}
        return {"id": it["id"], **judge.ask(datasets.prompt_for(task, it["text"]))}
    except Exception as exc:
        return {"id": it["id"], "verdict": None, "p_yes": None, "latency_s": None, "error": str(exc)[:300]}


def run_judge(name, tasks):
    judge = judges.make(name)
    meta_path = RESULTS / f"{judge.name}__meta.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    for task in tasks:
        out = RESULTS / f"{judge.name}__{task}.jsonl"
        done = {r["id"]: r for r in read_jsonl(out) if not r.get("error")} if out.exists() else {}
        todo = [it for it in datasets.load(task) if it["id"] not in done]
        if getattr(judge, "hosted", False):
            with ThreadPoolExecutor(max_workers=CLAUDE_WORKERS) as pool:
                new = list(pool.map(lambda it: _one(judge, task, it), todo))
        else:
            new = [_one(judge, task, it) for it in todo]
            meta["loaded_bytes"] = judge.loaded_bytes()
        write_jsonl(out, list(done.values()) + new)
        print(task, len(new), "new,", sum(1 for r in new if r.get("error")), "errors", flush=True)
    meta_path.write_text(json.dumps(meta, indent=2))


def rederive(name):
    """Recompute verdicts of stored Ollama results from their probability (no model call)."""
    for path in RESULTS.glob(f"{name}__*.jsonl"):
        rows = read_jsonl(path)
        for r in rows:
            if r.get("p_yes") is not None and not r.get("error"):
                r["verdict"] = "YES" if r["p_yes"] >= 0.5 else "NO"
        write_jsonl(path, rows)


def run_latency_probe(name):
    """Hosted judges run in parallel, so per-item latency is probed one call at a time."""
    judge = judges.make(name)
    items = datasets.load("honorific")[:LATENCY_PROBE]
    times = [_one(judge, "honorific", it)["latency_s"] for it in items]
    meta_path = RESULTS / f"{judge.name}__meta.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    meta["sequential_latency_s"] = [t for t in times if t is not None]
    meta_path.write_text(json.dumps(meta, indent=2))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        print(json.dumps(datasets.manifest(), indent=2))
    elif cmd == "baseline":
        run_baseline()
    elif cmd == "rederive":
        rederive(sys.argv[2])
    elif cmd == "judge":
        run_judge(sys.argv[2], sys.argv[3:] or list(datasets.TASKS))
        if getattr(judges.make(sys.argv[2]), "hosted", False):
            run_latency_probe(sys.argv[2])
