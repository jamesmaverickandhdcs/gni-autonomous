# HANDOFF S87 -> S88
DATE: 2026-08-29 | HEAD: `30020a9` + THIS docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S87-7). CONTRACT v7
(UNCHANGED this close — carry `CONTRACT_S85.md` forward). **Protocol v7** — PART D gained
step 8, ANALYTICAL STANCE; the old step 8 is now step 9.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S87.md` (generation 7). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green. `available` 226 on `33180919784`.
L2 MAD: `228634c` certified at S86; ROOT 1 closing, 1.11 open. Boundary now pinned 39-41.
L3 GPVS: untouched, six sessions running. L4 Quota: C1's real bill STILL unread since Jul 27.
L5 Public: publishes CRITICAL 10.0 every run while the instrument computed 19. `/debate`
  still publishes R1; F14 unresolved; "4 pipelines" wrong in 6 places.
STORAGE: 113/500 MB — **shared with Project Lens** (four `lens_*` tables in the same project),
  so every runway figure includes another system's growth. Backup: NONE.
SCHEDULE: free-tier lateness is a measured PROPERTY, not an event (R-S87-6). Count by RUN ID.
  Pipeline and MAD drift independently; spacing was 13 min on Aug 28 against 30 by design.
Target: TRUTHFULNESS OF OUTPUT. ROOT 8 stays top; 1.11's re-rank trigger did NOT fire.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| 8.2 CERT | `4b220ab` meets all four pre-registered predictions | row 2026-08-28 21:13:16Z |
| 8.2 proof | `base_total 14 · diversity 3 · combo 2 · raw 19 · final 10 · gate null` | same row |
| Control | the 14:22Z row (pre-commit) is null on all five fields | same query |
| 8.3 RULED | Fix-2 replayed = 192/192 CRITICAL, identical to production | `design_bench` |
| 8.3 also | actor-tier 0 runs changed; rupture-tier 187/192 | same bench |
| ROOT 8 core | uncapped 10.3-26.8, median 19.2; every published value 10.0 | 192 runs |
| Why | funnel pre-selects the 22 most escalatory; absolute threshold cannot measure it | R-S87-1 |
| Corpus | `pipeline_articles` starts 2026-05-24; crisis started February — one regime only | SQL |
| Replay | scorer is deterministic; `tools/replay_scorer.py` IMPORTS it, never re-implements | `31c1906` |
| Bench | `tools/design_bench.py` recomputes the graveyard every run | `30020a9` |
| 2.3 | escalation monthly medians 15.1/12.1/12.9/14.1, combo 5->7 in Aug, bearish 94->17% | replay |
| 2.3 ⇒ | tension ROSE in August while bearishness FELL; both external explanations die | same |
| Polarity | `ceasefire` scores as escalation, fires 50.3% | `GEO_SIGNALS` L18 |
| Silence | 19 keywords never fire; FIN 15 of them — the system never broke | 192 runs |
| Schedule | 133 runs since `b27474e`: median late 243/177/61 min by month, ZERO missed | `gh run list` |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S87.md` — generation 7, dated, superseding.
Do not re-derive a queue from this file. Do not fold items forward without re-ranking.
NEXT SESSION'S MISSION is declared at the top of that file.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| What causes the 4-month verdict slide? | external causes ELIMINATED | 2.3 — internal only now |
| Does `_high_escalation` EVER go False in production? | 0/6, and now no natural trigger | 8.5 |
| Is `bool(mad_bull_case)` still leaking past the veto? | docstring vs chain disagree | 1.8 — read L275-295 |
| What is the VALUE of `GROQ_MODEL_FALLBACK`? | never read | do not wire before reading |
| Does 2.1's clause 2 (LABELED coverage) trigger B? | unmeasured | the only thing keeping 2.1 open |
| C1's real token bill | unmeasured since Jul 27 | the `groq_quota` TELEGRAM line |
| How much of the 113 MB is Lens, not GNI? | never split | 6.6 |
| Do S69 flags F2/F3/F8/F9/F12-F15 still fire live? | unaudited since Jul | 9.5 |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| "`score_breakdown` may already be in the `full_analysis` blob for months" | 0 of 191 rows. `main.py` copied 3 of the 7 returned fields; the rest died at the merge | one SQL count |
| "Cert will land on the next MAD run" | `main.py` runs under `gni_pipeline.yml` only. MAD never touches it | grep of workflows |
| "Drift is growing and unstable" | It is SHRINKING: 243 -> 177 -> 61 min median, zero missed in 67 days, cause named in `b27474e` | 133-run harvest |
| "base >= 10 in ~90% of runs" | 64%. Combo and diversity are doing real work in the other third; March's "combos are dead code" was also false | replay n=191 |
| "Dropping actor words, or scoring only rupture words, will separate the runs" | actor-tier changed 0 runs; rupture-tier still 187/192 CRITICAL. Wrong axis twice | `design_bench` |
| Asserted 42 unique item IDs in the order before grepping; it is 43 | The pre-registered count was off by one — the assert did its job | close step 5 grep |

## 6. TRAPS (<=8 lines) — TEMPORARY ONLY, each with an expiry
- NEW (first carry): pipeline and MAD drift independently and their spacing was 13 min on
  Aug 28 against 30 by design. If the order inverts, MAD debates a stale article set and
  nothing raises. Expires after 14 days of measured spacing, or when a guard lands.
(PROMOTED at this close: R-S87-1..7, which absorbed all three carried traps —
 `_arb_asm` denominator -> R-S87-7 with 7.1 and 7.4; MSYS `grep --include` -> R-S87-5(b);
 the "schedule moved, cause unknown" trap -> R-S87-6, and RETIRED as a trap because it was
 never an event: `b27474e` names the cause in its own commit subject.)

## 7. LOAD CHECK — next AI echoes EXACTLY these 5 lines, nothing more
HEAD = the S87 docs commit (verify by ls-remote; `30020a9` was HEAD before it) TREE CLEAN
TARGET = TRUTHFULNESS OF OUTPUT; MISSION = ship 8.6 (publish the uncapped magnitude), then 8.7 (polarity)
ORDER = `docs/GNI_TARGET_AND_ORDER_S87.md` (highest number = live) is the queue — regenerate, never fold forward
GATE = CONTRACT v7 `LINEAGE:` on every lettered proposal; Protocol v7 PART D step 8 ANALYTICAL STANCE
FIRST MOVE = `date -u` + git status + ls-remote; then `python tools/design_bench.py` before any scorer opinion

## 8. POINTERS (<=5 lines)
**ROOT 8: run `python tools/design_bench.py` BEFORE proposing any scorer design.** It carries the
graveyard of falsified designs and recomputes it every run; reading about them is optional.
`escalation_scorer.py` (191) — lists L8-40, `CRITICAL_COMBOS` L42, PHI-003 L110-125, breakdown
L130, return L153-169. Merge site `main.py:306-314`. Writer `supabase_saver.py:174` (one insert).
Corpus `pipeline_articles` (title+summary+stage4_selected). Prompts: Protocol PART C / PART D.

## DIARY S87 (<=10 lines)
Eight of my claims died today and not one of them died to an argument. They died to counts:
one SQL, one grep of the workflows, one 133-run harvest, one replay. Twice I proposed a fix
axis with real confidence and the bench answered in three seconds that it changed nothing --
first the actor words, then the rupture words -- and both times I had reasoned carefully and
been wrong in the same way, tuning weights on a set somebody else had already chosen. The
lesson I want to keep is not humility, it is plumbing: a five-month-old design survived
because nothing could test it in under a week, and it died the hour a test existed. So the
right output of a session like this is not a better paragraph in the register, it is a file in
`tools/` that argues back. James asked why I was announcing things the record already held,
and he was right to; the labels in Protocol v7 step 8d exist because of that question.
