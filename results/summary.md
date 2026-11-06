# Results

## Latency and memory

| judge | median latency (s/item) | loaded size (GB) |
|---|---|---|
| baseline (batch, amortised) | 0.001 | 0.50 (peak RSS) |
| gemma4_12b | 0.34 | 20.7 |
| qwen3.5_27b | 0.91 | 28.4 |
| claude_haiku | 7.54 | hosted |
| jev | 0.20 | hosted |
| clef_flash | 0.49 | 21.3 |
| gpt_6_luna | 0.29 | hosted |

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
| qwen3.5_27b | double_honorific | 45/45 = 100% [92%-100%] | 41/209 = 20% [15%-26%] | 0 | 0 | no |
| qwen3.5_27b | humble_for_other | 19/45 = 42% [29%-57%] | 41/209 = 20% [15%-26%] | 0 | 0 | yes |
| qwen3.5_27b | honorific_for_self | 39/45 = 87% [74%-94%] | 41/209 = 20% [15%-26%] | 0 | 0 | yes |
| qwen3.5_27b | (all positives) | 103/135 = 76% [68%-83%] | 41/209 = 20% [15%-26%] | 0 | 0 | yes |
| claude_haiku | double_honorific | 45/45 = 100% [92%-100%] | 84/209 = 40% [34%-47%] | 0 | 0 | no |
| claude_haiku | humble_for_other | 43/45 = 96% [85%-99%] | 84/209 = 40% [34%-47%] | 0 | 0 | no |
| claude_haiku | honorific_for_self | 43/45 = 96% [85%-99%] | 84/209 = 40% [34%-47%] | 0 | 0 | no |
| claude_haiku | (all positives) | 131/135 = 97% [93%-99%] | 84/209 = 40% [34%-47%] | 0 | 0 | no |
| jev | double_honorific | 11/45 = 24% [14%-39%] | 30/209 = 14% [10%-20%] | 0 | 0 | no |
| jev | humble_for_other | 1/45 = 2% [0%-12%] | 30/209 = 14% [10%-20%] | 0 | 0 | no |
| jev | honorific_for_self | 26/45 = 58% [43%-71%] | 30/209 = 14% [10%-20%] | 0 | 0 | yes |
| jev | (all positives) | 38/135 = 28% [21%-36%] | 30/209 = 14% [10%-20%] | 0 | 0 | no |
| clef_flash | double_honorific | 0/45 = 0% [0%-8%] | 7/209 = 3% [2%-7%] | 0 | 0 | no |
| clef_flash | humble_for_other | 2/45 = 4% [1%-15%] | 7/209 = 3% [2%-7%] | 0 | 0 | no |
| clef_flash | honorific_for_self | 5/45 = 11% [5%-23%] | 7/209 = 3% [2%-7%] | 0 | 0 | yes |
| clef_flash | (all positives) | 7/135 = 5% [3%-10%] | 7/209 = 3% [2%-7%] | 0 | 0 | no |
| gpt_6_luna | double_honorific | 43/45 = 96% [85%-99%] | 59/209 = 28% [23%-35%] | 0 | 0 | no |
| gpt_6_luna | humble_for_other | 27/45 = 60% [45%-73%] | 59/209 = 28% [23%-35%] | 0 | 0 | no |
| gpt_6_luna | honorific_for_self | 39/45 = 87% [74%-94%] | 59/209 = 28% [23%-35%] | 0 | 0 | no |
| gpt_6_luna | (all positives) | 109/135 = 81% [73%-87%] | 59/209 = 28% [23%-35%] | 0 | 0 | no |

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
| gemma4_12b | aws_access_key | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| gemma4_12b | github_pat | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| gemma4_12b | slack_bot_token | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| gemma4_12b | stripe_live_key | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| gemma4_12b | gcp_api_key | 45/45 = 100% [92%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| gemma4_12b | (all positives) | 225/225 = 100% [98%-100%] | 69/225 = 31% [25%-37%] | 0 | 0 | no |
| qwen3.5_27b | aws_access_key | 45/45 = 100% [92%-100%] | 14/225 = 6% [4%-10%] | 0 | 0 | no |
| qwen3.5_27b | github_pat | 45/45 = 100% [92%-100%] | 14/225 = 6% [4%-10%] | 0 | 0 | no |
| qwen3.5_27b | slack_bot_token | 45/45 = 100% [92%-100%] | 14/225 = 6% [4%-10%] | 0 | 0 | no |
| qwen3.5_27b | stripe_live_key | 45/45 = 100% [92%-100%] | 14/225 = 6% [4%-10%] | 0 | 0 | no |
| qwen3.5_27b | gcp_api_key | 38/45 = 84% [71%-92%] | 14/225 = 6% [4%-10%] | 0 | 0 | no |
| qwen3.5_27b | (all positives) | 218/225 = 97% [94%-98%] | 14/225 = 6% [4%-10%] | 0 | 0 | no |
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
| gemma4_12b | llm_claude_haiku | 3/45 = 7% [2%-18%] | 1/25 = 4% [1%-20%] | 0 | 0 | no |
| gemma4_12b | llm_gemma4_12b | 12/45 = 27% [16%-41%] | 1/25 = 4% [1%-20%] | 0 | 0 | no |
| gemma4_12b | llm_qwen3.5_27b | 8/45 = 18% [9%-31%] | 1/25 = 4% [1%-20%] | 0 | 0 | no |
| gemma4_12b | (all positives) | 23/135 = 17% [12%-24%] | 1/25 = 4% [1%-20%] | 0 | 0 | no |
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
| gemma4_12b | 56.5% | 46.0% | 48.3% |
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
| gemma4_12b | authority | 45 | 23 | 51% (65%) | no |
| gemma4_12b | direct | 45 | 31 | 69% (80%) | no |
| gemma4_12b | fake_answer | 45 | 45 | 100% (100%) | no |
| qwen3.5_27b | authority | 33 | 33 | 100% (100%) (not measurable: fewer than 40) | not measurable |
| qwen3.5_27b | direct | 33 | 33 | 100% (100%) (not measurable: fewer than 40) | not measurable |
| qwen3.5_27b | fake_answer | 33 | 33 | 100% (100%) (not measurable: fewer than 40) | not measurable |
| claude_haiku | authority | 44 | 0 | 0% (8%) | yes |
| claude_haiku | direct | 44 | 3 | 7% (18%) | no |
| claude_haiku | fake_answer | 44 | 22 | 50% (64%) | no |
| jev | authority | 12 | 5 | 42% (68%) (not measurable: fewer than 40) | not measurable |
| jev | direct | 12 | 4 | 33% (61%) (not measurable: fewer than 40) | not measurable |
| jev | fake_answer | 12 | 0 | 0% (24%) (not measurable: fewer than 40) | not measurable |
| clef_flash | authority | 0 | 0 | 0% (100%) (not measurable: fewer than 40) | not measurable |
| clef_flash | direct | 0 | 0 | 0% (100%) (not measurable: fewer than 40) | not measurable |
| clef_flash | fake_answer | 0 | 0 | 0% (100%) (not measurable: fewer than 40) | not measurable |
| gpt_6_luna | authority | 39 | 37 | 95% (99%) (not measurable: fewer than 40) | not measurable |
| gpt_6_luna | direct | 39 | 12 | 31% (46%) (not measurable: fewer than 40) | not measurable |
| gpt_6_luna | fake_answer | 39 | 33 | 85% (93%) (not measurable: fewer than 40) | not measurable |

### injection_secrets

| judge | attack | flagged before | flipped | flip rate (upper 95% bound) | robust (bound <= 10%) |
|---|---|---|---|---|---|
| baseline | authority | 45 | 0 | 0% (8%) | yes |
| baseline | direct | 45 | 0 | 0% (8%) | yes |
| baseline | fake_answer | 45 | 0 | 0% (8%) | yes |
| gemma4_12b | authority | 45 | 43 | 96% (99%) | no |
| gemma4_12b | direct | 45 | 2 | 4% (15%) | no |
| gemma4_12b | fake_answer | 45 | 45 | 100% (100%) | no |
| qwen3.5_27b | authority | 44 | 44 | 100% (100%) | no |
| qwen3.5_27b | direct | 44 | 44 | 100% (100%) | no |
| qwen3.5_27b | fake_answer | 44 | 44 | 100% (100%) | no |
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
| gemma4_12b | 108/135 | 20/20 | 19/20 | 34/34 |
| qwen3.5_27b | 14/135 | 20/20 | 7/20 | 0/34 |
| claude_haiku | 30/135 | 20/20 | 13/20 | 21/34 |
| jev | 17/135 | 12/20 | 1/20 | 0/34 |
| clef_flash | 7/135 | 0/20 | 0/20 | 0/34 |
| gpt_6_luna | 39/135 | 10/20 | 0/20 | 10/34 |

### secrets: false warnings by kind of negative

| judge | neg_paired (n=225) |
|---|---|
| baseline | 60/225 |
| gemma4_12b | 69/225 |
| qwen3.5_27b | 14/225 |
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
| gemma4_12b | 0.78 | 0.91 | 1.00 | 0.72 |
| qwen3.5_27b | 0.86 | 0.94 | 0.99 | 0.41 |
| claude_haiku | n/a | n/a | n/a | n/a |
| jev | 0.63 | 0.75 | 0.99 | 0.69 |
| clef_flash | 0.56 | 0.73 | 0.95 | 0.75 |
| gpt_6_luna | 0.83 | 0.83 | 0.97 | 0.70 |

## Threshold chosen on one half, measured on the other

Judges that return a probability. The cut is the one maximising caught rate minus false-warning rate on the first half; both halves hold every class. Not part of the pass bar, which fixes 0.5.

| task | judge | cut | caught at 0.5 | false warnings at 0.5 | caught at the chosen cut | false warnings at the chosen cut |
|---|---|---|---|---|---|---|
| honorific | gemma4_12b | 1.00 | 66/66 = 100% [94%-100%] | 88/103 = 85% [77%-91%] | 59/66 = 89% [80%-95%] | 43/103 = 42% [33%-51%] |
| honorific | qwen3.5_27b | 0.75 | 61/66 = 92% [83%-97%] | 45/103 = 44% [35%-53%] | 54/66 = 82% [71%-89%] | 22/103 = 21% [15%-30%] |
| honorific | jev | 0.38 | 20/66 = 30% [21%-42%] | 14/103 = 14% [8%-22%] | 45/66 = 68% [56%-78%] | 56/103 = 54% [45%-64%] |
| honorific | clef_flash | 0.26 | 4/66 = 6% [2%-15%] | 4/103 = 4% [2%-10%] | 39/66 = 59% [47%-70%] | 51/103 = 50% [40%-59%] |
| honorific | gpt_6_luna | 0.55 | 55/66 = 83% [73%-90%] | 31/103 = 30% [22%-40%] | 54/66 = 82% [71%-89%] | 25/103 = 24% [17%-33%] |
| style | gemma4_12b | 1.00 | 56/63 = 89% [79%-95%] | 16/66 = 24% [16%-36%] | 44/63 = 70% [58%-80%] | 7/66 = 11% [5%-20%] |
| style | qwen3.5_27b | 0.29 | 54/66 = 82% [71%-89%] | 5/66 = 8% [3%-17%] | 60/66 = 91% [82%-96%] | 13/66 = 20% [12%-31%] |
| style | jev | 0.31 | 27/66 = 41% [30%-53%] | 5/66 = 8% [3%-17%] | 41/66 = 62% [50%-73%] | 14/66 = 21% [13%-33%] |
| style | clef_flash | 0.20 | 6/66 = 9% [4%-18%] | 1/66 = 2% [0%-8%] | 44/66 = 67% [55%-77%] | 23/66 = 35% [24%-47%] |
| style | gpt_6_luna | 0.04 | 22/66 = 33% [23%-45%] | 0/66 = 0% [0%-6%] | 43/66 = 65% [53%-76%] | 14/66 = 21% [13%-33%] |
| secrets | gemma4_12b | 1.00 | 110/110 = 100% [97%-100%] | 1/110 = 1% [0%-5%] | 104/110 = 95% [89%-97%] | 0/110 = 0% [0%-3%] |
| secrets | qwen3.5_27b | 0.93 | 110/110 = 100% [97%-100%] | 4/110 = 4% [1%-9%] | 102/110 = 93% [86%-96%] | 0/110 = 0% [0%-3%] |
| secrets | jev | 0.94 | 110/110 = 100% [97%-100%] | 8/110 = 7% [4%-14%] | 102/110 = 93% [86%-96%] | 0/110 = 0% [0%-3%] |
| secrets | clef_flash | 0.96 | 110/110 = 100% [97%-100%] | 105/110 = 95% [90%-98%] | 84/110 = 76% [68%-83%] | 0/110 = 0% [0%-3%] |
| secrets | gpt_6_luna | 0.99 | 110/110 = 100% [97%-100%] | 8/110 = 7% [4%-14%] | 107/110 = 97% [92%-99%] | 8/110 = 7% [4%-14%] |
| aitext | gemma4_12b | 0.00 | 15/66 = 23% [14%-34%] | 0/12 = 0% [0%-24%] | 62/66 = 94% [85%-98%] | 7/12 = 58% [32%-81%] |
| aitext | qwen3.5_27b | 0.25 | 0/66 = 0% [0%-6%] | 0/12 = 0% [0%-24%] | 11/66 = 17% [10%-27%] | 1/12 = 8% [1%-35%] |
| aitext | jev | 0.33 | 16/66 = 24% [16%-36%] | 1/12 = 8% [1%-35%] | 65/66 = 98% [92%-100%] | 12/12 = 100% [76%-100%] |
| aitext | clef_flash | 0.45 | 25/66 = 38% [27%-50%] | 2/12 = 17% [5%-45%] | 32/66 = 48% [37%-60%] | 3/12 = 25% [9%-53%] |
| aitext | gpt_6_luna | 0.50 | 57/66 = 86% [76%-93%] | 8/12 = 67% [39%-86%] | 57/66 = 86% [76%-93%] | 8/12 = 67% [39%-86%] |

## Two-stage setups

Not part of the pass bar (it scores single judges); reported because the article recommends combinations.

| task | setup | caught | false warnings |
|---|---|---|---|
| honorific | rule OR LLM: gemma4_12b | 135/135 = 100% [97%-100%] | 181/209 = 87% [81%-91%] |
| honorific | rule OR LLM: qwen3.5_27b | 103/135 = 76% [68%-83%] | 75/209 = 36% [30%-43%] |
| honorific | rule OR LLM: claude_haiku | 131/135 = 97% [93%-99%] | 97/209 = 46% [40%-53%] |
| honorific | rule OR LLM: jev | 72/135 = 53% [45%-62%] | 64/209 = 31% [25%-37%] |
| honorific | rule OR LLM: clef_flash | 52/135 = 39% [31%-47%] | 41/209 = 20% [15%-26%] |
| honorific | rule OR LLM: gpt_6_luna | 111/135 = 82% [75%-88%] | 83/209 = 40% [33%-46%] |
| secrets | gitleaks AND LLM: gemma4_12b | 225/225 = 100% [98%-100%] | 23/225 = 10% [7%-15%] |
| secrets | gitleaks AND LLM: qwen3.5_27b | 218/225 = 97% [94%-98%] | 3/225 = 1% [0%-4%] |
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
| gemma4_12b | injection_honorific | 19 |
| gpt_6_luna | injection_secrets | 2 |
