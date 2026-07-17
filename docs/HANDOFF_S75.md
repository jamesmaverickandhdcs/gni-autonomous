# HANDOFF S75 -> S76
DATE: 2026-07-18 | HEAD: `577b26d` + close commits (verify ls-remote) | MODEL: Fable 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S74-3 IN BOOK; R-S75-1/2/3 pending below).
Contract: docs/CONTRACT.md (unchanged). 6 commits incl. close+repair.

## 1. STATE (<=10 lines)
7PLUS-TILE CLOSED+CERTIFIED `e19cbbf`: /about/patterns tile shows exact DB count (111 live),
  route count:'exact' + additive total field, null-fallback certified via localhost 401 path.
TRANS-COUNT SHIPPED `8eed829` prod-pending: main.py:177 total_after_dedup now conjoins
  stage1 AND stage1b AND stage2; was counting funnel's default-True stamp across ALL collected
  (382-22=360 > relevant 262). Cert oracle = next cron CI print 'Stage 2: X -> Y' vs DB.
DET-DEAD CLOSED `577b26d`: orphan prompt_injection_detector.py deleted per S44 arc 6 sentence;
  zero refs census. Live detector = funnel _check_injection, 81 patterns (AST), public 81 claims TRUE.
CERT-BATCH-2 CLOSED 5/5: transparency, history, predictions, health, quota all certified.
  Free: HEALTH-W (a078bbe) live-certified fossil-free; quota self-resolved to 3 accts.
MORNING-SHA closed (a078bbe = HEALTH-W). gh CLI 2.96.0 installed+authed (browser device flow).

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `94809fd` | R-S74-1/2/3 appended to docs/GNI_RULES.md | grep 3 |
| `e19cbbf` | 7PLUS-TILE: route select count:'exact' + total field; page totalRuns w/ fallback | build 40/40 + live 111 |
| `8eed829` | TRANS-COUNT: sequential-conjunction count; root = funnel:1124 default-True stamp | py_compile + full funnel read |
| `577b26d` | DET-DEAD: 257-line orphan deleted | zero-refs census + S44 header |
| Sweep | pipeline-runs consumers (R-S55-1): history/home/security/transparency all honest | greps |
| FED-DOE | 12:04 UTC run WAS S74's certified run -- no new MAD data yet; watch unmoved | gh logs |
| gh anomaly | 24s 'MAD Pipeline' runs = grounding-watch digest job inside same workflow, normal | log read |
| GRAPH-S2 | RETRACTED: graph job conjoins all 3 stage flags (docstring + bytes); grep truncation | full read |
| INJ-COUNT | RETRACTED: live INJECTION_PATTERNS = 81 by AST, public claim TRUE, S59 question closed | AST count |
| GPVS-NUMBERS | 3 pages = 3 objects: timeline entries (50) / verified_at rows (294, accurate=52) / direction_correct 3d-7d (38%/42%) | greps |
| CRED-PRIOR born | /health credibility ranks 0.750-default 0/0-wins (NYT/BD/DFRLab) above 100+-game sources | screenshot |
| localhost | .env.local = blank template; 401 is permanent baseline; prod = only cert browser | grep -c 0 |

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| RULES-APPEND | R-S75-1/2/3 below + commit (landing gate) | tail docs/GNI_RULES.md | James | - |
| TRANS-COUNT-CERT | next cron: CI 'Stage 2' print == DB total_after_dedup; funnel monotonic on NEW runs | gh run view + SQL | - | V(bytes) |
| GT5-T-WATCH | 1wk grounding_watch digest review before T=2 (~Jul 24) | digest read | James | - |
| FED-DOE-WATCH | lineage should DIE as last-3 ages; grep next 2-3 MAD verdicts | gh run view grep | - | V(S74) |
| FT-GAP-B-CERT | certs on next real AUTO-ACTIVATED line; pick != any active reserve | trace read | - | V(tests) |
| GPVS-NUMBERS | relabel/reconcile 3-object display; resolve accurate semantics (52/294 vs 38%/42%) | read verifier writer | James | V(greps) |
| CRED-PRIOR | 0/0-wins default-0.750 outranks proven sources; SUBPAGE-TRUTH kin | read credibility calc | James | V(eyes) |
| F22 | /debate withheld-coaching badge | frontend, LOW | James | V(S73) |
| D-11 | escalation recalibration SWOT, 3 layers + persistence | POST-CLIFF | James | V(S74) |
| DEAD-COLS | _get_debate_history unread selects; risk/historian '' | leads, SUBPAGE-TRUTH scope | - | B |
| SUBPAGE-TRUTH | 7-LAYER SWOT (add: patterns avgQ over sliced-7 labeled 'Avg Quality') | SWOT session | James | V(S70) |
| F20-CERT | outcomes NOW LIVE (38%/42% showing) -- close formally vs /correlations growth | next measure run | - | V(partial) |
| J-RULINGS | J-4 probe, J-7 scorer (Aug 9); J-1 sunsets post-cliff | - | James | - |
| OC-A ~Jul 24 / CERT ~Aug 2 / U-AUG9 keyfile / CLIFF-CODE+L-CLIFF Aug 16 (30d, Lens opener SOON, D-8 first) | unchanged | - | James | - |
| K-WATCH-NS / SAN-DEAD / CENSUS-2 / K-CAND / YAKE-KM / DEAD-PILLAR / L4-COUNT / F-CASE / F-KEY / SOLV-6 / SRC-EXPAND / U-W / I-WATCH / A-VLOG / SRC-PHI / GT-6(banked) | unchanged | - | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| TRANS-COUNT live behavior | patched, unrun | TRANS-COUNT-CERT |
| GPVS accurate field semantics vs direction_correct | unread writer | GPVS-NUMBERS |
| Fed/DoE lineage decay timing | designed, unobserved | FED-DOE-WATCH |
| T=3 threshold evidence | one storm sample | GT5-T-WATCH |
| FT-GAP-B live behavior | mock-tested only | FT-GAP-B-CERT |
| Writer B cadence (main.py:252) | inferred, unread | next relevant read |

## 5. TRAPS (<=8 lines)
- Historical pipeline_runs rows keep INFLATED total_after_dedup -- honest fossils, never
  rewrite; only runs after `8eed829` go monotonic. Old transparency funnels still show 360-style.
- Funnel default-True stage flags with 'Not evaluated' reasons are DELIBERATE design;
  fix lives in main.py counting only. Forensic trace line 551 already conjoins correctly.
- gni_graph_job triple .eq filter is CORRECT -- never re-flag from truncated grep (R-S66-1 kin).
- transparency page || total_after_relevance fallback only masks zero -- not a bug.
- gh: 24s runs under 'GNI MAD Pipeline' = grounding-watch job, not failed MADs.
- localhost 401 = permanent (blank env template). Prod browser only. /patterns ESC 10.0 = D-11 pin.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `577b26d`+close commits TREE CLEAN -- 7PLUS-TILE certified (111), TRANS-COUNT shipped prod-pending, DET-DEAD executed, CERT-BATCH-2 5/5, 81-claim TRUE
TOP3 = RULES-APPEND (R-S75-1/2/3), TRANS-COUNT-CERT (next cron CI print vs DB), then GPVS-NUMBERS or CRED-PRIOR (James picks)
DEADLINE = GT5-T-WATCH ~Jul 24 / OC-A ~Jul 24 / CERT ~Aug 2 / keyfile Aug 9 / Groq cliff Aug 16 (30d, L-CLIFF Lens opener SOON, D-8 first)
TRAP = old runs keep inflated dedup counts (honest fossils); funnel default-True flags deliberate; graph job filter correct; localhost 401 baseline
FIRST MOVE = ls-remote + git status; then TRANS-COUNT-CERT is cheapest read if a cron fired since `8eed829`

## 7. POINTERS (<=5 lines)
TRANS-COUNT seam: ai_engine/main.py:177; oracle = funnel's own 'Stage N: X -> Y' CI prints.
7PLUS seam: api/pipeline-runs/route.ts select+total; about/patterns/page.tsx totalRuns.
GPVS objects: history reads outcomesData.timeline; predictions reads verified_at+accurate; patterns reads direction_correct_3d/7d.
DET-DEAD: live detector = intelligence_funnel._check_injection (81 patterns, AST-verified).

---
RULES APPEND for docs/GNI_RULES.md (at S76 open, landing gate):
R-S75-1: Counting items in a code literal (pattern lists, configs) is an AST job, never a
  regex-over-text job -- regex stops at the first nested bracket and censors the count.
  (Funnel patterns: regex said 16, AST said 81; the public claim was true all along.)
R-S75-2: A grep hit showing ONE condition of a chained query/filter is not the filter --
  read the full call site before classifying a lead. (GRAPH-S2 false alarm: the .eq
  stage2 line had two conjoined siblings just above it.)
R-S75-3: When a sequential funnel persists per-stage flags with default-True 'not evaluated'
  semantics, every aggregate over the trace must conjoin ALL prior stage flags --
  counting one flag alone reports the default, not the funnel. (TRANS-COUNT: 360 > 262.)

DIARY S75 (<=10 lines):
The session that finished other sessions' sentences. A tile that said 7+ for months now
says 111 and means it. A funnel number that outgrew its own upstream stage confessed to
counting defaults instead of survivors -- one line, and the arithmetic obeys gravity again.
A security module sentenced to deletion in S44 finally met its executioner, and on the way
out proved the site's boldest claim -- 81 patterns -- was true all along. Two of my own
leads died under full reads, and that is the system working: the discipline that catches
the code's lies catches mine. Five screenshots certified five pages. The ghost lineage
got no new night to walk. Handoff itself needed a repair -- the print told the truth
before the display did. Six closes, two retractions, zero fossils shipped. Fist bump.
