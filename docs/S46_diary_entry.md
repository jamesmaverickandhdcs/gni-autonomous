# Diary -- S46 (2026-06-21)

The day the 429 finally got cured for real, and MAD learned to think like a senior analyst.

We came in with two S46 phases already shipped (token metering, Bull de-bias) and a fresh
data-integrity bug discovered the night before. By the end we had five commits on main and
the next session's hardest problem already designed.

**Morning -- the false-neutral fix.** BEV showed the bug was worse than estimated: the
`mad_succeeded` gate leaked Arbitrator-only failures into the quality scorer and the IEEE
prediction data, corrupting it for months. We typed a `mad_arb_failed` flag as the single
source of truth, closed the leaky gate with a veto, added an integrity canary (an assumption
turned into a runtime assertion), made the dashboard honest (INCOMPLETE, not fake NEUTRAL),
backfilled 7 historical false-neutrals, and proved it 16/16 offline. Shipped 460ce84.

**Midday -- the rate governor, finally the real cure.** The history was humbling: we'd
"solved" the 429 four times across S13-S26, but every clean run was just a quiet-news morning
and every failure a stressed quota. Sleep-tuning never cured it -- calm news did, and we kept
crediting the sleeps. So this time we ran a LIVE 429 probe on James's real key and learned
the truth: the binding signal is `x-ratelimit-reset-tokens` (~56s), not the coarse
`retry-after` (4s); the key is 12K TPM standard; and one MAD run is ~2x the per-minute budget.
We built a pure header-aware governor that waits the real token-reset window, took control
with max_retries=0, closed the body-429 gap, kept transient resilience. 30/30 offline. Then
a CRITICAL Iran/Hormuz storm hit production and the governor waited 45/55/46s through three
429s and the Arbitrator completed bearish 0.83 -- the exact scenario that failed the day
before. The cure works. Shipped c40a5c2.

**Afternoon -- the consultant bug, and James's redefinition.** Fact-checking a live debate,
we caught a consultant hallucinating "the VP is Kamala Harris" (it's Vance -- the agent was
right) and the Bull capitulating. BEV found the literal cause: every consultant was TOLD to
"correct errors FIRST." James reframed the whole architecture: agents AND consultants on one
senior G+T+F hidden-pattern foundation, each consultant an EQUAL-RANK same-lens
insight-developer (no corrector role, no authority gradient). We drafted all 11 prompts to a
scratch file for word-by-word review, James approved, we wired them with the JSON schema
byte-identical and a Tier-1 grounding rule added. 31/31 offline; first live cron ran clean.
Shipped bb280a4.

**Evening -- the quota block, and the bookkeeping lie.** A second MAD got quota-blocked at
12:22. Chasing it, we found the real culprit wasn't adaptive burning Groq -- adaptive runs on
Cerebras and burns ZERO Groq, but it was logging a phantom 6175 Groq tokens that polluted the
shared budget. We zeroed the phantom log (kept the row for the dashboards). Then we fixed the
cron drift (moved off :00 to :13/:43/:58) -- though the BEV corrected our shared assumption that
spacing would help quota (it doesn't -- the bucket is per-UTC-day). Shipped ef3f9bf and b27474e.

**The two things we DIDN'T pretend to solve.** Real MAD now costs ~48-65K/run (Commit 3
enlarged the prompts); two of them may not fit the daily budget, and the quota gate's stale
7433 estimate has been hiding that by 6.5x. And the prompt-QUALITY of Commit 3 can only be
judged by reading a real transcript, which we haven't yet. Both honestly parked.

**The close.** James named the next move himself, and it's the elegant one: split the two MAD
crons across two separate Groq accounts so each gets its own 100K pool -- the budget constraint
dissolves at the root. Banked as the S47 top priority, with the three make-or-break checks.

A day where verify-first earned its keep at least five times -- the leaky gate, the probe-vs-docs,
the sacred-MAD trap, the cron-offset trap, and Opus 4.8 misreading a diff. The discipline held.
