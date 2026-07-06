# GNI S48 -- Next-Session Brief

**Written at S47 close, 2026-06-23, for the next session (also Claude, but WITHOUT this
session's working context).**

> Read this FIRST. Then `S47_Session_Audit.md` for detail. Then -- per the model-change
> re-audit ritual -- re-read the actual MAD code with fresh eyes before touching anything.
> This brief's code claims are LEADS (~40-50%), not ground truth. James is continuity; you
> are fresh analysis; code+registry is shared memory. Say "assumed, not verified" and let
> James aim BEV at the soft spots. Claude Code is available for complex local work.

---

## WHERE WE ARE (one paragraph)

S47 shipped ONE commit, `668abeb`: the two-account MAD split (James's design). MAD's evening
cron (10:43 UTC) now runs on a SEPARATE Groq account (`GROQ_MAD_EVENING`, separate Gmail =
separate 100K pool); the morning cron (02:43 UTC) stays on `GROQ_API_KEY`. `quota_guard` is
now account-aware (new `account` column on `groq_daily_usage`, default 'morning'). It is
PRODUCTION-PROVEN: on 2026-06-23 both accounts ran the SAME UTC day -- morning 58,221 tokens,
evening 52,538 tokens with a fresh 0/85000 pool despite morning already at ~64K. The 2xMAD
budget constraint is dissolved at the root. Nothing is half-built. Real MAD cost is now
measured (~52-63K/run), superseding the stale 7433 estimate (which is still in the code).

---

## TOP PRIORITY S48 -- MAD REASONING-QUALITY UPGRADE (James wants this; analysis DONE)

**The deep analysis is already done (S47). The build is the new work.** Goal: spend the freed
headroom (real run ~55K vs 80K working target = ~25K spare per account) on HIGHER REASONING
QUALITY, in service of the 3 pillars / Freedom-from-Fear mission.

**THE KEY INSIGHT (do not re-derive -- it's measured):** MAD is NOT article-starved. Each
agent already receives UP TO 60 articles (Claude Code measured: `_build_news_context` slices
`sorted_arts[:15]` per pillar x 4 pillars). The articles inject as ONE-LINE headlines:
`[{source}] {title[:80]} (score) -- {summary[:100]}` ~190 chars each. So the agents reason
over 60 HEADLINES, not 60 summaries. **The lever is DEPTH-per-article + reasoning-length, NOT
article count.** Raising count past 60 = most tokens, least quality, risks ceiling. (R-S47-5)

**MEASURED STRUCTURE (from Claude Code, S47 -- these are ~85% reliable measurements, but the
PROMPT TEXT itself was NOT read -- re-read it before editing):**
- System prompts (tokens): SENIOR_FOUNDATION ~277 (in all 11 prompts), agents ~670-749,
  consultants ~660-690, ARB_FINAL ~1042, GROUNDING_RULE ~119, GNI_WALL ~57.
- max_tokens: R1/R2 agents 350, consultants 250, R3 agents 600, Arbitrator 600.
- 21 calls (12 agent + 8 consultant [R1+R2 only] + 1 arb). Sleeps: 15s pre-consultant, 45s
  between rounds, 90s pre-arbitrator.
- Article context per agent at full load: ~60 x ~190 chars ~= 3,000 tok.
- Metering (`_TOKEN_USAGE`) separates prompt/completion/total/calls; counts retries.

**THE DESIGN (S47 lean -- propose to James, don't assume):**
- **Option A (cheapest, highest value):** deepen `summary[:100]` -> `summary[:~300]`. Cost
  ~+15-20K -> lands ~70-75K. Agents reason over 60 PARAGRAPHS not 60 headlines.
- **Option C (trivial, pure reasoning depth):** bump R1/R2 agent `max_tokens` 350 -> ~500.
  Cost ~+1.2K. Lets agents WRITE more developed positions.
- **LEAN = A + C together** (~72-76K, biggest quality-per-token, smallest risk, margin for
  429/503 retry overhead seen live in S47).
- **Option B (banked follow-up, bigger):** two-stage summarize-first -- a pre-pass condensing
  top ~40 articles to dense ~60-tok digests, then feed those. This is the PROVEN Myanmar
  P1->P2 pattern (condense each, then bundle) transplanted into MAD. Better grounding, more
  architecture/risk. Do only if A+C transcript still reads thin.
- **Do NOT raise article count past 60** (wrong lever, blows ceiling).

**MAKE-OR-BREAK / BEV CHECKS (all must be verified, none assumed):**
1. **Re-read mad_protocol.py PROMPT TEXT fresh** (S47 only measured structure, not wording).
   Confirm where `summary[:100]` and `title[:80]` slices live, and the `max_tokens` call sites
   (R1/R2 agents at lines ~652-722 per Claude Code; verify).
2. **Measure new cost on a dry-run / first live run** -- confirm A+C lands under 80K with the
   NEW caps before trusting it. The metering keys off live response.usage, so a real run tells
   truth. Watch the `calls` counter: clean run == 21; >21 means retries/503s (S47 saw a Bear
   503 handled gracefully).
3. **Confirm quality lift on a real transcript** -- read a post-change debate: do agents now
   cite specific articles with depth? Is hallucination still zero? Verdict still calibrated?

**Sequence:** BEV mad_protocol.py -> propose-to-scratch (word-by-word, prompt changes are the
engineering) -> James decides -> build (Claude Code good for the edit+dry-run loop) ->
py_compile -> dry-run measuring tokens -> commit -> ls-remote -> watch a live transcript.

---

## SECOND PRIORITY -- STALE 7433 TREASURE-3 FIX

`PIPELINE_COSTS['gni_mad'] = 7433` in `quota_guard.py` is ~8.5x low (real ~55K). Inert on the
sacred path but ACTIVE on non-sacred -> still mis-gates the MORNING account (checks against
22433 needed, runs ~58K, catches overrun only by accident on 2nd run). Fix: correct to real
~55K AND add a divergence assertion that FIRES when metered MAD cost diverges from estimate
(the Treasure-3 leaky-gate cure). Changes MORNING gating behaviour -> own commit, own dry-run,
do NOT fold into S48. Pairs naturally with S48 (fresh cost numbers either way). Also update the
stale `PIPELINE_RESERVATIONS` comment math (still cites 7433).

---

## WATCH ITEMS (verification, not building)
1. **Evening cron stability** -- S47 saw ONE clean evening run (live-proven). Confirm it keeps
   firing on subsequent days and logging `account='evening'`. GHA drift means it may fire
   hours late -- that's NORMAL (R-S47-4), not a fault.
2. **503 frequency** -- if S48 enlarges prompts, watch for more Bear-style 503 over-capacity
   errors; the system handles them gracefully but quality could dip if frequent.

## PENDING OFFERS (James can pick up anytime)
- **Onboarding prompt set** (continuity-leak cure) -- complete prompt set so a fresh session
  boots into full context fast. Not drafted.
- **Four Treasures -> Lens** -- `GNI_to_Lens_Four_Treasures.docx` BUILT; upload in next LENS
  session, append to lens-DOC-002. Lens-side, not GNI.

## OPERATOR CONTRACT REMINDERS (apply from message 1)
- Warm informal ("my buddy") + strict rigor. Cut preamble, answer first. Lettered options
  A/B/C/D with honest lean. "your call" = decide + full reasoning.
- **"BEV" = HARD STOP**, diagnose-only until full state shown. Gates: BIRD-EYE -> DEEP ANALYSIS
  -> SWOT (if architectural) -> PROPOSE -> JAMES DECIDES -> BUILD+TEST.
- **When James points to past records or says "usually X" -- STOP and read/believe the record
  before defending a position.** (S47: he was right 3x; GHA drift twice.) R-S47-4.
- Short message after long response = pause. One-question rule. Pause-over-push past deep-work.
- **Claude Code is available** -- delegate complex local read/measure/edit; design+review stays
  in chat; James gates the boundary; dimmed suggestions are SUGGESTIONS not executed actions.

## WORKFLOW REMINDERS
- GNI push: `git push origin main` then ALWAYS `git ls-remote origin main` to confirm hash.
- **Single-line git commit messages** (multi-line invited bracketed-paste corruption in S47).
- `printf '\e[?2004l'` before paste-heavy work. **Verify file BYTES (grep -n anchors) after
  any patch -- a success PRINT is not proof** (R-S47-3, the Patch-2 lesson).
- LR-078 ship-to-file over heredoc. LR-101 ASCII anchors only. W2 py_compile before commit.
- Dry-runs offline/hermetic (`os.environ.setdefault('GROQ_API_KEY','test-dummy-key')`,
  `GITHUB_ACTIONS='true'`, monkeypatched client).
- Schema changes = L2 (James approves + runs the SQL in Supabase).

## TRUST CALIBRATION FOR S48
A version/session change partially resets prior verifications. This brief's code claims are
LEADS (~40-50%). The mad_protocol.py PROMPT TEXT is explicitly UNREAD this session (only its
STRUCTURE was measured by Claude Code ~85%). Re-read the live file before editing. Files S47
read in detail (~90-95%): gni_mad.yml, quota_guard.py, mad_runner.py. Guards don't get tenure.
The two-account split is the one thing PROVEN to ~95% (live, both accounts, same day).
