"""Calendar and arithmetic consistency. Label 1 = the text contradicts itself, 0 = its consistent twin.

Each class has N pairs: a consistent statement and a copy with one value altered (pair_id). Truth is computed here,
independent of any judge: the era table below, datetime's weekday, and integer arithmetic with 10% tax rounded down.
- era_year: a Japanese era year against the Gregorian year;
- weekday: a Gregorian date against its weekday;
- invoice: unit price x quantity per line, the subtotal, the tax and the total.
Era years n = 1 and each era's last year are not used: the era changes inside those years, so a date there is ambiguous.
"""
import datetime

from .common import item, rng

N = 40
ERAS = [("明治", 1868, 45), ("大正", 1912, 15), ("昭和", 1926, 64), ("平成", 1989, 31), ("令和", 2019, 8)]
WEEKDAYS = "月火水木金土日"
PRODUCTS = ["ノート", "ボールペン", "クリアファイル", "付箋", "USBケーブル", "マウスパッド", "インク", "電池", "ホチキス", "封筒"]


def era_to_year(era, n):
    start = {e: s for e, s, _ in ERAS}[era]
    return start + n - 1


def weekday_name(y, m, d):
    return WEEKDAYS[datetime.date(y, m, d).weekday()]


def invoice_consistent(lines):
    subtotal = sum(u * q for u, q in lines)
    tax = subtotal * 10 // 100
    return subtotal, tax, subtotal + tax


def _yen(x):
    return f"{x:,}円"


def _invoice_text(lines, line_totals, subtotal, tax, total):
    rows = [f"{name} 単価 {_yen(u)} × {q}個 = {_yen(t)}" for (name, u, q), t in zip(lines, line_totals)]
    return "請求書\n" + "\n".join(rows) + f"\n小計 {_yen(subtotal)}\n消費税(10%) {_yen(tax)}\n合計 {_yen(total)}\n"


def _valid_date(r, y):
    while True:
        m, d = r.randrange(1, 13), r.randrange(1, 32)
        try:
            datetime.date(y, m, d)
            return m, d
        except ValueError:
            continue


def generate():
    r = rng("calendar")
    items, n = [], 0

    def add(cls, pair, good, bad, **meta):
        nonlocal n
        n += 1
        items.append(item("calendar", n, f"neg_{cls}", 0, good, pair_id=f"{cls}-{pair}", **meta))
        n += 1
        items.append(item("calendar", n, cls, 1, bad, pair_id=f"{cls}-{pair}", **meta))

    seen = set()
    for pair in range(N):
        while True:
            era, start, last = r.choice(ERAS)
            ny = r.randrange(2, last)
            if start + ny - 1 > 2030 or (era, ny) in seen:
                continue
            seen.add((era, ny))
            break
        y = era_to_year(era, ny)
        m, d = _valid_date(r, y)
        wrong = y + r.choice([-3, -2, -1, 1, 2, 3])
        tpl = r.choice(["{era}{n}年は西暦{y}年です。", "この書類は{era}{n}年{m}月{d}日付で、西暦では{y}年{m}月{d}日にあたります。", "{era}{n}年{m}月{d}日は、西暦{y}年{m}月{d}日のことです。"])
        fmt = lambda yy: tpl.format(era=era, n=ny, y=yy, m=m, d=d)
        add("era_year", pair, fmt(y), fmt(wrong), era=era, era_year=ny)

    seen = set()
    for pair in range(N):
        while True:
            y = r.randrange(2000, 2031)
            m, d = _valid_date(r, y)
            if (y, m, d) not in seen:
                seen.add((y, m, d))
                break
        w = weekday_name(y, m, d)
        wrong = r.choice([c for c in WEEKDAYS if c != w])
        tpl = r.choice(["{y}年{m}月{d}日は{w}曜日です。", "会議は{y}年{m}月{d}日（{w}曜日）に開催します。", "{y}年{m}月{d}日の{w}曜日までにご返信ください。"])
        add("weekday", pair, tpl.format(y=y, m=m, d=d, w=w), tpl.format(y=y, m=m, d=d, w=wrong), date=f"{y}-{m:02d}-{d:02d}")

    for pair in range(N):
        count = r.choice([2, 3, 4])
        names = r.sample(PRODUCTS, count)
        lines = [(nm, r.randrange(3, 40) * 50, r.randrange(1, 9)) for nm in names]
        totals = [u * q for _, u, q in lines]
        subtotal, tax, total = invoice_consistent([(u, q) for _, u, q in lines])
        good = _invoice_text(lines, totals, subtotal, tax, total)
        kind = ["line", "subtotal", "tax", "total"][pair % 4]
        delta = r.choice([-1000, -100, -10, 10, 100, 1000])
        bt, bs, bx, bg = list(totals), subtotal, tax, total
        if kind == "line":
            bt[r.randrange(count)] += delta
        elif kind == "subtotal":
            bs += delta
        elif kind == "tax":
            bx += abs(delta) if delta else 10
        else:
            bg += delta
        bad = _invoice_text(lines, bt, bs, bx, bg)
        add("invoice", pair, good, bad, altered=kind)
    return items


def consistent(text):
    """Re-derive the truth from the text alone (used by the baseline): True when no value contradicts another."""
    import re
    if text.startswith("請求書"):
        rows = re.findall(r"単価 ([\d,]+)円 × (\d+)個 = ([\d,]+)円", text)
        num = lambda s: int(s.replace(",", ""))
        if any(num(u) * int(q) != num(t) for u, q, t in rows):
            return False
        subtotal, tax, total = (num(x) for x in re.search(r"小計 ([\d,]+)円\n消費税\(10%\) ([\d,]+)円\n合計 ([\d,]+)円", text).groups())
        return subtotal == sum(num(t) for _, _, t in rows) and tax == subtotal * 10 // 100 and total == subtotal + tax
    era = re.search(r"(明治|大正|昭和|平成|令和)(\d+)年", text)
    if era:
        year = re.search(r"西暦(?:では)?(\d{4})年", text)
        return era_to_year(era.group(1), int(era.group(2))) == int(year.group(1))
    y, m, d = (int(x) for x in re.search(r"(\d{4})年(\d+)月(\d+)日", text).groups())
    return weekday_name(y, m, d) == re.search(r"([月火水木金土日])曜日", text).group(1)
