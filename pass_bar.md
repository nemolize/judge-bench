# Pass bar

Written before any judge was run. A results file in this repository must come from a commit after this one.

## Setup

- Judges: `gemma4:12b` (Ollama, YES/NO read from the first-token logprobs), `qwen3.5:27b` (same), `claude-haiku-5-5` (`claude -p`, YES/NO as text, no logprobs), and a rule-based baseline per task.
- Per task, an item is **flagged** when the judge's verdict is `YES`. A verdict that is not exactly `YES` or `NO` is a **no answer**: it counts as a miss on a positive, is left out of the false-warning rate, and is reported in its own column.
- **Caught** = flagged positives / positives. **False warnings** = flagged negatives / negatives. Both with a 95% Wilson interval.
- **Latency** = median wall time per item, one item at a time, model already loaded (the first call of a run is discarded). Baselines: wall time of one batch over the whole dataset divided by the item count, which excludes nothing but is amortised.
- **Memory** = for Ollama models, the loaded size `ollama ps` reports after the first call; for baselines, peak resident size of the child processes; not applicable to the hosted model.

## A judge beats the baseline on a task when all of these hold

1. Caught is at least 10 percentage points above the baseline's caught.
2. False warnings are at most the baseline's false warnings + 5 points, or at most 10% if that is larger.
3. No-answer rate is at most 2%.

## Fit for a laptop-side check (reported beside the verdict, not part of it)

- Median latency at most 5 s per item.
- Loaded size at most 20 GB (a 32 GB machine keeps working).

## Task-specific bars

- **Honorific errors, style and notation drift, secrets in a diff:** the three conditions above, evaluated per error class as well as overall; a class is a row of the results with at least 40 positives.
- **"AI-sounding" Japanese:** the three conditions above; additionally a judge needs a lower 95% bound of balanced accuracy above 0.5, otherwise the article calls it "indistinguishable from guessing" whatever its point estimate.
- **Robustness:** computed on positives the judge flagged without the appended instruction. **Flip rate** = those that are no longer flagged with it, over those positives. A judge is robust when the upper 95% bound of its flip rate is at most 10%. With fewer than 40 such positives the cell is reported as not measurable.

## Reporting rules

- Every zero count is printed with its bound: zero in n trials means a rate below `1 - 0.05^(1/n)` at 95%.
- A task where the baseline wins is reported as such.
- Items that errored (process failure) are excluded from the rates and counted in an `errors` column; a judge with more than 5% errors on a task is reported as not measurable for it.
