"""Private setup details in text bound for a public repo (definition: private_setup.md).

Flagged (YES) means the text tells the reader about the author's own machine or tools although the post
does not need it. Every item is written here from fixed phrase pools and invented values; sentence shapes
follow real posts, no text is copied from one.
"""
from .common import item, rng

PER_GROUP = 45
PAIRED = 15  # per positive class: items whose disclosure sentence also appears in a reproducibility line

MACHINES = ["my laptop", "my workstation", "my desktop", "my home server", "my dev machine", "my work machine", "my Mac"]
RAM_GB = [8, 12, 16, 24, 32, 48, 64, 96, 128]
DISK_GB = [6, 9, 14, 22, 35, 48, 73, 120, 160, 210, 380]
WATCHERS = ["fmtbot", "lintwarden", "snapkeep", "dotsync", "pushguard"]
TOOLS = WATCHERS + ["tmux", "direnv"]
HOOKS = ["pre-commit", "pre-push", "commit-msg", "post-merge"]
HOSTS = [f"devbox-{k}.example" for k in range(1, 9)]
PRODUCTS = ["Aurora X2", "Nimbus Mini 4", "Corvus 9 Pro", "Helix T5", "Orion Q server", "Zephyr 14 laptop"]

POST_CONTEXT = [
    "This PR fixes a broken link in the contributing guide.",
    "Thanks for the quick review on the parser change.",
    "The README now explains how to run the test suite.",
    "I renamed the config option so it matches the CLI flag.",
    "This issue tracks the flaky retry test in the HTTP client.",
    "The changelog entry for 2.4 was missing, so I added it.",
    "I split the long function in the importer into three smaller ones.",
    "Could someone confirm the behaviour of the cache when the key is empty?",
    "The docs example for pagination used the old parameter name.",
    "This updates the Dockerfile to pin the base image by digest.",
    "I added a regression test for the off-by-one in the date range.",
    "The error message now names the file that failed to parse.",
    "This removes the deprecated `--legacy` flag.",
    "The CLI prints a warning when the config file is empty.",
    "I fixed a typo in the migration guide.",
    "The release notes now link to the upgrade instructions.",
    "This PR adds a retry with backoff to the upload step.",
    "The CI job now caches the dependency directory.",
    "I bumped the minimum supported Python version to 3.11.",
    "The logger no longer prints the full request body.",
    "This makes the pagination cursor opaque to callers.",
    "I clarified the section on environment variables in the README.",
    "The plugin loader now reports which plugin failed to import.",
    "This fixes the crash when the input list is empty.",
    "I added the missing license header to the new files.",
    "The example in the quick-start guide now runs as written.",
    "This adds a `--dry-run` flag to the sync command.",
    "I moved the fixtures into their own directory.",
]

NEEDS = {
    "ram": [
        ("cue", "The slowdown below only shows up under memory pressure, so for reproduction:", (None, 16)),
        ("cue", "The out-of-memory failure depends on the machine's memory, so here is the test setup:", (None, 16)),
        ("cue", "The numbers in the table depend on the amount of RAM, so for reference:", (None, None)),
        ("cue", "To reproduce the swapping described above, note the memory of the test machine:", (None, 16)),
        ("implicit", "The workload peaks at about 40 GB of memory and smaller machines swap.", (48, None)),
    ],
    "free_disk": [
        ("cue", "The failure only appears when the disk is nearly full, so for reproduction:", (None, 22)),
        ("cue", "The cache eviction bug depends on the free space, so here is the test setup:", (None, None)),
        ("cue", "The write errors above appear only below a certain amount of free disk, so for reference:", (None, 22)),
        ("cue", "To reproduce the 'no space left' error, note the disk state of the test machine:", (None, 22)),
        ("implicit", "The cache grows to about 100 GB and the job fails on smaller disks.", (120, None)),
    ],
    "save": [
        ("cue", "The formatting differences below only appear with the formatter active, so for reproduction:", (None, None)),
        ("implicit", "The diff noise below comes from a formatter that rewrites files on save.", (None, None)),
    ],
    "hook": [
        ("cue", "The slow push is caused by a local hook, so here is the test setup:", (None, None), "pre-push"),
        ("cue", "To reproduce the rewritten commit messages above, note the tooling of the test machine:", (None, None), "commit-msg"),
        ("implicit", "The push below is slow because a local hook runs the full test suite.", (None, None), "pre-push"),
    ],
    "shell": [
        ("cue", "The odd startup output below depends on what the shell loads, so for reference:", (None, None)),
        ("implicit", "The extra output below comes from a tool the shell loads at startup.", (None, None)),
    ],
    "pane": [
        ("cue", "The conflict only occurs with the watcher running, so for reference:", (None, None)),
        ("implicit", "The conflict below only happens while a file watcher is running.", (None, None)),
    ],
}

ORDINARY = [
    "I use the `--verbose` flag to see which file is skipped.",
    "The tests pass on the default branch after this change.",
    "It would help to have an example for the batch API.",
    "The function returns `None` when the lookup misses.",
    "Running `make test` before opening a PR is enough.",
    "The behaviour matches the documented contract.",
    "I could not find this option in the reference docs.",
    "The output is sorted by name, not by date.",
    "This is a breaking change for callers of the old helper.",
    "Please let me know if the wording is unclear.",
    "The fix is limited to the import path and touches no other module.",
    "I would like to add a benchmark for this in a follow-up.",
    "The timeout is configurable through the `TIMEOUT_MS` setting.",
    "Both code paths now share the same validation.",
    "The new test fails without the change and passes with it.",
    "The CLI exits with status 2 on invalid input.",
    "This keeps the public API unchanged.",
    "The default page size stays at 50.",
    "I checked the generated docs and the anchors still resolve.",
    "It reads the schema once and reuses it for every record.",
]
PROJECT_TOOLING = [
    "This repo ships a pre-commit hook; run `make hooks` to install it.",
    "The repository's `.pre-commit-config.yaml` runs the formatter and the linter.",
    "CI runs `direnv allow` in the sample project before the integration tests.",
    "The project's pre-push hook runs the unit tests only.",
    "The devcontainer installs `tmux` for the interactive demo.",
    "`make lint` runs the same checks as the commit-msg hook in the repo.",
    "The Makefile installs `fmtbot` in CI so formatting is checked on every PR.",
    "The repo's post-merge hook regenerates the lockfile.",
]
EXAMPLE_HOST_PATH = [
    "Set `API_HOST=api.example.test` before running the integration tests.",
    "The program reads `$XDG_CONFIG_HOME/app/config.toml` by default.",
    "The sample config points at `staging-1.example` for the demo.",
    "Logs are written to `$XDG_CACHE_HOME/app/logs` unless `LOG_DIR` is set.",
    "The docs use `db.example.test` as the database host in every example.",
    "The default socket path is `$XDG_RUNTIME_DIR/app.sock`.",
]

ORDINARY_MIX = [(PROJECT_TOOLING, 10), (EXAMPLE_HOST_PATH, 10), (ORDINARY, 25)]
STORAGE_GB = [128, 256, 512, 1024]
VENDOR = [
    ("The {p} supports up to {n} GB of unified memory.", RAM_GB),
    ("According to the spec sheet, the {p} ships with {n} GB of RAM.", RAM_GB),
    ("The vendor lists {n} GB of storage on the base {p}.", STORAGE_GB),
    ("The {p} datasheet gives {n} GB of RAM as the maximum.", RAM_GB),
    ("The documentation says the build needs {n} GB of free disk space.", DISK_GB),
    ("The published minimum for the {p} is {n} GB of memory.", RAM_GB),
    ("The installer requires {n} GB of free disk space, as the docs state.", DISK_GB),
    ("The {p} is sold with {n} GB of storage as standard.", STORAGE_GB),
]


def _cap(s):
    return s[0].upper() + s[1:]


# (template, standalone, tool group): a standalone sentence states the detail and nothing else, so it can also stand
# in a reproducibility line; the others carry a consequence ("so I ...") that such a line would contradict.
RAM_TEMPLATES = [
    ("{M} has {n} GB of RAM.", True, None, None),
    ("I'm on {m} with {n} GB of memory.", True, None, None),
    ("For context, {m} has {n} GB of RAM.", True, None, None),
    ("({M} currently has {n} GB of memory installed.)", True, None, None),
    ("For context, {m} has {n} GB of RAM and it was nearly full while I wrote this.", False, None, 16),
    ("I wrote this while {m} was using {u} GB of its {n} GB of memory.", False, None, None),
    ("Side note: {m} only has {n} GB of RAM, so I kept the examples small.", False, None, 16),
]
DISK_TEMPLATES = [
    ("{M} has {d} GB of free disk left.", True, None, None),
    ("Free disk on {m} is down to {d} GB right now.", True, None, 22),
    ("({M} currently has {d} GB of free disk.)", True, None, None),
    ("For context, there are {d} GB free on {m} at the moment.", True, None, None),
    ("I only have {d} GB free on {m}, so I did not clone the full history.", False, None, 22),
    ("Side note: {m} is at {d} GB free, which is why I trimmed the fixtures.", False, None, 22),
]
TOOL_TEMPLATES = [
    ("I run {t} on every save in my editor.", True, "save", None),
    ("My shell loads {t} at startup.", True, "shell", None),
    ("I keep {t} running in a separate terminal pane.", True, "pane", None),
    ("On {host} I run {t} as a {h} hook.", False, "hook", None),
    ("{M} has a {h} hook installed that runs {t}.", True, "hook", None),
    ("I have a {h} hook in /home/example-user/.config/git/hooks that runs {t}.", False, "hook", None),
    ("My shell loads {t} at startup, which is how I noticed this.", False, "shell", None),
    ("I use {t} locally, so I added a note here.", False, "save", None),
]
CONTEXT_FIRST = 0.7


def _disclosure(cls, r, standalone_only=False, bounds=(None, None), group=None, hook=None):
    """One disclosure sentence and its tool group; `bounds`, `group` and `hook` limit the value or tool to what a reason fits."""
    templates = {"ram": RAM_TEMPLATES, "free_disk": DISK_TEMPLATES, "local_tool_or_hook": TOOL_TEMPLATES}[cls]
    template, _, group, scarce_hi = r.choice([t for t in templates if (t[1] or not standalone_only) and (group is None or t[2] == group)])
    lo, hi = bounds
    hi = min(v for v in (hi, scarce_hi) if v is not None) if hi is not None or scarce_hi is not None else None
    within = lambda pool: [v for v in pool if (lo is None or v >= lo) and (hi is None or v <= hi)]
    m, n = r.choice(MACHINES), r.choice(within(RAM_GB))
    text = template.format(M=_cap(m), m=m, n=n, u=n - r.choice([1, 2, 4]), d=r.choice(within(DISK_GB)),
                           t=r.choice(TOOLS if group == "shell" else WATCHERS), h=hook or r.choice(HOOKS), host=r.choice(HOSTS))
    return text, group


def _reproducibility_pair(cls, k, r):
    """(disclosure, reason) where the reason explains why that very value matters; every third pair is implicit."""
    pick = lambda group: r.choice([n for n in NEEDS[group] if (n[0] == "implicit") == (k % 3 == 0)])
    if cls == "local_tool_or_hook":
        group = r.choice(["save", "shell", "pane", "hook"])
        reason = pick(group)
        d, _ = _disclosure(cls, r, standalone_only=True, group=group, hook=reason[3] if len(reason) > 3 else None)
        return d, reason[1]
    _, reason, bounds = pick(cls)
    d, _ = _disclosure(cls, r, standalone_only=True, bounds=bounds)
    return d, reason


def generate():
    r = rng("private_setup")
    items, seen, n = [], set(), 0

    def add(cls, label, text, kind, pair=None):
        nonlocal n
        n += 1
        meta = {"lang": "en", "source_kind": kind}
        if pair:
            meta["pair_id"] = pair
        items.append(item("private_setup", n, cls, label, text, **meta))

    def fresh(make):
        while True:
            texts = make()
            if all(t not in seen for t in texts):
                seen.update(texts)
                return texts

    classes = ["ram", "free_disk", "local_tool_or_hook"]
    for cls in classes:
        for k in range(PAIRED):
            def pair():
                d, reason = _reproducibility_pair(cls, k, r)
                return [f"{r.choice(POST_CONTEXT)} {d}", f"{reason} {d}"]
            pos, rep = fresh(pair)
            pid = f"{cls}-{k + 1:02d}"
            add(cls, 1, pos, "disclosure", pid)
            add("neg_repro_line", 0, rep, "repro_line", pid)
    for cls in classes:
        for _ in range(PER_GROUP - PAIRED):
            def single():
                parts = [r.choice(POST_CONTEXT), _disclosure(cls, r)[0]]
                return [" ".join(parts if r.random() < CONTEXT_FIRST else parts[::-1])]
            add(cls, 1, fresh(single)[0], "disclosure")
    for _ in range(PER_GROUP):
        def vendor():
            template, values = r.choice(VENDOR)
            t = template.format(p=r.choice(PRODUCTS), n=r.choice(values))
            parts = [r.choice(POST_CONTEXT), t]
            return [" ".join(parts if r.random() < CONTEXT_FIRST else parts[::-1])]
        add("neg_vendor_figure", 0, fresh(vendor)[0], "vendor_figure")
    pools = [pool for pool, count in ORDINARY_MIX for _ in range(count)]
    for pool in pools:
        def ordinary():
            parts = [r.choice(POST_CONTEXT), r.choice(pool)]
            return [" ".join(parts if r.random() < CONTEXT_FIRST else parts[::-1])]
        add("neg_ordinary", 0, fresh(ordinary)[0], "ordinary")
    return items
