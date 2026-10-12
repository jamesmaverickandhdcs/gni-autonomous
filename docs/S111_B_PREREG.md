# S111 item (b): pre-registered test plan

Written on 2026-10-12, 03:35 (UTC+7), before the CSVs from S111_EXPORT7.sql were seen.
Nothing below changes after the data arrives. If a step has to change, the change gets its own
dated line, with the reason.

## Question

Can GNI's existing output be turned into a probability forecast of a market downside? The forecast must beat climatology out of sample. If it cannot, the redesign starts from the prompt and asks for a new forecast. If it can, the redesign starts from calibrating the output GNI already has.

Guidelines:
- WMO JWGFVR, and the JMA verification seminar: the Brier score, and the Brier skill score against climatology.
- Murphy 1993: verify the forecast against the matching observation.
- Diebold–Mariano 1995 with Harvey–Leybourne–Newbold 1997: compare the losses, allowing for serial correlation.
- Metaculus resolution criteria: fix the event, the source and the window in advance.
- Caldara & Iacoviello (AER 2022): the GPR index, used as the matching observation for escalation.

## Known bias, stated before the test

Event E was chosen after S111_EVIDENCE6 had shown four AUCs. It is the event with the highest AUC (0.628), so an in-sample or cross-validated result on this data is biased upward.

Only part F, the forward test on outcomes measured after the freeze, is free of that bias. Parts A to E decide whether the forward test is worth running. They are not proof of skill.

## Test

| | Fixed choice |
|---|---|
| Event E | SPY change over the 7-day verification window ≤ −1.0%. Source: `prediction_outcomes.spy_change_7d`, as the verifier stores it. |
| Rows | Every verified outcome with a non-null `spy_change_7d` and `sentiment_score`. Neutral calls are included, because the score is continuous. |
| Forecast | Logistic regression P(E) = σ(a + b·x), with x = −sentiment_score. Nothing else is entered as an input. |
| Reference | Climatology: the base rate of E in the training fold. |
| Cross-validation | Leave one ISO week out. Folds are blocked by the ISO week of `reports.created_at`, so reports from one week never sit in both the training and the test fold. |
| Score | Brier score of each out-of-fold forecast; BSS = 1 − BS_model / BS_climatology. |
| Significance | The per-row loss differential d = (f_clim − o)² − (f_model − o)², averaged per ISO week. A one-sided test that the mean is > 0 uses a HAC variance with 1 lag (adjacent weeks share 7-day windows) and the HLN small-sample correction, against Student t with W−1 degrees of freedom, where W = number of weeks. Implementation: `statsmodels.tsa.stattools.diebold_mariano_test(lags=1, harvey_adj=True, horizon=2)`, with the one-sided p taken from its statistic. |
| Calibration | A reliability table: 5 bins of the out-of-fold forecast, with the mean forecast and the observed frequency in each bin. |

### Pass criteria (cross-validation, parts A to E)

- BSS > 0, **and**
- the DM/HLN one-sided p-value < 0.05.

If both hold, the model's coefficients are frozen and part F runs. If either fails, the redesign starts from the prompt.

### Part F: forward test (the clean test)

Fit (a, b) on all rows measured up to 2026-10-12 and write the values into the order item. Score them, unchanged, on every outcome measured after 2026-10-12, using the same BSS and the same DM/HLN test.

The decision is taken after at least 8 new ISO weeks. That takes about 2 months at the current rate.

## Escalation versus GPR (part G)

| | Fixed choice |
|---|---|
| Data | The Caldara–Iacoviello daily "Recent" GPR file, as downloaded by James on 2026-10-12. Columns used: GPRD, the total, and the Threats and Acts series if present. |
| GNI series | The daily mean of `escalation_score_raw` across reports (the raw magnitude, uncapped). Days with no raw value are dropped. |
| Comparison | Spearman correlation of the ISO-week means of the GNI series and GPRD, on the weeks both cover. Also the same correlation with GPRD lagged one week. |
| Pass | Spearman ρ > 0, with a one-sided p < 0.05. |

The weekly averaging is what keeps the observations close to independent.

The capped `escalation_score` is not tested: 262 of 263 reports sit at the cap, so it has no variance to correlate.

## Dated changes

- 2026-10-12 03:41 - file-reading fix: the GPR date is read from the file's `date` column. `DAY`
  holds integers such as 20261002. The test itself is unchanged.
- 2026-10-12 03:42 - parts A-E run: FAIL (BSS 0.0029, p 0.31). Part G: not passed on 6 weeks,
  and the result is inconclusive. Part G will be re-run unchanged once 12 or more overlapping weeks exist. See S111_B_RESULTS.md.
