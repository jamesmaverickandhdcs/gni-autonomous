# HANDOFF S78 -> S79
DATE: 2026-07-22 | HEAD: `e90b6c0` (verify ls-remote) | MODEL: Fable 5
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S77-3 IN BOOK; R-S78-1/2 pending below).
Contract: docs/CONTRACT.md (unchanged). Crisis session: MODEL-404. 1 commit (rules), 0 code.

## 1. STATE (<=10 lines)
MODEL-404 CRISIS OPEN: Groq DECOMMISSIONED the primary model (secret-masked). Probe 404 confirmed
  by bytes on Jul 18 AND Jul 21 -- the Jul 18 GROQ_MODEL secret update NEVER SAVED (sudo email
  challenge interrupted the browser flow). Every green Intelligence run Jul 19-21 (#295/296/298/299)
  ran on FALLBACK llama-3.1-8b-instant. Intermittent ~1min FAILS (#294/297/300) = fallback 413
  (payload too large for 8b when account hot; quota 84-91% all week, escalation pinned 10/10).
FIX RULED: update GROQ_MODEL secret (GitHub UI) to llama-3.3-70b-versatile (Groq production tier,
  131K ctx). VERIFY-RUN 29855563370 dispatched Jul 22 ~00:55 BEFORE secret update confirmed --
  outcome UNKNOWN at close; if its probe 404s, the secret was still stale at dispatch.
R-S77-1/2/3 landed `e90b6c0`. SUBPAGE-TRUTH state unchanged from S77 handoff (C1-C6 shipped).

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `e90b6c0` | R-S77-1/2/3 appended (S78 landing gate) | grep 3 |
| MODEL-404 born | primary 404 "model does not exist"; probe arms fallback; analysis attempt1 retries dead primary, attempt2 8b -> 413; both fail -> no report | logs 29631643519 + 29634223201 + 29828297848 bytes |
| Fallback era proven | Jul 21 run STILL probes 404 -> all greens since Jul 19 = fallback-served | log 29828297848:374 |
| Fail pattern | 1m-class fails scattered between 6m greens = fallback 413 under quota heat, NOT deterministic | run list + telegram quota 84-91% |
| Model pick | llama-3.3-70b-versatile (production, Llama family, 131K ctx, 32K completion) over gpt-oss (untested prompts) | Groq docs screenshots |
| TRANS-COUNT unlock | greens #295+ ran post-8eed829 code -- cert possible from any green log vs DB | run list |
| Ops context | escalation 10/10 CRITICAL since Jul 18 (US-Iran); France 24 down, reserve Independent active (James replied 1); HRW down->recovered | telegram |
| a7833854 file closed | Jul 17 fails were pre-push; superseded by MODEL-404 as the live cause | S77 handoff + bytes |

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| RULES-APPEND | R-S78-1/2 below + commit (landing gate) | tail docs/GNI_RULES.md | James | - |
| MODEL-FIX | 1) browser: secrets page, read GROQ_MODEL "Updated" date (predict: pre-Jul 18) 2) update to llama-3.3-70b-versatile 3) confirm "Updated now" | browser | James | V(bytes) |
| MODEL-FIX-CERT | after fix: read 29855563370 log; if 404 -> dispatch fresh run; cert = NO "Probe HTTP 404" line + Status SUCCESS | ID=$(gh run list -w "GNI Intelligence Pipeline" -L1 --json databaseId -q '.[0].databaseId'); gh run view $ID --log \| grep -E "Probe\|fallback\|Deduplication" | - | V(bytes) |
| TRANS-COUNT-CERT | NOW CERTIFIABLE: green #295+ log 'Deduplication: X -> Y' vs pipeline_runs.total_after_dedup (main type, matching timestamp) | gh run view <green ID> --log \| grep Deduplication; then SQL | - | V(bytes) |
| FALLBACK-GAP | 8b fallback cannot carry 22-article payload (413) -- design payload-aware fallback (trim N or capable 2nd model) | SWOT | James | V(bytes) |
| MODEL-DEP-WATCH | Groq retires models w/o waiting for Aug 16 -- periodic deprecations-page check; consider probe alert -> Telegram | design | James | - |
| QUOTA-HEAT | worst account 84-91% for 4 days under pinned 10/10; watch for 429-class fails | telegram read | - | B |
| GT5-T-WATCH | DUE ~Jul 24 (now): 1wk digest before T=2 | digest read | James | - |
| RE-CERT / F3 / WORD-CONV / PHASE-NARR / WEIGHT-PRIOR / GATE-DESIGN / CRED-TOTAL-WATCH / F20-CERT / FED-DOE-WATCH / FT-GAP-B-CERT / F22 / D-11 / DEAD-COLS / J-RULINGS | unchanged from S77 handoff | - | see S77 | - |
| OC-A ~Jul 24 / CERT ~Aug 2 / keyfile Aug 9 / CLIFF Aug 16 (L-CLIFF waits on integrity per S77 ruling; MODEL-404 = evidence to revisit runway, James's call) | - | - | James | - |
| Parked 16 (K-WATCH-NS etc.) | unchanged | - | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| 29855563370 outcome (secret state at dispatch unknown) | dispatched blind | MODEL-FIX-CERT |
| GROQ_MODEL secret actual "Updated" date | prediction only | MODEL-FIX step 1 |
| Whether analysis attempt-1-retries-primary is by design or bug | code unread | FALLBACK-GAP read |
| Which model name the dead secret held | masked *** | (not needed for fix) |
| TRANS-COUNT live agreement | greens exist, unread | TRANS-COUNT-CERT |
| Fallback-era report quality (8b wrote Jul 19-21 reports) | unexamined | James's call |

## 5. TRAPS (<=8 lines)
- GREEN != PRIMARY: a successful run proves completion, not which model served it. Grep the
  probe line before crediting the primary (R-S78-2). Jul 19-21 greens were all fallback.
- The secret was "updated" once already and wasn't -- treat UI writes like patch asserts:
  verify the "Updated now" print before dispatching anything (R-S78-1).
- Placeholders in commands bite James's shell -- ship self-fetching ID=$(gh run list ...) form.
- Chat file-upload cap (100) hit -- new session must start fresh; logs arrive as uploads, unzip in
  /home/claude, grep there.
- Quota 84-91% standing: max ONE manual dispatch per diagnosis cycle.
- Fallback-era DB rows (Jul 19-21) are 8b-written -- don't baseline quality metrics on them.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `e90b6c0` TREE CLEAN -- MODEL-404 OPEN: primary decommissioned, secret update never saved, greens ran on 8b fallback, 1m fails = fallback 413
TOP3 = RULES-APPEND (R-S78-1/2), MODEL-FIX (secret -> llama-3.3-70b-versatile, verify Updated-now), MODEL-FIX-CERT (probe line must show NO 404)
DEADLINE = GT5-T-WATCH DUE ~Jul 24 / OC-A ~Jul 24 / CERT ~Aug 2 / keyfile Aug 9 / Groq cliff Aug 16 (MODEL-404 = cliff's advance party)
TRAP = green != primary (grep probe); UI secret writes need "Updated now" proof; self-fetching run IDs only; quota hot, one dispatch max
FIRST MOVE = ls-remote + git status; then browser secrets page: read GROQ_MODEL Updated date BEFORE anything else

---
RULES APPEND for docs/GNI_RULES.md (at S79 open, landing gate):
R-S78-1: A UI write (secret, setting) interrupted by an auth challenge must be treated like a
  failed patch assert -- zero bytes until the "Updated now" timestamp is read back. Never
  dispatch a verify run before reading it. (GROQ_MODEL "update" that never saved; 2 dispatches burned.)
R-S78-2: A green run proves the pipeline completed, not WHICH path served it -- grep the
  probe/fallback prints before crediting the primary. (4 greens ran entirely on the 8b fallback
  while the primary 404'd all week.)

DIARY S78 (<=10 lines):
The session the cliff sent a scout. A model died quietly upstream and the system, built to
survive, survived -- on its backup, without telling anyone loudly enough. Four green checkmarks
turned out to be the fallback wearing the primary's jersey; the one-minute failures were the
backup buckling under a week of 10/10 escalation heat. The fix we thought we shipped on Friday
had died in an email-verification dialog, and we learned to demand a receipt from every UI
write the way we demand a PATCHED print from every script. Diagnosis by bytes across three log
archives, one prediction left on the table for the next session to collect: a stale timestamp
on a secrets page. The autonomy held. The observability owes us an apology. Fist bump.
