"""Style and notation drift injected into clean text.

Classes: mixed_register (です・ます with である), width (half-width Latin turned full-width),
term_variant (サーバー then サーバ in one text). Negatives are the untouched passages and
consistent term pairs.
"""
import re

from . import aitext, corpus
from .common import item, rng

PER_CLASS = 45
VARIANTS = [("サーバー", "サーバ"), ("ユーザー", "ユーザ"), ("ブラウザー", "ブラウザ"), ("コンピューター", "コンピュータ"),
            ("ドライバー", "ドライバ"), ("メモリー", "メモリ"), ("ディレクトリー", "ディレクトリ"), ("プリンター", "プリンタ")]
TEMPLATES = ["{T}の設定を確認します。", "その後、{T}を再起動します。", "{T}に接続できることを確認します。",
             "{T}のログを開いて原因を調べます。", "最後に{T}の状態を保存します。", "{T}の更新が終わるまで待ちます。"]
REGISTER_PAIRS = [("{T}の設定を確認します。", "{T}は再起動が必要です。", "{T}は再起動が必要である。"),
                  ("{T}にログインします。", "{T}の更新は毎週です。", "{T}の更新は毎週である。"),
                  ("{T}のログを開きます。", "原因は{T}の設定です。", "原因は{T}の設定である。"),
                  ("{T}を停止します。", "停止の影響は小さいです。", "停止の影響は小さい。"),
                  ("{T}の状態を保存します。", "保存先は共有ディレクトリです。", "保存先は共有ディレクトリである。"),
                  ("{T}へ接続します。", "接続の確認は必須です。", "接続の確認は必須である。")]
ASCII_WORD = re.compile(r"[A-Za-z]{3,}")


def _clean_register(text):
    return re.search(r"(です|ます|でした|ました)。", text) and not re.search(r"(だ|である|だった)。", text)


def _bases():
    r = rng("style")
    humans = [h["text"] for h in corpus.human()]
    pairs = [humans[i] + humans[i + 1] for i in range(0, len(humans) - 1, 2)]
    _, spare = aitext.llm_split()
    bases = [t for t in pairs + [p["text"] for p in spare] if _clean_register(t) and len(t) >= 30]
    r.shuffle(bases)
    return bases


def _to_fullwidth(word):
    return "".join(chr(ord(c) + 0xFEE0) for c in word)


def _mix_register(text):
    m = list(re.finditer(r"です。", text))
    if not m or text.count("ます。") < 1:
        return None
    last = m[-1]
    return text[: last.start()] + "である。" + text[last.end():]


def _width(text):
    m = ASCII_WORD.search(text)
    if not m:
        return None
    return text[: m.start()] + _to_fullwidth(m.group()) + text[m.end():]


def generate():
    r = rng("style")
    bases = _bases()
    items, n = [], 0
    for cls, fn in (("mixed_register", _mix_register), ("width", _width)):
        made = 0
        for base in bases:
            bad = fn(base)
            if bad is None or made >= PER_CLASS:
                continue
            made += 1
            n += 1
            items.append(item("style", n, cls, 1, bad, base=base))
            n += 1
            items.append(item("style", n, f"neg_paired_{cls}", 0, base))
    reg = [(long, a, b, c) for long, _ in VARIANTS for a, b, c in REGISTER_PAIRS]
    r.shuffle(reg)
    for long, a, ok, bad in reg[: PER_CLASS - sum(1 for i in items if i["cls"] == "mixed_register")]:
        n += 1
        items.append(item("style", n, "mixed_register", 1, a.format(T=long) + bad.format(T=long), pair_id=f"reg-{n}"))
        n += 1
        items.append(item("style", n, "neg_paired_mixed_register", 0, a.format(T=long) + ok.format(T=long), pair_id=f"reg-{n - 1}"))
    combos = [(v, t1, t2) for v in VARIANTS for t1 in TEMPLATES for t2 in TEMPLATES if t1 != t2]
    r.shuffle(combos)
    for (long, short), t1, t2 in combos[:PER_CLASS]:
        n += 1
        items.append(item("style", n, "term_variant", 1, t1.format(T=long) + t2.format(T=short), terms=[long, short], pair_id=f"term-{n}"))
        n += 1
        items.append(item("style", n, "neg_paired_term_variant", 0, t1.format(T=long) + t2.format(T=long), pair_id=f"term-{n - 1}"))
    return items
