# judge-bench

Reproducible comparison of judge models on six tasks whose correct answer is built mechanically: honorific errors, "AI-sounding" Japanese, style and notation drift, secrets in a diff, private setup details in text bound for a public repo, and robustness against an instruction aimed at the judge.

Not related to [JudgeBench](https://github.com/ScalerLab/JudgeBench) (ICLR 2025), which scores LLM judges on English response-pair preferences; this repository compares rule-based, LLM and decision-model judges on Japanese judgement tasks.

Judges:

| Judge | Reached through | Verdict |
|---|---|---|
| `gemma4:12b`, `gemma4:26b`, `gemma4:31b`, `qwen3.5:27b` | Ollama | YES when the first-token probability of `YES` is at least that of `NO` |
| `gemma4:12b+think` | Ollama, thinking on | first word of the answer, no logprobs |
| `gemma4:26b+think` | Ollama, thinking on | same; honorific, style and private setup |
| `sync_m_think` (Qwen3.8-Flash-Next 125B MoE, Sync-M pack) | Sync-Strata 0.1.4 OpenAI-compatible API, `reasoning_effort` low | first line of the reply, no logprobs |
| `qwen3.8_iq3_s` (same model, ISTA-DASLab IQ3_S pack) | Strata 0.2.20 (terminal build 0.1.66) API, thinking off | YES when the first-token probability of `YES` is at least that of `NO` |
| `qwen3.8_iq3_s_think` | same engine, `reasoning_effort` low | first line of the reply, no logprobs |
| `claude_api_think`, `claude_api_off` (`claude-haiku-5-5`) | Messages API, thinking on / off | YES/NO as text, no logprobs |
| `gemini_flash` (sent as `gemini-3.7-flash`) | Gemini API | YES/NO as text, no logprobs; run on 2026-11-07, after the model was deprecated on 2026-10-08, so the API answered with `gemini-3.8-flash` (kept for the record, not in the article) |
| `gemini_3_8_flash` (`gemini-3.8-flash`), `gemini_4_hydrogen` (`gemini-4-hydrogen`) | Gemini API, `thinkingLevel` low | same as `gemini_flash`; run on 2026-11-27, each result records the `modelVersion` the API returned and the token counts |
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
# private-setup task only: its three judges (ollama pull gemma4:26b first)
python3 -m judgebench.run judge gemma4:12b private_setup
python3 -m judgebench.run judge gemma4:26b+think private_setup
ANTHROPIC_API_KEY=... python3 -m judgebench.run judge claude_api_think private_setup   # also probes its sequential latency on this task
GEMINI_API_KEY=... python3 -m judgebench.run judge gemini_flash   # gemini-3.7-flash; no logprobs, so the first line of the reply decides
GEMINI_API_KEY=... python3 -m judgebench.run judge gemini_3_8_flash   # same method, model gemini-3.8-flash
GEMINI_API_KEY=... python3 -m judgebench.run judge gemini_4_hydrogen  # same method, model gemini-4-hydrogen
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
| Private setup details | A list of regular expressions (`PRIVATE_SETUP_PATTERNS` in `judgebench/baselines.py`) | A first-person machine next to a size in GB or TB, a free-disk figure, "I run ... hook / tmux / zsh", a home-directory path. Committed before any result of the task, never tuned. |

`tests/test_baselines.py` shows each baseline flagging a known-bad example and passing a known-good one; the private-setup baseline's is in `tests/test_private_setup.py`.

## Ground truth

- **Honorific errors:** error types follow the Agency for Cultural Affairs' [敬語の指針](https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/keigo_tosin.pdf) (二重敬語, 尊敬語と謙譲語の取り違え). Each positive has a paired correct sentence; 敬語連結 (`お読みになっていらっしゃる`), established forms (`お召し上がりになる`, `お見えになる`) and correct `〜になられる` are extra negatives. The prompt tells the judge the speaker is addressing someone outside the company, and the swap classes use subjects that are unambiguously outside (`お客様`, `取引先の担当の方`, ...), so a sentence such as `部長が本社に参りました。` (fine about one's own manager) is not a positive.
- **"AI-sounding":** negatives are the author's own sentences from Zenn articles published before 2022-11-30 (`data/human_prose.jsonl`, dates from the Zenn API); positives are one-sentence texts on the same topics from three generators, `claude-haiku-5-5`, `gemma4:12b` and `qwen3.5:27b`, 45 each, drawn so that their length follows the human sentences' (`data/llm_sentences.jsonl`, cached so a rerun does not regenerate them). The summary reports the AUC of character count and of sentence count alone, as a check on what the dataset gives away.
- **Style:** clean passages from the author's prose and multi-sentence LLM passages (`data/llm_passages.jsonl`), plus synthetic sentence pairs; drift is injected.
- **Secrets:** random strings in the shape of AWS, GitHub, Slack, Stripe and Google keys planted in unified diffs; negatives carry placeholders, hashes, UUIDs and truncated look-alikes in the same place. The task is spotting a value that matches a key format; the values are never valid credentials, and the prompt says validity is not judged.
- **Private setup:** `private_setup.md` defines the class. 270 English items (`data/private_setup.jsonl`) are written by `judgebench/private_setup.py` from fixed phrase pools and invented values: 45 positives in each of `ram`, `free_disk` and `local_tool_or_hook` (a sentence about the author's own machine or tools next to an unrelated post sentence), and 45 negatives in each of `neg_ordinary` (fixes, questions, a repo's own hooks and documented defaults), `neg_vendor_figure` (a product's published figures or a documented requirement) and `neg_repro_line` (the same kind of detail, but the text says it is needed to reproduce the result). 15 items per positive class are paired with a `neg_repro_line` item that carries the identical disclosure sentence and differs only in the sentence before it (`pair_id`). Only sentence shapes follow real posts that leaked such details; no text is copied from one and every hostname, path, size and name is invented. The prompt is Japanese over English text, as for the secrets task.
- **Robustness:** three instructions aimed at the judge appended to honorific and secrets positives.

## Spot-check

`python3 -m judgebench.spotcheck` writes `spotcheck.md`: 10 random items per dataset, and for `private_setup` 2 from each of its six classes and groups (secret-shaped values masked). The earlier datasets' samples were read by hand after they were rebuilt (see History); the `private_setup` sample was read by hand against `private_setup.md` after the generator was last changed, and every label held. Labels held in every case: each positive carries the planted defect, each negative is the correct paired form or a placeholder, hash or UUID.

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

- The private-setup items come from a generator: a few dozen sentence templates and context sentences, recombined. Wording repeats far more than in real posts, the context sentence is always one short line, and the disclosure is easier to see than in a long README. A judge's catch rate here is a guide to how it would do in front of a real hook, not a measurement of one. What the author would not have meant to publish cannot be read off a published text, so the labels follow the rule in `private_setup.md`: a detail is a positive unless the text itself shows it is needed.
- Every reproducibility line in the private-setup set is built from a stated reason plus the disclosure, and the reason is matched to the value (a memory-pressure reason only goes with a small RAM figure). A third of them state the reason only implicitly ("The workload peaks at about 40 GB of memory and smaller machines swap."), the rest announce it ("so for reproduction:"); real posts can be vaguer than either, so the false-warning rate on this group is a lower bound for real text.
- For the private-setup task `results/summary.md` marks a row with fewer than 40 valid positives, or a judge with more than 5% errors, as not measurable; the other tasks' tables were published without that check and some of their rows exceed 5% errors.
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
- The Strata judges except `qwen3.8_q2_0` (below) ran on another machine than the Ollama ones (Manjaro Linux, i9-13900K, GeForce RTX 2070 SUPER 8 GB, 64 GB RAM), measured on 2026-11-23 and 24, one engine at a time. The runner stayed on the first machine and reached the engine through an SSH tunnel (about 0.02 s round trip, included in the latency; like every judge without a sequential probe, the median leaves out the first call). One run each.
- Versions: Sync-Strata 0.1.4 with the Sync-M pack (`sync-strata/Sync-M` at revision `435b4178227d9fb13b7e63f8645b7213819419a2`); Strata 0.2.20 (terminal build 0.1.66) with the ISTA-DASLab IQ3_S pack of Qwen3.8-Flash-Next (revision not recorded). Both run the same base model, so a difference between them comes from the pack or the engine, which this benchmark cannot separate.
- Sync-Strata returns no logprobs, so `sync_m_think` is decided by the first line of the reply, like the Claude and Gemini judges; it also gets their system message. `qwen3.8_iq3_s` is decided by probability, as the Ollama judges are, and gets no system message. The thinking runs use `reasoning_effort` low with room for 4,096 tokens. Do not compare these judges' no-answer or false-warning rates with the Ollama ones without this in mind.
- The memory column for the Strata judges (not `qwen3.8_q2_0`, below) is the engine process's resident memory (Sync-M 34.8 GiB, IQ3_S 49.8 GiB; about 7.3 to 7.5 GiB of the 8 GiB GPU on top), not the loaded size Ollama reports.
- Three more judges were run and then left out of `JUDGES` in `judgebench/report.py`, so they are not in `results/summary.md`; their result files stay in `results/`. `sync_m` and `inkling_2_mini` were left out because neither is usable on the honorific and style tasks; on secrets they were not that bad (`sync_m` caught 166 of 225 with 0 false warnings, `inkling_2_mini` 225 of 225 with 16, where gitleaks flags 60 of 225 negatives), so a reader who needs those rows can add the names back to `JUDGES`. `qwen3.8_q2_0` was left out for speed and honorific accuracy, as its entry says.
  - `sync_m` (Sync-M, thinking off): on the honorific prompt it caught 1 of 135 positives and flagged 0 of 209 negatives, and on style it caught 42 of 135. A 24-item check (12 positives, 12 negatives; not stored in `results/`) with other answer words gave one word for almost every item: with "NO means an error" 23 of 24 answers were NO, with "A means an error" 23 of 24 were A, and with "B means an error" 18 of 24 were B (12 of 12 positives, 6 of 12 negatives). On the honorific task its direct answer carried little information about the sentence, though thinking on (`sync_m_think`) judges well.
  - `qwen3.8_q2_0` (the Q2_0 pack of the same model): verdict: not usable as a local judge here. A model that needs 20 s or more per item is impractical for this use, so thinking on was dropped from the measurement instead of being run in full. Thinking off is near the 5 s bar but catches 57% of honorific errors with 33% false warnings, and it answered NO to all 135 items of each injection task.
    - Setup: upstream Strata 0.2.21.1 (terminal build 0.1.68, engine 0.1.67 `macos-arm64-metal`; model revision not recorded) on a Mac (Apple M2 Max, 32 GB), decided by probability like `qwen3.8_iq3_s`, measured on 2026-11-26, one call at a time, all seven tasks, no errors. The memory is smaller than the pack, so the engine streams the experts from the SSD. Decode is about 6 to 8 tokens/s and prompt reading about 15 to 22 tokens/s on a honorific prompt; the engine process holds about 2.6 GiB resident and maps 37.6 GB of the pack. These figures come from one probe and the engine's log; they are not stored in `results/`.
    - Latency: median 4.3 s (honorific, style) to 6.5 s (injection secrets) per item. In a single probe the 94-token prompt took most of that time; result rows carry no per-phase timing.
    - Against `qwen3.8_iq3_s` (caught, with false warnings in parentheses): honorific 57% (33%) against 79% (45%); style 88% (11%) against 92% (12%); secrets 100% (4%) against 100% (7%); private setup 93% (30%), no IQ3_S run; aitext 33% caught against 7% for IQ3_S.
    - Thinking on (`reasoning_effort` low) took 33 to 57 s per item (median about 40 s, 200 to 370 output tokens) on a 6-item probe of the honorific task, about 20 hours for all 1,764 items; no `qwen3.8_q2_0_think` result is stored.
    - The vendor's figure for a 32 GB M4 Mac mini is about 14 tokens/s for Q2_0; this Mac measured lower, and the pack and engine are not the only difference, so the two are not comparable. Other packs (IQ3_XXS, Gyro-S) were not run.
  - `inkling_2_mini` (Inkling-2-Mini SQ-20 on Strata 0.2.20, no logprobs) answered YES to 208 of 209 correct honorific sentences, to 57% of correct style passages and to 24 of 25 human sentences.
  - No committed Strata row carries `served_model` except the `qwen3.8_q2_0` rows: the check that a judge is not talking to another engine's model was added after the runs. Both servers answer with the loaded model's id unless the request names a configured alias (read in the Sync-Strata 0.1.4 and Strata 0.2.20 sources; the `qwen3.8_q2_0` rows were run after the check and carry it), so from now on a wrong engine is an error row. The `sync_m` rows also lack `output_tokens`; they were run with the same request (system message, `max_tokens` 8, `reasoning_effort` none). `run judge` keeps stored rows, so delete a judge's result files to regenerate them.

## Follow-up tasks: language identification, personal data, calendar consistency

Three tasks added for a second article, with their own bar (`pass_bar_followup.md`) and report:

| Task | Data | Label 1 (flag) |
|---|---|---|
| `langid` | Tatoeba sentences (`data/tatoeba_pool.tsv`, export of 2026-11-28, CC BY 2.0 FR, https://tatoeba.org; each sentence id is in `meta`), plus derived mixed, romaji and appended-sentence items | the main language is not Japanese |
| `personal_data` | generated dummy values (random digits; mobile numbers `0X0-0000-XXXX`; reserved `example.*` domains); no value is taken from a person | the text holds a valid My Number, a mobile number or a personal email address |
| `calendar` | generated era-year, date-weekday and invoice statements, each with a consistent twin | the text contradicts itself |

The phone-number shapes are generated, not checked against the numbering plan, so a value could coincide with an assigned number.

```sh
python3 -m unittest discover -s tests          # generators, labels and baselines
python3 -m judgebench.run baseline langid personal_data calendar
python3 -m judgebench.run fasttext <lid.176.ftz>   # pip install fasttext-numpy2-wheel; the model is not committed
python3 -m judgebench.run judge gemma4:12b langid personal_data calendar
JUDGEBENCH_ONLY_CLS=control_ja,control_en,control_zh,appended_ja,appended_other python3 -m judgebench.run judge gemma4:12b+think langid
python3 -m judgebench.run judge gemma4:12b+think calendar
ANTHROPIC_API_KEY=... python3 -m judgebench.run judge claude_api_off langid personal_data calendar
ANTHROPIC_API_KEY=... python3 -m judgebench.run judge claude_api_think langid personal_data calendar
GEMINI_API_KEY=... python3 -m judgebench.run judge gemini_decision langid personal_data calendar
python3 -m judgebench.followup_report          # results/followup_summary.json and .md
```

`tools/build_tatoeba_pool.py` rebuilds the Tatoeba pool from the per-language exports (needs `pykakasi` 2.3.0 for the romaji column; romaji is machine-made and sometimes unnatural). Limits: sentences are short and from one corpus; the romaji and mixed items are constructed, not found; the personal_data and calendar baselines restate the labelling rule.
