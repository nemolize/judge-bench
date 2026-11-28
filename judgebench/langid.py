"""Language identification: is the main language of a text something other than Japanese? (label 1 = yes, flag it)

Sentences come from data/tatoeba_pool.tsv (Tatoeba, CC BY 2.0 FR; tools/build_tatoeba_pool.py). The label is fixed by the
source sentence's language, and by a main-language rule for mixed texts, before any judge runs:

- mixed texts join a Japanese and an English sentence; the main language is the one with more letters of its script,
  and the pair is kept only when that count is at least MIXED_RATIO times the other's;
- romaji items spell a Japanese sentence in Latin letters and keep its Japanese label (the language, not the script);
- appended items are a control sentence plus one more sentence naming the opposite language; the label stays the control's.
Short strings and kanji-only text are not built here (language-drift article); the article quotes their results.
"""
import re

from .common import DATA, item, rng

N = 40
MIXED_RATIO = 1.5
APPEND_TO_JA = "これは中国語です。"
APPEND_TO_OTHER = "これは日本語です。"
KANA_HAN = re.compile(r"[぀-ヿ一-鿿]")
LATIN = re.compile(r"[A-Za-z]")


def pool():
    rows = {}
    with (DATA / "tatoeba_pool.tsv").open(encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or line.startswith("id\t"):
                continue
            sid, lang, kind, text, romaji = line.rstrip("\n").split("\t")
            rows.setdefault((lang, kind), []).append({"id": int(sid), "text": text, "romaji": romaji})
    return rows


def main_language(text):
    """'ja' / 'en' by letter count with the MIXED_RATIO margin; None when neither side wins by that margin."""
    ja, en = len(KANA_HAN.findall(text)), len(LATIN.findall(text))
    if ja >= MIXED_RATIO * en:
        return "ja"
    return "en" if en >= MIXED_RATIO * ja else None


def generate():
    p, r = pool(), rng("langid")
    ja_long, ja_short = p[("jpn", "long")], p[("jpn", "short")]
    en_long, en_short, zh = p[("eng", "long")], p[("eng", "short")], p[("cmn", "long")]
    with_romaji = [s for s in ja_long if s["romaji"]]
    plain = [s for s in ja_long if not s["romaji"]]
    r.shuffle(with_romaji)
    r.shuffle(plain)
    r.shuffle(en_long)
    r.shuffle(en_short)
    r.shuffle(zh)
    r.shuffle(ja_short)
    romaji_src = with_romaji[:N]
    rest = with_romaji[N:] + plain
    rest.sort(key=lambda s: (-len(s["text"]), s["id"]))  # the longest Japanese sentences carry the English phrase
    mixed_ja_src, control_ja = rest[:N], rest[N:2 * N]
    control_en, mixed_en_src = en_long[:N], en_long[N:2 * N]
    control_zh = zh[:N]

    specs = []  # (cls, label, text, meta)
    for s in control_ja:
        specs.append(("control_ja", 0, s["text"], {"tatoeba_id": s["id"], "source": "jpn"}))
    for s in control_en:
        specs.append(("control_en", 1, s["text"], {"tatoeba_id": s["id"], "source": "eng"}))
    for s in control_zh:
        specs.append(("control_zh", 1, s["text"], {"tatoeba_id": s["id"], "source": "cmn"}))
    for s in romaji_src:
        specs.append(("romaji_ja", 0, s["romaji"], {"tatoeba_id": s["id"], "source": "jpn", "kana": s["text"]}))
    short_en_used = set()
    en_by_letters = sorted(en_short, key=lambda e: len(LATIN.findall(e["text"])))
    for s in sorted(mixed_ja_src, key=lambda s: len(s["text"])):
        short = next(e for e in en_by_letters if e["id"] not in short_en_used and main_language(s["text"] + " " + e["text"]) == "ja")
        short_en_used.add(short["id"])
        text = f"{s['text']} {short['text']}" if r.random() < 0.5 else f"{short['text']} {s['text']}"
        specs.append(("mixed_ja_main", 0, text, {"tatoeba_ids": [s["id"], short["id"]]}))
    for s, short in zip(mixed_en_src, ja_short):
        text = f"{s['text']} {short['text']}" if r.random() < 0.5 else f"{short['text']} {s['text']}"
        assert main_language(text) == "en"
        specs.append(("mixed_en_main", 1, text, {"tatoeba_ids": [s["id"], short["id"]]}))

    items = []
    for n, (cls, label, text, meta) in enumerate(specs, 1):
        items.append(item("langid", n, cls, label, text, **meta))
    n = len(items)
    base_ids = {(it["cls"], it["meta"].get("tatoeba_id")): it["id"] for it in items}
    for cls, label, text, meta in specs:
        if cls == "control_ja":
            n += 1
            items.append(item("langid", n, "appended_ja", 0, text + "\n" + APPEND_TO_JA, **meta, base_id=base_ids[(cls, meta["tatoeba_id"])]))
    for cls, src in (("control_en", control_en), ("control_zh", control_zh)):
        for s in src[:N // 2]:
            n += 1
            items.append(item("langid", n, "appended_other", 1, s["text"] + "\n" + APPEND_TO_OTHER, tatoeba_id=s["id"],
                              source="eng" if cls == "control_en" else "cmn", base_id=base_ids[(cls, s["id"])]))
    return items
