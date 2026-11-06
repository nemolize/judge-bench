"""'AI-sounding' Japanese: flagged (YES) means the text was written by an LLM.

Negatives: the author's own sentences from articles published before ChatGPT (2022-11-30).
Positives: one-sentence LLM texts on the same topics from three generators, 45 each, drawn so that
their length distribution follows the human sentences' (data/llm_sentences.jsonl).
`llm_split` still serves the style task its spare multi-sentence passages (data/llm_passages.jsonl).
"""
from . import corpus
from .common import item, rng

POSITIVES = 60
PER_GENERATOR = 45
BINS = 5


def llm_split():
    passages = corpus.llm()
    r = rng("aitext")
    r.shuffle(passages)
    return passages[:POSITIVES], passages[POSITIVES:]


def _edges(lengths):
    xs = sorted(lengths)
    return [xs[round(len(xs) * k / BINS) - 1] for k in range(1, BINS)] + [10**9]


def _bin(length, edges):
    return next(i for i, e in enumerate(edges) if length <= e)


def _matched(candidates, human_lengths, r):
    """PER_GENERATOR texts whose length bins follow the human sentences' bins."""
    edges = _edges(human_lengths)
    share = [sum(1 for n in human_lengths if _bin(n, edges) == b) / len(human_lengths) for b in range(BINS)]
    pools = [[c for c in candidates if _bin(len(c["text"]), edges) == b] for b in range(BINS)]
    for pool in pools:
        r.shuffle(pool)
    picked, spare = [], []
    for b in range(BINS):
        want = round(PER_GENERATOR * share[b])
        picked += pools[b][:want]
        spare += pools[b][want:]
    r.shuffle(spare)
    return (picked + spare)[:PER_GENERATOR]


def generate():
    r = rng("aitext-sentences")
    neg = [h for h in corpus.human() if h["pre_ai"] and len(h["text"]) >= 20]
    lengths = [len(h["text"]) for h in neg]
    sentences = corpus.read_jsonl(corpus.DATA / "llm_sentences.jsonl")
    items, n = [], 0
    for gen in corpus.SENTENCE_GENERATORS:
        seen, cands = set(), []
        for s in sentences:
            if s["generator"] == gen and s["text"] not in seen:
                seen.add(s["text"])
                cands.append(s)
        for c in _matched(cands, lengths, r):
            n += 1
            items.append(item("aitext", n, f"llm_{gen}", 1, c["text"], topic=c["topic"], generator=gen))
    for h in neg:
        n += 1
        items.append(item("aitext", n, "neg_human", 0, h["text"], slug=h["slug"]))
    return items
