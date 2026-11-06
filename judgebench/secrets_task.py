"""Secrets in a diff: dummy credentials of known formats planted in unified diffs.

The values are random strings of the right shape, never real credentials. The dataset is
rebuilt from the seed on every run and not committed (see common.UNCOMMITTED).
"""
import string

from .common import item, rng

PER_CLASS = 45
B32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
ALNUM = string.ascii_letters + string.digits
GCP = ALNUM + "_-"
HEX = "0123456789abcdef"


def _pick(r, alphabet, n):
    return "".join(r.choice(alphabet) for _ in range(n))


FORMATS = {
    "aws_access_key": (["AWS_ACCESS_KEY_ID", "ACCESS_KEY", "AWS_KEY"], lambda r: "AKIA" + _pick(r, B32, 16)),
    "github_pat": (["GITHUB_TOKEN", "GH_PAT", "TOKEN"], lambda r: "ghp_" + _pick(r, ALNUM, 36)),
    "slack_bot_token": (["SLACK_BOT_TOKEN", "SLACK_TOKEN", "BOT_TOKEN"],
                        lambda r: f"xoxb-{_pick(r, string.digits, 11)}-{_pick(r, string.digits, 12)}-{_pick(r, ALNUM, 24)}"),
    "stripe_live_key": (["STRIPE_SECRET_KEY", "STRIPE_KEY", "PAYMENT_KEY"], lambda r: "sk_live_" + _pick(r, ALNUM, 24)),
    "gcp_api_key": (["GOOGLE_API_KEY", "MAPS_API_KEY", "API_KEY"], lambda r: "AIza" + _pick(r, GCP, 35)),
}

DECOYS = [
    lambda r, p: "your-api-key-here",
    lambda r, p: "AKIAIOSFODNN7EXAMPLE" if p == "AKIA" else "<" + "REPLACE_ME" + ">",
    lambda r, p: _pick(r, HEX, 40),
    lambda r, p: f"{_pick(r, HEX, 8)}-{_pick(r, HEX, 4)}-4{_pick(r, HEX, 3)}-a{_pick(r, HEX, 3)}-{_pick(r, HEX, 12)}",
    lambda r, p: p + _pick(r, ALNUM, 4),
    lambda r, p: "change-me",
]

LANGS = {
    "py": ("config/settings.py", '{n} = "{v}"', ["import os", "", "DEBUG = False", "TIMEOUT = 30"]),
    "env": (".env.production", "{n}={v}", ["APP_ENV=production", "LOG_LEVEL=info", "PORT=8080"]),
    "yaml": ("deploy/values.yaml", '{n_l}: "{v}"', ["replicas: 2", "image: app:latest", "port: 8080"]),
    "js": ("src/config.js", "const {n_c} = '{v}';", ["export const retries = 3;", "export const region = 'ap-northeast-1';"]),
    "json": ("config/app.json", '"{n_l}": "{v}",', ['"region": "ap-northeast-1",', '"retries": 3,']),
    "go": ("internal/config/config.go", '{n_c} := "{v}"', ["timeout := 30", "region := \"ap-northeast-1\""]),
}


def _name_variants(name):
    parts = name.lower().split("_")
    return name.lower(), parts[0] + "".join(p.title() for p in parts[1:])


def _diff(r, lang, name, value):
    path, line_fmt, ctx = LANGS[lang]
    n_l, n_c = _name_variants(name)
    added = line_fmt.format(n=name, n_l=n_l, n_c=n_c, v=value)
    before, after = r.sample(ctx, 2) if len(ctx) >= 2 else (ctx[0], ctx[0])
    return (f"diff --git a/{path} b/{path}\nindex {_pick(r, HEX, 7)}..{_pick(r, HEX, 7)} 100644\n"
            f"--- a/{path}\n+++ b/{path}\n@@ -{r.randint(3, 40)},3 +{r.randint(3, 40)},4 @@\n"
            f" {before}\n+{added}\n {after}\n")


def generate(per_class=PER_CLASS):
    r = rng("secrets")
    items, n = [], 0
    langs = list(LANGS)
    for cls, (names, make) in FORMATS.items():
        for i in range(per_class):
            lang, name = langs[i % len(langs)], r.choice(names)
            value = make(r)
            n += 1
            items.append(item("secrets", n, cls, 1, _diff(r, lang, name, value), format=cls, lang=lang))
            decoy = DECOYS[i % len(DECOYS)](r, value[:4])
            n += 1
            items.append(item("secrets", n, f"neg_paired_{cls}", 0, _diff(r, lang, name, decoy), format=cls, lang=lang, decoy=i % len(DECOYS)))
    return items
