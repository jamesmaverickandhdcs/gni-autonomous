# HANDOFF S76 -> S77
DATE: 2026-07-18 | HEAD: `6db7267` + close commits (verify ls-remote) | MODEL: Fable 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S75-3 IN BOOK; R-S76-1/2/3 pending below).
Contract: docs/CONTRACT.md (unchanged). 4 commits + 2 James-SQL.

## 1. STATE (<=10 lines)
CRED-PRIOR CLOSED+CERTIFIED `d71c60c` + SQL: seed 0.75 -> 0.5 (Laplace prior at 0/0); 3 fossil
  rows reset; /health board screenshot-certified, proven sources rank by earned score.
GPVS-NUMBERS CLOSED+CERTIFIED `62cd872`+`6db7267`: two systems byte-proven -- /predictions reads
  debate_predictions (MAD verifier, accurate = market fell >=2%); /patterns + /history read
  prediction_outcomes (GPVS outcome_verifier). C1 fixed null-denominator (nulls counted as wrong);
  C2 relabeled /predictions to MAD Debate Predictions + MATERIALIZED badges, /history to
  "report outcomes". NEW F20 BASELINE: 43%/48% (was 38%/42%, deflated).
CRED-TOTAL run to ground: 39 rows uniform gpvs_total=102 = Jul 16 11:56 pre-fix fossils
  (calc predates becbf45 by 2h). Fixed writer has NEVER fired -- gate is stochastic (see traps).
RULES-APPEND closed `89f6007`. TRANS-COUNT-CERT still parked -- no post-8eed829 Intelligence run yet.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `89f6007` | R-S75-1/2/3 appended | grep 3 + tail |
| `d71c60c` | CRED-PRIOR: seed 0.75->0.5 both sites | grep 0 hits 0.75 |
| SQL 1 | 3 fossil 0/0 rows -> 0.5 | GROUP BY: 0.5\|3 only |
| `62cd872` | C1 /patterns: 3d/7d denominators exclude null direction_correct | build 40/40; live 43/48 |
| `6db7267` | C2 relabels /predictions + /history | 3-page screenshot cert |
| SQL 2 | pipeline_runs COUNT(*) = 466 (all types); route filters pipeline_type='main' -> 111 tile TRUE | route read |
| ORACLE-FIX | TRANS-COUNT oracle = GNI Intelligence Pipeline wf (not MAD); print = 'Stage 2 (Deduplication): X -> Y articles' w/ unicode arrow | wf grep main.py:36 |
| Writer B | fires iff get_pipeline_run_count() (ALL types, 466) % 10 == 0 AT a main run -- stochastic ~1-in-10 mains | supabase_saver:434 + main.py:249 |
| judge() | MATERIALIZED_AT=-2.0 / NOT_MATERIALIZED_AT=-1.0; between = inconclusive | verifier:37-38 |
| F-EMA-COPY born | /patterns claims 1.1x/0.9x EMA; bytes = 0.7*old+0.3*factor(1.5/1.0/0.7), W-14 magnitude re-tiered | source_weights:135-155 |
| WEIGHT-PRIOR born | weights board topped by 1.00 seeds (breaking defense, dfrlab) over earned; EMA-owned, may be by-design | screenshot |
| CRLF | working copy is CRLF; a1 anchor with \n failed count=0, EOL-derived retry PATCHED | transcript |

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| RULES-APPEND | R-S76-1/2/3 below + commit (landing gate) | tail docs/GNI_RULES.md | James | - |
| TRANS-COUNT-CERT | first post-`8eed829` Intelligence run: grep 'Stage \[0-9\]\|Deduplication' vs DB total_after_dedup; monotonic | gh run list wf "GNI Intelligence Pipeline" -L1 | - | V(bytes) |
| CRED-TOTAL-WATCH | writer B fire (stochastic): watch CI for 'Updating source credibility scores' print, then SQL GROUP BY gpvs_total -- expect spread, not uniform 102 | gh log grep | - | V(bytes) |
| WEIGHT-PRIOR | 1.00 weight seeds outrank earned; EMA path owns weight -- read seed_roster_weights + ruling | read source_weights seeding | James | V(eyes) |
| GATE-DESIGN | credibility+health checks on stochastic %10 gate of a 3-writer counter; D-11 adjacent | SWOT w/ D-11 | James | V(bytes) |
| F20-CERT | close vs NEW 43%/48% baseline (38/42 stale, was null-deflated) | /correlations growth check | - | V(cert) |
| GT5-T-WATCH | 1wk grounding digest before T=2 (~Jul 24) | digest read | James | - |
| FED-DOE-WATCH | lineage decay; grep next 2-3 MAD verdicts | gh run view grep | - | V(S74) |
| FT-GAP-B-CERT | next real AUTO-ACTIVATED line | trace read | - | V(tests) |
| SUBPAGE-TRUTH | 7-LAYER SWOT session; riders now: avgQ label, F-EMA-COPY, 'prediction' word convention, /predictions residual GPVS copy (info box + footer + '52 correct' tile), Phase-narrative provenance, D-2, F1, F3 | SWOT session | James | V(S70+S76) |
| F22 | /debate withheld-coaching badge | frontend LOW | James | V(S73) |
| D-11 | escalation recalibration SWOT (+ GATE-DESIGN) | POST-CLIFF | James | V(S74) |
| DEAD-COLS | unread selects | leads | - | B |
| J-RULINGS | J-4 probe, J-7 scorer (Aug 9); J-1 sunsets post-cliff | - | James | - |
| OC-A ~Jul 24 / CERT ~Aug 2 / U-AUG9 keyfile / CLIFF-CODE+L-CLIFF Aug 16 (Lens opener SOON, D-8 first) | unchanged | - | James | - |
| K-WATCH-NS / SAN-DEAD / CENSUS-2 / K-CAND / YAKE-KM / DEAD-PILLAR / L4-COUNT / F-CASE / F-KEY / SOLV-6 / SRC-EXPAND / U-W / I-WATCH / A-VLOG / SRC-PHI / GT-6(banked) | unchanged | - | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| TRANS-COUNT live behavior | patched, no post-patch run yet | TRANS-COUNT-CERT |
| Fixed writer B live output (per-source totals) | code read only, never fired | CRED-TOTAL-WATCH |
| WEIGHT-PRIOR: 1.0 seed vs earned range = bug or design | screenshot only | WEIGHT-PRIOR ruling |
| debate verifier run cadence / backlog state (/patterns says 'backlogged, will backfill') | copy claim, unread | next verifier read |
| Fed/DoE lineage decay | designed, unobserved | FED-DOE-WATCH |
| T=3 threshold evidence | one storm sample | GT5-T-WATCH |

## 5. TRAPS (<=8 lines)
- Working copy is CRLF: multi-line patch anchors MUST derive nl from file bytes (R-S76-1).
  Single-line anchors immune. Failed assert = zero bytes written -- safe, but build/commit after
  a failed assert runs on the UNPATCHED tree (S76 did exactly this once; harmless, watch for it).
- TRANS-COUNT oracle prints use 'Stage N (Name):' + unicode arrow -- grep 'Stage [0-9]' or
  'Deduplication', never 'Stage 2:' (S75 paraphrase, matches nothing).
- 39 uniform gpvs_total=102 rows are honest fossils until writer B fires -- don't re-flag.
- 466 vs 111: pipeline_runs holds 3 run types; tile/route filter main. Both numbers true.
- /predictions '52 correct' + 'How GPVS works' box = residual copy, ruled to SUBPAGE-TRUTH, not bugs.
- Old inflated dedup fossils + funnel default-True flags + graph triple-.eq: all still deliberate (S75).

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `6db7267`+close commits TREE CLEAN -- CRED-PRIOR certified (0.5 prior), GPVS-NUMBERS certified (two systems; 43/48 new baseline), CRED-TOTAL = fossils, writer B stochastic never-fired
TOP3 = RULES-APPEND (R-S76-1/2/3), TRANS-COUNT-CERT (first post-8eed829 Intelligence run), CRED-TOTAL-WATCH (writer B fire print)
DEADLINE = GT5-T-WATCH ~Jul 24 / OC-A ~Jul 24 / CERT ~Aug 2 / keyfile Aug 9 / Groq cliff Aug 16 (L-CLIFF Lens opener SOON, D-8 first)
TRAP = CRLF anchors (derive EOL); oracle grep 'Deduplication' not 'Stage 2:'; uniform-102 rows are fossils; 466 vs 111 both true
FIRST MOVE = ls-remote + git status; then gh run list wf "GNI Intelligence Pipeline" -L1 -- any new ID is post-patch by construction

## 7. POINTERS (<=5 lines)
Two systems: /predictions <- debate_predictions <- debate_prediction_verifier.py (judge:86, thresholds:37); /patterns+/history <- prediction_outcomes <- outcome_verifier.py.
Writer B gate: main.py:249-252; counter: supabase_saver.py:434 (ALL types).
C1 seam: about/patterns/page.tsx valid3d/valid7d filters. C2 seams: predictions/page.tsx:56-57+badges; history/page.tsx:129.
EMA truth: source_weights.py:135-155 (0.7/0.3 blend, factors 1.5/1.0/0.7).

---
RULES APPEND for docs/GNI_RULES.md (at S77 open, landing gate):
R-S76-1: Multi-line patch anchors must derive the newline from the target file's own bytes
  (nl = CRLF if in file else LF) -- hardcoded \n silently matches zero on CRLF working copies.
  Single-line anchors are immune. (C1 first attempt: a1 count 0, zero bytes written.)
R-S76-2: A handoff oracle spec must record the exact workflow name AND the print format as
  bytes, not paraphrase -- 'Stage 2: X -> Y' matched nothing because the real print is
  'Stage 2 (Deduplication): X -> Y articles' in a different workflow. Grep the phenomenon,
  not the report of it.
R-S76-3: A uniform denominator across rows with varying numerators is arithmetically
  impossible from a per-item counting loop -- treat it as an instant fossil-or-bug tell.
  (39 sources, wins 28-70, every total exactly 102 = pre-fix global-count fossils.)

DIARY S76 (<=10 lines):
The session that found the second system. A seed that outranked every earned score confessed
to disagreeing with its own model's prior -- one constant, one SQL, and the trust board tells
the truth. A uniform 102 in forty rows turned out to be arithmetic's way of shouting fossil;
the fixed writer, we learned, rolls dice it doesn't know it holds. Then the prediction pages
split under the bytes: two verifiers, two tables, one word stretched over both -- the math bug
fixed by lunch, the false GPVS flag lowered by night, and honest percentages rose five points
just by refusing to count silence as failure. One patch died of the wrong newline and taught
us to ask the file how it ends its lines. Four commits, two SQLs, three certs, two watches
with real oracles. The board is smaller and truer than we found it. Fist bump.
