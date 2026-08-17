# HANDOFF S81 -> S82
DATE: 2026-08-17 (session ran Jul 25-27, closed Aug 17 after a 3-week gap) | HEAD: `43f74fc` (C1 transcript-carry) | MODEL: Opus 5 at close; Fable 5 for the Jul 25-27 build arc
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S81-8). CONTRACT v4.
**The QUEUE now lives in `docs/GNI_TARGET_AND_ORDER.md` (fixed path). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
MAD DEBATE IS ALIVE AND CERTIFIED. Five consecutive real verdicts on gpt-oss-120b
  (Jul 25 eve 0.48 / Jul 26 morn 0.53 / Jul 26 eve 0.53 / Jul 27 morn 0.52 / Aug 17 morn 0.53),
  zero 413 in all five, zero empties in the last three. E-3 fired live Jul 26.
THE ORGANISM SURVIVED THE AUG-16 CLIFF UNATTENDED: 3 weeks, no human touch, and
  `gh run list -L 40` grouped by conclusion = success 40 / failures 0 across the cliff.
TWO PATCHES SHIPPED S81: `0001f06` arb guaranteed-fit (ARB-FIT ladder, ARB_MIN_OUT 2500),
  `43f74fc` C1 transcript-carry (R2/R3 stop re-sending the article library).
S81 WAS NEVER CLOSED IN JULY — this file repairs that. Three weeks of state lived
  outside the repo, which is the largest risk this close retires.
TARGET DECLARED THIS CLOSE: TRUTHFULNESS OF OUTPUT (see the order file).

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| 0001f06 | ARB guaranteed-fit: arb ctx depth<=100, ladder drop-R1 -> R3@110w -> ctx-trim, NN-5 inside budget | greps 6/4/L1035/0; 59+/17- |
| 43f74fc | C1 transcript-carry: R2/R3 headline-only slim anchors, R3 embeds R2@150w | PATCHED 13 edits; greps 12/0/4 |
| Root cause | Arb 413 was the PROMPT side: transcript alone exceeded the 8K per-request ceiling; the L98 floor only ever guarded the answer side | Jul 25 cert log |
| Cert x5 | Real verdicts, no safe-defaults; last one (Aug 17) unwatched for 5 days | run 31991506106 |
| E-3 live | `LABELED blind_spot 2 hits` -> tg `[LOW GROUNDING -- 2 unverified span(s)]` | Jul 26 eve log + tg |
| Solver | First `status=OK` since migration (N=32 D=342 est=84986); est now conservative-high post-C1 | Jul 27 + Aug 17 logs |
| 429s | 9 per run, ALL recovered attempt 1/3, waits 46.6-60.4s (was 11-14 pre-C1) | Aug 17 log |
| OC-A | CLOSED: Copilot "AI model training" toggle Disabled on all 3 accounts (main had reverted to Enabled) | settings page, 3x |
| Sources | HRW down Jul 26 (403) -> ReliefWeb activated by digit reply -> HRW recovered Jul 27 -> auto-deactivated | tg receipts |
| Scheduler | Crons now fire 13-60 min after request, NOT the 1-3h recorded in S80 | Aug 16-17 run list |
| Lens brief | `NEXT_SESSION_BRIEF_LENS028_LCLIFF.md` written here, committed to Lens as `9b2836d` | ls-remote |
| Transfers in | `GNI_LOOPHOLE_TRANSFER_NOTES.md` (Aug 10) + `LENS_TO_GNI_TRANSFER_PACKET_II.md` (Aug 17) received from Lens | uploads |
| Rules | R-S81-1..8 appended; CONTRACT v4 (target/order separation + discovery policy) | GNI_RULES.md tail |
| Close repair | HANDOFF_S81 + GNI_TARGET_AND_ORDER born; queue no longer lives in the handoff | this commit |

## 3. QUEUE
**MOVED.** See `docs/GNI_TARGET_AND_ORDER.md` — dated, ranked, regenerated at every close.
Do not re-derive a queue from this file. Do not fold items forward without re-ranking.
NEXT SESSION'S MISSION is declared at the top of that file.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| C1's REAL token bill (est is conservative-high post-C1; predicted 60-75K vs July's 91-93K) | unmeasured | read the groq_quota line in Telegram (it is NOT in the workflow log) |
| Does anything verify what the arbitrator RECEIVED vs what was assembled for it? | unread | ROOT 1 — next session's mission |
| Are the 46-60s governor waits landing the retry inside the same TPM minute? | candidate, unread | ROOT 4.2 |
| Is GNI's per-account-day reservation model reasoning about a boundary that does not exist? | inferred from Lens | ROOT 4.3 |
| gpt-oss debate QUALITY vs the old 3.3-70b (verdict confidence sits timid at 0.48-0.53) | 5 verdicts, no judgment made | ROOT 2.1 |
| Whether GNI's three MAD accounts are separate Groq organizations (TPD isolation) | assumption | one small call at a real exhaustion |
| Keyfile rotation was due Aug 9 and did not happen | certain, unactioned | LIFECYCLE in the order file |

## 5. TRAPS (<=8 lines)
- A zero-match `--jq 'select(...)'` prints a BLANK LINE, indistinguishable from a broken filter.
  Prove the instrument saw rows (`--jq 'length'`) before reading silence as absence (R-S81-1).
- The `groq_quota` line is a TELEGRAM artifact. Grepping workflow logs for it returns nothing
  and that nothing means nothing.
- `gh run list -L1 -w "GNI MAD Pipeline"` returns the newest FLAVOR: the 11:13 grounding-watch
  (~20s) shares the workflow with the real debate (~11-15m). Pick by duration.
- 413 != 429. 413 = prompt+max_tokens over the per-request ceiling, UNRETRYABLE. Budget math first.
- ARB-FIT rides the FULL ladder on EVERY run (drop-R1, R3@110w, ctx-trim to ~5K). That is the
  design working at full stretch, not slack. Any prompt growth lands on the trim.
- Crons fire 13-60 min after request as of Aug 17. Requests: pipeline 02:13/10:13, MAD 02:43/10:43,
  grounding-watch 11:13 UTC.
- Repo mixes LF and CRLF PER FILE. Derive NL from each file's own bytes; never assert absolutely.
- Reasoning models: any small max_tokens is a starvation bomb. The 768 floor keeps calls alive,
  it does not keep them useful.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `43f74fc` TREE CLEAN -- MAD certified x5 on gpt-oss, cliff survived unattended, S81 closed late (Aug 17)
TARGET = TRUTHFULNESS OF OUTPUT; MISSION = ROOT 1 arbitrator-arrival audit + instrumentation commit
ORDER = `docs/GNI_TARGET_AND_ORDER.md` is the queue -- regenerate it at close, never fold items forward
TRAP = blank jq output != zero failures; groq_quota lives in Telegram; -L1 returns the newest MAD FLAVOR
FIRST MOVE = git status + ls-remote; then read ARB-FIT assembly at mad_protocol.py:964-998 before proposing anything

## DIARY S81 (<=10 lines)
Opened on a certification that failed honestly and closed three weeks later on one that
passed while nobody watched. The arbitrator had been dying of its own transcript -- the
budget guard we shipped in S80 protected the answer and never the question -- and the fix
was not a bigger clamp but a smaller prompt: read the library once in R1, then argue from
the debate itself. Five real verdicts followed, and E-3 said "hypothesis, not finding" in
public for the first time. Then James rested, the crons kept their own counsel, and the
Aug-16 cliff came and went without a single red run. What returns with him is a gift from
the other project: the loop-hole notes, which name why every session felt like a stranger
arriving -- no declared target, and a close prompt that grew the list by construction.
So this close is the first one that ends with an order instead of a pile.
