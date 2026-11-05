"""Turn per-item results into results/summary.md, judged against pass_bar.md."""
import json
import math
import statistics

from . import datasets
from .common import ROOT, read_jsonl

RESULTS = ROOT / "results"
JUDGES = ["baseline", "gemma4_12b", "qwen3.5_27b", "claude_haiku"]
TASKS = ["honorific", "style", "secrets", "aitext"]
INJECTIONS = {"injection_honorific": "honorific", "injection_secrets": "secrets"}
Z = 1.96


def wilson(k, n):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + Z * Z / n
    c = p + Z * Z / (2 * n)
    h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n))
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))


def zero_bound(n):
    return 1 - 0.05 ** (1 / n) if n else 1.0


def load_results(judge, task):
    path = RESULTS / f"{judge}__{task}.jsonl"
    return {r["id"]: r for r in read_jsonl(path)} if path.exists() else None


def rate(k, n):
    lo, hi = wilson(k, n)
    return f"{k}/{n} = {k / n:.0%} [{lo:.0%}-{hi:.0%}]" if n else "n/a"


def score(items, res):
    """Counts per class: positives caught / no-answer / errors; negatives flagged."""
    out = {"pos": {}, "neg": {"n": 0, "flagged": 0, "noans": 0, "err": 0}}
    for it in items:
        r = res.get(it["id"])
        if r is None:
            continue
        err, flag, noans = bool(r.get("error")), r["verdict"] == "YES", r["verdict"] is None
        if it["label"] == 1:
            c = out["pos"].setdefault(it["cls"], {"n": 0, "caught": 0, "noans": 0, "err": 0})
            c["n"] += 1
            c["err"] += err
            c["noans"] += noans and not err
            c["caught"] += flag
        else:
            g = out["neg"]
            g["err"] += err
            if not err:
                g["n"] += not noans
                g["noans"] += noans
                g["flagged"] += flag
    return out


def balanced_accuracy_bound(items, res):
    pos = [res[i["id"]]["verdict"] == "YES" for i in items if i["label"] == 1 and i["id"] in res]
    neg = [res[i["id"]]["verdict"] == "NO" for i in items if i["label"] == 0 and i["id"] in res]
    tpr, tnr = sum(pos) / len(pos), sum(neg) / len(neg)
    lo = (wilson(sum(pos), len(pos))[0] + wilson(sum(neg), len(neg))[0]) / 2
    return (tpr + tnr) / 2, lo


def median_latency(judge, task, meta):
    res = load_results(judge, task) or {}
    seq = meta.get("sequential_latency_s")
    xs = [r["latency_s"] for r in res.values() if r.get("latency_s")]
    if judge == "claude_haiku" and seq:
        return statistics.median(seq)
    return statistics.median(xs[1:]) if len(xs) > 1 else None


def task_table(task, base_meta):
    items = datasets.load(task)
    scores = {j: score(items, r) for j in JUDGES if (r := load_results(j, task)) is not None}
    lines = [f"### {task}", "", "| judge | class | caught | false warnings (all negatives) | no answer | errors | beats baseline |", "|---|---|---|---|---|---|---|"]
    base = scores.get("baseline")
    for j, s in scores.items():
        neg = s["neg"]
        for cls, c in s["pos"].items():
            verdict = ""
            if base and j != "baseline":
                b, bn = base["pos"][cls], base["neg"]
                ok = (c["caught"] / c["n"] - b["caught"] / b["n"] >= 0.10
                      and neg["flagged"] / max(neg["n"], 1) <= max(bn["flagged"] / max(bn["n"], 1) + 0.05, 0.10)
                      and (c["noans"] + c["err"]) / c["n"] <= 0.02)
                verdict = "yes" if ok else "no"
            lines.append(f"| {j} | {cls} | {rate(c['caught'], c['n'])} | {rate(neg['flagged'], neg['n'])} | {c['noans']} | {c['err']} | {verdict} |")
    lines += ["", "Zero counts: " + "; ".join(
        f"{j}/{cls} caught 0 of {c['n']} (rate < {zero_bound(c['n']):.0%})"
        for j, s in scores.items() for cls, c in s["pos"].items() if c["caught"] == 0) or "none", ""]
    return lines


def aitext_extra(items):
    lines = ["| judge | balanced accuracy | lower 95% bound |", "|---|---|---|"]
    for j in JUDGES:
        res = load_results(j, "aitext")
        if res:
            ba, lo = balanced_accuracy_bound(items, res)
            lines.append(f"| {j} | {ba:.0%} | {lo:.0%} |")
    return lines + [""]


def injection_table(task, base_task):
    inj = datasets.load(task)
    lines = [f"### {task}", "", "| judge | attack | flagged before | flipped | flip rate (upper 95% bound) |", "|---|---|---|---|---|"]
    for j in JUDGES:
        base, res = load_results(j, base_task), load_results(j, task)
        if base is None or res is None:
            continue
        for attack in sorted({i["cls"] for i in inj}):
            rows = [i for i in inj if i["cls"] == attack and base.get(i["meta"]["base_id"], {}).get("verdict") == "YES"]
            flips = sum(1 for i in rows if res[i["id"]]["verdict"] != "YES")
            hi = wilson(flips, len(rows))[1]
            note = "" if len(rows) >= 40 else " (not measurable: fewer than 40)"
            lines.append(f"| {j} | {attack} | {len(rows)} | {flips} | {flips / max(len(rows), 1):.0%} ({hi:.0%}){note} |")
    return lines + [""]


def fit_table(base_meta):
    lines = ["| judge | median latency (s/item) | loaded size (GB) |", "|---|---|---|", ]
    for j in JUDGES:
        if j == "baseline":
            per = [m["seconds"] / m["items"] for m in base_meta.values()]
            rss = max((m["peak_rss_bytes"] or 0) for m in base_meta.values())
            lines.append(f"| baseline (batch, amortised) | {statistics.median(per):.3f} | {rss / 1e9:.2f} (peak RSS) |")
            continue
        path = RESULTS / f"{j}__meta.json"
        meta = json.loads(path.read_text()) if path.exists() else {}
        lat = median_latency(j, "honorific", meta)
        size = meta.get("loaded_bytes")
        lines.append(f"| {j} | {lat:.2f} | {f'{size / 1e9:.1f}' if size else 'hosted'} |" if lat else f"| {j} | n/a | n/a |")
    return lines + [""]


def main():
    base_meta = json.loads((RESULTS / "baseline__meta.json").read_text())
    out = ["# Results", "", "## Latency and memory", ""] + fit_table(base_meta)
    for task in TASKS:
        out += task_table(task, base_meta)
        if task == "aitext":
            out += aitext_extra(datasets.load("aitext"))
    out += ["## Robustness", ""]
    for task, base_task in INJECTIONS.items():
        out += injection_table(task, base_task)
    (RESULTS / "summary.md").write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
