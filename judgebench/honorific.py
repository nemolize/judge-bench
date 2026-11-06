"""Honorific errors: known error types injected into correct sentences.

Error types follow the Agency for Cultural Affairs' 敬語の指針 (2007):
  double_honorific  二重敬語 (尊敬語 + れる/られる, e.g. お読みになられる)
  humble_for_other  謙譲語を相手の行為に使う (e.g. お客様が申しました)
  honorific_for_self 尊敬語を自分側の行為に使う (e.g. 私がおっしゃいました)
Hard negatives: the paired correct sentence, 敬語連結 (allowed by the 指針) and
established forms such as お召し上がりになる / お見えになる.
"""
from .common import item, rng

OUTSIDERS = ["先生", "お客様", "取引先の担当の方", "取引先の部長", "取引先の社長", "ご来訪の方"]
SELVES = ["私", "わたくし", "私ども", "弊社の担当", "当方"]

DOUBLE = [
    ("資料をお読みになりました", "資料をお読みになられました"),
    ("その件をおっしゃいました", "その件をおっしゃられました"),
    ("見積書をご覧になりました", "見積書をご覧になられました"),
    ("早めにお帰りになりました", "早めにお帰りになられました"),
    ("会議室でお話しになりました", "会議室でお話しになられました"),
    ("返信をお書きになりました", "返信をお書きになられました"),
    ("昼食を召し上がりました", "昼食を召し上がられました"),
    ("窓際の席にお座りになりました", "窓際の席にお座りになられました"),
    ("新しい端末をお使いになりました", "新しい端末をお使いになられました"),
    ("今後の方針をお考えになりました", "今後の方針をお考えになられました"),
    ("入口でお待ちになりました", "入口でお待ちになられました"),
    ("九時に会社へお戻りになりました", "九時に会社へお戻りになられました"),
    ("本社にいらっしゃいました", "本社にいらっしゃられました"),
    ("出張にお出かけになりました", "出張にお出かけになられました"),
    ("日程をお決めになりました", "日程をお決めになられました"),
    ("プランをお選びになりました", "プランをお選びになられました"),
    ("急いでお帰りになります", "急いでお帰りになられます"),
    ("明日からお休みになります", "明日からお休みになられます"),
]
HUMBLE_FOR_OTHER = [
    ("おっしゃいました", "申しました"),
    ("そのようにおっしゃいました", "そのように申しました"),
    ("本社にいらっしゃいました", "本社に参りました"),
    ("会議室にいらっしゃいました", "会議室に参りました"),
    ("受付にいらっしゃいました", "受付に参りました"),
    ("オフィスにいらっしゃいます", "オフィスに参ります"),
    ("そうおっしゃいます", "そう申します"),
    ("その件をご存じです", "その件を存じています"),
    ("その話をご存じです", "その話を存じています"),
]
HONORIFIC_FOR_SELF = [
    ("そのように申します", "そのようにおっしゃいます"),
    ("明日そちらに参ります", "明日そちらにいらっしゃいます"),
    ("明日そちらに伺います", "明日そちらにいらっしゃいます"),
    ("お茶をいただきます", "お茶を召し上がります"),
    ("資料を拝見します", "資料をご覧になります"),
    ("その件を存じております", "その件をご存じです"),
    ("昨日お話をうかがいました", "昨日お話をお聞きになりました"),
    ("資料を後ほどお送りします", "資料を後ほどお送りになります"),
]
FRAMES_PAST = ["{S}が{V}。", "昨日、{S}が{V}。", "先ほど{S}が{V}。"]
FRAMES_NONPAST = ["{S}が{V}。", "明日、{S}が{V}。", "午後に{S}が{V}。"]
FRAMES_STATE = ["{S}は{V}。", "{S}も{V}。"]

CONNECTED = [
    "お読みになっていらっしゃいます", "お書きになっていらっしゃいました", "お使いになっていらっしゃいます",
    "お待ちになっていらっしゃいました", "お考えになっていらっしゃいます", "ご覧になっていらっしゃいました",
    "お話しになっていらっしゃいます", "お決めになっていらっしゃいました", "お選びになっていらっしゃいます",
    "お聞きになっていらっしゃいました",
]
ESTABLISHED = [
    "お召し上がりになりました", "お見えになりました", "お召し上がりになります", "お見えになります",
    "お召しになりました", "お出でになりました", "お召し上がりになりましたか", "お見えになりましたか",
    "お出でになります", "お召しになります",
]


ROLES = ["部長", "取締役", "リーダー"]
NARU_FRAMES = ["来月から{S}が{R}になられます。", "先月、{S}が{R}になられました。"]


TIME_WORDS = ("昨日", "明日", "後ほど", "先ほど", "九時", "午後", "来月", "先月", "早めに", "急いで")


def _frames(v):
    frames = _frames_by_tense(v)
    return frames[:1] if any(w in v for w in TIME_WORDS) else frames


def _frames_by_tense(v):
    if v.endswith("ました") or v.endswith("ましたか"):
        return FRAMES_PAST
    if v.endswith("ます"):
        return FRAMES_NONPAST
    return FRAMES_STATE


def _combos(entries, subjects, r, n):
    pool = [(s, e, f) for s in subjects for e in entries for f in _frames(e[0])]
    r.shuffle(pool)
    seen, out = set(), []
    for s, e, f in pool:
        text = f.format(S=s, V=e[1])
        if text not in seen:
            seen.add(text)
            out.append((s, e, f))
    return out[:n]


def generate(per_class=45):
    r = rng("honorific")
    items, n = [], 0
    specs = [
        ("double_honorific", DOUBLE, OUTSIDERS),
        ("humble_for_other", HUMBLE_FOR_OTHER, OUTSIDERS),
        ("honorific_for_self", HONORIFIC_FOR_SELF, SELVES),
    ]
    for cls, entries, subjects in specs:
        for k, (s, (ok, bad), f) in enumerate(_combos(entries, subjects, r, per_class)):
            n += 1
            items.append(item("honorific", n, cls, 1, f.format(S=s, V=bad), pair=ok, pair_id=f"{cls}-{k}"))
            n += 1
            items.append(item("honorific", n, f"neg_paired_{cls}", 0, f.format(S=s, V=ok), pair_id=f"{cls}-{k}"))
    for cls, forms in (("neg_connected", CONNECTED), ("neg_established", ESTABLISHED)):
        for v in forms:
            for s in r.sample(OUTSIDERS, 2):
                n += 1
                items.append(item("honorific", n, cls, 0, f"{s}が{v}。"))
    for s in OUTSIDERS:
        for role in (x for x in ROLES if x not in s):
            for f in NARU_FRAMES:
                n += 1
                items.append(item("honorific", n, "neg_naru_honorific", 0, f.format(S=s, R=role)))
    return items
