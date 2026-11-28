"""Summary of the three follow-up tasks (langid, personal_data, calendar): results/followup_summary.json and .md.

Counts follow pass_bar.md's reporting rules: a no-answer on a positive is a miss, a no-answer on a negative is left out of
the false-alarm denominator, an errored item is excluded and counted in `errors`; every zero carries its bound.
"""
import json
import statistics
import urllib.request

from . import datasets
from .common import ROOT, read_jsonl
from .run import CLAUDE_WORKERS

RESULTS = ROOT / "results"
TASKS = ["langid", "personal_data", "calendar"]
JUDGES = ["baseline", "fasttext", "claude_api_off", "claude_api_think", "gemma4_12b", "gemma4_12b_think", "gemini_decision"]
Z = 1.96
NO_REASONING_BELOW = 5  # output tokens: a reply under this holds no reasoning, only the verdict word


def zero_bound(n):
    return 1 - 0.05 ** (1 / n) if n else 1.0


def load(judge, task):
    path = RESULTS / f"{judge}__{task}.jsonl"
    return {r["id"]: r for r in read_jsonl(path)} if path.exists() else None


def score(items, res):
    pos, neg = {}, {}
    errors = noans = 0
    for it in items:
        r = res.get(it["id"])
        if r is None:
            continue  # not run by this judge (a slow judge runs only some classes)
        if r.get("error"):
            errors += 1
            continue
        none = r["verdict"] is None
        noans += none
        flag = r["verdict"] == "YES"
        if it["label"] == 1:
            c = pos.setdefault(it["cls"], {"k": 0, "n": 0})
            c["n"] += 1
            c["k"] += flag
        elif not none:
            c = neg.setdefault(it["cls"], {"k": 0, "n": 0})
            c["n"] += 1
            c["k"] += flag
    total = lambda d: {"k": sum(c["k"] for c in d.values()), "n": sum(c["n"] for c in d.values())}
    return {"pos": pos, "neg": neg, "all_pos": total(pos), "all_neg": total(neg), "noans": noans, "errors": errors}


def flips(items, res, appended_cls):
    """Per appended item with a usable verdict pair (control, appended): `to_yes` = NO became YES, `to_no` = YES became NO."""
    out = {"n": 0, "to_yes": 0, "to_no": 0}
    for it in items:
        if it["cls"] != appended_cls:
            continue
        a, b = res.get(it["id"]), res.get(it["meta"]["base_id"])
        if not a or not b or a.get("error") or b.get("error") or a["verdict"] is None or b["verdict"] is None:
            continue
        out["n"] += 1
        out["to_yes"] += b["verdict"] == "NO" and a["verdict"] == "YES"
        out["to_no"] += b["verdict"] == "YES" and a["verdict"] == "NO"
    return out


def median_s(res):
    xs = [r["latency_s"] for r in res.values() if r.get("latency_s")]
    return statistics.median(xs[1:]) if len(xs) > 1 else None


def environment():
    """Versions of the interpreter and tools on the machine that builds the report, which is the one that ran the judges."""
    import importlib.metadata
    import platform
    import subprocess
    ollama = subprocess.run(["ollama", "--version"], capture_output=True, text=True).stdout.strip().rsplit(" ", 1)[-1]
    tags = json.loads(urllib.request.urlopen("http://localhost:11434/api/tags", timeout=10).read())
    digest = next(m["digest"][:12] for m in tags["models"] if m["name"] == "gemma4:12b")
    return {"python": platform.python_version(), "ollama": ollama, "gemma4_12b_digest": digest,
            "fasttext_numpy2_wheel": importlib.metadata.version("fasttext-numpy2-wheel"), "hosted_parallel_calls": CLAUDE_WORKERS}


def build():
    summary = {"judges": {}, "tasks": {}, "appended": {}, "environment": environment()}
    for task in TASKS:
        items = datasets.load(task)
        summary["tasks"][task] = {"items": len(items), "judges": {}}
        for j in JUDGES:
            res = load(j, task)
            if res is None:
                continue
            entry = score(items, res)
            entry["median_s"] = median_s(res)
            models = {r.get("served_model") for r in res.values() if r.get("served_model")}
            dates = {r.get("measured_at") for r in res.values() if r.get("measured_at")}
            entry["served_models"] = sorted(models)
            entry["measured_at"] = sorted(dates)
            entry["no_reasoning"] = sum(1 for r in res.values() if r.get("output_tokens") is not None and r["output_tokens"] < NO_REASONING_BELOW)
            summary["tasks"][task]["judges"][j] = entry
    items = datasets.load("langid")
    for j in JUDGES:
        res = load(j, "langid")
        if res is not None:
            summary["appended"][j] = {"appended_ja": flips(items, res, "appended_ja"), "appended_other": flips(items, res, "appended_other")}
    return summary


def pct(k, n):
    return f"{k}/{n} = {k / n:.0%}" if n else "n/a"


def markdown(summary):
    lines = ["# Follow-up results", "", "Detection = flagged positives / positives (a no-answer is a miss). False alarm = flagged negatives / negatives with a verdict.", ""]
    for task, t in summary["tasks"].items():
        lines += [f"## {task}", ""]
        classes_pos = sorted({c for e in t["judges"].values() for c in e["pos"]})
        classes_neg = sorted({c for e in t["judges"].values() for c in e["neg"]})
        lines += ["| judge | detection | " + " | ".join(classes_pos) + " | false alarm | " + " | ".join(classes_neg) + " | no answer | errors | median s |",
                  "|---|---|" + "---|" * (len(classes_pos) + len(classes_neg) + 4)]
        for j, e in t["judges"].items():
            cells = [pct(e["pos"][c]["k"], e["pos"][c]["n"]) if c in e["pos"] else "-" for c in classes_pos]
            ncells = [pct(e["neg"][c]["k"], e["neg"][c]["n"]) if c in e["neg"] else "-" for c in classes_neg]
            lat = f"{e['median_s']:.2f}" if e["median_s"] else "n/a"
            lines.append(f"| {j} | {pct(e['all_pos']['k'], e['all_pos']['n'])} | " + " | ".join(cells) + f" | {pct(e['all_neg']['k'], e['all_neg']['n'])} | " + " | ".join(ncells) + f" | {e['noans']} | {e['errors']} | {lat} |")
        zeros = [f"{j}/{c}: 0 of {v['n']} (< {zero_bound(v['n']):.1%})" for j, e in t["judges"].items() for grp in ("pos", "neg") for c, v in e[grp].items() if v["n"] and v["k"] == 0]
        lines += ["", "Zero counts: " + ("; ".join(zeros) or "none"), ""]
    lines += ["## Appended sentence: verdict flipped by the appended sentence", "",
              "`to_yes` = NO became YES, `to_no` = YES became NO, against the control sentence. For appended_ja (a Japanese text, label NO) to_yes is the harm; for appended_other (a non-Japanese text, label YES) to_no is.", "",
              "| judge | appended_ja to_yes / to_no | appended_other to_yes / to_no |", "|---|---|---|"]
    for j, a in summary["appended"].items():
        cell = lambda c: f"{c['to_yes']} / {c['to_no']} of {c['n']}"
        lines.append(f"| {j} | {cell(a['appended_ja'])} | {cell(a['appended_other'])} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    s = build()
    (RESULTS / "followup_summary.json").write_text(json.dumps(s, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (RESULTS / "followup_summary.md").write_text(markdown(s), encoding="utf-8")
    print("wrote results/followup_summary.json and .md")
