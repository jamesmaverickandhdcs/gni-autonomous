# S111 item (b): results of the pre-registered test

- **Run date:** 2026-10-12, 03:42 (UTC+7)
- **Test plan:** S111_B_PREREG.md, written at 03:35, before any data was seen
- **Data:** S111_EXPORT7b.sql gave 274 outcomes and 281 reports; both counts were checked against the export. GPR came from the Caldara–Iacoviello daily "Recent" file, data up to 2026-10-05.
- **Script:** `tools/b_test_s111.py`. It was checked first on synthetic data: it returned PASS when a signal was planted and FAIL when none was.

A first run used the 100-row CSVs from S111_EXPORT7.sql, because the SQL Editor's grid stops at 100 rows. That run is void and was not used.

## Parts A to E: can the existing output be calibrated? **FAIL**

| | Value |
|---|---|
| Rows / ISO weeks / events | 274 / 21 / 64 (base rate 0.234) |
| Brier score, model (out of fold) | 0.1879 |
| Brier score, climatology | 0.1884 |
| BSS | **0.0029** (needs > 0, and the DM test below) |
| DM/HLN over 21 weekly means | stat 0.517, one-sided **p = 0.31** (needs < 0.05) |

Reliability of the out-of-fold forecasts, from lowest to highest forecast:

| Mean forecast | Observed frequency |
|---|---|
| 0.150 | 0.286 |
| 0.226 | 0.407 |
| 0.249 | 0.351 |
| 0.260 | 0.073 |
| 0.282 | 0.038 |

The relationship runs backwards. Where the forecast was highest, the event happened least often.

### Why the pooled AUC of 0.628 (S111_EVIDENCE6) did not survive

These checks were added after the test, to explain its result. They do not change the verdict.

- **AUC inside a single ISO week: 0.517.** Within one week, the score does not separate the windows where SPY fell from those where it did not.
- **Across the 21 weeks:** the Spearman correlation between a week's mean (−sentiment_score) and that week's event rate is 0.38, with a two-sided p of 0.086.
- The events cluster in whole weeks: W23, W24, W26, W29, W30 and W34 have rates of 0.53–0.79, and 12 weeks have none.
- The pooled AUC came almost entirely from a few weeks where both the score and the event rate were low (W21, W25, W41). It was a between-week effect, not a per-report signal. Leaving each week out removes it.

My earlier wording in S111 was "a weak signal for 7-day downside". It is **withdrawn**: out of sample, the signal is not there.

### Consequence

The (b) redesign starts from the prompt, as the plan says. GNI's current output cannot be calibrated into a downside probability that beats climatology.

## Part G: escalation against GPR, **not passed, too few weeks**

`escalation_score_raw` has been stored since S90 (end of August). Only **6 ISO weeks** overlap the GPR file.

| GPR series | Spearman ρ (weekly means) | One-sided p | GPR lagged one week: ρ / p |
|---|---|---|---|
| GPRD (total) | 0.657 | 0.078 | −0.500 / 0.80 |
| GPRD_THREAT | 0.714 | 0.055 | 0.100 / 0.44 |
| GPRD_ACT | −0.543 | 0.87 | −0.600 / 0.86 |

The test needs p < 0.05, and it is not met. With n = 6, the test can barely detect anything, so this result is **inconclusive**. It is not a negative finding.

Added on 2026-10-12, after the result: part G is re-run unchanged once at least 12 overlapping weeks exist, which will be around mid-November. Nothing else about part G changes.

## What the order item carries forward

1. **A new forecast in the prompt.**
   - The report states a probability for a defined event, using the ICD 203 bands. Example event: SPY 7-day change ≤ −1.0%, from the verifier's stored value, window in UTC.
   - The event, the source and a fallback source are written down before the forecast, following Metaculus.
   - It is scored with the Brier score and the BSS against climatology, plus a reliability table, plus DM/HLN on weekly means.
   - The decision waits for at least 8 forward weeks.
2. **Part G re-run** at 12 weeks or more, on the same plan.
3. **The direction label.** The skill check that R60 shipped stays as it is until 1 replaces it.
