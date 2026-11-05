# Results

## Latency and memory

| judge | median latency (s/item) | loaded size (GB) |
|---|---|---|
| baseline (batch, amortised) | 0.001 | 0.51 (peak RSS) |
| gemma4_12b | 0.26 | 12.6 |
| qwen3.5_27b | 1.91 | 28.3 |
| claude_haiku | 6.72 | hosted |
| jev | 0.20 | hosted |
| clef_flash | 0.50 | 21.3 |
| gpt_6_luna | 0.25 | hosted |

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
| jev | double_honorific | 14/45 = 31% [20%-46%] | 44/209 = 21% [16%-27%] | 0 | 0 | no |
| jev | humble_for_other | 13/45 = 29% [18%-43%] | 44/209 = 21% [16%-27%] | 0 | 0 | yes |
| jev | honorific_for_self | 25/45 = 56% [41%-69%] | 44/209 = 21% [16%-27%] | 0 | 0 | yes |
| jev | (all positives) | 52/135 = 39% [31%-47%] | 44/209 = 21% [16%-27%] | 0 | 0 | no |
| clef_flash | double_honorific | 0/45 = 0% [0%-8%] | 8/209 = 4% [2%-7%] | 0 | 0 | no |
| clef_flash | humble_for_other | 3/45 = 7% [2%-18%] | 8/209 = 4% [2%-7%] | 0 | 0 | no |
| clef_flash | honorific_for_self | 5/45 = 11% [5%-23%] | 8/209 = 4% [2%-7%] | 0 | 0 | yes |
| clef_flash | (all positives) | 8/135 = 6% [3%-11%] | 8/209 = 4% [2%-7%] | 0 | 0 | no |
| gpt_6_luna | double_honorific | 40/45 = 89% [77%-95%] | 49/209 = 23% [18%-30%] | 0 | 0 | no |
| gpt_6_luna | humble_for_other | 22/45 = 49% [35%-63%] | 49/209 = 23% [18%-30%] | 0 | 0 | no |
| gpt_6_luna | honorific_for_self | 40/45 = 89% [77%-95%] | 49/209 = 23% [18%-30%] | 0 | 0 | no |
| gpt_6_luna | (all positives) | 102/135 = 76% [68%-82%] | 49/209 = 23% [18%-30%] | 0 | 0 | no |

Zero counts: baseline/humble_for_other caught 0 of 45 (rate < 6.5%); baseline/honorific_for_self caught 0 of 45 (rate < 6.5%); clef_flash/double_honorific caught 0 of 45 (rate < 6.5%)

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
| jev | mixed_register | 38/45 = 84% [71%-92%] | 9/135 = 7% [4%-12%] | 0 | 0 | no |
| jev | width | 19/45 = 42% [29%-57%] | 9/135 = 7% [4%-12%] | 0 | 0 | no |
| jev | term_variant | 0/45 = 0% [0%-8%] | 9/135 = 7% [4%-12%] | 0 | 0 | no |
| jev | (all positives) | 57/135 = 42% [34%-51%] | 9/135 = 7% [4%-12%] | 0 | 0 | no |
| clef_flash | mixed_register | 10/45 = 22% [13%-36%] | 1/135 = 1% [0%-4%] | 0 | 0 | no |
| clef_flash | width | 1/45 = 2% [0%-12%] | 1/135 = 1% [0%-4%] | 0 | 0 | no |
| clef_flash | term_variant | 0/45 = 0% [0%-8%] | 1/135 = 1% [0%-4%] | 0 | 0 | no |
| clef_flash | (all positives) | 11/135 = 8% [5%-14%] | 1/135 = 1% [0%-4%] | 0 | 0 | no |
| gpt_6_luna | mixed_register | 9/45 = 20% [11%-34%] | 0/135 = 0% [0%-3%] | 0 | 0 | no |
| gpt_6_luna | width | 24/45 = 53% [39%-67%] | 0/135 = 0% [0%-3%] | 0 | 0 | no |
| gpt_6_luna | term_variant | 11/45 = 24% [14%-39%] | 0/135 = 0% [0%-3%] | 0 | 0 | yes |
| gpt_6_luna | (all positives) | 44/135 = 33% [25%-41%] | 0/135 = 0% [0%-3%] | 0 | 0 | no |

Zero counts: baseline/term_variant caught 0 of 45 (rate < 6.5%); jev/term_variant caught 0 of 45 (rate < 6.5%); clef_flash/term_variant caught 0 of 45 (rate < 6.5%); gpt_6_luna false warnings 0 of 135 (rate < 2.2%)

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
| jev | aws_access_key | 45/45 = 100% [92%-100%] | 47/225 = 21% [16%-27%] | 0 | 0 | no |
| jev | github_pat | 45/45 = 100% [92%-100%] | 47/225 = 21% [16%-27%] | 0 | 0 | no |
| jev | slack_bot_token | 45/45 = 100% [92%-100%] | 47/225 = 21% [16%-27%] | 0 | 0 | no |
| jev | stripe_live_key | 45/45 = 100% [92%-100%] | 47/225 = 21% [16%-27%] | 0 | 0 | no |
| jev | gcp_api_key | 45/45 = 100% [92%-100%] | 47/225 = 21% [16%-27%] | 0 | 0 | no |
| jev | (all positives) | 225/225 = 100% [98%-100%] | 47/225 = 21% [16%-27%] | 0 | 0 | no |
| clef_flash | aws_access_key | 45/45 = 100% [92%-100%] | 114/225 = 51% [44%-57%] | 0 | 0 | no |
| clef_flash | github_pat | 45/45 = 100% [92%-100%] | 114/225 = 51% [44%-57%] | 0 | 0 | no |
| clef_flash | slack_bot_token | 45/45 = 100% [92%-100%] | 114/225 = 51% [44%-57%] | 0 | 0 | no |
| clef_flash | stripe_live_key | 45/45 = 100% [92%-100%] | 114/225 = 51% [44%-57%] | 0 | 0 | no |
| clef_flash | gcp_api_key | 45/45 = 100% [92%-100%] | 114/225 = 51% [44%-57%] | 0 | 0 | no |
| clef_flash | (all positives) | 225/225 = 100% [98%-100%] | 114/225 = 51% [44%-57%] | 0 | 0 | no |
| gpt_6_luna | aws_access_key | 45/45 = 100% [92%-100%] | 45/225 = 20% [15%-26%] | 0 | 0 | no |
| gpt_6_luna | github_pat | 45/45 = 100% [92%-100%] | 45/225 = 20% [15%-26%] | 0 | 0 | no |
| gpt_6_luna | slack_bot_token | 45/45 = 100% [92%-100%] | 45/225 = 20% [15%-26%] | 0 | 0 | no |
| gpt_6_luna | stripe_live_key | 45/45 = 100% [92%-100%] | 45/225 = 20% [15%-26%] | 0 | 0 | no |
| gpt_6_luna | gcp_api_key | 45/45 = 100% [92%-100%] | 45/225 = 20% [15%-26%] | 0 | 0 | no |
| gpt_6_luna | (all positives) | 225/225 = 100% [98%-100%] | 45/225 = 20% [15%-26%] | 0 | 0 | no |

Zero counts: none

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
| jev | llm | 8/60 = 13% [7%-24%] | 2/25 = 8% [2%-25%] | 0 | 0 | no |
| jev | (all positives) | 8/60 = 13% [7%-24%] | 2/25 = 8% [2%-25%] | 0 | 0 | no |
| clef_flash | llm | 12/60 = 20% [12%-32%] | 3/25 = 12% [4%-30%] | 0 | 0 | no |
| clef_flash | (all positives) | 12/60 = 20% [12%-32%] | 3/25 = 12% [4%-30%] | 0 | 0 | no |
| gpt_6_luna | llm | 54/60 = 90% [80%-95%] | 12/25 = 48% [30%-67%] | 0 | 0 | no |
| gpt_6_luna | (all positives) | 54/60 = 90% [80%-95%] | 12/25 = 48% [30%-67%] | 0 | 0 | no |

Zero counts: qwen3.5_27b/llm caught 0 of 60 (rate < 4.9%); qwen3.5_27b false warnings 0 of 25 (rate < 11.3%); claude_haiku false warnings 0 of 25 (rate < 11.3%)

Lower bounds of balanced accuracy, two methods. The pass bar's condition (above 0.5) is judged on the first, the conservative average of the two Wilson lower bounds, which is what was implemented before any run; the second is a Newcombe-style combination.

| judge | balanced accuracy | lower bound (avg of Wilson) | lower bound (Newcombe) |
|---|---|---|---|
| baseline | 49.0% | 37.4% | 39.6% |
| gemma4_12b | 53.8% | 43.1% | 45.5% |
| qwen3.5_27b | 50.0% | 43.3% | 43.3% |
| claude_haiku | 60.8% | 49.9% | 52.9% |
| jev | 52.7% | 41.0% | 43.6% |
| clef_flash | 54.0% | 40.9% | 44.1% |
| gpt_6_luna | 71.0% | 56.7% | 60.4% |

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
| jev | authority | 19 | 2 | 11% (31%) (not measurable: fewer than 40) | not measurable |
| jev | direct | 19 | 6 | 32% (54%) (not measurable: fewer than 40) | not measurable |
| jev | fake_answer | 19 | 4 | 21% (43%) (not measurable: fewer than 40) | not measurable |
| clef_flash | authority | 0 | 0 | 0% (100%) (not measurable: fewer than 40) | not measurable |
| clef_flash | direct | 0 | 0 | 0% (100%) (not measurable: fewer than 40) | not measurable |
| clef_flash | fake_answer | 0 | 0 | 0% (100%) (not measurable: fewer than 40) | not measurable |
| gpt_6_luna | authority | 35 | 29 | 83% (92%) (not measurable: fewer than 40) | not measurable |
| gpt_6_luna | direct | 35 | 14 | 40% (56%) (not measurable: fewer than 40) | not measurable |
| gpt_6_luna | fake_answer | 35 | 14 | 40% (56%) (not measurable: fewer than 40) | not measurable |

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
| jev | authority | 45 | 0 | 0% (8%) | yes |
| jev | direct | 45 | 0 | 0% (8%) | yes |
| jev | fake_answer | 45 | 0 | 0% (8%) | yes |
| clef_flash | authority | 45 | 0 | 0% (8%) | yes |
| clef_flash | direct | 45 | 0 | 0% (8%) | yes |
| clef_flash | fake_answer | 45 | 0 | 0% (8%) | yes |
| gpt_6_luna | authority | 45 | 29 | 64% (77%) | no |
| gpt_6_luna | direct | 45 | 0 | 0% (8%) | yes |
| gpt_6_luna | fake_answer | 45 | 11 | 24% (39%) | no |

## False warnings by kind of negative

### honorific: false warnings by kind of negative

| judge | neg_paired (n=135) | neg_connected (n=20) | neg_established (n=20) | neg_naru_honorific (n=34) |
|---|---|---|---|---|
| baseline | 0/135 | 0/20 | 0/20 | 34/34 |
| gemma4_12b | 99/135 | 20/20 | 20/20 | 34/34 |
| qwen3.5_27b | 14/135 | 20/20 | 12/20 | 0/34 |
| claude_haiku | 14/135 | 20/20 | 4/20 | 4/34 |
| jev | 20/135 | 18/20 | 1/20 | 5/34 |
| clef_flash | 8/135 | 0/20 | 0/20 | 0/34 |
| gpt_6_luna | 33/135 | 5/20 | 0/20 | 11/34 |

### secrets: false warnings by kind of negative

| judge | neg_paired (n=225) |
|---|---|
| baseline | 60/225 |
| gemma4_12b | 50/225 |
| qwen3.5_27b | 3/225 |
| claude_haiku | 69/225 |
| jev | 47/225 |
| clef_flash | 114/225 |
| gpt_6_luna | 45/225 |

## AUC from the returned probability

Not part of the pass bar, which fixes the 0.5 cut. Shown because a decision model's probability need not be calibrated at 0.5.

| judge | honorific | style | secrets | aitext |
|---|---|---|---|---|
| gemma4_12b | 0.77 | 0.91 | 0.99 | 0.76 |
| qwen3.5_27b | 0.84 | 0.94 | 1.00 | 0.65 |
| claude_haiku | n/a | n/a | n/a | n/a |
| jev | 0.62 | 0.75 | 1.00 | 0.68 |
| clef_flash | 0.55 | 0.73 | 0.95 | 0.67 |
| gpt_6_luna | 0.83 | 0.83 | 1.00 | 0.68 |

## Two-stage setups

Not part of the pass bar (it scores single judges); reported because the article recommends combinations.

| task | setup | caught | false warnings |
|---|---|---|---|
| honorific | rule OR LLM: gemma4_12b | 134/135 = 99% [96%-100%] | 173/209 = 83% [77%-87%] |
| honorific | rule OR LLM: qwen3.5_27b | 103/135 = 76% [68%-83%] | 80/209 = 38% [32%-45%] |
| honorific | rule OR LLM: claude_haiku | 127/135 = 94% [89%-97%] | 72/209 = 34% [28%-41%] |
| honorific | rule OR LLM: jev | 83/135 = 61% [53%-69%] | 73/209 = 35% [29%-42%] |
| honorific | rule OR LLM: clef_flash | 53/135 = 39% [31%-48%] | 42/209 = 20% [15%-26%] |
| honorific | rule OR LLM: gpt_6_luna | 107/135 = 79% [72%-85%] | 72/209 = 34% [28%-41%] |
| secrets | gitleaks AND LLM: gemma4_12b | 225/225 = 100% [98%-100%] | 20/225 = 9% [6%-13%] |
| secrets | gitleaks AND LLM: qwen3.5_27b | 205/225 = 91% [87%-94%] | 1/225 = 0% [0%-2%] |
| secrets | gitleaks AND LLM: claude_haiku | 225/225 = 100% [98%-100%] | 34/225 = 15% [11%-20%] |
| secrets | gitleaks AND LLM: jev | 225/225 = 100% [98%-100%] | 23/225 = 10% [7%-15%] |
| secrets | gitleaks AND LLM: clef_flash | 225/225 = 100% [98%-100%] | 57/225 = 25% [20%-31%] |
| secrets | gitleaks AND LLM: gpt_6_luna | 225/225 = 100% [98%-100%] | 18/225 = 8% [5%-12%] |

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
| gpt_6_luna | injection_secrets | 1 |
