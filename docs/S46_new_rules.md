# GNI Rules -- new/affirmed in S46 (append to registry)

> Assign GNI-R-NNN numbers per the live registry's next-available sequence. Text below is
> the rule content; renumber to match the registry on commit.

## R-S46-1 -- Protections guilty until BEV'd
Before any fix, the BEV must explicitly answer: "What is SUPPOSED to protect against the bad
case, and have I CONFIRMED it actually does?" -- not merely "does my fix work." Claude's
mechanism guesses are usually right; protection / blast-radius / "already-handled" guesses are
usually too optimistic. When you assume a gate/guard exists, BEV the gate before trusting it.
(Born from the leaky `mad_succeeded` gate that corrupted prediction data for months while
"running fine.")

## R-S46-2 -- Move assumptions into code as runtime assertions
Every load-bearing assumption should live as a runtime assertion that shouts on violation, not
as a fact remembered between sessions -- so a fresh/amnesiac Claude cannot silently re-break it.
Example shipped: `_assert_mad_integrity` fires if `mad_succeeded && mad_arb_failed` co-occur.
Next target: the stale `PIPELINE_COSTS['gni_mad']=7433` should assert when real metered MAD
cost diverges from the estimate.

## R-S46-3 -- Tag every claim verified-vs-assumed
In any analysis, explicitly mark each claim as verified (read in the live code this session)
or assumed (reasoning/memory). This lets the operator aim BEV at the soft spots. Trust bands:
Claude-verified-this-session ~90-95% (never 100%); unverified estimates ~50-60%; earlier-model
unread code ~30-40%; memory summaries ~40-50%.

## R-S46-4 -- Model-change re-audit ritual
On any model change (new session OR new version), prior verifications partially reset. Re-read
the project with fresh eyes before resuming -- a stronger model earns its value by re-examining
guards an earlier model wrote past. A version upgrade is a free high-value re-audit, not
overhead.

## R-S46-5 -- Honor the token-reset, not retry-after, on token-limited 429s
Groq's `retry-after` (coarse, ~4s) tells you when you may make a request; `x-ratelimit-reset-
tokens` (~56s) tells you when the TPM bucket actually refills. For a token-limited 429, wait
the token-reset window -- retrying on the 4s retry-after fires into a near-empty bucket and
re-429s. (Established by live probe; built into `mad_rate_governor.compute_wait_from_headers`.)

## R-S46-6 -- Governor owns all 429 waits (max_retries=0)
The Groq SDK's internal retries honor only retry-after (capped 60s) and fire into empty buckets
during token storms -- counterproductive. Set `Groq(max_retries=0)` so the rate governor is the
single source of wait-truth. Compensate by handling transient non-429 errors (5xx/timeout/conn)
with one backoff retry in the governor so resilience isn't lost.

## R-S46-7 -- Adaptive is Cerebras-only; never log it as Groq
Adaptive runs on Cerebras (zero Groq, no Groq fallback in production). It must log
`tokens_used=0` for Groq accounting. `get_today_usage()` sums tokens_used across ALL pipelines
unfiltered, so any phantom Groq charge on a Cerebras run pollutes the shared Groq ceiling and
can starve the real scheduled MAD. Keep the activity row (dashboards read it); zero the tokens.

## R-S46-8 -- Cron spacing does not raise daily quota (per-UTC-day bucket)
`usage_date = now(UTC).date()` -- both daily runs land in the same per-UTC-calendar-day bucket
regardless of intra-day spacing. Re-spacing crons buys PREDICTABILITY (less GHA top-of-hour
drift) and reduces collision with storms, NOT daily headroom. To raise effective headroom, use
separate accounts (separate pools), not separate times.

## R-S46-9 -- Sacred is not free: a sacred run can breach the hard cap
Marking a pipeline sacred (always-permitted) means it runs even above the safe ceiling. Before
making anything sacred, confirm its real cost cannot breach `TPD_HARD_LIMIT`. Two sacred MADs
(~96-130K real) would breach the 100K hard cap -- sacred-MAD is unsafe without a dedicated pool.

## R-S46-10 -- Off-:00 cron offsets fight GHA scheduler drift
GitHub Actions delays top-of-hour (`:00`) scheduled jobs under load. Schedule heavy crons at
odd minutes (e.g. :13/:43/:58) to reduce observed drift. When moving a cron, update any
`github.event.schedule == '...'` literal that gates a dependent job (e.g. verify-outcomes), or
that job silently stops; and keep MAD inside its GNI-R-122 protection window.

## AFFIRMED (existing rules that bit us again this session)
- LENS-010 quota isolation: separate KEYS on the SAME account share the pool -- useless. Only
  separate ACCOUNTS (different Gmail) give separate 100K TPD. (`GROQ_API_KEY_2` removed in S46.)
- LR-101: patch anchors pure ASCII only.
- W2: py_compile before every commit.
- GNI-R-110: MAD runs after pipeline with a clean TPM window; handshake-gated.
- GNI-R-122: adaptive-suppression protection windows around the pipeline runs.
