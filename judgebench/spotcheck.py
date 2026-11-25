"""Write spotcheck.md: 10 random items per dataset for reading by hand (secret-shaped values masked)."""
import re

from . import datasets
from .common import ROOT, rng

SAMPLE = 10
PER_CLASS_TASKS = {"private_setup": 2}
SECRET_SHAPED = re.compile(r"[A-Za-z0-9_\-]{20,}")


def mask(text):
    return SECRET_SHAPED.sub(lambda m: m.group()[:4] + "…<masked>", text)


def _sample(task, items):
    """Most tasks: SAMPLE random items. Tasks in PER_CLASS_TASKS: that many from every class, so no group goes unread."""
    r = rng(f"spot-{task}")
    if task not in PER_CLASS_TASKS:
        return r.sample(items, SAMPLE)
    by_cls = {}
    for it in items:
        by_cls.setdefault(it["cls"], []).append(it)
    return [it for cls in sorted(by_cls) for it in r.sample(by_cls[cls], PER_CLASS_TASKS[task])]


def main():
    out = ["# Spot-check sample", "", f"{SAMPLE} random items per dataset, drawn with the seeded generator; {PER_CLASS_TASKS['private_setup']} per class or group for `private_setup`. Secret-shaped values are masked.", ""]
    for task in datasets.TASKS:
        items = datasets.load(task)
        for it in _sample(task, items):
            out += [f"## {it['id']} · {it['cls']} · label {it['label']}", "", "```", mask(it["text"]).rstrip("\n"), "```", ""]
    (ROOT / "spotcheck.md").write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    main()
