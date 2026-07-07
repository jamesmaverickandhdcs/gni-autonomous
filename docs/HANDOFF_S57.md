# HANDOFF S57 -> S58
DATE: 2026-07-07 | HEAD: `04acf45` (verify ls-remote) | MODEL: Fable 5 (full session)
Read ONCE. Standing rules: GNI_RULES.md by ID (now current through R-S57-1). Contract: docs/CONTRACT.md.
Do not re-read old audits/handoffs unless a queue item points there.

## 1. STATE (<=10 lines)
L1 Pipeline: healthy, 2x SUCCESS Jul-6 (~17K tokens/run). Reserves live-proven; NYT ACTIVE for Stimson
  (James picked via fixed alert menu -- I3-r CLOSED). Breaking Defense self-recovered (flaky bot-wall).
L2 MAD: morning clean (100% quality); evening Arbitrator 429-starves terminally in storms, quarantine
  holds (mad_arb_failed=True, excluded). Solver overshoots ~10%: est 84986, real 92-94K per MAD.
L3 GPVS: verifier fossil-proofed (guard + 18 SQL resets). ~122 future-dated rows pending maturity.
L4 Quota: 4 accounts now: morning / evening / not_mad / GROQ_TEST_ONLY (NEW, experiments, secret set).
L5 Public: tech-tier cadence fixed (Ars+RoW->48h, Krebs->120h) -- live-proof pending next cron.
Repo hygiene: .gitignore had UTF-16LE corruption (repaired); rules registry committed to R-S57-1;
  probe committed; O1/O4/F2 closed. mad_reasoning 429 fossils rewritten honest (11 rows).
Live watch: Iran-US CRITICAL 10/10 ongoing.

## 2. DELTA (<=15 lines)
| Commit | What | Proof |
|--------|------|-------|
| `05d8842` | I3-b: HTML-escape class closed -- fix-suggester plain-text+double-confess, notifier 10 escapes | 5x PATCHED, py_compile, live admin test 200 |
| `0dce28e` | I2-b: fossil guard in verifier + 18 judged fossils SQL-reset to fossil_error_row | dry-run, SQL census 18->18 marked, 0 left |
| `c45b5a2`+`abab1e0` | I3-c: Ars+RoW->review/48h, Krebs->opinion/120h + tier-map comment synced + 8->6 fossil | 4x PATCHED + 2-edit follow-up |
| `13aed42` | U3 probe committed to repo root (S57 rebuild, 306 lines) | on disk + tracked |
| `c566fc6` | O1: rules R-S55-1..5 + R-S56-1 + R-S57-1 committed; S55_appends absorbed+deleted; dryrun kept | tail -6 shows rules |
| `04acf45` | .gitignore UTF-16LE fragment (PowerShell >>) stripped; check_*.py restored; exports/ ACTUALLY ignored | file=ASCII, 0 NUL/CR, ?? gone |
Root causes: (1) reserve-alert 967h shadow = unescaped 403 reason poisoning its own HTML send (S56 fix
live-proven this session -- menu arrived, James picked NYT). (2) probe file never existed on disk --
S56 built in chat only; rebuilt byte-faithful from archive, FIXTURE_USER fresh-frozen (3259 chars, no
prior runs so freeze-from-now is valid). (3) exports/ "ignored" in c566fc6 was FALSE -- check-ignore
lied because .gitignore line 55 was UTF-16 NUL-interleaved; repaired in 04acf45.
No-commit closures: F2 phantom (page already says 21); O4 census 11/11 already flagged, text rewritten
honest via SQL; U1+U3 fire+U2+I1 consolidated to Aug 9 by James's ruling.

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| U-AUG9 | MARATHON, fixed order: keyfile check -> U3 llama baseline x3 FIRST -> U1 decide -> candidate probes+max_tokens sweep -> U2 migrate ~13 sites (secrets trio GROQ_MODEL/GROQ_MAD_MODEL/GROQ_MODEL_FALLBACK exist, values unknown) -> I1 (solver recal, Arb reserve, <95K, scorer, grounding gate) -> methodology copy sweep. NOTHING else that day. Cliff Aug 16. | notepad ../groq_probe_key.txt with GROQ_TEST_ONLY key | James | V(prep) |
| U-W | Weekly July: Groq lineup glance (2 min) | Groq models page | James | - |
| F1 | validation-log stale dates + auto-populate claim -- wording steer FIRST GATE of S58; verifier now EXISTS so honest copy changed | James picks A loud / B quiet / C own words | James | V |
| F3 | Q3/Q4 roadmap badges read overdue -- product call | James: bump / reword / leave | James | V |
| I2-w | Wire verifier into cron (2-line patch near gni_pipeline.yml:81) after 1-2 more trusted manual runs + browser-check predictions page | manual run --apply | James | B |
| I3-c-p | Live-proof tier fix: next cron expect Tech 3-4/4, Ars/RoW/Krebs passing | read next run log | - | V(built) B(live) |
| W9 | Watch-item: alert path when TWO sources down simultaneously (06:47 Jul-6 double-fail printed Could not send; 14:02 single-fail sent clean -- pre/post-fix timing OR real multi-fail bug) | tripwire: next double-down day | - | 50% |
| O3 | Kill BOM in intelligence_funnel.py -> live pattern count -> sweep BOTH "81" consumers (homepage:1008 + developer-hub ~line 82 "81-pattern") | kill BOM | James | L |
| I4 | Rolling 7-day integrity check on not_mad | design | James | B |
| UNK | Arb terminal-fail TPD-vs-TPM: read x-ratelimit headers on one failed evening run | one log read | - | 80% TPD |
| UNK2 | First 180d long-horizon prediction rows: eyeball before trusting | when due | - | 60% |
| O6 | Arc C temporal pattern discovery (LAST, by design) | - | - | B |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| GROQ_MODEL / GROQ_MAD_MODEL / GROQ_MODEL_FALLBACK secret VALUES (names confirmed Jul-7) | 50% | one run log model string, or Aug 9 |
| Tech tier fix real-world yield (Krebs gaps can exceed 120h -- accepted, Bellingcat-class) | 70% | next 2-3 cron logs |
| Double-down alert path (W9) | 50% | next multi-failure day |
| Arbitrator terminal 429 = TPD vs TPM | 80% TPD | x-ratelimit headers once |
| mad_reasoning honest-text rewrite rendered OK on debate page | 90% | one browser look |

## 5. TRAPS (<=8 lines)
- Do NOT reopen: I3-b/I2-b/I3-c/O1/O4/F2/I3-r (closed this session), L4 consumers, L5 sweep, O5, O2.
- not_mad RESERVED (pipeline+I4+ArcC). GROQ_TEST_ONLY = experiments ONLY. Never MAD on either.
- Do NOT fire the probe before Aug 9 (James's ruling) and NEVER on morning/evening (each MAD alone
  burns 92-94K of its 100K pool -- probe on top starves the Arbitrator we are studying).
- FIXTURE_USER in mad_model_probe.py is FROZEN -- do not edit once any trial has fired.
- No solver recalibration before migration (R-S55-4). One calibration, inside I1.
- market_proxy_v1 verdicts are coarse directional proxies, not semantic truth.
- PowerShell >> writes UTF-16 on this machine -- never append to config files with it (R-S57-1 class).
- Line endings are per-ANCHOR facts: every patch carries LF<->CRLF fallback + confesses which hit.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `04acf45`
TOP3 = Aug 9 marathon prep (keyfile!), F1+F3 steers (S58 first gate), I2-w after trusted runs
DEADLINE = Aug 9 marathon (decide+probe+migrate+I1) / Groq cliff Aug 16
TRAP = probe waits for Aug 9, never on MAD accounts; FIXTURE frozen; PowerShell >> = UTF-16 poison
FIRST MOVE = verify HEAD via ls-remote; check next cron log for Tech 3-4/4 (I3-c live-proof); then James steers F1/F3

## 7. POINTERS (<=5 lines)
Probe harness + run flags: mad_model_probe.py header (repo root, committed `13aed42`).
Fossil guard: debate_prediction_verifier.py row-loop top; fossil_error_row is the quarantine marker.
Tier mechanism: rss_collector.py ~245-268 (TIER_WINDOW_HOURS, per-source "tier" field, S57 comment map).
Escape-at-boundary pattern: telegram_notifier.py (10 escapes) + code_fix_suggester._send_telegram.
F1/F3 fossil details: S55-era audit chat "Project status review and next steps" (Jul-6) -- decision-ready table.
