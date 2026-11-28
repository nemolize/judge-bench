"""Build data/tatoeba_pool.tsv from the Tatoeba per-language exports (run once; the pool is committed).

  python3 tools/build_tatoeba_pool.py <dir holding jpn/eng/cmn_sentences.tsv.bz2> <export date YYYY-MM-DD>

Needs pykakasi 2.3.0 for the romaji column. The selection filters are fixed here, before any judge result exists.
Tatoeba sentences are CC BY 2.0 FR (https://tatoeba.org/en/terms_of_use); the id column names each sentence.
"""
import bz2
import random
import re
import sys
from pathlib import Path

import pykakasi

SEED = "tatoeba-pool:20260101"
KANA = re.compile(r"[぀-ヿ]")
HAN = re.compile(r"[一-鿿]")
ASCII_WORD = re.compile(r"[A-Za-z0-9]")
KINDS = {  # (lang, kind) -> (min chars, max chars, how many)
    ("jpn", "long"): (18, 40, 160), ("jpn", "short"): (6, 12, 70),
    ("eng", "long"): (35, 80, 160), ("eng", "short"): (12, 25, 70),
    ("cmn", "long"): (10, 30, 130),
}
ROMAJI_FOR = 110  # the first N long Japanese sentences also get a romaji form


def ok(lang, kind, text):
    lo, hi, _ = KINDS[(lang, kind)]
    if not lo <= len(text) <= hi or "\t" in text or "\n" in text:
        return False
    if lang == "jpn":
        return not ASCII_WORD.search(text) and len(KANA.findall(text)) >= (3 if kind == "long" else 2)
    if lang == "eng":
        return text.isascii() and text[0].isupper() and text[-1] in ".?!" and not re.search(r"\d", text)
    return bool(HAN.search(text)) and not KANA.search(text) and not ASCII_WORD.search(text)


def romaji(kks, text):
    out = " ".join(p["hepburn"] for p in kks.convert(text))
    out = re.sub(r"\s+([.,?!])", r"\1", out).replace("。", ".").replace("、", ",").replace("？", "?").replace("！", "!")
    return out[:1].upper() + out[1:]


def main(src, export_date):
    kks = pykakasi.kakasi()
    rows, r = [], random.Random(SEED)
    for lang in ("jpn", "eng", "cmn"):
        sentences = []
        with bz2.open(Path(src) / f"{lang}_sentences.tsv.bz2", "rt", encoding="utf-8") as f:
            for line in f:
                sid, _, text = line.rstrip("\n").split("\t", 2)
                sentences.append((int(sid), text))
        sentences.sort()
        r.shuffle(sentences)
        for (lg, kind), (_, _, n) in KINDS.items():
            if lg != lang:
                continue
            picked = []
            for sid, text in sentences:
                if len(picked) == n:
                    break
                if ok(lang, kind, text) and all(text != p[1] for p in picked) and not any(text == x[3] for x in rows):
                    picked.append((sid, text))
            assert len(picked) == n, (lang, kind, len(picked))
            for k, (sid, text) in enumerate(picked):
                rom = romaji(kks, text) if lang == "jpn" and kind == "long" and k < ROMAJI_FOR else ""
                rows.append((sid, lang, kind, text, rom))
    out = Path(__file__).resolve().parent.parent / "data" / "tatoeba_pool.tsv"
    with out.open("w", encoding="utf-8") as f:
        f.write(f"# Tatoeba export of {export_date}, CC BY 2.0 FR, https://tatoeba.org; romaji by pykakasi 2.3.0 (Hepburn)\n")
        f.write("id\tlang\tkind\ttext\tromaji\n")
        for row in rows:
            f.write("\t".join(map(str, row)) + "\n")
    print(len(rows), "rows ->", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
