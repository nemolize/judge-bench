# Follow-up results

Detection = flagged positives / positives (a no-answer is a miss). False alarm = flagged negatives / negatives with a verdict.

## langid

| judge | detection | appended_other | control_en | control_zh | mixed_en_main | false alarm | appended_ja | control_ja | mixed_ja_main | romaji_ja | no answer | errors | median s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 80/160 = 50% | 0/40 = 0% | 40/40 = 100% | 40/40 = 100% | 0/40 = 0% | 39/160 = 24% | 0/40 = 0% | 0/40 = 0% | 0/40 = 0% | 39/40 = 98% | 0 | 0 | n/a |
| fasttext | 121/160 = 76% | 21/40 = 52% | 40/40 = 100% | 39/40 = 98% | 21/40 = 52% | 40/160 = 25% | 0/40 = 0% | 0/40 = 0% | 0/40 = 0% | 40/40 = 100% | 0 | 0 | n/a |
| claude_api_off | 124/160 = 78% | 29/40 = 72% | 40/40 = 100% | 38/40 = 95% | 17/40 = 42% | 24/160 = 15% | 2/40 = 5% | 0/40 = 0% | 10/40 = 25% | 12/40 = 30% | 1 | 0 | 0.92 |
| claude_api_think | 159/160 = 99% | 39/40 = 98% | 40/40 = 100% | 40/40 = 100% | 40/40 = 100% | 0/160 = 0% | 0/40 = 0% | 0/40 = 0% | 0/40 = 0% | 0/40 = 0% | 0 | 0 | 1.19 |
| gemma4_12b | 87/160 = 54% | 28/40 = 70% | 21/40 = 52% | 29/40 = 72% | 9/40 = 22% | 1/160 = 1% | 0/40 = 0% | 0/40 = 0% | 1/40 = 2% | 0/40 = 0% | 0 | 0 | 0.36 |
| gemma4_12b_think | 120/120 = 100% | 40/40 = 100% | 40/40 = 100% | 40/40 = 100% | - | 0/80 = 0% | 0/40 = 0% | 0/40 = 0% | - | - | 0 | 0 | 9.19 |
| gemini_decision | 145/160 = 91% | 40/40 = 100% | 40/40 = 100% | 40/40 = 100% | 25/40 = 62% | 1/160 = 1% | 0/40 = 0% | 0/40 = 0% | 1/40 = 2% | 0/40 = 0% | 0 | 0 | 0.34 |

Zero counts: baseline/mixed_en_main: 0 of 40 (< 7.2%); baseline/appended_other: 0 of 40 (< 7.2%); baseline/control_ja: 0 of 40 (< 7.2%); baseline/mixed_ja_main: 0 of 40 (< 7.2%); baseline/appended_ja: 0 of 40 (< 7.2%); fasttext/control_ja: 0 of 40 (< 7.2%); fasttext/mixed_ja_main: 0 of 40 (< 7.2%); fasttext/appended_ja: 0 of 40 (< 7.2%); claude_api_off/control_ja: 0 of 40 (< 7.2%); claude_api_think/control_ja: 0 of 40 (< 7.2%); claude_api_think/romaji_ja: 0 of 40 (< 7.2%); claude_api_think/mixed_ja_main: 0 of 40 (< 7.2%); claude_api_think/appended_ja: 0 of 40 (< 7.2%); gemma4_12b/control_ja: 0 of 40 (< 7.2%); gemma4_12b/romaji_ja: 0 of 40 (< 7.2%); gemma4_12b/appended_ja: 0 of 40 (< 7.2%); gemma4_12b_think/control_ja: 0 of 40 (< 7.2%); gemma4_12b_think/appended_ja: 0 of 40 (< 7.2%); gemini_decision/control_ja: 0 of 40 (< 7.2%); gemini_decision/romaji_ja: 0 of 40 (< 7.2%); gemini_decision/appended_ja: 0 of 40 (< 7.2%)

## personal_data

| judge | detection | email_personal | mobile_number | my_number_valid | false alarm | neg_email_role | neg_my_number_invalid | neg_phone_nonpersonal | no answer | errors | median s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 120/120 = 100% | 40/40 = 100% | 40/40 = 100% | 40/40 = 100% | 0/120 = 0% | 0/40 = 0% | 0/40 = 0% | 0/40 = 0% | 0 | 0 | n/a |
| claude_api_off | 105/120 = 88% | 40/40 = 100% | 36/40 = 90% | 29/40 = 72% | 30/115 = 26% | 0/40 = 0% | 30/35 = 86% | 0/40 = 0% | 10 | 0 | 0.74 |
| claude_api_think | 113/120 = 94% | 40/40 = 100% | 40/40 = 100% | 33/40 = 82% | 1/120 = 1% | 0/40 = 0% | 1/40 = 2% | 0/40 = 0% | 0 | 0 | 1.25 |
| gemma4_12b | 99/120 = 82% | 22/40 = 55% | 37/40 = 92% | 40/40 = 100% | 40/120 = 33% | 0/40 = 0% | 40/40 = 100% | 0/40 = 0% | 0 | 0 | 0.46 |
| gemini_decision | 101/120 = 84% | 40/40 = 100% | 36/40 = 90% | 25/40 = 62% | 27/120 = 22% | 0/40 = 0% | 27/40 = 68% | 0/40 = 0% | 0 | 0 | 0.32 |

Zero counts: baseline/neg_my_number_invalid: 0 of 40 (< 7.2%); baseline/neg_phone_nonpersonal: 0 of 40 (< 7.2%); baseline/neg_email_role: 0 of 40 (< 7.2%); claude_api_off/neg_phone_nonpersonal: 0 of 40 (< 7.2%); claude_api_off/neg_email_role: 0 of 40 (< 7.2%); claude_api_think/neg_phone_nonpersonal: 0 of 40 (< 7.2%); claude_api_think/neg_email_role: 0 of 40 (< 7.2%); gemma4_12b/neg_phone_nonpersonal: 0 of 40 (< 7.2%); gemma4_12b/neg_email_role: 0 of 40 (< 7.2%); gemini_decision/neg_phone_nonpersonal: 0 of 40 (< 7.2%); gemini_decision/neg_email_role: 0 of 40 (< 7.2%)

## calendar

| judge | detection | era_year | invoice | weekday | false alarm | neg_era_year | neg_invoice | neg_weekday | no answer | errors | median s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 120/120 = 100% | 40/40 = 100% | 40/40 = 100% | 40/40 = 100% | 0/120 = 0% | 0/40 = 0% | 0/40 = 0% | 0/40 = 0% | 0 | 0 | n/a |
| claude_api_off | 39/120 = 32% | 4/40 = 10% | 33/40 = 82% | 2/40 = 5% | 22/114 = 19% | 1/40 = 2% | 21/40 = 52% | 0/34 = 0% | 12 | 0 | 0.66 |
| claude_api_think | 119/120 = 99% | 40/40 = 100% | 39/40 = 98% | 40/40 = 100% | 0/120 = 0% | 0/40 = 0% | 0/40 = 0% | 0/40 = 0% | 0 | 0 | 1.13 |
| gemma4_12b | 63/120 = 52% | 34/40 = 85% | 20/40 = 50% | 9/40 = 22% | 44/120 = 37% | 31/40 = 78% | 4/40 = 10% | 9/40 = 22% | 0 | 0 | 0.54 |
| gemma4_12b_think | 120/120 = 100% | 40/40 = 100% | 40/40 = 100% | 40/40 = 100% | 0/116 = 0% | 0/40 = 0% | 0/40 = 0% | 0/36 = 0% | 4 | 0 | 22.49 |
| gemini_decision | 111/120 = 92% | 40/40 = 100% | 31/40 = 78% | 40/40 = 100% | 6/120 = 5% | 1/40 = 2% | 0/40 = 0% | 5/40 = 12% | 0 | 0 | 0.32 |

Zero counts: baseline/neg_era_year: 0 of 40 (< 7.2%); baseline/neg_weekday: 0 of 40 (< 7.2%); baseline/neg_invoice: 0 of 40 (< 7.2%); claude_api_off/neg_weekday: 0 of 34 (< 8.4%); claude_api_think/neg_era_year: 0 of 40 (< 7.2%); claude_api_think/neg_weekday: 0 of 40 (< 7.2%); claude_api_think/neg_invoice: 0 of 40 (< 7.2%); gemma4_12b_think/neg_era_year: 0 of 40 (< 7.2%); gemma4_12b_think/neg_weekday: 0 of 36 (< 8.0%); gemma4_12b_think/neg_invoice: 0 of 40 (< 7.2%); gemini_decision/neg_invoice: 0 of 40 (< 7.2%)

## Appended sentence: verdict flipped by the appended sentence

`to_yes` = NO became YES, `to_no` = YES became NO, against the control sentence. For appended_ja (a Japanese text, label NO) to_yes is the harm; for appended_other (a non-Japanese text, label YES) to_no is.

| judge | appended_ja to_yes / to_no | appended_other to_yes / to_no |
|---|---|---|
| baseline | 0 / 0 of 40 | 0 / 40 of 40 |
| fasttext | 0 / 0 of 40 | 0 / 19 of 40 |
| claude_api_off | 2 / 0 of 40 | 0 / 10 of 40 |
| claude_api_think | 0 / 0 of 40 | 0 / 1 of 40 |
| gemma4_12b | 0 / 0 of 40 | 13 / 4 of 40 |
| gemma4_12b_think | 0 / 0 of 40 | 0 / 0 of 40 |
| gemini_decision | 0 / 0 of 40 | 0 / 0 of 40 |
