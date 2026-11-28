# Pass bar for the follow-up tasks (langid, personal_data, calendar)

Fixed for the three tasks added after the first six. `pass_bar.md` still governs the older tasks; its three beating conditions, its reporting rules and its flagged / no-answer / error definitions apply here unchanged.

When it was written: the judge set below was agreed on the tracking issue before any judge call, and the rule-based baselines had already been run when this file was committed (they are deterministic and cannot be tuned on judge results). The first judge calls started a few minutes before this commit; no judge result was read before it. The commit that adds a results file comes after this one.

## Judges (fixed; none added after a result was seen)

| Group | Judge | Reached through | Verdict |
|---|---|---|---|
| Cloud | `claude_api_off`, `claude_api_think` (`claude-haiku-5-5`) | Messages API, thinking disabled / default | first line of the reply: `YES` or `NO` |
| Local | `gemma4_12b` | Ollama, thinking off | `YES` when the first-token probability of `YES` is at least that of `NO` |
| Local | `gemma4_12b_think` | Ollama, thinking on | first word of the answer |
| Judge-only | `gemini_decision` (`gemini-decision-1`) | Gemini Decisions API | `YES` when the probability is at least 0.5 |

`gemma4_12b_think` runs only the calendar task and the langid classes needed for the appended-sentence comparison (`control_ja`, `control_en`, `control_zh`, `appended_ja`, `appended_other`), because one answer takes seconds to minutes. Every other judge runs every task. Each result row carries `served_model` and `measured_at` where the API reports a model name.

Other judges (Jev, `gemini-3.8-flash`, `gpt-6-luna`, the Qwen3.8 packs) are not run here; the article quotes the language-drift article's numbers for short and kanji-only text only.

## Baselines (committed before any result of these tasks)

| Task | Baseline | Flagged when |
|---|---|---|
| langid | `baseline`: kana presence (`judgebench/baselines.py`); `fasttext`: `lid.176.ftz` | no kana; the top label is not `ja` |
| personal_data | regular expressions plus the My Number check digit | a 12-digit run with a valid check digit, a 0X0-XXXX-XXXX mobile number, or `<given>.<family>@example.*` |
| calendar | `calendar_task.consistent` (era table, `datetime`, integer arithmetic) | the text contradicts itself |

The personal_data and calendar baselines restate the rule that built the labels, so they are exact by construction. The article reports them as the cost-free ceiling, not as a competitor that earned its score.

## Questions asked of the judges (`prompts/*.txt`, `prompts/decisions.json`)

- `langid`: is the text mainly written in a language other than Japanese (language, not script; romaji Japanese is Japanese)? `YES` = flag.
- `personal_data`: does the text hold personal data (a My Number whose check digit is valid, a mobile number, a personal email address)?
- `calendar`: does the text contradict itself in era-to-year, date-to-weekday or invoice arithmetic (10% tax, rounded down)?

## What is compared

- Per task and per class: detection (flagged positives / positives; a no-answer is a miss) and false alarm (flagged negatives / negatives with a verdict), each with its count and n; a zero carries `1 - 0.05^(1/n)`.
- Thinking effect: `claude_api_think` against `claude_api_off`, and `gemma4_12b_think` against `gemma4_12b`, on the calendar task and on the appended-sentence classes, as differences in the same items.
- Appended sentence: the share of control items whose verdict changes when the opposite-language sentence is appended.
- A task where the baseline is as good as every judge is reported as "no LLM needed".
- Errors and no-answers follow `pass_bar.md`; a judge with more than 5% errors on a task is not measurable for it.
