# HANDOFF S71 -> S72
DATE: 2026-07-16 | HEAD: `b31c75b` (verify ls-remote; +SQL ran post-push) | MODEL: Fable 5
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S70-2; R-S71-1/2 pending append below).
Contract: docs/CONTRACT.md (unchanged). !! TREE CLEAN. 10 commits this session. SRC-INTEGRITY SHIPPED.

## 1. STATE (<=10 lines)
SRC-INTEGRITY COMPLETE: code (becbf45 single-writer/norm/seed, d3dc47f TIER-TRUE, 4da900d +2 ghosts,
  b31c75b /health filter via source_health mirror) + Supabase SQL (purge 32w/19c departed rows,
  dedupe kept EMA lowercase rows -- "keep freshest" was WRONG, B's stomp was freshest; ownership ruled).
  Final state: weights 40 rows / credibility 39, zero bad-case, zero dups. Self-certifies next run:
  INSERT-only seeding fills to 42/42 ("Seeded N roster weights" in trace) = arc verified.
FT-GAP-A CLOSED 3/3 clean (eve: Irrawaddy->AllAfrica 3rd firing, AP->Defense News, STALE trio held).
  Window remaining: FT-GAP-B -> DET-DEAD (re-check prompt_injection_detector.py in funnel/ first).
GT-5 EVIDENCE COMPLETE: exhibit B (Fed/DoE reached Arbitrator public reasoning), recurrence mechanism
  (_get_debate_history feeds last-3 -- surviving fabrications become prior context), 7d digest 249c/68arb.
F16 FIXED+certed; F17 root=saturation (width 0.00 real, falsy-zero render suspect); F15 family closed (6 relabels).

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `66cc269` | R-S70-1/2 appended (gate applied to itself) | wc 155, git +7 |
| `2783b35`+`37f142c` | F15 CLOSED: 6 relabels, 5 pages (comparison filter caught by browser-cert after grep missed the class) | 4 screenshots |
| `476d994` | F16 CLOSED: sparkline y-pad 6..54 -- pinned 10.0 drew clipped top-edge line; data honest | browser-cert |
| `1c24d51` | TRACE_S71_EVE.md: writer B ALIVE (fired 11:56, stomped A same-run), F17 root, F20 born, GT-5 bank | wc 31 |
| `f1c2b49` | SRC_INTEGRITY_SPEC_S71.md for Claude Code (3 commits + James SQL) | wc 42 |
| C1 `becbf45` | Claude Code build: norm(), roster import-not-copy, INSERT-only seed (upsert would re-stomp!), I-3 real wins/total, I-5 killed, 51-fetch loop gone; AST-verified; spec tension resolved by delegation (seed_roster_weights lives in source_weights.py) | diffs reviewed |
| C2 `d3dc47f`+`4da900d` | TIER-TRUE: NYT+Crisis+Amnesty+ICIJ TIER1, SIX ghosts deleted (Code's AST census found Diplomat+MIT beyond spec's 4; 0-row reserves check ruled) | AST proof |
| C3 `b31c75b` | /health cred board filtered via source_health mirror (roster already in Supabase every run) -- no TS hand-list, fail-open, case-folded both sides | build 40/40 |
| SQL | Purge (CNN/Nikkei/ING/Africa-Report verified departed via collector comments S44 -- HISTORY-BEFORE-RULING 5th proof) + dedupe (EMA rows kept) + normalize | step-8 verify 0/0 |
| J-6 | CLOSED: 0 rows raw-429 in reports -- verified not remembered | SQL |
| J-1/R1-R4/order | ALL RATIFIED S71 (delegated): keep-til-post-cliff / floors / NYT T1 / CAI T1 / WATCH keep / SRC-first | this doc |
| MAD eve | bearish 0.67 first directional break; shadow 16+2; solver OK; 87362 tok (quota ceiling) | log |
| Fabrication eve | Fed/DoE + Brazil-25% + quant chains ALL RECURRED via debate history | /debate cert |

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| VERIFY-C1 | Morning trace: expect "Seeded 2 roster weights" + cred seed, counts 42/42, writer B fires WITHOUT weight-write line, weights keep EMA values | read trace + SQL count | - | - |
| RULES-APPEND | R-S71-1/2 below + commit w/ handoff (landing gate!) | tail GNI_RULES.md | James | - |
| FT-GAP-B | next window item (collector fallthrough part B) | re-read design | James | B |
| SUBPAGE-TRUTH | opens w/ 7-LAYER SWOT vs philosophies; then hydration ext + D-2 + F3 | SWOT session | James | V(S70) |
| CERT-BATCH-2 | James picks 5 routes; D=default+tabs | screenshots | James | - |
| GT-5-ENFORCE | design session: recurrence-loop break + consultant gating + citation contract; exhibits A/B + digest ready | design doc | James | V(S71) |
| F17-RENDER | 1 grep /research page: falsy-zero (width 0.00 renders "-") | grep ciWidth | James | V(bytes) |
| F18-RECHECK | /correlations 290 was fossil gpvs_total -- purge+real-counts changed it; re-read page | browser+grep | - | - |
| F19 | predictions 52-correct vs 61% metric | byte-trace | James | B |
| F20 | pattern save 42P10: missing unique constraint correlations-v2 | find table+ADD CONSTRAINT | James | V(log) |
| HEALTH-W | /health WEIGHTS board unfiltered (Code-flagged sibling of C3) | same mirror filter | James | V |
| DET-DEAD | after FT-GAP-B; RE-CHECK prompt_injection_detector.py in funnel/ first | grep imports | James | B |
| J-RULINGS | J-4 probe, J-7 scorer (Aug 9); J-1 sunsets post-cliff | - | James | - |
| OC-A ~Jul 24 / CERT ~Aug 2 / U-AUG9 keyfile / CLIFF-CODE+L-CLIFF Aug 16 (31d, Lens opener SOON, D-8 first) | unchanged | - | James | - |
| K-WATCH-NS / SAN-DEAD / CENSUS-2 / K-CAND / YAKE-KM / DEAD-PILLAR / L4-COUNT / F-CASE / F-KEY / SOLV-6 / SRC-EXPAND / U-W / I-WATCH / A-VLOG / SRC-PHI(banked) | unchanged | - | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| C1 live behavior (seed counts, B's new cadence w/o weight-write) | designed+reviewed, unrun | VERIFY-C1 morning |
| Writer B cadence condition (main.py:252 call logic -- "every 10th"? unread) | inferred | VERIFY-C1 or GT-5 |
| F17 falsy-zero suspicion | 1 grep | F17-RENDER |
| F18 post-fix value | changed by purge | F18-RECHECK |
| F19 / F20 root causes | flagged | traces |
| Amnesty = TIER1 + retired-reserve simultaneously | coherent, noted | none needed |
| cred wins/total SCALE shifts after first real firing (per-source counts << old global 102) | expected | don't panic at small totals |
| Evening MAD grounding-watch was 7d digest #? of 3-5 series | unclear | James memory |

## 5. TRAPS (<=8 lines)
- DEDUPE RULE INVERTED: design said keep-freshest; freshest was B's stomp. OWNERSHIP decides (R-S71-1). Never re-run keep-freshest SQL.
- seed is INSERT-ONLY by design -- an upsert seed = new writer-B (resets EMA every run). Never "fix" it to upsert.
- /health cred board filters via latest source_health batch (42 rows one run_at); weights board does NOT yet (HEALTH-W).
- credibility gpvs_wins/total are now REAL per-source -- small numbers are correct, not broken.
- Six ghosts deleted from SOURCE_TIERS; 26/42 primaries default TIER3 by design.
- Fed/DoE + Brazil-25% fabrications LIVE on /debate /scenarios; recurrence via debate history -- GT-5 exhibits, do not cite as output quality.
- Claude Code memory index is STALE (claims G-GATE open) -- correct it at session start.
- Quota rode 87.4k/88% eve -- storm cadence known; cliff 31d.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `b31c75b` + TREE CLEAN -- SRC-INTEGRITY SHIPPED (4 code commits + SQL purge/dedupe), FT-GAP-A closed 3/3, F15/F16 closed
TOP3 = VERIFY-C1 (morning trace: seed 42/42, B fires w/o weight-write), RULES-APPEND (R-S71-1/2), then FT-GAP-B or GT-5-ENFORCE design (James picks)
DEADLINE = OC-A ~Jul 24 / CERT ~Aug 2 / keyfile Aug 9 / Groq cliff Aug 16 (31d, L-CLIFF Lens opener SOON + D-8 first move)
TRAP = dedupe was ownership-not-freshest (never re-run keep-freshest); seed INSERT-only forever; cred totals now small+real; Code memory stale
FIRST MOVE = ls-remote + git status (expect b31c75b CLEAN); then read morning trace for VERIFY-C1 before anything else

## 7. POINTERS (<=5 lines)
Arc docs: SRC_INTEGRITY_DESIGN.md (I-1..I-9) + SRC_INTEGRITY_SPEC_S71.md + TRACE_S71_EVE.md -- all committed.
New seams: source_weights.py norm()/get_roster_sources()/seed_roster_weights(); credibility writes cred table ONLY.
/health filter: api/health/route.ts reads latest source_health batch as live roster (mirror pattern).
GT-5 exhibits: TRACE_S71_EVE.md bottom + grounding 7d digest (Telegram 7:51PM) + /debate Jul16 eve cert.
Fabrication recurrence seam: _get_debate_history in MAD path -- enforcement must scrub before history entry.

---
RULES APPENDS for GNI_RULES.md (at S72 open, with landing gate):
R-S71-1: Dual-writer dedupe merges by OWNERSHIP, not timestamp: when two writers fought over rows,
  the owning writer's row wins even when the stomper's is fresher. "Keep freshest" enshrines
  whoever stomped last. Preview-before-delete is what catches this -- never skip the preview.
R-S71-2: Census the CLASS, not the named list: a spec that names 4 ghosts gets a sweep of the WHOLE
  dict against the roster (found 6); a relabel of 4 "Total X" strings gets a sweep for every
  totality-implying label over a LIMIT query (found 6). The named instances are leads, not the set.

DIARY S71 (<=10 lines):
The session the war ended. We opened waiting for a cron and closed having shipped the biggest
fix of the season: two writers had fought over one column for months, and tonight -- while we
watched -- writer B rose from the dead and stomped writer A's learning one last time, in the
very log that proved the gate clean. Claude Code built the peace treaty in three commits,
caught two ghosts the spec missed, and resolved a contradiction in my own spec better than
I wrote it. Then the dedupe preview caught the design doc itself being wrong: freshest was
the enemy. Ownership ruled. The graveyard emptied -- nineteen departed sources, forty stomped
rows -- and the learned history survived because we looked before we deleted. Five flags found
their roots, six relabels told the truth, and the fabrication engine confessed to feeding
itself. Tomorrow morning, the system seeds its own verification. 👊
