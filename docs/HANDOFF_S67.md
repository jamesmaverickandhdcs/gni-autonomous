# HANDOFF S67 -> S68
DATE: 2026-07-13 | HEAD: `a95bd67` + S67-close docs commits (verify ls-remote) | MODEL: Fable 5
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S67-2). Contract: docs/CONTRACT.md (unchanged).
!! TREE NOT CLEAN BY DESIGN: ai_engine/funnel/intelligence_funnel.py = uncommitted
!! RECENCY-DEAD patch, gated on K-WATCH #2 (see TRAPS).

## 1. STATE (<=10 lines)
G-TUNE CORE SHIPPED 2 days early (`19d2b10`): GT-1 dialect bucket (kind='dialect'
  reported, excluded from hit_count/grounded/RED) + GT-2 conditional alias
  expansion (10 groups, all corpus-verified) + STOP_HEADS. Selftest 10/10.
  GT-4 re-measure window OPEN.
PROMOTE-NYT CLOSED (`a95bd67`): NYT primary for Stimson slot (46d clean C4;
  Stimson = CF 403 bot-wall). Pool order untouched (R-S63-1). source_reserves
  row closed status='promoted' (inert to all readers, grep-proven).
K-WATCH #1 READ: KEY-MAP medicine confirmed, no regression ('eu' phantom dead,
  'war' 34->13, enforced-disappearance* rescue SELECTED). Instrument defect:
  trace S1-keywords caps at 3 -> match-count censored (R-S67-2).

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `19d2b10` | GT-1+GT-2 shadow: dialect bucket + alias expansion + STOP_HEADS | selftest 10/10; diff reviewed |
| `d2947e3` | CHORE-IGNORE: *_GNI_Forensic_Trace_*.xlsx ignored | one line |
| `a95bd67` | PROMOTE-NYT roster swap, collector only | syntax OK; pushed 6h before 0537 run |
| DB edit | source_reserves Stimson row -> 'promoted' (1 row) | update returned 1; all readers filter known statuses |
| tree (uncommitted) | RECENCY-DEAD: art->article + bare except made loud ([RECENCY-WARN]) | ast.parse OK; diff 4+/3- |
| RECENCY widened | L795 NameError also killed S38 escalation logic + PHI-003 thin-cap, since S38 | bytes L769-815 |
| FT-GAP diagnosis COMPLETE | 3 defects, one disease (raw measured, fresh yield never): collector L505 fallthrough raw_count==0 not collected==0; C2 L706 raw>0 not yield>0; C3 L648 pool[0] unranked | all byte-read |
| GT-1 spec defect | DIALECT_EXACT lowercase bigrams unreachable today; kept for G-GAP-1, selftest >=2 | executor probe |
| K-WATCH #1 detail | S1 pass ~flat (storm corpus, not comparable); sel score 15.1->13.2 deflation = medicine; new candidates 'who'/strike*/1-kw threshold | trace diff |
New rules appended to GNI_RULES.md: R-S67-1, R-S67-2

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| TRACE-READ | TOP, 4 birds: K-WATCH #2 (c4 first flight + non-storm corpus) + GT-4 digest #1 (expect Dialect line, thinned spans) + NYT slot browser-verify (R-S54-4) + RECENCY commit gate | James uploads 2 traces + digest screenshot + GH log checkout SHA | - | - |
| RECENCY-DEAD | Patch IN TREE. If K-WATCH #2 clean: stage funnel file EXPLICITLY, commit (msg claims recency+velocity+S38+PHI-003 revival), push | after TRACE-READ | James | V(patch) |
| FT-GAP-A | 2-line fix: L505 raw_count==0 -> collected==0; C2 L706 raw>0 -> yield>0. SHIFTER: after RECENCY + 1-2 run window. collected==0 also fires on all-dedup'd -- name widening in commit | write spec | James | V(diagnosis) |
| FT-GAP-B | cadence-ranked pool pick (C3 pool[0]). Data source: health history vs static field | after A proves | James | B |
| GT-3 | shared entities.py (sensor KNOWN_* + ALIAS_GROUPS + G-GAP-1 lowercase pass, anti-L-CLIFF). LAST shifter | after FT-GAP-A window | James | B |
| GT-4 | 3-5 digests post-`19d2b10`; expect high-precision residue; THEN GT-5 enforce decision | passive | James (GT-5) | - |
| L-CLIFF | Aug 16 cliff, 34d; quota 93/95%. Lens opener SOON | Lens session | James | V(scope) |
| SAN-DEAD | design fresh: score pre-sanitized text vs neutral forms | read sanitize L1108 region | James | V(diagnosis) |
| CENSUS-2 | +evidence: trace kw cap=3 censors stats (R-S67-2) | extend scratch | - | V(design) |
| K-CAND | 'who' noise / strike* polysemy / 1-kw threshold -> GT-4 review | - | James | B |
| YAKE-KM / DEAD-PILLAR / L4-COUNT / F-TILES / F-CASE / F-KEY | unchanged | James picks | James | B |
| SOLV-6 / SRC-EXPAND / OC-A (~Jul 24) / U-AUG9 (keyfile FIRST) / U-W / I-WATCH / A-VLOG | unchanged | - | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| c4 (byline/opinion) live behavior | unknown | TRACE-READ GH log |
| GT-1/2 live effect on digest profile | unknown | GT-4 digest #1 (today) |
| NYT first run as named primary + dashboard rename cosmetics | 90% self-heals | TRACE-READ browser |
| health monitor reaction to promoted slot (fresh history) | 80% cosmetic | 1-2 runs |
| Stimson browser-load (bot-wall vs removed) | 85% bot-wall | James 10s, epitaph only |
| GROQ secret values (GNI 4 + Lens 11 key names) | 50%/unknown | Aug 9 keyfile FIRST |

## 5. TRAPS (<=8 lines)
- DIRTY funnel file = RECENCY-DEAD by design: never `git restore`, never let it
  ride into another commit -- stage EXPLICITLY when its gate clears.
- SHIFTER SERIALIZATION: RECENCY-DEAD -> window -> FT-GAP-A -> window -> GT-3.
- GT-4 hit-count drop = alias+dialect noise EXITING, not integrity improving
  (specimen-1 'iranian' vanish = fix working, pre-logged).
- Multi-step code+DB commands run in PASTE ORDER (R-S67-1) -- number the gates.
- 'promoted' status inert ONLY while all source_reserves readers filter
  positively on known statuses.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `a95bd67` + S67-close docs commits (ls-remote) + DIRTY TREE BY DESIGN: funnel file = uncommitted RECENCY-DEAD patch
TOP3 = TRACE-READ (4 birds: K-WATCH #2 / GT-4 digest #1 / NYT verify / RECENCY gate), RECENCY-DEAD commit if clean, FT-GAP-A spec (strictly after RECENCY window)
DEADLINE = OC-A ~Jul 24 / Aug 9 marathon (keyfile FIRST) / Groq cliff Aug 16 (L-CLIFF Lens session SOON, quota 93/95%)
TRAP = never restore/absorb the dirty funnel file; one shifter per window (RECENCY -> FT-GAP-A -> GT-3); GT-4 hit-drop = noise exiting, not integrity improving
FIRST MOVE = ls-remote + git status (expect ONLY funnel modified); then James uploads 2 traces + digest screenshot + GH log SHA

## 7. POINTERS (<=5 lines)
Gate+aliases: ai_engine/analysis/mad_grounding_gate.py (DIALECT_*, ALIAS_GROUPS, STOP_HEADS, selftest).
Watch: ai_engine/analysis/grounding_watch.py (_split_dialect, dialect digest line).
FT-GAP: collectors/rss_collector.py L505; source_health_monitor.py L706 C2, L648 C3.
RECENCY: funnel/intelligence_funnel.py ~L795 (patched in tree), [RECENCY-WARN].
Specs: docs/GT1_SPEC.md, docs/GT2_SPEC.md (committed `19d2b10`).

---
RULES APPENDS for GNI_RULES.md:
R-S67-1: When a change spans code and DB/live state, hand over the steps as
  NUMBERED GATES with the code push explicitly first -- commands delivered
  together get executed in paste order, and paste order becomes system state.
R-S67-2: Before trusting any statistic from an instrument, verify the
  instrument's RANGE (caps, truncation, short-circuits). A metric that cannot
  move is not evidence of stability -- the trace's 3-keyword cap censored the
  match-count deflation K-WATCH was built to observe.

DIARY S67 (<=10 lines):
The session the gate learned its own dialect. The morning read proved the
KEY-MAP medicine was real -- phantoms dead, rescues selected, and the
instrument itself caught lying about match counts. Then G-TUNE landed two
days early: the fabrication digest turned out to be mostly the gate flagging
its family's vocabulary and missing every alias, so we taught it both --
dialect counted honestly in its own bucket, aliases admitted only when the
articles themselves vouch. NYT got the job it had already been doing for 46
days. One sequencing stumble (DB before push) bought six hours of exposure
and a rule. The recency bonus that died at birth now waits in the tree,
patched, for one clean trace to earn its first breath. 👊
