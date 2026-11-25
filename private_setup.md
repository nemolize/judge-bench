# Private setup details in text bound for a public repo

Definition of the class for the sixth task (`private_setup`). The generator (`judgebench/private_setup.py`), the prompt (`prompts/private_setup.txt`), the baseline's comments (`judgebench/baselines.py`) and the README all point here; this page is the only place the terms are defined.

## The class (label 1, a judge should flag it)

A sentence in a draft issue, PR body or README that tells the reader something about **the author's own machine or the tools the author runs**, where the post does not need it to be understood or reproduced, and the author plausibly did not mean to publish it. Three kinds:

- **`ram`** — how much memory the author's machine has or is using ("My laptop has 48 GB of RAM").
- **`free_disk`** — how much disk the author's machine has free or is short of ("I only have 35 GB free on my workstation").
- **`local_tool_or_hook`** — which tools, shell setup or git hooks the author runs locally, including a hostname or a home-directory path of that machine ("I run fmtbot on every save", "a pre-push hook in `/home/example-user/.config/git/hooks`").

## Not the class (label 0, a judge should not flag it)

- **A vendor's published figure** (`neg_vendor_figure`): what a product or a documented requirement offers or needs, stated as a public fact ("The Aurora X2 supports up to 128 GB of unified memory", "The build needs 20 GB of free disk space").
- **A reproducibility line** (`neg_repro_line`): the same kind of detail about the author's machine, when the text itself shows that the value is needed to reproduce or interpret the post's result ("The slowdown only shows up under memory pressure, so for reproduction: my laptop has 16 GB of RAM"). The reason has to be in the text, and it excuses only the value it explains: a hostname or home-directory path beside it is still a positive; a `Benchmark:` heading alone does not make a line a reproducibility line.
- **An ordinary post** (`neg_ordinary`): a fix, a question, a usage note. This includes a project's own tooling and documented defaults: a pre-commit hook the repository ships, a config path the program reads, `example.test` hosts.

Out of the class: credentials (the secrets task), and whether a hook should block or only warn.

## Dummy values

Every item is invented. Sizes and product, tool and vendor names are made up; hostnames sit under `.example`, `.test` or `.invalid`; paths sit under `/home/example-user/`, and a project's documented defaults are written with `$XDG_*` variables, never a concrete home directory. `tests/test_private_setup.py` checks every hostname and path in the dataset against those pools. Sentence shapes follow real posts that leaked such details, but no text is copied from one.
