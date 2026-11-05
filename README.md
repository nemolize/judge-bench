# judge-bench

Reproducible comparison of judge models on five tasks whose correct answer is built mechanically: honorific errors, "AI-sounding" Japanese, style and notation drift, secrets in a diff, and robustness against an instruction aimed at the judge.

Judges: `gemma4:12b` and `qwen3.5:27b` through Ollama (YES/NO read from the first-token logprobs), `claude-haiku-5-5` through `claude -p` (YES/NO as text, no logprobs), three decision models called through a decisions API that returns the probability of yes (`jev-1.14.0` from TypeSafe, `clef-flash` served by Ollama, `gpt-6-luna` from OpenAI; YES when the probability is at least 0.5), and a rule-based baseline per task. `pass_bar.md` fixes what counts as beating the baseline; it was committed before any results file. The three decision models were added after the first four judges had been run, under the same bar. `results/summary.md` is the outcome.

## Rerun

Needs Python 3.13, Node with pnpm, [Ollama](https://ollama.com), [gitleaks](https://github.com/gitleaks/gitleaks) and, for the Claude judge, the `claude` CLI.

```sh
pnpm install                                  # textlint and its rules
ollama pull gemma4:12b && ollama pull qwen3.5:27b
python3 -m unittest discover -s tests         # generators are deterministic, 40+ positives per class, baselines flag a known-bad example
python3 -m judgebench.run build               # (re)generate every dataset from the seed
python3 -m judgebench.run baseline
python3 -m judgebench.run judge gemma4:12b
python3 -m judgebench.run judge qwen3.5:27b
python3 -m judgebench.run judge claude_haiku
python3 -m judgebench.run judge clef_flash                   # Ollama, model clef-flash
TYPESAFE_API_KEY=... python3 -m judgebench.run judge jev     # a TypeSafe API key
OPENAI_API_KEY=... python3 -m judgebench.run judge gpt_6_luna
python3 -m judgebench.report                  # writes results/summary.md
```

`data/secrets.jsonl` and `data/injection_secrets.jsonl` are rebuilt from the seed and not committed: random strings in the shape of real tokens trip secret scanners and push protection. Everything in this repository is dummy data; no live credential is in it.

## Baselines

| Task | Baseline | What it is |
|---|---|---|
| Honorific errors | `textlint` with `textlint-rule-ja-no-abusage` and `textlint-rule-prh` using `baselines/prh-honorific.yml` | No honorific rule exists on npm (searched `keigo`, `honorific`, `二重敬語`), so the dictionary lists the double-honorific shapes named in 文化庁「敬語の指針」 (`になられ`, `おっしゃられ`, `いらっしゃられ`, `召し上がられ`). It cannot see role swaps. |
| Style and notation drift | `textlint` with `no-mix-dearu-desumasu`, `ja-no-orthographic-variants` and a `prh` rule for full-width Latin and digits | |
| Secrets in a diff | `gitleaks detect --no-git` over each diff as a plain file | |
| "AI-sounding" Japanese | A fixed list of stock phrases (`judgebench/baselines.py`) | Hand-written before any run, never tuned; no off-the-shelf detector is claimed. |

`tests/test_baselines.py` shows each baseline flagging a known-bad example and passing a known-good one.

## Ground truth

- **Honorific errors:** error types follow the Agency for Cultural Affairs' [敬語の指針](https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/keigo_tosin.pdf) (二重敬語, 尊敬語と謙譲語の取り違え). Each positive has a paired correct sentence; 敬語連結 (`お読みになっていらっしゃる`) and established forms (`お召し上がりになる`, `お見えになる`) are extra negatives the 指針 allows.
- **"AI-sounding":** negatives are the author's own sentences from Zenn articles published before 2022-11-30 (`data/human_prose.jsonl`, dates from the Zenn API); positives are `claude -p` passages on the same topics (`data/llm_passages.jsonl`, cached so a rerun does not regenerate them).
- **Style:** clean passages from the author's prose and the LLM passages not used above, plus synthetic sentence pairs; drift is injected.
- **Secrets:** random strings in the shape of AWS, GitHub, Slack, Stripe and Google keys planted in unified diffs; negatives carry placeholders, hashes, UUIDs and truncated look-alikes in the same place.
- **Robustness:** three instructions aimed at the judge appended to honorific and secrets positives.

## Spot-check

`python3 -m judgebench.spotcheck` writes `spotcheck.md`: 10 random items per dataset (60 in all, secret-shaped values masked). All 60 were read by hand. Labels held in every case: each positive carries the planted defect, each negative is the correct paired form or a placeholder, hash or UUID. One item reads oddly without being wrong (`午後に課長が明日こちらにいらっしゃいます。`, two time words from the frame and the entry); it is a correct honorific sentence and stays a negative.

## Known limits

- The human class of the "AI-sounding" task has 25 sentences, not 40: the author's pre-ChatGPT articles hold no more prose. The 40-item floor applies to positives (60 LLM passages); the false-warning rate there carries a wide interval.
- The LLM passages mention commands and product names the author's sentences also use, but topic and length are only loosely matched; a judge may be reading content style, not authorship.
- Honorific and style text is synthetic or pulled from a few articles; a judge that does well here has not been shown to do well on arbitrary prose.
- The honorific baseline is a hand-written dictionary of the double-honorific shapes the 指針 names, and the generator draws on the same source. It is expected to do well on that class and cannot see the other two.
- Claude latency is a sequential probe of 20 calls; the 1,419 judged items ran six at a time. Local latency is one call at a time, model loaded.
- `gitleaks` flags 60 of 225 look-alike negatives (40-hex strings and UUIDs next to a variable named like a token): the scanner's generic-key rule, not noise in the dataset.
- The AI-class passages were all written by `claude-haiku-5-5`, the same model as the `claude_haiku` judge, the only judge near the bar there. The test covers one source model.
- After the first run, a review found that the honorific dictionary also matches correct sentences such as `部長になられました`, which the first negative set did not contain. Thirty-four such negatives (`neg_naru_honorific`) were added and all three judges and the baseline were rerun on them; earlier item ids and verdicts are unchanged, but every false-warning figure now divides by 209 negatives, not 175. `results/summary.md` splits false warnings by kind of negative.
- The bar's balanced-accuracy condition was implemented as the average of the two Wilson lower bounds, which is conservative. `results/summary.md` also prints a Newcombe-style bound; for `claude_haiku` on the "AI-sounding" task the two sit on either side of 0.5 (49.9% and 52.9%), so that verdict depends on the method.
- The loaded size Ollama reports varies between runs of the same model (`gemma4:12b` read 21.0 GB in the first run and 12.6 GB in the rerun; `qwen3.5:27b` 28.4 and 28.3 GB). `results/` keeps the last reading.
- The two honorific classes that `claude_haiku` passes depend on the added negatives. On the first 175 negatives its false warnings were 38/175 (22%), above the limit of 10%, so neither class passed. After the 34 additions the baseline's own false warnings are 34/209 (16.3%), which loosens condition 2 to 21.3%, and `claude_haiku` at 42/209 (20.1%) fits by 1.2 points.
- The decision models are asked the question as an instruction with true/false criteria (`prompts/decisions.json`), not the YES/NO prompt the other judges get, and the text goes in as the input. The 0.5 cut is the pass bar's, not tuned per model; `results/summary.md` adds a threshold-free AUC from the returned probability, which can differ a lot from the 0.5 result (a judge with a high AUC and low recall at 0.5 ranks well but is not calibrated for this question).
- `clef-flash` is the small Clef variant installed locally; the larger `clef` was not run.
- `gpt-6-luna` returned no answer for one injected secrets item (counted as not flagged).
