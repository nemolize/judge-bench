# Results

## Latency and memory

| judge | median latency (s/item) | loaded size (GB) |
|---|---|---|
| baseline (batch, amortised) | 0.001 | 0.51 (peak RSS) |
| gemma4_12b | 0.26 | 21.0 |
| qwen3.5_27b | 2.04 | 28.4 |
| claude_haiku | 8.17 | hosted |

### honorific

| judge | class | caught | false warnings (all negatives) | no answer | errors | beats baseline |
|---|---|---|---|---|---|---|
| baseline | double_honorific | 45/45 = 100% [92%-100%] | 0/175 = 0% [0%-2%] | 0 | 0 |  |
| baseline | humble_for_other | 0/45 = 0% [0%-8%] | 0/175 = 0% [0%-2%] | 0 | 0 |  |
| baseline | honorific_for_self | 0/45 = 0% [0%-8%] | 0/175 = 0% [0%-2%] | 0 | 0 |  |
| gemma4_12b | double_honorific | 45/45 = 100% [92%-100%] | 139/175 = 79% [73%-85%] | 0 | 0 | no |
| gemma4_12b | humble_for_other | 44/45 = 98% [88%-100%] | 139/175 = 79% [73%-85%] | 0 | 0 | no |
| gemma4_12b | honorific_for_self | 45/45 = 100% [92%-100%] | 139/175 = 79% [73%-85%] | 0 | 0 | no |
| qwen3.5_27b | double_honorific | 45/45 = 100% [92%-100%] | 46/175 = 26% [20%-33%] | 0 | 0 | no |
| qwen3.5_27b | humble_for_other | 23/45 = 51% [37%-65%] | 46/175 = 26% [20%-33%] | 0 | 0 | no |
| qwen3.5_27b | honorific_for_self | 35/45 = 78% [64%-87%] | 46/175 = 26% [20%-33%] | 0 | 0 | no |
| claude_haiku | double_honorific | 44/45 = 98% [88%-100%] | 38/175 = 22% [16%-28%] | 0 | 0 | no |
| claude_haiku | humble_for_other | 37/45 = 82% [69%-91%] | 38/175 = 22% [16%-28%] | 0 | 0 | no |
| claude_haiku | honorific_for_self | 45/45 = 100% [92%-100%] | 38/175 = 22% [16%-28%] | 0 | 0 | no |

Zero counts: baseline/humble_for_other caught 0 of 45 (rate < 6%); baseline/honorific_for_self caught 0 of 45 (rate < 6%)

### style

| judge | class | caught | false warnings (all negatives) | no answer | errors | beats baseline |
|---|---|---|---|---|---|---|
| baseline | mixed_register | 39/45 = 87% [74%-94%] | 1/135 = 1% [0%-4%] | 0 | 0 |  |
| baseline | width | 43/45 = 96% [85%-99%] | 1/135 = 1% [0%-4%] | 0 | 0 |  |
| baseline | term_variant | 0/45 = 0% [0%-8%] | 1/135 = 1% [0%-4%] | 0 | 0 |  |
| gemma4_12b | mixed_register | 45/45 = 100% [92%-100%] | 36/135 = 27% [20%-35%] | 0 | 0 | no |
| gemma4_12b | width | 27/45 = 60% [45%-73%] | 36/135 = 27% [20%-35%] | 0 | 0 | no |
| gemma4_12b | term_variant | 45/45 = 100% [92%-100%] | 36/135 = 27% [20%-35%] | 0 | 0 | no |
| qwen3.5_27b | mixed_register | 40/45 = 89% [77%-95%] | 3/135 = 2% [1%-6%] | 0 | 0 | no |
| qwen3.5_27b | width | 9/45 = 20% [11%-34%] | 3/135 = 2% [1%-6%] | 0 | 0 | no |
| qwen3.5_27b | term_variant | 11/45 = 24% [14%-39%] | 3/135 = 2% [1%-6%] | 0 | 0 | yes |
| claude_haiku | mixed_register | 44/45 = 98% [88%-100%] | 11/135 = 8% [5%-14%] | 0 | 0 | yes |
| claude_haiku | width | 40/45 = 89% [77%-95%] | 11/135 = 8% [5%-14%] | 0 | 0 | no |
| claude_haiku | term_variant | 45/45 = 100% [92%-100%] | 11/135 = 8% [5%-14%] | 0 | 0 | yes |

Zero counts: baseline/term_variant caught 0 of 45 (rate < 6%)

### secrets

| judge | class | caught | false warnings (all negatives) | no answer | errors | beats baseline |
|---|---|---|---|---|---|---|
| baseline | aws_access_key | 45/45 = 100% [92%-100%] | 60/225 = 27% [21%-33%] | 0 | 0 |  |
| baseline | github_pat | 45/45 = 100% [92%-100%] | 60/225 = 27% [21%-33%] | 0 | 0 |  |
| baseline | slack_bot_token | 45/45 = 100% [92%-100%] | 60/225 = 27% [21%-33%] | 0 | 0 |  |
| baseline | stripe_live_key | 45/45 = 100% [92%-100%] | 60/225 = 27% [21%-33%] | 0 | 0 |  |
| baseline | gcp_api_key | 45/45 = 100% [92%-100%] | 60/225 = 27% [21%-33%] | 0 | 0 |  |
| gemma4_12b | aws_access_key | 45/45 = 100% [92%-100%] | 50/225 = 22% [17%-28%] | 0 | 0 | no |
| gemma4_12b | github_pat | 45/45 = 100% [92%-100%] | 50/225 = 22% [17%-28%] | 0 | 0 | no |
| gemma4_12b | slack_bot_token | 45/45 = 100% [92%-100%] | 50/225 = 22% [17%-28%] | 0 | 0 | no |
| gemma4_12b | stripe_live_key | 45/45 = 100% [92%-100%] | 50/225 = 22% [17%-28%] | 0 | 0 | no |
| gemma4_12b | gcp_api_key | 45/45 = 100% [92%-100%] | 50/225 = 22% [17%-28%] | 0 | 0 | no |
| qwen3.5_27b | aws_access_key | 37/45 = 82% [69%-91%] | 3/225 = 1% [0%-4%] | 0 | 0 | no |
| qwen3.5_27b | github_pat | 45/45 = 100% [92%-100%] | 3/225 = 1% [0%-4%] | 0 | 0 | no |
| qwen3.5_27b | slack_bot_token | 45/45 = 100% [92%-100%] | 3/225 = 1% [0%-4%] | 0 | 0 | no |
| qwen3.5_27b | stripe_live_key | 45/45 = 100% [92%-100%] | 3/225 = 1% [0%-4%] | 0 | 0 | no |
| qwen3.5_27b | gcp_api_key | 33/45 = 73% [59%-84%] | 3/225 = 1% [0%-4%] | 0 | 0 | no |
| claude_haiku | aws_access_key | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| claude_haiku | github_pat | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| claude_haiku | slack_bot_token | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| claude_haiku | stripe_live_key | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| claude_haiku | gcp_api_key | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |

Zero counts: 

### aitext

| judge | class | caught | false warnings (all negatives) | no answer | errors | beats baseline |
|---|---|---|---|---|---|---|
| baseline | llm | 6/60 = 10% [5%-20%] | 3/25 = 12% [4%-30%] | 0 | 0 |  |
| gemma4_12b | llm | 7/60 = 12% [6%-22%] | 1/25 = 4% [1%-20%] | 0 | 0 | no |
| qwen3.5_27b | llm | 0/60 = 0% [0%-6%] | 0/25 = 0% [0%-13%] | 0 | 0 | no |
| claude_haiku | llm | 13/60 = 22% [13%-34%] | 0/25 = 0% [0%-13%] | 0 | 0 | yes |

Zero counts: qwen3.5_27b/llm caught 0 of 60 (rate < 5%)

| judge | balanced accuracy | lower 95% bound |
|---|---|---|
| baseline | 49% | 37% |
| gemma4_12b | 54% | 43% |
| qwen3.5_27b | 50% | 43% |
| claude_haiku | 61% | 50% |

## Robustness

### injection_honorific

| judge | attack | flagged before | flipped | flip rate (upper 95% bound) |
|---|---|---|---|---|
| baseline | authority | 15 | 0 | 0% (20%) (not measurable: fewer than 40) |
| baseline | direct | 15 | 0 | 0% (20%) (not measurable: fewer than 40) |
| baseline | fake_answer | 15 | 0 | 0% (20%) (not measurable: fewer than 40) |
| gemma4_12b | authority | 45 | 10 | 22% (36%) |
| gemma4_12b | direct | 45 | 8 | 18% (31%) |
| gemma4_12b | fake_answer | 45 | 45 | 100% (100%) |
| qwen3.5_27b | authority | 34 | 33 | 97% (99%) (not measurable: fewer than 40) |
| qwen3.5_27b | direct | 34 | 34 | 100% (100%) (not measurable: fewer than 40) |
| qwen3.5_27b | fake_answer | 34 | 34 | 100% (100%) (not measurable: fewer than 40) |
| claude_haiku | authority | 42 | 3 | 7% (19%) |
| claude_haiku | direct | 42 | 1 | 2% (12%) |
| claude_haiku | fake_answer | 42 | 9 | 21% (36%) |

### injection_secrets

| judge | attack | flagged before | flipped | flip rate (upper 95% bound) |
|---|---|---|---|---|
| baseline | authority | 45 | 0 | 0% (8%) |
| baseline | direct | 45 | 0 | 0% (8%) |
| baseline | fake_answer | 45 | 0 | 0% (8%) |
| gemma4_12b | authority | 45 | 2 | 4% (15%) |
| gemma4_12b | direct | 45 | 0 | 0% (8%) |
| gemma4_12b | fake_answer | 45 | 45 | 100% (100%) |
| qwen3.5_27b | authority | 40 | 40 | 100% (100%) |
| qwen3.5_27b | direct | 40 | 40 | 100% (100%) |
| qwen3.5_27b | fake_answer | 40 | 40 | 100% (100%) |
| claude_haiku | authority | 45 | 0 | 0% (8%) |
| claude_haiku | direct | 45 | 0 | 0% (8%) |
| claude_haiku | fake_answer | 45 | 3 | 7% (18%) |
