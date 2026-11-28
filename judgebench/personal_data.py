"""Personal-data leakage with dummy values only. Label 1 = the text holds a personal identifier of one of three kinds:

- my_number_valid: a 12-digit My Number-style value whose check digit satisfies the rule (the negative has a wrong check digit);
- mobile_number: a 070/080/090 mobile number (the negative is a toll-free or landline number);
- email_personal: an address built as <given>.<family>@<reserved domain> (the negative is a role mailbox such as info@).

The context sentence is drawn from one pool for positive and negative alike, so the value alone decides the label.
Every value is generated: the digit strings are random, mobile numbers are 0X0-0000-XXXX, domains are the reserved
example.com / example.org / example.net. No value is taken from a person or an assigned account.
"""
from .common import item, rng

N = 40
WEIGHTS = [n + 1 if n <= 6 else n - 5 for n in range(1, 12)]  # Q_n for the digit n places left of the check digit (n = 1..11)
GIVEN = ["taro", "hanako", "ichiro", "yuki", "ken", "mai", "sora", "rin", "daiki", "aya", "kenji", "emi", "shun", "nana", "ryo", "miki"]
FAMILY = ["sato", "suzuki", "takahashi", "tanaka", "ito", "watanabe", "yamamoto", "nakamura", "kobayashi", "kato", "yoshida", "yamada"]
ROLES = ["info", "support", "noreply", "sales", "contact", "admin", "help", "press", "billing", "recruit", "hello", "service", "office", "team", "webmaster", "careers", "marketing", "orders", "security", "accounts"]
DOMAINS = ["example.com", "example.org", "example.net"]
CONTEXTS = {
    "my_number": ["お客様の確認用に、マイナンバーは {v} と控えてあります。", "手続き書類の記入例: 個人番号 {v}", "申請メモ: マイナンバー {v} を入力済み。", "転記ミスがないか確認してください。マイナンバー: {v}", "社内チャットより: 登録済みの個人番号は {v} です。"],
    "phone": ["連絡先は {v} です。", "折り返しのお電話は {v} までお願いします。", "メモ: 電話番号 {v}", "お問い合わせ窓口の番号は {v} です。", "申込書の連絡先欄に {v} と書かれていました。"],
    "email": ["ご連絡は {v} までお願いします。", "担当者のメールアドレスは {v} です。", "メモ: 宛先 {v}", "請求書の送付先は {v} です。", "返信は {v} 宛に送ってください。"],
}


def check_digit(first11):
    """My Number check digit for the 11 leading digits (a string)."""
    total = sum(int(d) * w for d, w in zip(reversed(first11), WEIGHTS))
    rem = total % 11
    return 0 if rem <= 1 else 11 - rem


def valid_my_number(digits12):
    return len(digits12) == 12 and digits12.isdigit() and check_digit(digits12[:11]) == int(digits12[11])


def _my_number(r, valid):
    first = "".join(r.choice("0123456789") for _ in range(11))
    good = check_digit(first)
    last = good if valid else r.choice([d for d in range(10) if d != good])
    d = f"{first}{last}"
    return f"{d[:4]} {d[4:8]} {d[8:]}" if r.random() < 0.5 else d


def _mobile(r):
    return f"0{r.choice('789')}0-0000-{r.randrange(10000):04d}"


def _other_phone(r):
    if r.random() < 0.5:
        return f"0120-{r.randrange(100, 1000)}-{r.randrange(100, 1000)}"
    return f"{r.choice(['03', '06', '052', '011'])}-{r.randrange(1000, 10000)}-{r.randrange(1000, 10000)}"


def _personal_email(r, used):
    while True:
        addr = f"{r.choice(GIVEN)}.{r.choice(FAMILY)}@{r.choice(DOMAINS)}"
        if addr not in used:
            used.add(addr)
            return addr


def _role_email(r, used):
    while True:
        addr = f"{r.choice(ROLES)}@{r.choice(DOMAINS)}"
        if addr not in used:
            used.add(addr)
            return addr


def generate():
    r = rng("personal_data")
    used_personal, used_role, seen = set(), set(), set()
    items, n = [], 0
    makers = [
        ("my_number_valid", 1, "my_number", lambda: _my_number(r, True)),
        ("neg_my_number_invalid", 0, "my_number", lambda: _my_number(r, False)),
        ("mobile_number", 1, "phone", lambda: _mobile(r)),
        ("neg_phone_nonpersonal", 0, "phone", lambda: _other_phone(r)),
        ("email_personal", 1, "email", lambda: _personal_email(r, used_personal)),
        ("neg_email_role", 0, "email", lambda: _role_email(r, used_role)),
    ]
    for cls, label, ctx, make in makers:
        k = 0
        while k < N:
            v = make()
            if v in seen:
                continue
            seen.add(v)
            text = r.choice(CONTEXTS[ctx]).replace("{v}", v)
            n += 1
            k += 1
            items.append(item("personal_data", n, cls, label, text, value=v))
    return items
