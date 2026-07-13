# HANDOFF S68 -> S69
DATE: 2026-07-13 | HEAD: `9991c4a` (verify ls-remote) | MODEL: Fable 5
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S68-2). Contract: docs/CONTRACT.md (unchanged).
!! TREE CLEAN. RECENCY-DEAD is COMMITTED -- live from next run, observation window OPEN.

## 1. STATE (<=10 lines)
RECENCY-DEAD SHIPPED (`9991c4a`): art->article L795 + bare except made loud
  ([RECENCY-WARN]). Revives recency+velocity bonuses, S38 escalation logic,
  PHI-003 thin-cap (all dead since S38). Gates held: AST OK, build 40/40,
  explicit stage, ls-remote verified, tree clean.
TRACE-READ 4 birds DONE: morning #282 + evening #283 both on `5965204`.
  c4 CLEAN both flights (3 review kills, full L1->L4 chain). KEY-MAP zero
  regression ('eu' hits 2 morn / 10 eve -- ALL legitimate standalone-EU wave).
  NYT slot LIVE: 17/17 Healthy, fresh history. GT-4 digest #1: Dialect line
  LIVE (27 consultant / 4 arb).
CLIFF census COMPLETE: 2 hardcode landmines + doomed fallback chain (DELTA).

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `9991c4a` | RECENCY-DEAD fix, one file, 4+/3- | AST OK; 40/40; ls-remote |
| TRACE-READ | 4 birds read by bytes (2 traces, 3 CI logs, digest, dashboard) | S68 |
| c4 verdict | L1->L4 chain works live; 3 review kills over 2 flights; UNKNOWNS row closed | trace rows |
| KEY-MAP verdict | zero regression; 'who' 11-12/flight hot (feeds K-CAND) | trace census |
| R-S67-2 worse | 75/163 + 78/191 pass rows AT the 3-kw cap (~44% censored) -- CENSUS-2 evidence | trace census |
| GT-4 digest #1 | Dialect line live; headline 221/60 = 7d window mostly pre-`19d2b10`, decay expected digests #2-5; alias-family spans still in ARB HITS | GW CI log |
| FT-GAP-A spec | PASTE-READY: collector ~L502 `raw_count==0` -> `collected==0`; monitor C2 ~L706 `raw>0` -> `int(stat.get("yield",0))>0` (field name byte-confirmed) | bytes |
| Path fixes | collector = ai_engine/collectors/; monitor = ai_engine/analysis/ (S67 pointers were stale) | find |
| SAN-DEAD grounded | sanitize runs Stage 1b (L1161) BEFORE Stage 3 -> S3 scores neutralized text | bytes L1150-75 |
| CLIFF landmine 1 | funnel L1065: "llama-3.1-8b-instant" BARE hardcode in c4 L4 call, no env read | grep |
| CLIFF landmine 2 | gni_adaptive.yml:48 GROQ_MODEL hardcoded literal, not secrets ref | grep |
| CLIFF contradiction | mad_protocol.py:9 "confirmed" llama-3.3-70b vs fix_mad_model.py gpt-oss-120b; CI logs mask *** | grep |
| Quota mapping | morning acct = morning-MAD key; 1 MAD run ~90.5K = ~90.5% of daily quota (structural) | MAD log |
| Keyfile inventory | GNI: 4 GROQ key secrets + 3 model-string secrets, names banked | Settings |
New rules appended to GNI_RULES.md: R-S68-1, R-S68-2

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| TRACE-READ-2 | TOP: RECENCY first breath -- next morning trace + pipeline log: expect NO [RECENCY-WARN], live recency/velocity bonuses, selection shift = medicine | James uploads trace + log | - | - |
| FT-GAP-A | SHIFTER #2: 2-line fix, spec paste-ready (DELTA); commit msg names `collected==0` widening (all-dedup'd now falls through -- correct) | after TRACE-READ-2 clean + 1-2 run window | James | V(bytes) |
| FT-GAP-B | cadence-ranked pool pick (C3 `pool[0]` byte-confirmed unranked) | after A proves | James | V(diag) |
| GT-3 | shared entities.py (sensor KNOWN_* + ALIAS_GROUPS + G-GAP-1) -- LAST shifter | after FT-GAP-A window | James | B |
| GT-4 | digests #2-5: watch legacy fabricated counts decay + alias-family ARB spans thin; THEN GT-5 enforce decision | passive, ~18:13+drift local | James (GT-5) | - |
| CLIFF-CODE | NEW: one commit -- funnel L1065 env-read, adaptive.yml:48 secrets ref, 6-file dying-default sweep; + check gni_selfbias/gni_graph LLM env | after GT-3 or swap-day | James | V(census) |
| U-AUG9 | keyfile FIRST: resolves GROQ_MAD_MODEL contradiction + all secret values | marathon day | James | - |
| L-CLIFF | Lens opener SOON; Aug 16 = 34d; quota structural (1 MAD run = 90.5%/day) | Lens session | James | V(scope) |
| K-WATCH-NS | non-storm corpus read still owed (Hormuz storm since S67) | first quiet-day trace | - | - |
| SAN-DEAD | design session: scoring-vs-sanitize ordering options | grounded, design fresh | James | V(bytes) |
| CENSUS-2 | 3-kw cap censors ~44% of pass rows -- instrument fix design | extend scratch | - | V(evidence) |
| F-TILES | Stimson ghost tile frozen at 7/12 forever (browser-confirmed) + prior cleanup | James picks | James | V(observed) |
| SUBPAGE-IC | OPEN ARC: full integrity walk of all ~35 routes (claim real? current data? silent fail?) -- S52 fixed only its triaged subset, full census NEVER certified | 5-page read-only batches | James | B |
| K-CAND | 'who' noise / strike* polysemy / 1-kw threshold -> GT-4 review | - | James | B |
| YAKE-KM / DEAD-PILLAR / L4-COUNT / F-CASE / F-KEY | unchanged | James picks | James | B |
| SOLV-6 / SRC-EXPAND / OC-A (~Jul 24) / U-W / I-WATCH / A-VLOG | unchanged | - | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| RECENCY live behavior (first breath) | unknown | TRACE-READ-2 |
| GROQ_MAD_MODEL current value (llama-3.3-70b vs gpt-oss-120b) | 50/50 | keyfile day; CI logs mask *** |
| GROQ_MODEL / GROQ_MODEL_FALLBACK current values | unknown | keyfile day |
| Whether llama-3.1-8b-instant also dies Aug 16 (funnel L1065 + probe fallback) | assume yes | Groq deprecation page |
| Dialect-bucket decay rate | visible by digest #3? | GT-4 passive |
| gni_selfbias / gni_graph LLM usage without GROQ_MODEL injection | unchecked | CLIFF-CODE |
| Non-storm keyword profile | unknown | K-WATCH-NS |

## 5. TRAPS (<=8 lines)
- SHIFTER SERIALIZATION: RECENCY owns the window until TRACE-READ-2 is clean;
  then FT-GAP-A -> window -> FT-GAP-B/GT-3. One shifter per window.
- RECENCY selection SHIFT is the MEDICINE: recent articles outranking stale
  vs S68 traces = fix working. Do NOT diagnose as regression.
- GT-4 headline counts are 7d-window contaminated: falling numbers = legacy
  runs aging out, NOT integrity improving (pre-logged).
- Cron drift observed 2.3-3.5h this session: nominal+4h before declaring missing.
- fix_mad_model.py / fix_consultant_prompts.py are HISTORICAL scripts -- their
  instructed secret values are ~50% leads, not current state.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `9991c4a` (ls-remote) + TREE CLEAN -- RECENCY-DEAD live from next run, observation window OPEN
TOP3 = TRACE-READ-2 (RECENCY first breath: no [RECENCY-WARN] + live bonuses + selection shift = medicine), FT-GAP-A ship (spec paste-ready, strictly after RECENCY window), GT-4 decay watch
DEADLINE = OC-A ~Jul 24 / Aug 9 marathon (keyfile FIRST -- resolves GROQ_MAD_MODEL contradiction) / Groq cliff Aug 16 (CLIFF-CODE: 2 hardcode landmines censused; L-CLIFF Lens SOON)
TRAP = one shifter per window (RECENCY -> FT-GAP-A -> GT-3); RECENCY selection shift = medicine; GT-4 falling counts = window decay not integrity
FIRST MOVE = ls-remote + git status (expect CLEAN); then James uploads morning trace + pipeline log for RECENCY read

## 7. POINTERS (<=5 lines)
RECENCY: ai_engine/funnel/intelligence_funnel.py ~L795 ([RECENCY-WARN]); sanitize L883/L915/L1161.
FT-GAP-A: ai_engine/collectors/rss_collector.py ~L502; ai_engine/analysis/source_health_monitor.py C2 ~L706 (field = stat["yield"]), C3 ~L648.
CLIFF: funnel L1065 (bare hardcode); .github/workflows/gni_adaptive.yml:48; 6 default files censused in S68 DELTA.
Specs: FT-GAP-A inline in S68 DELTA; docs/GT1_SPEC.md, GT2_SPEC.md (`19d2b10`).

---
RULES APPENDS for GNI_RULES.md:
R-S68-1: A model/secret swap plan is incomplete until a BARE-HARDCODE census
  runs -- grep call-site literals and workflow YAML, not just os.getenv
  defaults. The funnel L4 call and gni_adaptive.yml both hid from the
  secrets-only view.
R-S68-2: GitHub Actions masks secret values as *** in CI logs -- a log can
  prove a secret is SET, never what it contains. Don't burn session time
  trying; only the keyfile ritual resolves values.

DIARY S68 (<=10 lines):
The session the dead code drew breath. Four birds flew home in one day --
the gate spoke its own dialect in digest #1, the classifier made its first
kills, NYT wore the badge it had already earned, and every phantom we hunted
turned out to be honest EU headlines. Then the tree's only dirty file -- the
recency bonus that died at birth in S38 -- passed its gates and shipped:
9991c4a, four lines, thirty sessions late. The cliff census found the two
landmines a secrets-only plan would have stepped on, and one structural truth
surfaced: a single MAD run eats 90% of a day's quota. One dead end (GitHub
stars out its secrets), zero regressions, tree clean. Tomorrow morning the
funnel scores time itself for the first time since S38. 👊
