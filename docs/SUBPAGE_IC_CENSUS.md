# SUBPAGE-IC CENSUS — S69 (2026-07-15) — v2, 35/35 CLOSED
Method: web_fetch shell-read 32 routes + James browser-read /alerts, /brief, /comparison + browser verifies.
Data-layer (numbers load? current?) certified ONLY where James's screenshots show it; rest = browser batches pending.

## VERDICT
- 35/35 routes alive. ZERO dead routes. Structure map (tabs/layers/links) confirmed incl. /stocks 6th Bond tab.
- Browser-certified LIVE with real data: /alerts, /brief (fresh Jul 15 12:11 PM run), /comparison, /about, /stocks.
- /brief confirms FFF (PHI-003) section rendering live. /about sprint stats live: 189 runs, 86,831+ articles,
  61% GPVS 7d accuracy, 81 patterns.

## FLAGS — open
| # | Where | Claim | Conflict / truth | Sev |
|---|-------|-------|------------------|-----|
| F1 | /developer-hub prose+card AND /about Dev Console card | "70-pattern" | /security, /about stats tile, /about/feedback, /about/devops, /methodology = 81 (S52 canonical) | TRUTH |
| F2 | /developer tile + /developer-hub prose | "21 API Endpoints" | S52 corrected a count 21→27 (`ac536dd`); resolve by BYTES: count route.ts | TRUTH |
| F3 | /source-health legend 3 states | /developer-hub "seven states"; W-AUTO code = 5-state | TRUTH |
| F4 | /methodology + /about/devops | crons "02:00/10:00 + 02:30/10:30 UTC" | Real :13/:43 since S46 | STALE |
| F5 | /methodology + /about infra | "llama-3.3-70b-versatile" / "Groq API (Llama 3)" in UI copy | 3rd landmine class → fold into CLIFF scope (CLIFF-DOC) | CLIFF |
| F6 | /methodology | "33 pages live" | Census = 35 | STALE |
| F7 | /methodology | "15 tables" | O-SEC S60 = 37 | STALE |
| F8 | /about/patterns | GPVS horizons "3 and 7 days" | Others say 7d/30d/180d; resolve by BYTES in GPVS verifier | TRUTH |
| F9 | /reports card + /validation-log | "FUTURE / Available Apr 10 vs Apr 14, 2026+" | Dates passed; GPVS live w/ 61% 7d accuracy displayed on /about. Flip to LIVE | STALE |
| F10 | /about Dev Console card, /about/feedback, /about/devops prose | "$" dropped: "proving .00/month", ".00/Month" | REAL in browser (Dev Console card). Main cost sections render "$0.00" fine. Escaping bug, targeted sweep | COSMETIC |
| F12 | /alerts log text | "Low article collection: avg 0 < 100" | avg=0 while pipeline collects 400+/run — alert math or text suspect | DATA |
| F13 | /alerts tiles | Adaptive Triggers = 0, Critical Alerts = 0 | vs adaptive runs existing + weeks of CRITICAL 10.0 escalation. Counter wiring suspect | DATA |
| F14 | /comparison AGREE banner | "Both signals point BEARISH" while MAD verdict = NEUTRAL 62% | Copy asserts false fact; AGREE logic treats NEUTRAL as agree — copy/logic mismatch | TRUTH |
| F15 | /comparison | "Total Runs 10", timeline Run #1–#10 (Jul 10–15) | 189 runs exist; unlabeled 10-row window — R-S64-1 LIMIT pattern suspect | DATA |

## RESOLVED
- F11 CLOSED: Bond tab real (browser). /stocks = 6 categories; pre-check list updated.
- F10 narrowed: not site-wide — specific prose spots only.

## PER-ROUTE
Clean (shell or browser): /, /about/quantum, /adaptive-log, /autonomy, /brief, /correlations, /debate, /health,
/history, /map, /mission-control, /model-learning(FUTURE-legit), /pattern-library(FUTURE-legit), /pillars,
/predictions, /quota, /research, /researcher, /scenarios, /security, /stocks, /transparency, /weekly-digest
Flagged: /about(F1,F5,F10), /about/devops(F4,F10), /about/feedback(F10), /about/patterns(F8), /alerts(F12,F13),
/comparison(F14,F15), /developer(F2), /developer-hub(F1,F2,F3), /methodology(F4-F7), /reports(F9),
/source-health(F3), /validation-log(F9)

## SEQUENCE (decided S69)
1. TRACE-READ-2 FIRST — Jul 15 12:11 PM run = RECENCY first breath; outranks all subpage work.
2. Byte-census batch (read-only): route.ts count → F2; GPVS horizon grep → F8; alerts/comparison page reads → F12-F15 root cause.
3. Fix commits AFTER byte-census, one family each: SUBPAGE-TRUTH (F1,F2,F3,F6,F7,F8,F14), SUBPAGE-STALE (F4,F9), F10 cosmetic. F5 → CLIFF scope.
4. Remaining data-layer browser walk: 5-page batches (pages not yet screenshot-certified).
