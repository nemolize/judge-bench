"""Shared dataset plumbing: items, seeded RNG, JSONL io, digests."""
import hashlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SEED = 20260101

# Token-shaped text trips push protection, so these stay local.
UNCOMMITTED = {"secrets", "injection_secrets"}


def rng(name):
    return random.Random(f"{name}:{SEED}")


def item(task, n, cls, label, text, **meta):
    return {"id": f"{task}-{n:04d}", "task": task, "cls": cls, "label": label, "text": text, "meta": meta}


def write_jsonl(path, items):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path):
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def digest(items):
    blob = "\n".join(json.dumps(it, ensure_ascii=False, sort_keys=True) for it in items)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def positives_per_class(items):
    out = {}
    for it in items:
        if it["label"] == 1:
            out[it["cls"]] = out.get(it["cls"], 0) + 1
    return out
