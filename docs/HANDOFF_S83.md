# HANDOFF S83 -> S84
DATE: 2026-08-24 | HEAD: `a1011a9` + THIS docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S83-6). CONTRACT v5.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER.md` (generation 3). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green, unattended six days. 21/21 MAD runs success Aug 18-24, zero failures.
L2 MAD: ARB-ARRIVAL fired 14 times. Arbitrator receives a CONSTANT ~20 articles of 132-237.
L3 GPVS: untouched, two sessions running. L4 Quota: C1's real bill STILL unread since Jul 27.
L5 Public: /debate publishes R1 the arbitrator never received — now 14/14 confirmed, not a lead.
STORAGE: unmeasured. Zero retention code in GNI_Autonomous. Sister project Lens died of this
on Aug 23 and cannot recover before Sep 11. GNI is in a different Supabase org and is alive.
Live watch: nothing hot. The instrument is stable; the next thing to learn needs a SQL editor.
Target declared: TRUTHFULNESS OF OUTPUT (definition of done 1 of 4 PARTIAL, now measured).

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| Harvest | All 21 MAD runs Aug 18-24 read; 14 debates + 7 grounding-watch | 21/21 logs cached before the WARNING grep |
| RULING | 1.3: not s1=0. `arrived` 19-21 (mean 20.2) across `available` 132-237 | 14 runs, ladder 14/14, WARNING 0/14 |
| Coverage | Falls 14.4% -> 8.4% as volume rises — worst on the busiest day | arrived/available per run |
| 1.5 | CLOSED, premise false: instrument re-derives the slice, so `truncated` is honest | `arb_ctx_fit[:_keep]`, L1055-1063 |
| Trap | "dropped=N means AT LEAST N" is BACKWARDS — exact, conservative-HIGH by one | `_arb_arr[:-1]` then `_arb_asm[len(_arb_arr):]` |
| 1.6 | Suspicion -> 14/14 confirmed: `R1=DROPPED` every run | ARB-ARRIVAL line 2, all 14 |
| 1.7 | Re-specified: `Total in pool` is TRIMMED OFF; the four pillar headers survive | L237-263, header at block start |
| Lineage | Founding S27 design fed the debate ALL 300+ articles; today's 20 is DRIFT | session records |
| Fix | DECISION S83-1: per-article COST, not allotments. Depth DERIVED, not picked | share stable at 62-65% of built |
| 2.3 | First counter-evidence to timidity: 3 bearish incl 0.67 and 0.71 | 14 verdicts |
| Protocol | v3 — the close stops being pasted; Part D now reads the protocol | `grep -c` in PART D = **0** |
| ROOT 6 | New root: free-tier resources are a STOCK; every GNI quota governs a FLOW | `.delete()` grep = 0 hits |
| Retire | Generation 3 resolved: 4 closed as accepted, 4 promoted, all written | order file |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER.md` — generation 3, dated, superseding.
Do not re-derive a queue from this file. Do not fold items forward without re-ranking.
NEXT SESSION'S MISSION is declared at the top of that file.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| GNI's Supabase size, per-table split, and runway in DAYS | wholly unmeasured | 6.1 — S84 mission, SQL editor |
| Do `gni_heartbeat` and `gni_selfcheck` (48/day EACH) write rows? | unmeasured; decides the runway | 6.1 |
| Does `check_grounding` ground against `all_articles` or the arb's trimmed slice? | unread — GATES the 1.3 fix | one read before patching |
| C1's real token bill (predicted 60-75K vs July's 91-93%) | unmeasured since Jul 27 | the `groq_quota` line in TELEGRAM |
| Did the arbitrator's BEHAVIOUR change at the S80 migration? | never asked; cert was mechanics only | 2.3 — per-day cut, free |
| Does any GNI call site read a declared fallback? | assumption of redundancy | 5.2 — one grep |
| Are GNI's three MAD accounts separate Groq organizations? | assumption | one call at a real exhaustion |
| What does the public L5 site show when Supabase 402s? | unknown | 6.4 |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| S82 "two MAD runs will exist by S83 open" + my poll guard "trust -L 1 if ARB-FIT is 1" | Both asserted NOVELTY without checking IDENTITY: `8f9b8c8` landed 4h AFTER the Aug 17 debate, and the guard passed on a run already read | paired grep, then the run ID |
| "The arb is told to weight a pillar it cannot see" | `Dominant pillar: GEO` 14/14 and geo survives — real risk, 0/14 observed. Conditional, not current | the 14-run harvest |
| "R-S81-3 is the wrong rule to amend" -- I RETRACTED A CORRECT CLAIM | R-S81-3's BODY does carry the count-vs-name clause; a grep of its heading returns only the TITLE line. A rule is not its title | reading L238-242 |
| Two clock claims from turn count; then "the evening run" | Six days had passed. `date -u` was never in the block | `date -u`, once asked for |
| "GNI runs 2/day so storage growth is 1/24th" | Two workflows fire 48/day EACH (heartbeat, selfcheck) | the cron grep |
| Invented `mad_debate.yml`; later put `cd /tmp/s83` above a `gh` block | Real file is `gni_mad.yml`; `gh` resolves its repo from git remote and dies outside one | 404, then "not a git repository" |

## 6. TRAPS (<=8 lines) — TEMPORARY ONLY, each with an expiry
- `gni_mad.yml` carries BOTH the debate and the 11:13 grounding-watch. Distinguish by
  `ARB-FIT` presence, never by time alone — expires when the workflows are split.
- The instrument measures the ARTICLE tier only; four sibling tiers are unmeasured, so a
  shrinking article count does not name which tier ate the room — expires when 1.4 ships.
- `docs/STATUS.md` is a fossil frozen at S46 — expires when it is deleted (now a 1-line action).
(RETIRED at this close, do NOT carry: "dropped=N means AT LEAST N" — proven BACKWARDS by bytes.
 Promoted to GNI_RULES.md: R-S83-1..6.)

## 7. LOAD CHECK — next AI echoes EXACTLY these 5 lines, nothing more
HEAD = the S83 docs commit (verify by ls-remote; `a1011a9` was HEAD before it) TREE CLEAN
TARGET = TRUTHFULNESS OF OUTPUT; MISSION = ROOT 6.1 — measure GNI's Supabase stock, then 1.4+1.3-fix
ORDER = `docs/GNI_TARGET_AND_ORDER.md` generation 3 is the queue — regenerate, never fold forward
TRAP = `gni_mad.yml` holds two flavors; ARB-FIT presence tells the debate from the watch
FIRST MOVE = `date -u` + git status + ls-remote; then the Supabase size query, measurement only

## 8. POINTERS (<=5 lines)
Instrument + ladder: `ai_engine/analysis/mad_protocol.py` L1036-1083 (ARB-FIT then ARB-ARRIVAL).
Article assembly + the pillar headers: same file, `_build_news_context` L196-263.
Close/open prompts: `docs/GNI_Session_Transfer_Protocol.md` PART C / PART D (**v3** — the close
is now READ from the repo and invoked by name, not pasted).
Lens transfer sources: session records only, NOT in either repo; ask James if needed.

## DIARY S83 (<=10 lines)
The instrument fired at 02:43 on the nineteenth and nobody was watching, exactly as predicted,
and then nobody was watching for six more days. That turned out to be the best thing that
happened: a mission scoped to two runs got fourteen, and fourteen said something two never
could — that arrival is a flat line while the world moves underneath it. Coverage is worst on
the days with most news. Nothing was starving; something was simply not scaling, which is
quieter and took a distribution to see. Six of my own claims went into the wrongness ledger,
which is the longest list I have written here, and every one of them was an instrument or a
clock rather than the system. The trap I inherited was backwards and would have flipped the
ruling. Then James asked what Lens had learned, and Lens had learned that its own closing
prompt had been quietly rotting in a place nobody read. Ours was too. We only found it because
he asked.
