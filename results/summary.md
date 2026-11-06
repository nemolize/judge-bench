# Results

## Latency and memory

| judge | median latency (s/item) | loaded size (GB) |
|---|---|---|
| baseline (batch, amortised) | 0.001 | 0.51 (peak RSS) |
| gemma4_12b | 0.27 | 24.9 |
| qwen3.5_27b | 0.89 | 28.3 |
| claude_haiku | 8.43 | hosted |
| jev | 0.17 | hosted |
| clef_flash | 0.77 | 21.3 |
| gpt_6_luna | 0.30 | hosted |

### honorific

| judge | class | caught | false warnings (all negatives) | no answer | errors | beats baseline |
|---|---|---|---|---|---|---|
| baseline | double_honorific | 45/45 = 100% [92%-100%] | 34/209 = 16% [12%-22%] | 0 | 0 |  |
| baseline | humble_for_other | 0/45 = 0% [0%-8%] | 34/209 = 16% [12%-22%] | 0 | 0 |  |
| baseline | honorific_for_self | 0/45 = 0% [0%-8%] | 34/209 = 16% [12%-22%] | 0 | 0 |  |
| baseline | (all positives) | 45/135 = 33% [26%-42%] | 34/209 = 16% [12%-22%] | 0 | 0 |  |
| gemma4_12b | double_honorific | 45/45 = 100% [92%-100%] | 181/209 = 87% [81%-91%] | 0 | 0 | no |
| gemma4_12b | humble_for_other | 45/45 = 100% [92%-100%] | 181/209 = 87% [81%-91%] | 0 | 0 | no |
| gemma4_12b | honorific_for_self | 45/45 = 100% [92%-100%] | 181/209 = 87% [81%-91%] | 0 | 0 | no |
| gemma4_12b | (all positives) | 135/135 = 100% [97%-100%] | 181/209 = 87% [81%-91%] | 0 | 0 | no |
| qwen3.5_27b | double_honorific | 45/45 = 100% [92%-100%] | 105/209 = 50% [44%-57%] | 0 | 0 | no |
| qwen3.5_27b | humble_for_other | 37/45 = 82% [69%-91%] | 105/209 = 50% [44%-57%] | 0 | 0 | no |
| qwen3.5_27b | honorific_for_self | 45/45 = 100% [92%-100%] | 105/209 = 50% [44%-57%] | 0 | 0 | no |
| qwen3.5_27b | (all positives) | 127/135 = 94% [89%-97%] | 105/209 = 50% [44%-57%] | 0 | 0 | no |
| claude_haiku | double_honorific | 45/45 = 100% [92%-100%] | 38/209 = 18% [14%-24%] | 0 | 0 | no |
| claude_haiku | humble_for_other | 42/45 = 93% [82%-98%] | 38/209 = 18% [14%-24%] | 0 | 0 | yes |
| claude_haiku | honorific_for_self | 44/45 = 98% [88%-100%] | 38/209 = 18% [14%-24%] | 0 | 0 | yes |
| claude_haiku | (all positives) | 131/135 = 97% [93%-99%] | 38/209 = 18% [14%-24%] | 0 | 0 | yes |
| jev | double_honorific | 8/45 = 18% [9%-31%] | 33/209 = 16% [11%-21%] | 0 | 0 | no |
| jev | humble_for_other | 2/45 = 4% [1%-15%] | 33/209 = 16% [11%-21%] | 0 | 0 | no |
| jev | honorific_for_self | 26/45 = 58% [43%-71%] | 33/209 = 16% [11%-21%] | 0 | 0 | yes |
| jev | (all positives) | 36/135 = 27% [20%-35%] | 33/209 = 16% [11%-21%] | 0 | 0 | no |
| clef_flash | double_honorific | 0/45 = 0% [0%-8%] | 7/209 = 3% [2%-7%] | 0 | 0 | no |
| clef_flash | humble_for_other | 2/45 = 4% [1%-15%] | 7/209 = 3% [2%-7%] | 0 | 0 | no |
| clef_flash | honorific_for_self | 5/45 = 11% [5%-23%] | 7/209 = 3% [2%-7%] | 0 | 0 | yes |
| clef_flash | (all positives) | 7/135 = 5% [3%-10%] | 7/209 = 3% [2%-7%] | 0 | 0 | no |
| gpt_6_luna | double_honorific | 42/45 = 93% [82%-98%] | 64/209 = 31% [25%-37%] | 0 | 0 | no |
| gpt_6_luna | humble_for_other | 27/45 = 60% [45%-73%] | 64/209 = 31% [25%-37%] | 0 | 0 | no |
| gpt_6_luna | honorific_for_self | 39/45 = 87% [74%-94%] | 64/209 = 31% [25%-37%] | 0 | 0 | no |
| gpt_6_luna | (all positives) | 108/135 = 80% [72%-86%] | 64/209 = 31% [25%-37%] | 0 | 0 | no |

Zero counts: baseline/humble_for_other caught 0 of 45 (rate < 6.5%); baseline/honorific_for_self caught 0 of 45 (rate < 6.5%); clef_flash/double_honorific caught 0 of 45 (rate < 6.5%)

### style

| judge | class | caught | false warnings (all negatives) | no answer | errors | beats baseline |
|---|---|---|---|---|---|---|
| baseline | mixed_register | 39/45 = 87% [74%-94%] | 1/135 = 1% [0%-4%] | 0 | 0 |  |
| baseline | width | 43/45 = 96% [85%-99%] | 1/135 = 1% [0%-4%] | 0 | 0 |  |
| baseline | term_variant | 0/45 = 0% [0%-8%] | 1/135 = 1% [0%-4%] | 0 | 0 |  |
| baseline | (all positives) | 82/135 = 61% [52%-69%] | 1/135 = 1% [0%-4%] | 0 | 0 |  |
| gemma4_12b | mixed_register | 45/45 = 100% [92%-100%] | 37/135 = 27% [21%-35%] | 0 | 0 | no |
| gemma4_12b | width | 27/45 = 60% [45%-73%] | 37/135 = 27% [21%-35%] | 0 | 0 | no |
| gemma4_12b | term_variant | 45/45 = 100% [92%-100%] | 37/135 = 27% [21%-35%] | 0 | 0 | no |
| gemma4_12b | (all positives) | 117/135 = 87% [80%-91%] | 37/135 = 27% [21%-35%] | 0 | 0 | no |
| qwen3.5_27b | mixed_register | 44/45 = 98% [88%-100%] | 10/135 = 7% [4%-13%] | 0 | 0 | yes |
| qwen3.5_27b | width | 35/45 = 78% [64%-87%] | 10/135 = 7% [4%-13%] | 0 | 0 | no |
| qwen3.5_27b | term_variant | 30/45 = 67% [52%-79%] | 10/135 = 7% [4%-13%] | 0 | 0 | yes |
| qwen3.5_27b | (all positives) | 109/135 = 81% [73%-87%] | 10/135 = 7% [4%-13%] | 0 | 0 | yes |
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
| gemma4_12b | aws_access_key | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| gemma4_12b | github_pat | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| gemma4_12b | slack_bot_token | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| gemma4_12b | stripe_live_key | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| gemma4_12b | gcp_api_key | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| gemma4_12b | (all positives) | 225/225 = 100% [98%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| qwen3.5_27b | aws_access_key | 45/45 = 100% [92%-100%] | 68/225 = 30% [25%-37%] | 0 | 0 | no |
| qwen3.5_27b | github_pat | 45/45 = 100% [92%-100%] | 68/225 = 30% [25%-37%] | 0 | 0 | no |
| qwen3.5_27b | slack_bot_token | 45/45 = 100% [92%-100%] | 68/225 = 30% [25%-37%] | 0 | 0 | no |
| qwen3.5_27b | stripe_live_key | 45/45 = 100% [92%-100%] | 68/225 = 30% [25%-37%] | 0 | 0 | no |
| qwen3.5_27b | gcp_api_key | 45/45 = 100% [92%-100%] | 68/225 = 30% [25%-37%] | 0 | 0 | no |
| qwen3.5_27b | (all positives) | 225/225 = 100% [98%-100%] | 68/225 = 30% [25%-37%] | 0 | 0 | no |
| claude_haiku | aws_access_key | 45/45 = 100% [92%-100%] | 57/225 = 25% [20%-31%] | 0 | 0 | no |
| claude_haiku | github_pat | 45/45 = 100% [92%-100%] | 57/225 = 25% [20%-31%] | 0 | 0 | no |
| claude_haiku | slack_bot_token | 45/45 = 100% [92%-100%] | 57/225 = 25% [20%-31%] | 0 | 0 | no |
| claude_haiku | stripe_live_key | 45/45 = 100% [92%-100%] | 57/225 = 25% [20%-31%] | 0 | 0 | no |
| claude_haiku | gcp_api_key | 45/45 = 100% [92%-100%] | 57/225 = 25% [20%-31%] | 0 | 0 | no |
| claude_haiku | (all positives) | 225/225 = 100% [98%-100%] | 57/225 = 25% [20%-31%] | 0 | 0 | no |
| jev | aws_access_key | 45/45 = 100% [92%-100%] | 65/225 = 29% [23%-35%] | 0 | 0 | no |
| jev | github_pat | 45/45 = 100% [92%-100%] | 65/225 = 29% [23%-35%] | 0 | 0 | no |
| jev | slack_bot_token | 45/45 = 100% [92%-100%] | 65/225 = 29% [23%-35%] | 0 | 0 | no |
| jev | stripe_live_key | 45/45 = 100% [92%-100%] | 65/225 = 29% [23%-35%] | 0 | 0 | no |
| jev | gcp_api_key | 45/45 = 100% [92%-100%] | 65/225 = 29% [23%-35%] | 0 | 0 | no |
| jev | (all positives) | 225/225 = 100% [98%-100%] | 65/225 = 29% [23%-35%] | 0 | 0 | no |
| clef_flash | aws_access_key | 45/45 = 100% [92%-100%] | 180/225 = 80% [74%-85%] | 0 | 0 | no |
| clef_flash | github_pat | 45/45 = 100% [92%-100%] | 180/225 = 80% [74%-85%] | 0 | 0 | no |
| clef_flash | slack_bot_token | 45/45 = 100% [92%-100%] | 180/225 = 80% [74%-85%] | 0 | 0 | no |
| clef_flash | stripe_live_key | 45/45 = 100% [92%-100%] | 180/225 = 80% [74%-85%] | 0 | 0 | no |
| clef_flash | gcp_api_key | 45/45 = 100% [92%-100%] | 180/225 = 80% [74%-85%] | 0 | 0 | no |
| clef_flash | (all positives) | 225/225 = 100% [98%-100%] | 180/225 = 80% [74%-85%] | 0 | 0 | no |
| gpt_6_luna | aws_access_key | 45/45 = 100% [92%-100%] | 55/225 = 24% [19%-30%] | 0 | 0 | no |
| gpt_6_luna | github_pat | 45/45 = 100% [92%-100%] | 55/225 = 24% [19%-30%] | 0 | 0 | no |
| gpt_6_luna | slack_bot_token | 45/45 = 100% [92%-100%] | 55/225 = 24% [19%-30%] | 0 | 0 | no |
| gpt_6_luna | stripe_live_key | 45/45 = 100% [92%-100%] | 55/225 = 24% [19%-30%] | 0 | 0 | no |
| gpt_6_luna | gcp_api_key | 45/45 = 100% [92%-100%] | 55/225 = 24% [19%-30%] | 0 | 0 | no |
| gpt_6_luna | (all positives) | 225/225 = 100% [98%-100%] | 55/225 = 24% [19%-30%] | 0 | 0 | no |

Zero counts: none

### aitext

| judge | class | caught | false warnings (all negatives) | no answer | errors | beats baseline |
|---|---|---|---|---|---|---|
| baseline | llm_claude_haiku | 6/45 = 13% [6%-26%] | 3/25 = 12% [4%-30%] | 0 | 0 |  |
| baseline | llm_gemma4_12b | 18/45 = 40% [27%-55%] | 3/25 = 12% [4%-30%] | 0 | 0 |  |
| baseline | llm_qwen3.5_27b | 7/45 = 16% [8%-29%] | 3/25 = 12% [4%-30%] | 0 | 0 |  |
| baseline | (all positives) | 31/135 = 23% [17%-31%] | 3/25 = 12% [4%-30%] | 0 | 0 |  |
| gemma4_12b | llm_claude_haiku | 5/45 = 11% [5%-23%] | 1/25 = 4% [1%-20%] | 0 | 0 | no |
| gemma4_12b | llm_gemma4_12b | 12/45 = 27% [16%-41%] | 1/25 = 4% [1%-20%] | 0 | 0 | no |
| gemma4_12b | llm_qwen3.5_27b | 8/45 = 18% [9%-31%] | 1/25 = 4% [1%-20%] | 0 | 0 | no |
| gemma4_12b | (all positives) | 25/135 = 19% [13%-26%] | 1/25 = 4% [1%-20%] | 0 | 0 | no |
| qwen3.5_27b | llm_claude_haiku | 0/45 = 0% [0%-8%] | 0/25 = 0% [0%-13%] | 0 | 0 | no |
| qwen3.5_27b | llm_gemma4_12b | 0/45 = 0% [0%-8%] | 0/25 = 0% [0%-13%] | 0 | 0 | no |
| qwen3.5_27b | llm_qwen3.5_27b | 0/45 = 0% [0%-8%] | 0/25 = 0% [0%-13%] | 0 | 0 | no |
| qwen3.5_27b | (all positives) | 0/135 = 0% [0%-3%] | 0/25 = 0% [0%-13%] | 0 | 0 | no |
| claude_haiku | llm_claude_haiku | 3/45 = 7% [2%-18%] | 0/25 = 0% [0%-13%] | 0 | 0 | no |
| claude_haiku | llm_gemma4_12b | 11/45 = 24% [14%-39%] | 0/25 = 0% [0%-13%] | 0 | 0 | no |
| claude_haiku | llm_qwen3.5_27b | 12/45 = 27% [16%-41%] | 0/25 = 0% [0%-13%] | 0 | 0 | yes |
| claude_haiku | (all positives) | 26/135 = 19% [13%-27%] | 0/25 = 0% [0%-13%] | 0 | 0 | no |
| jev | llm_claude_haiku | 4/45 = 9% [4%-21%] | 2/25 = 8% [2%-25%] | 0 | 0 | no |
| jev | llm_gemma4_12b | 17/45 = 38% [25%-52%] | 2/25 = 8% [2%-25%] | 0 | 0 | no |
| jev | llm_qwen3.5_27b | 11/45 = 24% [14%-39%] | 2/25 = 8% [2%-25%] | 0 | 0 | no |
| jev | (all positives) | 32/135 = 24% [17%-32%] | 2/25 = 8% [2%-25%] | 0 | 0 | no |
| clef_flash | llm_claude_haiku | 12/45 = 27% [16%-41%] | 3/25 = 12% [4%-30%] | 0 | 0 | no |
| clef_flash | llm_gemma4_12b | 20/45 = 44% [31%-59%] | 3/25 = 12% [4%-30%] | 0 | 0 | no |
| clef_flash | llm_qwen3.5_27b | 14/45 = 31% [20%-46%] | 3/25 = 12% [4%-30%] | 0 | 0 | no |
| clef_flash | (all positives) | 46/135 = 34% [27%-42%] | 3/25 = 12% [4%-30%] | 0 | 0 | no |
| gpt_6_luna | llm_claude_haiku | 33/45 = 73% [59%-84%] | 12/25 = 48% [30%-67%] | 0 | 0 | no |
| gpt_6_luna | llm_gemma4_12b | 39/45 = 87% [74%-94%] | 12/25 = 48% [30%-67%] | 0 | 0 | no |
| gpt_6_luna | llm_qwen3.5_27b | 41/45 = 91% [79%-96%] | 12/25 = 48% [30%-67%] | 0 | 0 | no |
| gpt_6_luna | (all positives) | 113/135 = 84% [77%-89%] | 12/25 = 48% [30%-67%] | 0 | 0 | no |

Zero counts: qwen3.5_27b/llm_claude_haiku caught 0 of 45 (rate < 6.5%); qwen3.5_27b/llm_gemma4_12b caught 0 of 45 (rate < 6.5%); qwen3.5_27b/llm_qwen3.5_27b caught 0 of 45 (rate < 6.5%); qwen3.5_27b false warnings 0 of 25 (rate < 11.3%); claude_haiku false warnings 0 of 25 (rate < 11.3%)

Lower bounds of balanced accuracy, two methods. The pass bar's condition (above 0.5) is judged on the first, the conservative average of the two Wilson lower bounds, which is what was implemented before any run; the second is a Newcombe-style combination.

| judge | balanced accuracy | lower bound (avg of Wilson) | lower bound (Newcombe) |
|---|---|---|---|
| baseline | 55.5% | 43.4% | 46.0% |
| gemma4_12b | 57.3% | 46.7% | 49.0% |
| qwen3.5_27b | 50.0% | 43.3% | 43.3% |
| claude_haiku | 59.6% | 50.1% | 52.4% |
| jev | 57.9% | 46.2% | 48.8% |
| clef_flash | 61.0% | 48.3% | 51.3% |
| gpt_6_luna | 67.9% | 55.0% | 57.9% |

## Robustness

### injection_honorific

| judge | attack | flagged before | flipped | flip rate (upper 95% bound) | robust (bound <= 10%) |
|---|---|---|---|---|---|
| baseline | authority | 15 | 0 | 0% (20%) (not measurable: fewer than 40) | not measurable |
| baseline | direct | 15 | 0 | 0% (20%) (not measurable: fewer than 40) | not measurable |
| baseline | fake_answer | 15 | 0 | 0% (20%) (not measurable: fewer than 40) | not measurable |
| gemma4_12b | authority | 45 | 3 | 7% (18%) | no |
| gemma4_12b | direct | 45 | 33 | 73% (84%) | no |
| gemma4_12b | fake_answer | 45 | 45 | 100% (100%) | no |
| qwen3.5_27b | authority | 43 | 17 | 40% (54%) | no |
| qwen3.5_27b | direct | 43 | 42 | 98% (100%) | no |
| qwen3.5_27b | fake_answer | 43 | 43 | 100% (100%) | no |
| claude_haiku | authority | 45 | 0 | 0% (8%) | yes |
| claude_haiku | direct | 45 | 3 | 7% (18%) | no |
| claude_haiku | fake_answer | 45 | 24 | 53% (67%) | no |
| jev | authority | 10 | 0 | 0% (28%) (not measurable: fewer than 40) | not measurable |
| jev | direct | 10 | 2 | 20% (51%) (not measurable: fewer than 40) | not measurable |
| jev | fake_answer | 10 | 1 | 10% (40%) (not measurable: fewer than 40) | not measurable |
| clef_flash | authority | 0 | 0 | 0% (100%) (not measurable: fewer than 40) | not measurable |
| clef_flash | direct | 0 | 0 | 0% (100%) (not measurable: fewer than 40) | not measurable |
| clef_flash | fake_answer | 0 | 0 | 0% (100%) (not measurable: fewer than 40) | not measurable |
| gpt_6_luna | authority | 39 | 38 | 97% (100%) (not measurable: fewer than 40) | not measurable |
| gpt_6_luna | direct | 39 | 12 | 31% (46%) (not measurable: fewer than 40) | not measurable |
| gpt_6_luna | fake_answer | 39 | 31 | 79% (89%) (not measurable: fewer than 40) | not measurable |

### injection_secrets

| judge | attack | flagged before | flipped | flip rate (upper 95% bound) | robust (bound <= 10%) |
|---|---|---|---|---|---|
| baseline | authority | 45 | 0 | 0% (8%) | yes |
| baseline | direct | 45 | 0 | 0% (8%) | yes |
| baseline | fake_answer | 45 | 0 | 0% (8%) | yes |
| gemma4_12b | authority | 45 | 43 | 96% (99%) | no |
| gemma4_12b | direct | 45 | 2 | 4% (15%) | no |
| gemma4_12b | fake_answer | 45 | 45 | 100% (100%) | no |
| qwen3.5_27b | authority | 45 | 45 | 100% (100%) | no |
| qwen3.5_27b | direct | 45 | 45 | 100% (100%) | no |
| qwen3.5_27b | fake_answer | 45 | 45 | 100% (100%) | no |
| claude_haiku | authority | 45 | 0 | 0% (8%) | yes |
| claude_haiku | direct | 45 | 0 | 0% (8%) | yes |
| claude_haiku | fake_answer | 45 | 1 | 2% (12%) | no |
| jev | authority | 45 | 0 | 0% (8%) | yes |
| jev | direct | 45 | 0 | 0% (8%) | yes |
| jev | fake_answer | 45 | 0 | 0% (8%) | yes |
| clef_flash | authority | 45 | 0 | 0% (8%) | yes |
| clef_flash | direct | 45 | 0 | 0% (8%) | yes |
| clef_flash | fake_answer | 45 | 0 | 0% (8%) | yes |
| gpt_6_luna | authority | 45 | 27 | 60% (73%) | no |
| gpt_6_luna | direct | 45 | 0 | 0% (8%) | yes |
| gpt_6_luna | fake_answer | 45 | 2 | 4% (15%) | no |

## False warnings by kind of negative

### honorific: false warnings by kind of negative

| judge | neg_paired (n=135) | neg_connected (n=20) | neg_established (n=20) | neg_naru_honorific (n=34) |
|---|---|---|---|---|
| baseline | 0/135 | 0/20 | 0/20 | 34/34 |
| gemma4_12b | 107/135 | 20/20 | 20/20 | 34/34 |
| qwen3.5_27b | 58/135 | 20/20 | 13/20 | 14/34 |
| claude_haiku | 8/135 | 20/20 | 4/20 | 6/34 |
| jev | 20/135 | 8/20 | 2/20 | 3/34 |
| clef_flash | 7/135 | 0/20 | 0/20 | 0/34 |
| gpt_6_luna | 39/135 | 9/20 | 6/20 | 10/34 |

### secrets: false warnings by kind of negative

| judge | neg_paired (n=225) |
|---|---|
| baseline | 60/225 |
| gemma4_12b | 69/225 |
| qwen3.5_27b | 68/225 |
| claude_haiku | 57/225 |
| jev | 65/225 |
| clef_flash | 180/225 |
| gpt_6_luna | 55/225 |

## Checks on what the AI-text dataset gives away

Not judges: a threshold-free AUC of a trivial feature, so a reader can see how much length or sentence count alone explains.

| feature | AUC |
|---|---|
| character count | 0.44 |
| number of sentences | 0.50 |

| generator | AUC of character count (AI vs human) |
|---|---|
| claude_haiku | 0.51 |
| gemma4_12b | 0.45 |
| qwen3.5_27b | 0.35 |

| group | n | median characters |
|---|---|---|
| human | 25 | 53 |
| claude_haiku | 45 | 51 |
| gemma4_12b | 45 | 48 |
| qwen3.5_27b | 45 | 44 |

## AUC from the returned probability

Not part of the pass bar, which fixes the 0.5 cut. Shown because a decision model's probability need not be calibrated at 0.5.

| judge | honorific | style | secrets | aitext |
|---|---|---|---|---|
| gemma4_12b | 0.77 | 0.91 | 1.00 | 0.72 |
| qwen3.5_27b | 0.86 | 0.94 | 0.99 | 0.41 |
| claude_haiku | n/a | n/a | n/a | n/a |
| jev | 0.64 | 0.75 | 0.99 | 0.69 |
| clef_flash | 0.57 | 0.73 | 0.95 | 0.75 |
| gpt_6_luna | 0.82 | 0.83 | 0.97 | 0.70 |

## Threshold chosen on one half, measured on the other

Judges that return a probability. The cut is the one maximising caught rate minus false-warning rate on the first half; both halves hold every class. Not part of the pass bar, which fixes 0.5.

| task | judge | cut | caught at 0.5 | false warnings at 0.5 | caught at the chosen cut | false warnings at the chosen cut |
|---|---|---|---|---|---|---|
| honorific | gemma4_12b | 1.00 | 66/66 = 100% [94%-100%] | 89/103 = 86% [78%-92%] | 61/66 = 92% [83%-97%] | 37/103 = 36% [27%-46%] |
| honorific | qwen3.5_27b | 0.75 | 62/66 = 94% [85%-98%] | 53/103 = 51% [42%-61%] | 57/66 = 86% [76%-93%] | 20/103 = 19% [13%-28%] |
| honorific | jev | 0.40 | 19/66 = 29% [19%-41%] | 13/103 = 13% [8%-20%] | 47/66 = 71% [59%-81%] | 47/103 = 46% [36%-55%] |
| honorific | clef_flash | 0.28 | 4/66 = 6% [2%-15%] | 3/103 = 3% [1%-8%] | 27/66 = 41% [30%-53%] | 38/103 = 37% [28%-47%] |
| honorific | gpt_6_luna | 0.57 | 52/66 = 79% [67%-87%] | 32/103 = 31% [23%-41%] | 50/66 = 76% [64%-84%] | 19/103 = 18% [12%-27%] |
| style | gemma4_12b | 0.99 | 57/64 = 89% [79%-95%] | 17/66 = 26% [17%-37%] | 52/64 = 81% [70%-89%] | 12/66 = 18% [11%-29%] |
| style | qwen3.5_27b | 0.38 | 53/66 = 80% [69%-88%] | 7/66 = 11% [5%-20%] | 56/66 = 85% [74%-92%] | 10/66 = 15% [8%-26%] |
| style | jev | 0.32 | 27/66 = 41% [30%-53%] | 5/66 = 8% [3%-17%] | 40/66 = 61% [49%-71%] | 13/66 = 20% [12%-31%] |
| style | clef_flash | 0.20 | 6/66 = 9% [4%-18%] | 1/66 = 2% [0%-8%] | 41/66 = 62% [50%-73%] | 23/66 = 35% [24%-47%] |
| style | gpt_6_luna | 0.05 | 23/66 = 35% [24%-47%] | 0/66 = 0% [0%-6%] | 40/66 = 61% [49%-71%] | 9/66 = 14% [7%-24%] |
| secrets | gemma4_12b | 1.00 | 105/105 = 100% [96%-100%] | 31/105 = 30% [22%-39%] | 102/105 = 97% [92%-99%] | 1/105 = 1% [0%-5%] |
| secrets | qwen3.5_27b | 0.87 | 105/105 = 100% [96%-100%] | 32/105 = 30% [22%-40%] | 101/105 = 96% [91%-99%] | 0/105 = 0% [0%-4%] |
| secrets | jev | 0.94 | 105/105 = 100% [96%-100%] | 30/105 = 29% [21%-38%] | 99/105 = 94% [88%-97%] | 0/105 = 0% [0%-4%] |
| secrets | clef_flash | 0.96 | 105/105 = 100% [96%-100%] | 82/105 = 78% [69%-85%] | 82/105 = 78% [69%-85%] | 6/105 = 6% [3%-12%] |
| secrets | gpt_6_luna | 0.99 | 105/105 = 100% [96%-100%] | 23/105 = 22% [15%-31%] | 102/105 = 97% [92%-99%] | 6/105 = 6% [3%-12%] |
| aitext | gemma4_12b | 0.00 | 14/66 = 21% [13%-33%] | 0/12 = 0% [0%-24%] | 59/66 = 89% [80%-95%] | 5/12 = 42% [19%-68%] |
| aitext | qwen3.5_27b | 0.16 | 0/66 = 0% [0%-6%] | 0/12 = 0% [0%-24%] | 15/66 = 23% [14%-34%] | 3/12 = 25% [9%-53%] |
| aitext | jev | 0.42 | 17/66 = 26% [17%-37%] | 1/12 = 8% [1%-35%] | 49/66 = 74% [63%-83%] | 4/12 = 33% [14%-61%] |
| aitext | clef_flash | 0.30 | 23/66 = 35% [24%-47%] | 1/12 = 8% [1%-35%] | 56/66 = 85% [74%-92%] | 4/12 = 33% [14%-61%] |
| aitext | gpt_6_luna | 0.46 | 57/66 = 86% [76%-93%] | 4/12 = 33% [14%-61%] | 63/66 = 95% [87%-98%] | 8/12 = 67% [39%-86%] |

## Two-stage setups

Not part of the pass bar (it scores single judges); reported because the article recommends combinations.

| task | setup | caught | false warnings |
|---|---|---|---|
| honorific | rule OR LLM: gemma4_12b | 135/135 = 100% [97%-100%] | 181/209 = 87% [81%-91%] |
| honorific | rule OR LLM: qwen3.5_27b | 127/135 = 94% [89%-97%] | 125/209 = 60% [53%-66%] |
| honorific | rule OR LLM: claude_haiku | 131/135 = 97% [93%-99%] | 66/209 = 32% [26%-38%] |
| honorific | rule OR LLM: jev | 73/135 = 54% [46%-62%] | 64/209 = 31% [25%-37%] |
| honorific | rule OR LLM: clef_flash | 52/135 = 39% [31%-47%] | 41/209 = 20% [15%-26%] |
| honorific | rule OR LLM: gpt_6_luna | 111/135 = 82% [75%-88%] | 88/209 = 42% [36%-49%] |
| secrets | gitleaks AND LLM: gemma4_12b | 225/225 = 100% [98%-100%] | 23/225 = 10% [7%-15%] |
| secrets | gitleaks AND LLM: qwen3.5_27b | 225/225 = 100% [98%-100%] | 25/225 = 11% [8%-16%] |
| secrets | gitleaks AND LLM: claude_haiku | 225/225 = 100% [98%-100%] | 15/225 = 7% [4%-11%] |
| secrets | gitleaks AND LLM: jev | 225/225 = 100% [98%-100%] | 15/225 = 7% [4%-11%] |
| secrets | gitleaks AND LLM: clef_flash | 225/225 = 100% [98%-100%] | 60/225 = 27% [21%-33%] |
| secrets | gitleaks AND LLM: gpt_6_luna | 225/225 = 100% [98%-100%] | 9/225 = 4% [2%-7%] |

## What gitleaks flags among the secrets negatives

| look-alike | flagged |
|---|---|
| hex40 | 29 |
| uuid | 31 |
| other | 0 |

## No-answer verdicts

| judge | task | no answer |
|---|---|---|
| gpt_6_luna | injection_secrets | 2 |
