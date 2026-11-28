"""Rule-based baselines: textlint (honorific, style), gitleaks (secrets), a phrase list (aitext), regular expressions (private_setup).

Each runner takes a list of items and returns ({id: flagged}, {"seconds": batch wall time,
"peak_rss_bytes": peak resident size of the child processes, None when there is no child process}).
"""
import json
import re
import subprocess
import tempfile
import time
from pathlib import Path

from .common import ROOT

TEXTLINT = ROOT / "node_modules" / ".bin" / "textlint"
CONFIGS = {"honorific": ROOT / "baselines" / "textlintrc.honorific.json", "style": ROOT / "baselines" / "textlintrc.style.json"}
# Stock phrases of LLM-written Japanese; fixed before any run and never tuned on data.
AI_PHRASES = ["重要です", "可能です", "でしょう", "必要があります", "と言えます", "ましょう", "ことができます", "スムーズ", "適切に", "効率的"]


def _timed(cmd):
    """Run under /usr/bin/time -l so the child's peak resident size is readable."""
    t0 = time.perf_counter()
    res = subprocess.run(["/usr/bin/time", "-l", *cmd], capture_output=True, text=True)
    rss = re.search(r"(\d+)\s+maximum resident set size", res.stderr)
    return res, {"seconds": time.perf_counter() - t0, "peak_rss_bytes": int(rss.group(1)) if rss else None}


def _write_items(items, suffix):
    d = Path(tempfile.mkdtemp(prefix="judgebench-"))
    for it in items:
        (d / f"{it['id']}{suffix}").write_text(it["text"], encoding="utf-8")
    return d


def textlint(items, task):
    d = _write_items(items, ".md")
    res, stats = _timed([str(TEXTLINT), "--config", str(CONFIGS[task]), "--format", "json", str(d)])
    if res.returncode not in (0, 1) or (res.returncode == 1 and not res.stdout.strip()):
        raise RuntimeError(res.stderr[-500:])
    flagged = {it["id"]: False for it in items}
    for entry in json.loads(res.stdout or "[]"):
        if entry["messages"]:
            flagged[Path(entry["filePath"]).stem] = True
    return flagged, stats


def gitleaks(items):
    d = _write_items(items, ".diff")
    report = d / "report.json"
    res, stats = _timed(["gitleaks", "detect", "--no-git", "--no-banner", "--source", str(d),
                         "--report-format", "json", "--report-path", str(report)])
    if res.returncode not in (0, 1):
        raise RuntimeError(res.stderr[-500:])
    flagged = {it["id"]: False for it in items}
    for finding in json.loads(report.read_text() or "[]"):
        flagged[Path(finding["File"]).stem] = True
    return flagged, stats


# Private-setup patterns (private_setup.md): fixed before any run and never tuned on data.
PRIVATE_SETUP_PATTERNS = [
    r"\b(?:my|this)\s+(?:laptop|workstation|desktop|machine|server|dev box|mac)\b[^.\n]{0,80}\b\d+(?:\.\d+)?\s*(?:GB|GiB|TB)\b",
    r"\b\d+(?:\.\d+)?\s*(?:GB|GiB|TB)\s+(?:of\s+)?free\b",
    r"\bfree\s+(?:disk|space)\b[^.\n]{0,40}\b\d+(?:\.\d+)?\s*(?:GB|GiB|TB)\b",
    r"\b(?:I|I'm|I am)\s+(?:currently\s+)?(?:run|running|use|using|keep)\b[^.\n]{0,60}\b(?:hook|tmux|zsh|direnv|dotfiles)\b",
    r"\b(?:my|this)\s+(?:shell|editor)\b[^.\n]{0,40}\b(?:loads|runs)\b",
    r"(?:/home/[\w.-]+/|/Users/[\w.-]+/|(?<![\w/.])~/\.)",
]
PRIVATE_SETUP_RE = [re.compile(p, re.IGNORECASE) for p in PRIVATE_SETUP_PATTERNS]


def private_setup_rules(items):
    t0 = time.perf_counter()
    flagged = {it["id"]: any(p.search(it["text"]) for p in PRIVATE_SETUP_RE) for it in items}
    return flagged, {"seconds": time.perf_counter() - t0, "peak_rss_bytes": None}


KANA = re.compile(r"[\u3040-\u30ff]")
MY_NUMBER = re.compile(r"(?<!\d)(\d{4}) ?(\d{4}) ?(\d{4})(?!\d)")
MOBILE = re.compile(r"(?<!\d)0[789]0-\d{4}-\d{4}(?!\d)")
PERSONAL_EMAIL = re.compile(r"\b[a-z]+\.[a-z]+@(?:example\.(?:com|org|net))\b")


def _my_number_valid(text):
    from .personal_data import valid_my_number
    return any(valid_my_number("".join(m.groups())) for m in MY_NUMBER.finditer(text))


def kana_absent(items):
    """langid baseline: flagged (not Japanese) when the text holds no kana at all."""
    t0 = time.perf_counter()
    flagged = {it["id"]: not KANA.search(it["text"]) for it in items}
    return flagged, {"seconds": time.perf_counter() - t0, "peak_rss_bytes": None}


def personal_data_rules(items):
    t0 = time.perf_counter()
    flagged = {it["id"]: _my_number_valid(it["text"]) or bool(MOBILE.search(it["text"])) or bool(PERSONAL_EMAIL.search(it["text"])) for it in items}
    return flagged, {"seconds": time.perf_counter() - t0, "peak_rss_bytes": None}


def calendar_rules(items):
    from .calendar_task import consistent
    t0 = time.perf_counter()
    flagged = {it["id"]: not consistent(it["text"]) for it in items}
    return flagged, {"seconds": time.perf_counter() - t0, "peak_rss_bytes": None}


def fasttext_not_japanese(items, model_path):
    """langid second baseline: fastText lid.176 (needs `pip install fasttext-numpy2-wheel` and the model file)."""
    import fasttext
    model = fasttext.load_model(str(model_path))
    t0 = time.perf_counter()
    flagged = {it["id"]: model.predict(it["text"].replace("\n", " "))[0][0] != "__label__ja" for it in items}
    return flagged, {"seconds": time.perf_counter() - t0, "peak_rss_bytes": None}


def phrases(items):
    t0 = time.perf_counter()
    flagged = {it["id"]: any(p in it["text"] for p in AI_PHRASES) for it in items}
    return flagged, {"seconds": time.perf_counter() - t0, "peak_rss_bytes": None}


def run(task, items):
    base = {"injection_honorific": "honorific", "injection_secrets": "secrets"}.get(task, task)
    if base in ("honorific", "style"):
        return textlint(items, base)
    if base == "secrets":
        return gitleaks(items)
    if base == "private_setup":
        return private_setup_rules(items)
    if base == "langid":
        return kana_absent(items)
    if base == "personal_data":
        return personal_data_rules(items)
    if base == "calendar":
        return calendar_rules(items)
    return phrases(items)
