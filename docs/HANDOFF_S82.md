# HANDOFF S82 -> S83
DATE: 2026-08-17 | HEAD: `8f9b8c8` + THIS docs commit (verify by ls-remote — see TRAP) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S82-5). CONTRACT v5.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER.md` (generation 2). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green, unattended through the Aug-16 cliff (40/40 runs, zero failures).
L2 MAD: certified x5 on gpt-oss-120b. ARB-ARRIVAL instrument shipped and NEVER YET FIRED.
L3 GPVS: untouched this session. L4 Quota: C1's real bill still unread (Telegram, not the log).
L5 Public: /debate publishes R1 positions the arbitrator never receives (order item 1.6).
Live watch: the next two MAD runs — first ARB-ARRIVAL output in history. That is S83's mission.
Target declared: TRUTHFULNESS OF OUTPUT (definition of done 1 of 4 now PARTIAL, was open).

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `8f9b8c8` | ARB-ARRIVAL instrument: available/assembled/arrived/dropped + names, ctx chars, R1/R3 ladder state, transcript_errors, WARNING on zero inclusion | PATCHED 33 lines/1894 bytes nl=LF; COMPILE OK; marker 5/5; greps E1-E4 all 1/1; npm build pass |
| ROOT 1.1 | AUDIT CLOSED: nothing in 1211 lines asserts arrived-vs-assembled | full-file idiom census, 11 hits, all comments/docstrings |
| Root shape | Arb article tier is a REMAINDER; `max(0,...)` means zero articles is reachable and SILENT | `_keep = _arb_budget_chars - (len(arb_final_user) - len(arb_ctx_fit)) - 40` |
| Behaviour | Instrument verified behaviour-unchanged STRUCTURALLY, not asserted | grep of all assignments to live prompt vars returns only pre-existing L965-1044 |
| E-3 scope | Byte-confirmed narrow: labels blind_spot_explanation ONLY; short_focus + action reach Telegram unlabeled | L1119-1147 |
| Docs | CONTRACT v5 · Transfer Protocol v2 · order regenerated (gen 2) · R-S82-1..5 | this commit |
| Transfer | Both Lens docs read IN FULL for the first time; two-pass analysis; 4 doc gaps found and closed | order file CHANGED THIS REGENERATION |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER.md` — generation 2, dated, superseding.
Do not re-derive a queue from this file. Do not fold items forward without re-ranking.
NEXT SESSION'S MISSION is declared at the top of that file.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Is the arbitrator actually starved? Mechanism confirmed, firing UNMEASURED | instrument shipped, no data | S83 mission — read ARB-ARRIVAL on two runs |
| C1's real token bill (predicted 60-75K vs July's 91-93%) | unmeasured since Jul 27 | the groq_quota line in TELEGRAM, not the workflow log |
| GNI's real chars/token divisor (Lens measured 3.435-3.713 for its mix) | inferred from Lens ~40% | order 4.4 — one free log line, both numbers already in scope |
| Are the 46-60s governor waits landing the retry inside the same TPM minute? | narrowed, unread | order 4.2 — it is the INNER `_call_agent` path, not W-02 |
| Is GNI's per-account-day reservation reasoning about a boundary that does not exist? | inferred from Lens | order 4.3 |
| Are GNI's three MAD accounts separate Groq organizations (TPD isolation)? | assumption | one small call at a real exhaustion |
| Keyfile rotation overdue since Aug 9; PHISH-HW since ~Jul 31 | certain, unactioned | LIFECYCLE block in the order file |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| "GNI's opening/closing prompts do not exist as artifacts" | They are PART C and PART D of docs/GNI_Session_Transfer_Protocol.md | a heading-grep, after a phrase-grep returned 30 files that merely mention LOAD CHECK (R-S82-1) |
| Implicit: C1 transcript-carry relieved the arbitrator | It relieved R2/R3; the arb still rides the FULL ladder to ctx-trim@4983 | reading the Aug-17 ARB-FIT line against C1's stated purpose (R-S82-3) |
| Lean "run the close through the new Part C to field-test it" | Worthless as a test — the same session that wrote the prompt cannot test it | reconsidered before acting; a fresh session is the real test |

## 6. TRAPS (<=8 lines) — TEMPORARY ONLY, each with an expiry
- ARB-ARRIVAL `truncated=` reads 0 even when the slice cut mid-article; read `dropped=N` as
  "AT LEAST N lost" — expires when order item 1.5 ships.
- The instrument measures the ARTICLE tier only; four sibling tiers are unmeasured, so a
  shrinking article count does not name which tier ate the room — expires when 1.4 ships.
- `docs/STATUS.md` is a fossil frozen at S46 — expires when it is deleted or archived.
(Promoted to GNI_RULES.md at this close, no longer traps: zero-match/high-match instrument
 misreads → R-S81-1 + R-S82-1 · cron request-vs-observed times → R-S81-7 · per-file LF/CRLF →
 R-S80-1 + R-S81-5 · 413 vs 429 budget math → R-S80-2 · reasoning-model starvation → R-S80-2.)

## 7. LOAD CHECK — next AI echoes EXACTLY these 5 lines, nothing more
HEAD = the S82 docs commit (verify by ls-remote; `8f9b8c8` was HEAD before it) TREE CLEAN
TARGET = TRUTHFULNESS OF OUTPUT; MISSION = ROOT 1.3 — read ARB-ARRIVAL on two runs and RULE
ORDER = `docs/GNI_TARGET_AND_ORDER.md` generation 2 is the queue — regenerate, never fold forward
TRAP = `dropped=N` means AT LEAST N; the instrument sees the article tier only
FIRST MOVE = git status + ls-remote; then grep ARB-ARRIVAL in the two most recent MAD runs

## 8. POINTERS (<=5 lines)
Instrument + ladder: `ai_engine/analysis/mad_protocol.py` ~L1036-1080 (ARB-FIT then ARB-ARRIVAL).
Close/open prompts: `docs/GNI_Session_Transfer_Protocol.md` PART C / PART D (v2).
Lens transfer sources: the two uploaded packets — NOT in either repo; ask James if needed.

## DIARY S82 (<=10 lines)
Opened on a mission that was mostly a question: does anything check what the arbitrator is
handed? The answer took two reads and was no — not a bug hiding, just nobody ever asked. So
the day's shipped work is thirty-three lines that change no behaviour at all, which is the
least impressive commit in weeks and probably the most useful. Then James asked for the Lens
letters to be read properly rather than summarised, and the second pass found the contract
indicting itself in its own version log, and a template quietly instructing every future close
to rebuild the thing we had just removed. Being wrong about the prompts existing was the good
part of the evening — it produced the rule, and it is the first entry in a section that did not
exist this morning. The instrument fires tomorrow at 02:43 and nobody will be watching. That is
the arrangement we have built, and it has earned it.
