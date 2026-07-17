# HANDOFF S74 -> S75
DATE: 2026-07-17 | HEAD: `a783385` + close commit (verify ls-remote) | MODEL: Fable 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S73-2 IN BOOK; R-S74-1/2/3 pending below).
Contract: docs/CONTRACT.md (unchanged). NOTE: GNI_RULES.md MOVED to docs/ this session. 6 commits.

## 1. STATE (<=10 lines)
GT5-CERT PASSED LIVE: evening MAD (12:04 UTC, checkout a783385, Iran storm) printed
  GATED c1_bear 5 / GATED c2_swan 5 + "GT-5 save-time grounding: bull=2 bear=0 bs=3 ost=3 (8)".
  DB: report 27ef3938 mad_grounding_hits = structured JSON (kind/span/location per case). CERTIFIED.
F23 CLOSED+CERTIFIED `4d7db66`: patterns page read scores from pipeline_runs which NEVER had
  the columns (3 phantom interface fields incl sentiment); fix = FK join to reports. Live: real Q, 8.8 avg.
F24 -> D-11 REGISTERED `cc2a438`: escalation_scorer 3-layer saturation (109/110 = 10.0);
  June Option B never executed, no queue row existed (R-S69-2 disease). SWOT post-cliff.
FT-GAP-B SHIPPED `a783385`: auto-activate excludes already-active reserves (double-voice guard),
  all-busy falls back LOUD; roster order documented as priority. Tests 3/3, prod-pending.
RULES moved to docs/ `130a3ae` (census clean); R-S73-1/2 appended `a17b135`; D-9 re-verified 1/1/1.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `a17b135` | R-S73-1/2 appended (root path at the time) | grep 2 |
| `130a3ae` | GNI_RULES.md -> docs/ (100% rename; only doc-prose consumers) | git rename |
| `4d7db66` | F23: route select joins reports(esc,quality,sentiment); page reads run.reports.*; avg over non-null only, N/A honest | build 40/40 + browser |
| `cc2a438` | D-11 born in DEBT_REGISTER (D-10 existed Mar 23 -- assert caught my next-free-ID guess, LR-102) | register tail |
| `a783385` | FT-GAP-B: busy-set exclusion + DOUBLE-VOICE fallback + docstring truth | 3/3 mock tests, py_compile |
| SQL | escalation dist 109x10.0 + 1x5.0 (gate's lone firing); sentiment 93B/12N/5Bu NOT pinned | queries |
| Logs | Morning MAD (05:29) checkout a078bbe = pre-GT5 state, NULL correct; evening = a783385 full GT5 | checkout SHAs |
| Browser | /patterns certified (real ESC 10.0 rows = D-11's pin, real Q, Bearish badges via join) | screenshot |
| Digest | Grounding Watch 7d: 253 cons / 65 arb hits, 15/15 runs -- GT5's workload quantified | Telegram |
| Quota | Morning acct 84,150 (99% of 85K safe); today showed 2 accts pre-evening-cron (self-resolves) | /quota |

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| RULES-APPEND | R-S74-1/2/3 below + commit (landing gate) | tail docs/GNI_RULES.md | James | - |
| GT5-T-WATCH | 1wk grounding_watch digest review before T=2 (~Jul 24) | digest read | James | - |
| FED-DOE-WATCH | Fed/DoE lineage should DIE as last-3 ages (alive tonight in Ostrich) | grep next 2-3 MAD verdicts | - | V(S74) |
| FT-GAP-B-CERT | certs on next real AUTO-ACTIVATED line; verify pick != any active reserve | trace read | - | V(tests) |
| MORNING-SHA | identify a078bbe: `git log --oneline -1 a078bbe` (footnote, 1 min) | that command | - | B |
| 7PLUS-TILE | patterns "Pipeline Runs 7+" = runs.length after slice(0,7) under "Total" caption (R-S71-2 kin) | fix w/ real count or honest label | James | V(bytes) |
| F22 | /debate withheld-coaching badge | frontend, LOW | James | V(S73) |
| D-11 | escalation recalibration SWOT session, 3 layers + persistence | POST-CLIFF | James | V(S74) |
| DET-DEAD | next window item; RE-CHECK prompt_injection_detector.py imports in funnel/ first | grep imports | James | B |
| DEAD-COLS | _get_debate_history unread selects; risk/historian '' | leads, SUBPAGE-TRUTH scope | - | B |
| SUBPAGE-TRUTH | 7-LAYER SWOT vs philosophies; hydration ext + D-2 + F3; historical_correlations accretion | SWOT session | James | V(S70) |
| CERT-BATCH-2 | James picks 5 routes | screenshots | James | - |
| F20-CERT | correlation-engine firing -> /correlations grows | next measure run | - | V |
| J-RULINGS | J-4 probe, J-7 scorer (Aug 9); J-1 sunsets post-cliff | - | James | - |
| OC-A ~Jul 24 / CERT ~Aug 2 / U-AUG9 keyfile / CLIFF-CODE+L-CLIFF Aug 16 (30d, Lens opener SOON, D-8 first) | unchanged | - | James | - |
| K-WATCH-NS / SAN-DEAD / CENSUS-2 / K-CAND / YAKE-KM / DEAD-PILLAR / L4-COUNT / F-CASE / F-KEY / SOLV-6 / SRC-EXPAND / U-W / I-WATCH / A-VLOG / SRC-PHI / GT-6(banked) | unchanged | - | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| a078bbe identity (morning cron checkout, pre-GT5) | benign, unidentified | MORNING-SHA |
| Fed/DoE lineage decay timing (last-3 aging) | designed, unobserved | FED-DOE-WATCH |
| T=3 threshold on tonight's evidence (c1/c2 gated at 5 hits each) | one storm sample | GT5-T-WATCH |
| FT-GAP-B live behavior | mock-tested only | FT-GAP-B-CERT |
| D-10 (Mar staging checker) extinct? | likely | if ever relevant |
| Writer B cadence (main.py:252) | inferred, unread | next relevant read |

## 5. TRAPS (<=8 lines)
- GNI_RULES.md is at docs/ NOW -- root path greps return nothing; not a deletion.
- arb raw vs _gated split DELIBERATE, never merge; SEAM 3 observe-only RATIFIED --
  tonight's arb hits (65/7d digest, Fed/DoE in verdict) are EXPECTED, not GT5 failure.
- Pre-GT5 NULL grounding rows = honest unknown, history includes them. Correct.
- FT-GAP-B: roster order is LOAD-BEARING (R-S63-1 webhook numbers) -- exclusion picks
  around it, NEVER reorders; DOUBLE-VOICE fallback is declared-by-design, not a bug.
- /patterns ESC 10.0 rows are REAL DB values -- that's D-11's pinned instrument, not F23 regressing.
- Paste-display can swallow heredoc tails while the script ran whole -- trust the PATCHED print.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `a783385`+close commit TREE CLEAN -- GT5-CERT PASSED LIVE (gates+score+DB), F23 closed certified, D-11 born, FT-GAP-B shipped, rules at docs/
TOP3 = RULES-APPEND (R-S74-1/2/3), FED-DOE-WATCH grep next MAD verdict, then DET-DEAD or 7PLUS-TILE (James picks)
DEADLINE = GT5-T-WATCH ~Jul 24 / OC-A ~Jul 24 / CERT ~Aug 2 / keyfile Aug 9 / Groq cliff Aug 16 (30d, L-CLIFF Lens opener SOON, D-8 first)
TRAP = rules file at docs/ now; SEAM 3 arb hits expected not failure; FT-GAP-B never reorders roster; /patterns 10.0 = D-11 not F23
FIRST MOVE = ls-remote + git status (expect close commit CLEAN); then FED-DOE-WATCH is cheapest read if a MAD has fired

## 7. POINTERS (<=5 lines)
FT-GAP-B seam: source_health_monitor.py _auto_activate_reserve (busy-set + avail + DOUBLE-VOICE).
F23 join: api/pipeline-runs/route.ts select string; about/patterns/page.tsx interface + avgQ + renders.
D-11 evidence: escalation_scorer.py caps/diversity/combos + PHI-003 gate; DEBT_REGISTER S74 appends.
GT-5 log line format: "GT-5 save-time grounding: bull=N ..." in run-mad step 5; checkout SHA in step 2.

---
RULES APPEND for docs/GNI_RULES.md (at S75 open, landing gate):
R-S74-1: Registry appends assert ID-uniqueness against FILE BYTES before writing -- the next
  free ID is a read result, never a memory. (D-10 collision: assert caught a duplicate the
  handoff-informed guess would have shipped.)
R-S74-2: A frontend interface declaring DB fields is a HYPOTHESIS -- verify every field against
  information_schema before trusting any page's type. (F23: three phantom fields rendered
  fossils for weeks; the March sprint doc warned this verbatim.)
R-S74-3: Certifying shipped code via CI logs starts at the run's CHECKOUT SHA -- a missing
  feature line proves nothing until you know which commit executed. (Morning NULL was
  pre-GT5 state, not a failed seam.)

DIARY S74 (<=10 lines):
The session that read margins. A screenshot's edge said ESC never moves -- one query later,
109 of 110 reports confessed the gauge was welded at ten, and a fix half-shipped in June had
laundered its missing half into "done." We wrote the debt back where it can't hide. The
patterns page turned out to be reading a table that never held what it displayed; the join
took an evening, the fossils took months to notice. Then the reserve picker learned not to
give one feed two voices. And at 19:04 the machine we built yesterday breathed on camera in
a real Iran storm: two consultants gated, eight hits scored to the row, the loop that fed
ghosts to tomorrow's debate cut live. The Fed/DoE ghost still walks -- but now it's dated,
counted, and starving. Six commits, three censuses, one collision caught by its own assert. 👊
