"""'AI-sounding' Japanese: flagged (YES) means the text was written by an LLM.

Negatives: the author's own sentences from articles published before ChatGPT (2022-11-30).
Positives: LLM passages on the same topics (data/llm_passages.jsonl); the first POSITIVES are used,
the rest feed the style task.
"""
from . import corpus
from .common import item, rng

POSITIVES = 60


def llm_split():
    passages = corpus.llm()
    r = rng("aitext")
    r.shuffle(passages)
    return passages[:POSITIVES], passages[POSITIVES:]


def generate():
    pos, _ = llm_split()
    neg = [h for h in corpus.human() if h["pre_ai"] and len(h["text"]) >= 20]
    items, n = [], 0
    for p in pos:
        n += 1
        items.append(item("aitext", n, "llm", 1, p["text"], topic=p["topic"]))
    for h in neg:
        n += 1
        items.append(item("aitext", n, "neg_human", 0, h["text"], slug=h["slug"]))
    return items
