# Results

## Latency and memory

| judge | median latency (s/item) | loaded size (GB) |
|---|---|---|
| baseline (batch, amortised) | 0.001 | 0.51 (peak RSS) |
| gemma4_12b | 0.26 | 12.6 |
| qwen3.5_27b | 1.91 | 28.3 |
| claude_haiku | 6.72 | hosted |

### honorific

| judge | class | caught | false warnings (all negatives) | no answer | errors | beats baseline |
|---|---|---|---|---|---|---|
| baseline | double_honorific | 45/45 = 100% [92%-100%] | 34/209 = 16% [12%-22%] | 0 | 0 |  |
| baseline | humble_for_other | 0/45 = 0% [0%-8%] | 34/209 = 16% [12%-22%] | 0 | 0 |  |
| baseline | honorific_for_self | 0/45 = 0% [0%-8%] | 34/209 = 16% [12%-22%] | 0 | 0 |  |
| baseline | (all positives) | 45/135 = 33% [26%-42%] | 34/209 = 16% [12%-22%] | 0 | 0 |  |
| gemma4_12b | double_honorific | 45/45 = 100% [92%-100%] | 173/209 = 83% [77%-87%] | 0 | 0 | no |
| gemma4_12b | humble_for_other | 44/45 = 98% [88%-100%] | 173/209 = 83% [77%-87%] | 0 | 0 | no |
| gemma4_12b | honorific_for_self | 45/45 = 100% [92%-100%] | 173/209 = 83% [77%-87%] | 0 | 0 | no |
| gemma4_12b | (all positives) | 134/135 = 99% [96%-100%] | 173/209 = 83% [77%-87%] | 0 | 0 | no |
| qwen3.5_27b | double_honorific | 45/45 = 100% [92%-100%] | 46/209 = 22% [17%-28%] | 0 | 0 | no |
| qwen3.5_27b | humble_for_other | 23/45 = 51% [37%-65%] | 46/209 = 22% [17%-28%] | 0 | 0 | no |
| qwen3.5_27b | honorific_for_self | 35/45 = 78% [64%-87%] | 46/209 = 22% [17%-28%] | 0 | 0 | no |
| qwen3.5_27b | (all positives) | 103/135 = 76% [68%-83%] | 46/209 = 22% [17%-28%] | 0 | 0 | no |
| claude_haiku | double_honorific | 44/45 = 98% [88%-100%] | 42/209 = 20% [15%-26%] | 0 | 0 | no |
| claude_haiku | humble_for_other | 37/45 = 82% [69%-91%] | 42/209 = 20% [15%-26%] | 0 | 0 | yes |
| claude_haiku | honorific_for_self | 45/45 = 100% [92%-100%] | 42/209 = 20% [15%-26%] | 0 | 0 | yes |
| claude_haiku | (all positives) | 126/135 = 93% [88%-96%] | 42/209 = 20% [15%-26%] | 0 | 0 | yes |

Zero counts: baseline/humble_for_other caught 0 of 45 (rate < 6.5%); baseline/honorific_for_self caught 0 of 45 (rate < 6.5%)

### style

| judge | class | caught | false warnings (all negatives) | no answer | errors | beats baseline |
|---|---|---|---|---|---|---|
| baseline | mixed_register | 39/45 = 87% [74%-94%] | 1/135 = 1% [0%-4%] | 0 | 0 |  |
| baseline | width | 43/45 = 96% [85%-99%] | 1/135 = 1% [0%-4%] | 0 | 0 |  |
| baseline | term_variant | 0/45 = 0% [0%-8%] | 1/135 = 1% [0%-4%] | 0 | 0 |  |
| baseline | (all positives) | 82/135 = 61% [52%-69%] | 1/135 = 1% [0%-4%] | 0 | 0 |  |
| gemma4_12b | mixed_register | 45/45 = 100% [92%-100%] | 36/135 = 27% [20%-35%] | 0 | 0 | no |
| gemma4_12b | width | 27/45 = 60% [45%-73%] | 36/135 = 27% [20%-35%] | 0 | 0 | no |
| gemma4_12b | term_variant | 45/45 = 100% [92%-100%] | 36/135 = 27% [20%-35%] | 0 | 0 | no |
| gemma4_12b | (all positives) | 117/135 = 87% [80%-91%] | 36/135 = 27% [20%-35%] | 0 | 0 | no |
| qwen3.5_27b | mixed_register | 40/45 = 89% [77%-95%] | 3/135 = 2% [1%-6%] | 0 | 0 | no |
| qwen3.5_27b | width | 9/45 = 20% [11%-34%] | 3/135 = 2% [1%-6%] | 0 | 0 | no |
| qwen3.5_27b | term_variant | 11/45 = 24% [14%-39%] | 3/135 = 2% [1%-6%] | 0 | 0 | yes |
| qwen3.5_27b | (all positives) | 60/135 = 44% [36%-53%] | 3/135 = 2% [1%-6%] | 0 | 0 | no |
| claude_haiku | mixed_register | 44/45 = 98% [88%-100%] | 11/135 = 8% [5%-14%] | 0 | 0 | yes |
| claude_haiku | width | 40/45 = 89% [77%-95%] | 11/135 = 8% [5%-14%] | 0 | 0 | no |
| claude_haiku | term_variant | 45/45 = 100% [92%-100%] | 11/135 = 8% [5%-14%] | 0 | 0 | yes |
| claude_haiku | (all positives) | 129/135 = 96% [91%-98%] | 11/135 = 8% [5%-14%] | 0 | 0 | yes |

Zero counts: baseline/term_variant caught 0 of 45 (rate < 6.5%)

### secrets

| judge | class | caught | false warnings (all negatives) | no answer | errors | beats baseline |
|---|---|---|---|---|---|---|
| baseline | aws_access_key | 45/45 = 100% [92%-100%] | 60/225 = 27% [21%-33%] | 0 | 0 |  |
| baseline | github_pat | 45/45 = 100% [92%-100%] | 60/225 = 27% [21%-33%] | 0 | 0 |  |
| baseline | slack_bot_token | 45/45 = 100% [92%-100%] | 60/225 = 27% [21%-33%] | 0 | 0 |  |
| baseline | stripe_live_key | 45/45 = 100% [92%-100%] | 60/225 = 27% [21%-33%] | 0 | 0 |  |
| baseline | gcp_api_key | 45/45 = 100% [92%-100%] | 60/225 = 27% [21%-33%] | 0 | 0 |  |
| baseline | (all positives) | 225/225 = 100% [98%-100%] | 60/225 = 27% [21%-33%] | 0 | 0 |  |
| gemma4_12b | aws_access_key | 45/45 = 100% [92%-100%] | 50/225 = 22% [17%-28%] | 0 | 0 | no |
| gemma4_12b | github_pat | 45/45 = 100% [92%-100%] | 50/225 = 22% [17%-28%] | 0 | 0 | no |
| gemma4_12b | slack_bot_token | 45/45 = 100% [92%-100%] | 50/225 = 22% [17%-28%] | 0 | 0 | no |
| gemma4_12b | stripe_live_key | 45/45 = 100% [92%-100%] | 50/225 = 22% [17%-28%] | 0 | 0 | no |
| gemma4_12b | gcp_api_key | 45/45 = 100% [92%-100%] | 50/225 = 22% [17%-28%] | 0 | 0 | no |
| gemma4_12b | (all positives) | 225/225 = 100% [98%-100%] | 50/225 = 22% [17%-28%] | 0 | 0 | no |
| qwen3.5_27b | aws_access_key | 37/45 = 82% [69%-91%] | 3/225 = 1% [0%-4%] | 0 | 0 | no |
| qwen3.5_27b | github_pat | 45/45 = 100% [92%-100%] | 3/225 = 1% [0%-4%] | 0 | 0 | no |
| qwen3.5_27b | slack_bot_token | 45/45 = 100% [92%-100%] | 3/225 = 1% [0%-4%] | 0 | 0 | no |
| qwen3.5_27b | stripe_live_key | 45/45 = 100% [92%-100%] | 3/225 = 1% [0%-4%] | 0 | 0 | no |
| qwen3.5_27b | gcp_api_key | 33/45 = 73% [59%-84%] | 3/225 = 1% [0%-4%] | 0 | 0 | no |
| qwen3.5_27b | (all positives) | 205/225 = 91% [87%-94%] | 3/225 = 1% [0%-4%] | 0 | 0 | no |
| claude_haiku | aws_access_key | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| claude_haiku | github_pat | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| claude_haiku | slack_bot_token | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| claude_haiku | stripe_live_key | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| claude_haiku | gcp_api_key | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| claude_haiku | (all positives) | 225/225 = 100% [98%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |

Zero counts: 

### aitext

| judge | class | caught | false warnings (all negatives) | no answer | errors | beats baseline |
|---|---|---|---|---|---|---|
| baseline | llm | 6/60 = 10% [5%-20%] | 3/25 = 12% [4%-30%] | 0 | 0 |  |
| baseline | (all positives) | 6/60 = 10% [5%-20%] | 3/25 = 12% [4%-30%] | 0 | 0 |  |
| gemma4_12b | llm | 7/60 = 12% [6%-22%] | 1/25 = 4% [1%-20%] | 0 | 0 | no |
| gemma4_12b | (all positives) | 7/60 = 12% [6%-22%] | 1/25 = 4% [1%-20%] | 0 | 0 | no |
| qwen3.5_27b | llm | 0/60 = 0% [0%-6%] | 0/25 = 0% [0%-13%] | 0 | 0 | no |
| qwen3.5_27b | (all positives) | 0/60 = 0% [0%-6%] | 0/25 = 0% [0%-13%] | 0 | 0 | no |
| claude_haiku | llm | 13/60 = 22% [13%-34%] | 0/25 = 0% [0%-13%] | 0 | 0 | no |
| claude_haiku | (all positives) | 13/60 = 22% [13%-34%] | 0/25 = 0% [0%-13%] | 0 | 0 | no |

Zero counts: qwen3.5_27b/llm caught 0 of 60 (rate < 4.9%)

Lower bounds of balanced accuracy, two methods. The pass bar's condition (above 0.5) is judged on the first, the conservative average of the two Wilson lower bounds, which is what was implemented before any run; the second is a Newcombe-style combination.

| judge | balanced accuracy | lower bound (avg of Wilson) | lower bound (Newcombe) |
|---|---|---|---|
| baseline | 49.0% | 37.4% | 39.6% |
| gemma4_12b | 53.8% | 43.1% | 45.5% |
| qwen3.5_27b | 50.0% | 43.3% | 43.3% |
| claude_haiku | 60.8% | 49.9% | 52.9% |

## Robustness

### injection_honorific

| judge | attack | flagged before | flipped | flip rate (upper 95% bound) | robust (bound <= 10%) |
|---|---|---|---|---|---|
| baseline | authority | 15 | 0 | 0% (20%) (not measurable: fewer than 40) | not measurable |
| baseline | direct | 15 | 0 | 0% (20%) (not measurable: fewer than 40) | not measurable |
| baseline | fake_answer | 15 | 0 | 0% (20%) (not measurable: fewer than 40) | not measurable |
| gemma4_12b | authority | 45 | 10 | 22% (36%) | no |
| gemma4_12b | direct | 45 | 8 | 18% (31%) | no |
| gemma4_12b | fake_answer | 45 | 45 | 100% (100%) | no |
| qwen3.5_27b | authority | 34 | 33 | 97% (99%) (not measurable: fewer than 40) | not measurable |
| qwen3.5_27b | direct | 34 | 34 | 100% (100%) (not measurable: fewer than 40) | not measurable |
| qwen3.5_27b | fake_answer | 34 | 34 | 100% (100%) (not measurable: fewer than 40) | not measurable |
| claude_haiku | authority | 42 | 3 | 7% (19%) | no |
| claude_haiku | direct | 42 | 1 | 2% (12%) | no |
| claude_haiku | fake_answer | 42 | 9 | 21% (36%) | no |

### injection_secrets

| judge | attack | flagged before | flipped | flip rate (upper 95% bound) | robust (bound <= 10%) |
|---|---|---|---|---|---|
| baseline | authority | 45 | 0 | 0% (8%) | yes |
| baseline | direct | 45 | 0 | 0% (8%) | yes |
| baseline | fake_answer | 45 | 0 | 0% (8%) | yes |
| gemma4_12b | authority | 45 | 2 | 4% (15%) | no |
| gemma4_12b | direct | 45 | 0 | 0% (8%) | yes |
| gemma4_12b | fake_answer | 45 | 45 | 100% (100%) | no |
| qwen3.5_27b | authority | 40 | 40 | 100% (100%) | no |
| qwen3.5_27b | direct | 40 | 40 | 100% (100%) | no |
| qwen3.5_27b | fake_answer | 40 | 40 | 100% (100%) | no |
| claude_haiku | authority | 45 | 0 | 0% (8%) | yes |
| claude_haiku | direct | 45 | 0 | 0% (8%) | yes |
| claude_haiku | fake_answer | 45 | 3 | 7% (18%) | no |

## False warnings by kind of negative

### honorific: false warnings by kind of negative

| judge | neg_paired (n=135) | neg_connected (n=20) | neg_established (n=20) | neg_naru_honorific (n=34) |
|---|---|---|---|---|
| baseline | 0/135 | 0/20 | 0/20 | 34/34 |
| gemma4_12b | 99/135 | 20/20 | 20/20 | 34/34 |
| qwen3.5_27b | 14/135 | 20/20 | 12/20 | 0/34 |
| claude_haiku | 14/135 | 20/20 | 4/20 | 4/34 |

### secrets: false warnings by kind of negative

| judge | neg_paired (n=225) |
|---|---|
| baseline | 60/225 |
| gemma4_12b | 50/225 |
| qwen3.5_27b | 3/225 |
| claude_haiku | 69/225 |

## Two-stage setups

Not part of the pass bar (it scores single judges); reported because the article recommends combinations.

| task | setup | caught | false warnings |
|---|---|---|---|
| honorific | rule OR LLM: gemma4_12b | 134/135 = 99% [96%-100%] | 173/209 = 83% [77%-87%] |
| honorific | rule OR LLM: qwen3.5_27b | 103/135 = 76% [68%-83%] | 80/209 = 38% [32%-45%] |
| honorific | rule OR LLM: claude_haiku | 127/135 = 94% [89%-97%] | 72/209 = 34% [28%-41%] |
| secrets | gitleaks AND LLM: gemma4_12b | 225/225 = 100% [98%-100%] | 20/225 = 9% [6%-13%] |
| secrets | gitleaks AND LLM: qwen3.5_27b | 205/225 = 91% [87%-94%] | 1/225 = 0% [0%-2%] |
| secrets | gitleaks AND LLM: claude_haiku | 225/225 = 100% [98%-100%] | 34/225 = 15% [11%-20%] |

## What gitleaks flags among the secrets negatives

| look-alike | flagged |
|---|---|
| hex40 | 29 |
| uuid | 31 |
| other | 0 |

## No-answer verdicts

| judge | task | no answer |
|---|---|---|
| gemma4_12b | injection_honorific | 4 |
