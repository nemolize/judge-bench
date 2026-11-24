# judge-bench

Reproducible comparison of judge models on five tasks whose correct answer is built mechanically: honorific errors, "AI-sounding" Japanese, style and notation drift, secrets in a diff, and robustness against an instruction aimed at the judge.

Not related to [JudgeBench](https://github.com/ScalerLab/JudgeBench) (ICLR 2025), which scores LLM judges on English response-pair preferences; this repository compares rule-based, LLM and decision-model judges on Japanese judgement tasks.

Judges:

| Judge | Reached through | Verdict |
|---|---|---|
| `gemma4:12b`, `gemma4:26b`, `gemma4:31b`, `qwen3.5:27b` | Ollama | YES when the first-token probability of `YES` is at least that of `NO` |
| `gemma4:12b+think` | Ollama, thinking on | first word of the answer, no logprobs |
| `gemma4:26b+think` | Ollama, thinking on | same; honorific and style only |
| `sync_m_think` (Qwen3.8-Flash-Next 125B MoE, Sync-M pack) | Sync-Strata 0.1.4 OpenAI-compatible API, `reasoning_effort` low | first line of the reply, no logprobs |
| `qwen3.8_iq3_s` (same model, ISTA-DASLab IQ3_S pack) | Strata 0.2.20 (terminal build 0.1.66) API, thinking off | YES when the first-token probability of `YES` is at least that of `NO` |
| `qwen3.8_iq3_s_think` | same engine, `reasoning_effort` low | first line of the reply, no logprobs |
| `claude_api_think`, `claude_api_off` (`claude-haiku-5-5`) | Messages API, thinking on / off | YES/NO as text, no logprobs |
| `gemini_flash` (`gemini-3.7-flash`) | Gemini API | YES/NO as text, no logprobs |
| `jev` (`jev-1.14.0`), `clef_flash`, `clef` (27B, Cloudflare Workers AI), `gpt-6-luna`, `gemini_decision` (`gemini-decision-1`, Gemini Decisions API) | decisions API (`clef-flash` served by Ollama) | YES when the probability of yes is at least 0.5 |
| `claude_haiku` | `claude -p` | YES/NO as text; run first, disagrees with the API runs, not used in the article |

Each task also has a rule-based baseline. `pass_bar.md` fixes what counts as beating the baseline; it was committed before any results file. The decision models were added after the first judges had been run, under the same bar. `results/summary.md` is the outcome.

## Rerun

Needs Python 3.13, Node with pnpm 10 or later, [Ollama](https://ollama.com), [gitleaks](https://github.com/gitleaks/gitleaks) and, for the `claude_haiku` judge only, the `claude` CLI.

```sh
pnpm install                                  # textlint and its rules
ollama pull gemma4:12b && ollama pull gemma4:26b && ollama pull gemma4:31b && ollama pull qwen3.5:27b
python3 -m unittest discover -s tests         # generators are deterministic, 40+ positives per class, baselines flag a known-bad example
python3 -m judgebench.run build               # (re)generate every dataset from the seed
python3 -m judgebench.run baseline
python3 -m judgebench.run judge gemma4:12b
python3 -m judgebench.run judge gemma4:26b
python3 -m judgebench.run judge gemma4:31b
python3 -m judgebench.run judge gemma4:12b+think
python3 -m judgebench.run judge gemma4:26b+think honorific style   # thinking on, no logprobs; the first word of the answer decides
python3 -m judgebench.run judge qwen3.5:27b
# Strata judges: start the engine (Sync-Strata `sync.sh up --api-only`, or Strata `strata launch --family qwen --model iq3_s --context 32k --vision off`), then point STRATA_URL at it
STRATA_URL=http://127.0.0.1:8080/v1 python3 -m judgebench.run judge sync_m+think          # one engine at a time: they share the GPU
STRATA_URL=http://127.0.0.1:8080/v1 python3 -m judgebench.run judge qwen3.8_iq3_s
STRATA_URL=http://127.0.0.1:8080/v1 python3 -m judgebench.run judge qwen3.8_iq3_s+think
python3 -m judgebench.run judge claude_haiku
pip install anthropic                        # only for the two claude_api_* judges
ANTHROPIC_API_KEY=... python3 -m judgebench.run judge claude_api_think   # Messages API, default thinking
ANTHROPIC_API_KEY=... python3 -m judgebench.run judge claude_api_off     # Messages API, thinking disabled
GEMINI_API_KEY=... python3 -m judgebench.run judge gemini_flash   # gemini-3.7-flash; no logprobs, so the first line of the reply decides
python3 -m judgebench.run judge clef_flash                   # Ollama, model clef-flash
TYPESAFE_API_KEY=... python3 -m judgebench.run judge jev     # a TypeSafe API key
CLOUDFLARE_ACCOUNT_ID=... CLOUDFLARE_API_TOKEN=... python3 -m judgebench.run judge clef   # Workers AI Read
OPENAI_API_KEY=... python3 -m judgebench.run judge gpt_6_luna
GEMINI_API_KEY=... python3 -m judgebench.run judge gemini_decision   # gemini-decision-1; the probability is clamped to 0.01-0.99 by the API
python3 -m judgebench.report                  # writes results/summary.md
pip install matplotlib && python3 -m judgebench.charts <dir>   # the article's three charts
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

- **Honorific errors:** error types follow the Agency for Cultural Affairs' [敬語の指針](https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/keigo_tosin.pdf) (二重敬語, 尊敬語と謙譲語の取り違え). Each positive has a paired correct sentence; 敬語連結 (`お読みになっていらっしゃる`), established forms (`お召し上がりになる`, `お見えになる`) and correct `〜になられる` are extra negatives. The prompt tells the judge the speaker is addressing someone outside the company, and the swap classes use subjects that are unambiguously outside (`お客様`, `取引先の担当の方`, ...), so a sentence such as `部長が本社に参りました。` (fine about one's own manager) is not a positive.
- **"AI-sounding":** negatives are the author's own sentences from Zenn articles published before 2022-11-30 (`data/human_prose.jsonl`, dates from the Zenn API); positives are one-sentence texts on the same topics from three generators, `claude-haiku-5-5`, `gemma4:12b` and `qwen3.5:27b`, 45 each, drawn so that their length follows the human sentences' (`data/llm_sentences.jsonl`, cached so a rerun does not regenerate them). The summary reports the AUC of character count and of sentence count alone, as a check on what the dataset gives away.
- **Style:** clean passages from the author's prose and multi-sentence LLM passages (`data/llm_passages.jsonl`), plus synthetic sentence pairs; drift is injected.
- **Secrets:** random strings in the shape of AWS, GitHub, Slack, Stripe and Google keys planted in unified diffs; negatives carry placeholders, hashes, UUIDs and truncated look-alikes in the same place. The task is spotting a value that matches a key format; the values are never valid credentials, and the prompt says validity is not judged.
- **Robustness:** three instructions aimed at the judge appended to honorific and secrets positives.

## Spot-check

`python3 -m judgebench.spotcheck` writes `spotcheck.md`: 10 random items per dataset (60 in all, secret-shaped values masked). All 60 were read by hand after the datasets were rebuilt (see History). Labels held in every case: each positive carries the planted defect, each negative is the correct paired form or a placeholder, hash or UUID.

## History

The first full run was reviewed before publication and several design problems were found; the datasets and prompts below were then changed and every judge was rerun on the changed tasks (the style task and its results are unchanged). The pass bar, the judges' calls and the report's pass logic were not changed. Earlier versions stay in the git history.

- The AI-class texts were multi-sentence while every human text was one sentence, so "more than one sentence means AI" alone scored 71.7% balanced accuracy. The positives are now one sentence, length-matched, from three generators.
- The secrets prompt asked for "usable credentials" while every positive was an invalid random string. The prompt now asks for a value matching a key format and says validity is not judged.
- Some honorific positives were only wrong if the subject was outside the company. The prompt now states the setting and the swap classes use unambiguous subjects.
- The honorific dictionary also matches correct `〜になられる`; 34 such negatives were added before this rerun.
- A second review found that the honorific setting ("speaking to someone outside the company") made `部長が本社にいらっしゃいました` wrong, yet unaffiliated `部長` / `課長` / `社長` subjects were still used in the double-honorific and negative sets (58 negatives; `claude_haiku` flagged 54 of them). Every honorific sentence now uses a subject that is unambiguously outside the company or the speaker; honorific and injection results were rerun.
- A third review found that `先生がお話をうかがいました` can be correct depending on whose talk was heard, and that some honorific sentences carried two time expressions (`先ほど私が昨日お話を…`). The humble-for-other class now uses only forms that are wrong for any outside subject (`申す`, `参る`, `存じる`, with the matching honorific); predicates that already hold a time word take no extra one; duplicate sentences are dropped. Honorific and injection results were rerun for every judge.
- The threshold halves now keep identical sentences, derivations of one source text and both members of each positive/negative pair (`pair_id`) together, so no sentence or pair spans both sides.
- For the Ollama LLMs, the sampled first token and the returned probabilities disagreed (23 of 1,494 results for `gemma4_12b`, 224 for `qwen3.5_27b`: at temperature 0 the sampled token is not always the more probable one). The verdict is now decided by the probability, as it is for the decision models; stored results were rederived with `python3 -m judgebench.run rederive <judge>`, and the honorific results were rerun.
- The threshold analysis split each task into alternating halves by id, which put whole file types and whole decoy kinds in one half. The halves are now seeded shuffles within each class, file type and decoy kind.

## Known limits

- The human class of the "AI-sounding" task has 25 sentences, not 40: the author's pre-ChatGPT articles hold no more prose. The 40-item floor applies to positives (45 per generator); the false-warning rate there carries a wide interval.
- The human sentences come from one author and four articles; the AI sentences are prompted to match their topics and length, not their style.
- Honorific and style text is synthetic or pulled from a few articles; a judge that does well here has not been shown to do well on arbitrary prose.
- The honorific baseline is a hand-written dictionary of the double-honorific shapes the 指針 names, and the generator draws on the same source. It is expected to do well on that class and cannot see the other two.
- Claude, Jev and GPT latency is a sequential probe of 20 calls; the judged items ran six at a time. Local latency is one call at a time, model loaded.
- `gitleaks` flags 60 of 225 look-alike negatives (40-hex strings and UUIDs next to a variable named like a token): the scanner's generic-key rule, not noise in the dataset.
- The bar's balanced-accuracy condition was implemented as the average of the two Wilson lower bounds, which is conservative. `results/summary.md` also prints a Newcombe-style bound, and the verdict for a judge near 0.5 can depend on the method.
- The loaded size Ollama reports varies between runs of the same model. `results/` keeps the last reading.
- The decision models are asked the question as an instruction with true/false criteria (`prompts/decisions.json`), not the YES/NO prompt the other judges get, and the text goes in as the input. The pass bar fixes the 0.5 cut; `results/summary.md` adds a threshold-free AUC and a table where the cut is chosen on one half of each task and measured on the other half. The chosen cut is a post-hoc analysis, not part of the bar.
- `clef-flash` is the small Clef variant (9B) run locally through Ollama; `clef` (27B) was run on Cloudflare Workers AI, so the two differ in size and in where they run. The Workers AI request body carries no `model` field (the model is in the URL): a body with the full `@cf/cloudflare/clef` id returned HTTP 400, and the requests without it all succeeded (1,494 results, no errors). Cloudflare's model page lists a `model` field, so the call may need revisiting if the API changes; its answers are wrapped in `result`.
- Injection flip rates are conditional on the items a judge flagged without the instruction, so the denominators differ by judge, and only three instruction texts were tried.
- Results without a probability keep the sampled-token verdict and are left out of the threshold analysis: 3 style and 3 honorific-injection results of `gemma4_12b`; `gpt-6-luna` gave no answer for 2 injected secrets items (counted as not flagged).
- Transient HTTP 5xx answers from the hosted APIs are retried; an item that still fails is recorded as an error and rerun, never scored as `NO`.
- The Strata judges ran on another machine than the Ollama ones (Manjaro Linux, i9-13900K, GeForce RTX 2070 SUPER 8 GB, 62 GB RAM), measured on 2026-11-23 and 24, one engine at a time. The runner stayed on the first machine and reached the engine through an SSH tunnel (about 0.02 s round trip, included in the latency; the first call is not discarded). One run each.
- Versions: Sync-Strata 0.1.4 with the Sync-M pack (`sync-strata/Sync-M` at revision `435b4178227d9fb13b7e63f8645b7213819419a2`); Strata 0.2.20 (terminal build 0.1.66) with the ISTA-DASLab IQ3_S pack of Qwen3.8-Flash-Next (revision not recorded). Both run the same base model, so a difference between them comes from the pack or the engine, which this benchmark cannot separate.
- Sync-Strata returns no logprobs, so `sync_m_think` is decided by the first line of the reply, like the Claude and Gemini judges; it also gets their system message. `qwen3.8_iq3_s` is decided by probability, as the Ollama judges are, and gets no system message. The thinking runs use `reasoning_effort` low with room for 4,096 tokens. Do not compare these judges' no-answer or false-warning rates with the Ollama ones without this in mind.
- The memory column for the Strata judges is the engine process's resident memory (Sync-M 34.8 GiB, IQ3_S 49.8 GiB; about 7.3 to 7.5 GiB of the 8 GiB GPU on top), not the loaded size Ollama reports.
- Two more judges were run and then left out of `JUDGES` in `judgebench/report.py`, so they are not in `results/summary.md`; their result files stay in `results/`. `sync_m` (Sync-M, thinking off) answered the same word whatever the sentence: with the honorific prompt it caught 1 of 135 positives and flagged 0 of 209 negatives, and a 24-item check (12 positives, 12 negatives; not stored in `results/`) with other answer words gave one word for almost every item: with "NO means an error" 23 of 24 answers were NO, with "A means an error" 23 of 24 were A, and with "B means an error" 18 of 24 were B (12 of 12 positives, 6 of 12 negatives). Its direct answer carried little information about the sentence, though thinking on (`sync_m_think`) judges well. `inkling_2_mini` (Inkling-2-Mini SQ-20 on Strata 0.2.20, no logprobs) answered YES to 208 of 209 correct honorific sentences, to 57% of correct style passages and to 24 of 25 human sentences.
