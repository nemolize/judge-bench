"""Write spotcheck.md: 10 random items per dataset for reading by hand (secret-shaped values masked)."""
import re

from . import datasets
from .common import ROOT, rng

SAMPLE = 10
SECRET_SHAPED = re.compile(r"[A-Za-z0-9_\-]{20,}")


def mask(text):
    return SECRET_SHAPED.sub(lambda m: m.group()[:4] + "…<masked>", text)


def main():
    out = ["# Spot-check sample", "", f"{SAMPLE} random items per dataset, drawn with the seeded generator. Secret-shaped values are masked.", ""]
    for task in datasets.TASKS:
        items = datasets.load(task)
        for it in rng(f"spot-{task}").sample(items, SAMPLE):
            out += [f"## {it['id']} · {it['cls']} · label {it['label']}", "", "```", mask(it["text"]).rstrip("\n"), "```", ""]
    (ROOT / "spotcheck.md").write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    main()
