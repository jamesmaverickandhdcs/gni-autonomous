# GNI Autonomous — Rules Registry
# Team Geeks | James Maverick + Claude Sonnet 4.6
# Reference by ID — do not re-derive

## GNI-R Rules (Architecture/Operational)

**GNI-R-240** — MAD Handshake Gate: MAD waits for Intelligence pipeline completion via polling (60s intervals, 25 attempts max) before running. Time assumptions replaced by guarantee-based gate.

**GNI-R-241** — Content Type Classification Mandatory: Every article passing Stage 1 MUST have content_type set to news, news_with_review, or review_only before reaching Stage 2. Any pipeline run skipping classification is invalid.

**GNI-R-242** — A Fix Is a Hypothesis Until Verified: No fix is "done" until verified against regenerated output or live data. Test-clean (compiles, passes self-test, no crash) is NOT proven-working (actually catches/produces the intended result in production). State fixes as test-clean-but-prod-pending until live data confirms. (S40: flatline check never fired <4 reports; workflow alerts untested on real failure; published_at confirmed only after a post-fix run.)

## LR Rules (Lessons Learned)

**LR-078** — Ship-to-file patch over bash heredoc: Git Bash corrupts heredocs with bracketed paste. Always write patches to /tmp/*.py files and run with python /tmp/patch.py.

**LR-091** — Naming consistency check required: Before any integration commit involving new env vars or DB column names, grep all files that read those names and verify exact string match. The 343-hour Telegram webhook darkness (SUPABASE_SERVICE_ROLE_KEY vs SUPABASE_SERVICE_KEY) is the permanent reminder — one wrong character = silent failure for weeks.

**LR-092** — py_compile ALL modified .py files before commit.

**LR-095** — HTTP error: always check r.text[:200] first, never diagnose from status code alone.

**LR-096** — Never dump raw DB blob columns >1000 chars into AI prompts.

**LR-098** — When removing pip package: grep code/ for imports first across ALL files, not just one.
**LR-102** — Confidence is a signal to slow down, not speed up: When a task feels familiar or a fix feels obvious, treat that feeling as the trigger to read the full file / trace the data first — not as permission to skip BEV. "I know this" is not evidence. (S40: guessed a table name, guessed where GNI-R-228 lived, reconstructed file content from memory, assumed the next-free rule number — every time, the actual read corrected it.)
**LR-103** — Real data over constructed tests: A test you wrote proves the code does what you IMAGINED; only real, un-curated input proves it does what the world NEEDS. When validating, include at least one live example (real headline, real input), not only cases designed to pass. (S40: entity_extractor passed 8/8 constructed but real headlines "Japan's"/"Lebanon's" instantly exposed a possessive bug -- the constructed tests never used a possessive.)
**LR-104** — Rank work by blast radius, not just possibility: Before building, sort candidate tasks by risk -- schema/production changes = highest (hold for fresh focus + SQL-before-code); config/standalone modules = safe. Energy or enthusiasm is never a reason to do the riskiest thing at the tail of a long session. (S40: built new sources + standalone modules safely; deliberately held B3 schema-wiring for a fresh session.)
**LR-105** — Protect the future of the work over the momentum of the moment: Never make a failing check pass cosmetically. Revert to the honest proven state and log the real finding loud. A codebase must never lie about what it can do. (S40: a real-headline test found a genuine bug at 8/10 -- reverted to honest 8/8 + logged the bug for a proper fix rather than papering it green.)

**LR-099** — Philosophy Compatibility Gate: When Claude reads a finalized philosophy document AND has access to the implementation codebase, Claude must perform a compatibility audit unprompted. Map each non-negotiable principle to its code implementation. Any gap found must be surfaced immediately. Full context visibility = full audit responsibility. Reference: phi_compatibility_check.md in repo root.

## PHI-003 Non-Negotiables (Quick Reference)

- NN-PHI-1: GNI serves the human being, not the market. Teenager Standard.
- NN-PHI-2: All news directions equal — good, bad, opportunity, threat.
- NN-PHI-3: Manipulation techniques never in GNI output.
- NN-PHI-4: Every threat must have a path. fff_human_path always required.
- NN-PHI-5: Absence is intelligence. Coverage gaps reported. (OPEN — S37)
- NN-PHI-6: Adversarial sources are signal not authority.
- NN-PHI-7: Data reset when philosophy resets.

Last updated: May 24, 2026 — GNI S36

## LR-106 -- LLM JSON parsers must guarantee dict-or-None
Any function parsing LLM JSON output (e.g. _parse_json_response) MUST coerce the
result to dict-or-None before returning. LLMs intermittently wrap the report in an
array [{...}]; json.loads then returns a list and downstream .get() crashes ('list'
object has no attribute 'get'). Unwrap single-object lists to the dict; return None
for [] or non-dict arrays. Root-caused from Jun 7 Intelligence #210 (the only failure
in 9 autonomous days). Fix: commit a15bcc0.

## LR-107 -- A brief-claimed bug is a hypothesis, not a fact
A bug asserted in a prior session's brief (or by anyone) is unverified until reproduced
against live execution. S42 had TWO false ones: the S41 "URGENT" possessive bug (a test
artifact from heredoc apostrophe-stripping) and the initial "Sunday digest mutates shared
state" theory for #210 (the code shared no state; real cause was list-shaped JSON). Verify
before fixing. Confidence is the tell to slow down. Extends GNI-R-233 / LR-102.

- **R-S55-1 - Sibling sweep:** when a bug is found in ONE consumer of a shared route/field, grep ALL consumers before closing the arc. (The 4th false-185% sibling on /about/devops sat undiscovered for 2 sessions.)
- **R-S55-2 - Widen the fossil grep:** after any fossil is found, generalize its pattern before declaring the class swept. (The "02:00" grep missed the ":30" MAD variants.)
- **R-S55-3 - Confirm the patch ran before trusting the verify:** require the PATCHED/DONE print first; verify-greps on an unpatched file prove nothing. (U1 was "verified" twice on an unpatched file.)
- **R-S55-4 - One calibration:** model-coupled fixes (budget solver, quality scorer, grounding gate) bundle WITH the model migration, never before it.
- **R-S55-5 - Transfer Protocol v1 adopted:** HANDOFF_S{N}.md + CONTRACT.md replace the 6-file close. Caps hard, delta-only, LOAD CHECK echo mandatory. Spec: docs/GNI_Session_Transfer_Protocol.md.

- **R-S56-1 - Escape at the boundary:** a failure reason (or any external/LLM text) is hostile input to any formatting channel (Telegram HTML, etc). Escape at insertion or drop the parser. (The Stimson 403 reason contained literal <unknown>, poisoned its own alert, and shadow-killed reserves for 967h. Sibling sweep closed the class across 3 files in S56-S57.)
- **R-S57-1 - Line endings are per-ANCHOR facts:** this repo mixes CRLF and LF per-file AND per-region. Every patch script carries the LF->CRLF fallback and confesses which matched; never infer a file's convention from one hit.

- **R-S58-1 - Text-mode patching banned:** Python text-mode open() is a line-ending NORMALIZER: it converts CRLF->LF on read, so writing the
string back rewrites the entire file's endings even for a 2-char edit. ALL patch scripts on this
repo read rb / write wb with BYTE anchors (b"..."). Text-mode file patching is banned.

R-S59-1: Census before sweep -- grep the FULL tree for a claim before patching any instance; never chain a git commit after a sweep-verify grep in the same paste (81->70 took 3 commits because commit fired before census was read).

R-S60-1: Browser verification requires a hard-refresh (Ctrl+Shift+R) first -- a stale client
  bundle perfectly mimics a code bug (V-W13: code, API, and DB were all clean; cache was the bug).
R-S60-2: Structural quality scores do not measure grounding. A MAD run scoring 100% published
  two fabricated entities. Grounding requires its own deterministic gate against the article basket.
R-S60-3: Never pipe an ungrounded layer's output into grounded layers unchecked. Consultants
  receive no article basket; labeling their text "PERSONAL CONSULTANT TO YOU" launders invention
  into evidence. 4/4 confirmed specimens entered through this channel.

R-S62-1: Claude Code tasks get a POST-RUN mechanical verification block (greps + diff-stat +
  build) and a one-command revert path. Never assign live watch-duty to the operator --
  safety lives in commands, not attention.
R-S62-2: Any placeholder in a command MUST be loudly marked (warning emoji + "PLACEHOLDER" +
  what to substitute). The operator runs commands verbatim. (S62: <path> and YOUR_KEY both ran literally.)
R-S62-3: Server-side Supabase reads go through createNoStoreClient (src/lib/supabaseNoStore.ts).
  New API routes never call createClient directly -- Vercel Data Cache serves fossils otherwise.

R-S63-1: Any option list whose reply-number maps to list POSITION in a consumer (Telegram
  webhook class) must preserve numbering across changes -- annotate bad options, never
  filter, until every consumer is read and updated in the same commit.
R-S63-2: Fallback resources (reserves, backups, secondaries) are guilty-until-verified:
  live-check + dedupe-against-primaries before they may be offered as safety. A dead
  reserve is worse than none -- it converts an outage into a silent one.
R-S63-3: No protection may permanently mute its own alert path. Any "already handled ->
  skip alert" state needs an escalation branch for re-failure.

R-S64-1: "Success. No rows returned" (any silent DB response) proves nothing. Every
  UPDATE gets a SELECT verify, and state audits census the WHOLE table (no LIMIT) --
  a LIMIT hid a live PRIMARY-DUP row in S64.
R-S64-2: Aggregated views (trace Collected, dashboard counts) cannot answer WHO served
  a slot -- reserve articles log under the primary's name. The run's raw console log is
  the only authority on serve-path questions; read it before concluding.
R-S64-3: Dedupe fallback resources by feed DOMAIN, not display name. "Radio Free
  Europe" vs "RFE/RL" sailed past a name-set guard while serving identical rferl.org
  content -- name spelling is not identity.
R-S65-1: Fetch-based "recovery" is not recovery. Any auto-retire/auto-activate criterion
  must consult yield or serve-path, not transport alone -- C2 retired a reserve for a
  primary that fetched fine and served zero.
R-S65-2: Executor (Claude Code) diffs get chat clearance BEFORE the git trigger, every
  time, however clean they look. Review-then-trigger is the contract's protection for
  the day the diff isn't clean.
R-S65-3: Never blind-wrap keyword lists in word boundaries. Lists contain deliberate
  stems (extremis, geopolit); use an explicit stem convention ('*' suffix) and annotate
  conservatively -- a too-greedy stem is the substring bug wearing a different hat.

R-S66-1: A keyword-level census proves kills; only an article-level comparison
  proves signal preservation. When a ruling ADDS vocabulary, the keyword census
  is structurally blind to the rescue -- verify at the article level.
R-S66-2: Substring bugs can be load-bearing. Before anchoring any matcher,
  census what REAL signal entered through the bug's side door (demonyms via
  country names, 'enforced' via 'forced', IranWire via 'iran') and re-admit it
  deliberately -- silent suppression is worse than the inflation being fixed.
R-S66-3: A proxy in a vocabulary list (brand-as-actor, source-as-signal) is
  allowed only if declared in-code AS a proxy, with the honest cost and the
  proper fix named. Undeclared proxies are future fossils.
R-S67-1: When a change spans code and DB/live state, hand over the steps as
  NUMBERED GATES with the code push explicitly first -- commands delivered
  together get executed in paste order, and paste order becomes system state.
R-S67-2: Before trusting any statistic from an instrument, verify the
  instrument's RANGE (caps, truncation, short-circuits). A metric that cannot
  move is not evidence of stability -- the trace's 3-keyword cap censored the
  match-count deflation K-WATCH was built to observe.

R-S68-1: A model/secret swap plan is incomplete until a BARE-HARDCODE census runs -- grep call-site literals and workflow YAML, not just os.getenv defaults. The funnel L4 call and gni_adaptive.yml both hid from the secrets-only view.
R-S68-2: GitHub Actions masks secret values as *** in CI logs -- a log can prove a secret is SET, never what it contains. Don't burn session time trying; only the keyfile ritual resolves values.
R-S69-1: A byte-census says what IS; only session history says which side is canonical.
  No public-copy fix ships without reading the claim's design lineage first -- the S59
  sweep and the S69 near-sweep pointed OPPOSITE directions off the same bytes.
R-S69-2: Any mid-session fallback substitution ("simpler approach for now") and any
  James-deferral must leave an instrument in the same message: a queue row, a date or
  trigger, and a scheduled verify. Close docs mark "DONE (fallback: X deferred)" --
  never bare DONE. Substitution without a debt record launders itself into fact.
R-S69-3: Protections-guilty extends to WIRING: a security module's first BEV question
  is "who imports me?" A green self-test on an orphan module is a false positive.
  Run the orphan-import census at every model-change re-audit.
R-S70-1: Shared DB state gets shared-route discipline (R-S55-1 kin): any table gaining a
  new writer triggers a WRITERS census -- name every function writing each column. Two
  writers with different formulas for one column is a design review, not a merge; audit
  the seam, not the files.
R-S70-2: Chat-generated docs get a landing gate before first commit: wc -l on disk vs
  expected, STOP on mismatch. A cat >> to a never-saved path silently creates a stub --
  the D-8 disease in commit form.
R-S71-1: Dual-writer dedupe merges by OWNERSHIP, not timestamp: when two writers fought over rows,
  the owning writer's row wins even when the stomper's is fresher. "Keep freshest" enshrines
  whoever stomped last. Preview-before-delete is what catches this -- never skip the preview.
R-S71-2: Census the CLASS, not the named list: a spec that names 4 ghosts gets a sweep of the WHOLE
  dict against the roster (found 6); a relabel of 4 "Total X" strings gets a sweep for every
  totality-implying label over a LIMIT query (found 6). The named instances are leads, not the set.

R-S72-1: Multi-line patch anchors join on the file's DETECTED newline ('\r\n' if '\r\n' in d
  else '\n'); an LF-joined anchor against a CRLF working copy counts 0 and dies clean but wastes
  the round. Single-line anchors are immune. Print NEWLINE=%r before asserting.

R-S73-1: One semantic contract = ONE definition. When two sites need the same list/whitelist/
  threshold, extract a shared builder placed next to its source of truth and import it --
  hand-copies drift silently and the drift ships as divergent behavior.
R-S73-2: Before gating/sanitizing a value in place, census ALL its consumers first. A value
  feeding both a feedback loop and a public exhibit/metric gets a GATED COPY for the loop;
  the raw original stays for everything else. In-place gating erases exhibits silently.

R-S74-1: Registry appends assert ID-uniqueness against FILE BYTES before writing -- the next
  free ID is a read result, never a memory. (D-10 collision: assert caught a duplicate the
  handoff-informed guess would have shipped.)
R-S74-2: A frontend interface declaring DB fields is a HYPOTHESIS -- verify every field against
  information_schema before trusting any page's type. (F23: three phantom fields rendered
  fossils for weeks; the March sprint doc warned this verbatim.)
R-S74-3: Certifying shipped code via CI logs starts at the run's CHECKOUT SHA -- a missing
  feature line proves nothing until you know which commit executed. (Morning NULL was
  pre-GT5 state, not a failed seam.)

R-S75-1: Counting items in a code literal (pattern lists, configs) is an AST job, never a
  regex-over-text job -- regex stops at the first nested bracket and censors the count.
  (Funnel patterns: regex said 16, AST said 81; the public claim was true all along.)
R-S75-2: A grep hit showing ONE condition of a chained query/filter is not the filter --
  read the full call site before classifying a lead. (GRAPH-S2 false alarm: the .eq
  stage2 line had two conjoined siblings just above it.)
R-S75-3: When a sequential funnel persists per-stage flags with default-True 'not evaluated'
  semantics, every aggregate over the trace must conjoin ALL prior stage flags --
  counting one flag alone reports the default, not the funnel. (TRANS-COUNT: 360 > 262.)

R-S76-1: Multi-line patch anchors must derive the newline from the target file's own bytes (nl = CRLF if in file else LF) -- hardcoded \n silently matches zero on CRLF working copies. Single-line anchors are immune. (C1 first attempt: a1 count 0, zero bytes written.)
R-S76-2: A handoff oracle spec must record the exact workflow name AND the print format as bytes, not paraphrase -- 'Stage 2: X -> Y' matched nothing because the real print is 'Stage 2 (Deduplication): X -> Y articles' in a different workflow. Grep the phenomenon, not the report of it.
R-S76-3: A uniform denominator across rows with varying numerators is arithmetically impossible from a per-item counting loop -- treat it as an instant fossil-or-bug tell. (39 sources, wins 28-70, every total exactly 102 = pre-fix global-count fossils.)
R-S77-1: Chained build/verify/commit commands after a patch script run UNCONDITIONALLY -- a failed assert writes zero bytes but the chain proceeds on the unpatched tree. Gate the chain on the PATCHED print, or run patch and commit as separate pastes. (C5 first attempt.)
R-S77-2: For count claims in prose copy, removing the number beats hydrating it -- prose that names no count can never rot, and plumbing-to-prose is bad engineering. Hydrate only where a number is displayed as a stat. (Feedback SWOT: two mentions cured count-free.)
R-S77-3: A live-computed stat can still lie by ATTRIBUTION -- verify the label's system name against the data source, not just the number's math. ('52 correct' was live math under a GPVS label while reading debate_predictions.)
R-S78-1: A UI write (secret, setting) interrupted by an auth challenge must be treated like a
  failed patch assert -- zero bytes until the "Updated now" timestamp is read back. Never
  dispatch a verify run before reading it. (GROQ_MODEL "update" that never saved; 2 dispatches burned.)
R-S78-2: A green run proves the pipeline completed, not WHICH path served it -- grep the
  probe/fallback prints before crediting the primary. (4 greens ran entirely on the 8b fallback
  while the primary 404'd all week.)
R-S79-1: Browser-UI steps are not executable in this partnership — every action ships as a runnable
  command; config writes go through gh CLI with byte receipts (gh secret list before/after). Never
  ship a gated command block in the same message as its gate. (S78's dispatch mistake repeated at S79.)
R-S79-2: A deprecation list proves the list, not the runtime. Grep live logs before declaring a
  component dead or alive. (Lens-1 served HTTP 200 all week with a "shut down" model configured;
  MAD's byte-level comment beat a remembered search claiming gpt-oss adoption.)
R-S80-1: Binary patch anchors derive NL from the target file's own bytes (repo mixes LF and
  CRLF per file). A patch script that dies mid-sequence has written NOTHING — verify which
  files actually changed (git status) before staging; never commit a spec against unpatched code.
R-S80-2: An instrument certifies only the call-shape it holds. The MAD probe's arbitrator-shaped
  fixture validated a floor that 413'd on agent-shaped prompts. Budget math (prompt + max_tokens
  vs per-request ceiling, per-model quota buckets) precedes any uniform limit change.
R-S80-3: Speculation may flow but must not reach humans dressed as a finding. Label at output
  seams (estimative language), don't suppress — suppression creates its own lies. The gate acts
  on the shadow verdict; it never suppresses the recording of it.

## S81 EARNED RULES (2026-08-17)

- R-S81-1 (Zero-match indicts the pattern first): A filter that returns no rows prints a BLANK
  line, which is indistinguishable from a broken filter, a bad field name, or an empty fetch.
  Prove the instrument saw data before reading silence as absence — count first
  (`gh run list -L 40 --json conclusion --jq 'length'`), then group. Born Aug 17: a cliff-survival
  check returned two spaces and was almost read as "zero failures". It was correct, but nothing
  in the output said so.

- R-S81-2 (Verify what ARRIVED, not what was fetched): Any consumer that assembles inputs under
  a budget must log what was INCLUDED against what was AVAILABLE. A guard that tests the fetched
  list passes whenever the fetch succeeds, and cannot detect its own starvation. Zero inclusion
  of a required input is a FAILURE, not a quiet loop break. Corollary: a failure that grows with
  upstream health does not look like a failure. Mirrors Lens LR-141, adopted by reference;
  GNI's own evidence pending the ROOT 1 audit.

- R-S81-3 (Absolute allotments, never leftover budgeting): No consumer's share may be defined by
  what another consumer left over. Each tier gets an absolute allotment measured exclusive of
  every other tier; a total cap may exist as a backstop but must not be the allocator. When a
  tier drops content, log WHICH item was dropped by name — a count says the tier shrank, a name
  says which perspective was lost. Mirrors Lens's Mission Analyst finding.

- R-S81-4 (One load-bearing block per message; rollbacks never travel with applies): When a
  message contains a patch block, multi-block pastes get PARTIALLY executed — a commit block can
  run while its patch block does not, committing nothing and looking like success. And a rollback
  command sitting in the same message WILL eventually be pasted along with everything else.
  Offer recovery separately, on request, only after the apply is verified. Assume any block may
  run twice, out of order, or not at all. Mirrors Lens LR-140.

- R-S81-5 (A guard's expected value must be derived, not hand-counted): Any assertion whose
  expected number was counted by eye is a banked estimate living inside a tool built to stop
  banked estimates. Derive it from the same data the change is made from (sum the deltas across
  the edit list, do not count lines). Assert RELATIVE to the file's state read at the start of
  the patch, never absolutely — a hardcoded "this file must be LF" starts failing on files
  nobody touched the first time autocrlf converts them. Extends R-S80-1. Mirrors Lens LR-139.

- R-S81-6 (Grep the agreement, not the message): `git log --stat` proves message-vs-contents. It
  cannot prove contents-vs-agreement. Before committing a change agreed in conversation, grep ONE
  DISTINGUISHING PHRASE PER AGREED ELEMENT and report the hits; absence of a hit means that
  element did not land. The phrase must be unique by construction — a commit SHA proves nothing
  because SHAs legitimately recur in a document. Presence alone is not enough: assert UNIQUENESS
  whenever an ordered list gains an item. The trap stated plainly: producing text in conversation
  FEELS like shipping it, and the same illusion works on the reader. Mirrors Lens LR-138.

- R-S81-7 (Record requested time and observed time separately): The trap book recorded when crons
  FIRED and called it the schedule. YAML holds the request; run history holds reality; the delay
  is its own measurement and it drifts. S80 banked "1-3 hours late"; by Aug 17 the same crons
  fired 13-60 minutes late, and a wait anchored on the stale figure wastes a session. Requests:
  pipeline 02:13/10:13, MAD 02:43/10:43, grounding-watch 11:13 UTC.

- R-S81-8 (Groq refills continuously; there is no daily reset): TPD is a leaky bucket refilling at
  Limit/86400 per second — about 8,333 tokens/hour at a 200K limit, with no midnight anywhere.
  Recovering 50,000 tokens costs roughly six hours of wall clock. A live 200 carries exactly six
  x-ratelimit headers, all per-MINUTE; there is NO daily token header, so TPD is observable only
  from a 429 body or the console, and a 404 carries no rate headers at all (so any pre-flight
  reading them fails open on a dead model name). Any reasoning of the form "the quota resets and
  we start fresh" is reasoning about a fiction. Measured in Lens to the millisecond across seven
  readings; adopted here by reference, and GNI's per-account-day reservation model is unaudited
  against it (order item 4.3).

## S82 EARNED RULES (2026-08-17)

- R-S82-1 (To find an artifact, grep its STRUCTURE, not its name): A phrase-grep for a
  document's contents returns every file that MENTIONS it and hides the one that IS it.
  S82 ran `grep -rln "LOAD CHECK"`, got 30 handoffs back, and concluded from that noise
  that GNI's opening and closing prompts did not exist as artifacts. They existed the
  whole time, as PART C and PART D of `docs/GNI_Session_Transfer_Protocol.md`, and a
  heading-grep (`grep -nE "^#{1,4} "`) found them in one call. Sibling of R-S81-1: there
  a zero-match indicted the pattern, here a HIGH match count did. Match volume is not
  evidence in either direction; only the shape of the match is.

- R-S82-2 (An instrument dumps the whole category, not the expected field): When adding
  measurement, log every member of the category under test, not the one the hypothesis
  names. S82's ARB-ARRIVAL instrument measured the article tier and skipped the four
  sibling tiers (constraint_block, R1, R2, R3, tail) that compete for the same budget --
  so when the arb prompt grows, the log will show articles shrinking without naming which
  tier ate the room, which is the very question the next item must answer. Corollary from
  Lens: a measurement that FALSIFIES the instruction that requested it is a success, not a
  failed mission. Design for that outcome.

- R-S82-3 (A stopgap never closes a root): Capacity freed by a stopgap flows wherever the
  system routes it, not where the fix intended, so a stopgap's own cert cannot close the
  root it was aimed at. Evidence: C1 transcript-carry (S81) freed prompt room, certified
  PASS on its own terms (zero 413, zero empties, bill down) -- and the arbitrator gained
  nothing, still riding the FULL fit ladder to `ctx-trim@4983` three weeks later. A root
  closes on a measurement OF THE ROOT. Extends R-S69-2: a substitution without a debt
  record launders itself into fact; a stopgap without a root-measurement does the same.

- R-S82-4 (When law changes, sweep the TEMPLATES): A template is law that executes itself
  in the next session. CONTRACT v4 moved the queue out of the handoff and into the order
  file; HANDOFF_S81 obeyed, but PART B of the Transfer Protocol still instructed the next
  session to build a `QUEUE (<=25 lines)`. Two closes would have restored the queue by
  template alone, silently undoing the change. R-S55-1's sibling sweep applies to docs:
  after any rule-of-engagement change, grep every template that encodes the old rule.

- R-S82-5 (Apply the law-vs-state test to the version log itself): "Law edited most
  sessions means target-level content leaked in" is a test that must be run against the
  contract's OWN edit history, not only its sections. GNI's CONTRACT reached v4 in six
  weeks; reading the log, v2 was a model roster (pure state, and already false -- it named
  Opus 4.8 while S82 ran on Opus 5) and v3 mixed a genuine rule of engagement with the
  model names that dated it. The leak was visible in the version log for three weeks and
  went unread because every review looked at the newest SECTION instead.

## S83 EARNED RULES (2026-08-24)

- R-S83-1 (A disclosed limitation is a CLAIM, not a fact): A limitation stated at ship time
  carries the same trust as any other unverified assertion, and it must be checked against
  the instrument's FIRST real output. S82 disclosed that ARB-ARRIVAL's `truncated=` would
  always read 0, reasoning that ctx-trim appends `'\n[ctx trimmed to fit]\n'` after slicing.
  It read 1 on the first run. The instrument never touches the assembled prompt -- it
  RE-DERIVES the slice as `arb_ctx_fit[:_keep]`, so the appended marker was never in the
  string the `endswith` test sees. The trap built on that disclosure said `dropped=N` means
  "at least N"; the bytes say it is EXACT and conservative-HIGH by one, because a partially
  delivered article is trimmed from `arrived` and counted as fully dropped. Carried into the
  ruling, the trap would have inverted it. A self-reported weakness is a lead like any other.

- R-S83-2 (Novelty is an identity question; a content check cannot answer it): To prove an
  artifact is NEW, compare its IDENTITY against what has already been read -- never its
  contents. S83 issued a guard that accepted a fetched run if `ARB-FIT` appeared once. That
  test distinguishes the debate from the grounding-watch flavor and says nothing about
  freshness, so when `-L 1` returned the run already read that morning, every check passed
  and the block would have been logged as a second sample. Sibling of R-S81-1 and R-S82-1:
  there a zero-match and a high match count misled; here a CORRECT match on a stale artifact
  did. Compare ids, and print the id next to the claim.

- R-S83-3 (Read the clock in the block that makes the claim): Never state elapsed time, a
  schedule position, or "the next run is due about now" from turn count, from conversational
  distance, or from memory. S83 did it twice, calling a run late that was sixteen minutes
  early, and then called a run "this evening's" when six days had passed since the previous
  message. Both were resolved by one `date -u` that had not been asked for. Pair every wait
  estimate, deadline, and freshness claim with a clock read in the SAME command block --
  and the same for a repo: `gh` resolves its target from the git remote, so a `cd` out of
  the repo silently removes the world the command was meant to query.

- R-S83-4 (A cert that measures mechanics has not certified the instrument): Passing on
  finish_reason, absence of 413s, absence of empties, and "the output arrived" proves the
  PLUMBING survived a change; it says nothing about whether what flows through the plumbing
  is the same. Evidence from Project Lens: a July migration certified clean on mechanics, and
  three weeks later the same positions were extracting twice the actors and THREE TIMES the
  claims per row, while the headline consistency metric moved 0.834 -> 0.853 and hid it. GNI
  owns the same debt: the S80 MAD migration was certified on 413s and empties, and ROOT 2.3
  has been asking since July whether the arbitrator's verdicts changed. A behaviour cert
  needs a BAND measured before the change and re-measured after, from stored rows.

- R-S83-5 (A ritual document needs a path into the session that begins with a READ): A prompt,
  template, or checklist that reaches a session only by being pasted has no single source of
  truth -- the pasted copy and the repo copy drift, and nothing can detect the drift because
  nothing ever compares them. Byte evidence: `sed -n '/PART D/,/PART E/p' | grep -c
  "Transfer_Protocol"` returned 0. GNI's CONTRACT cited the prompts by path since v5, the
  protocol file existed and was correct, and no artifact in the repo ever instructed anyone
  to open it. Lens shipped the identical fix after discovering its pasted close prompt had
  silently lost two clauses present in the repo. Extends R-S82-4: sweeping templates when law
  changes is worthless if no template is ever read.

- R-S83-6 (Flow discipline does not protect a stock): Rate limits, per-minute pacers and
  per-day reservations all govern a FLOW, and a system fluent in flow control can be entirely
  blind to accumulation. Storage only grows; nothing consumes it back; and its failure is not
  a slow degradation but a hard refusal of every read at once. Project Lens ran sophisticated
  token-per-minute and token-per-day governors while its database grew unmetered to 287% of a
  free-tier quota, and went fully offline for nineteen days. GNI_Autonomous has `quota_guard.py`
  and ZERO retention code -- `grep -rn "\.delete()"` returns nothing. For every free-tier
  resource, ask whether it is spent or ACCUMULATED, and meter the accumulated ones. Corollary
  amending R-S81-6: read the METER, not the mail -- Lens missed two announcement emails a
  month apart and lost five positions to one and its whole database to the other.

## AMENDMENT TO AN EXISTING RULE (no new number -- R-S83 deliberately does not re-mint)

- R-S81-3 (AMENDED 2026-08-24): the existing rule says a count tells you the tier shrank while
  a NAME tells you which perspective was lost. Amended: the count must be of DISTINCT IDENTITY,
  not of rows. Project Lens's arrival check reported `s1=4/4` on a wave where all four rows
  were the same lens produced four times -- a perfect score over a single perspective. GNI's
  ARB-ARRIVAL has the identical blind spot: `arrived=20` counts lines beginning `'  - ['`, so
  fifteen geopolitical articles and five financial ones report exactly as four pillars would.
  Count the distinct category, then name the losses.
  *(This is an amendment rather than R-S83-7 on purpose: Lens re-minted a rule it already held
  and paid for the duplicate. Before minting a number, search the register for the rule that
  already says it -- and search BOTH ID schemes, `GNI-R-###` and `R-S##-#`, since a grep for
  one is blind to the other.)*

## S84 EARNED RULES (2026-08-25)

- R-S84-1 (A pure function is a free simulator -- do not derive a formula you can measure):
  Before writing a formula with a constant in it, check whether the code that produces the
  thing is PURE. If it is, call it again with the arguments you were about to model and take
  `len()`. S84 was about to size the arbitrator's context with an assumed ~138-char per-article
  overhead; the byte read gave the real cost as
  `21 + len(src) + len(title[:80]) + len(str(score)) + len(summary[:depth])`, which varies
  114-130 chars per article with source and title length -- so every fixed-overhead formula is
  wrong on every run. `_build_news_context` and `_assemble_arb` are pure, so ARB-DRYRUN
  measures four candidate depths per run at zero API cost. Satisfies R-S81-5 by construction:
  a guard value that was BUILT cannot have been hand-derived.

- R-S84-2 (When two meters disagree, calibrate against the one that ENFORCES): A self-built
  meter must read the same number the platform bills and blocks on, not the number that is
  convenient to query. GNI's `pg_database_size` reports 93 MB; the Supabase panel reports
  113 MB against the 500 MB quota; the ~20 MB gap is platform-side and invisible from inside
  the database. Table-level figures agree EXACTLY (63.29 MB both ways), which is what makes the
  disagreement dangerous -- the instrument looks correct everywhere you can check it and is
  wrong precisely where it decides. A meter built on the internal number would have reported
  healthy headroom while the platform returned 402 on every read. Corollary to R-S83-6: read
  the meter -- and read the ENFORCING meter.

- R-S84-3 (A conclusion that was corrected but never WRITTEN DOWN as corrected will re-form):
  GNI-R-233 says reset to zero when corrected. S84 found the gap: a reset that lives only in a
  session's memory is not durable, and the same wrong conclusion re-forms in a later session
  with fresh confidence. S84 re-derived "the grounding gate is grounding against material the
  pipeline rejected" from `weak_articles` being in the basket -- a conclusion this project had
  already reset once, having established that score:0 -> Swan is BY DESIGN (the Johari
  weak-signal pool). Recidivism is worse than the original error because it consumes the
  correction's credibility. When a conclusion is reset, the reset itself is an artifact: write
  it where the next session will read it, or expect to pay for it twice.

- R-S84-4 (PROMOTED FROM A TRAP carried unchanged twice -- `gni_mad.yml` holds two flavors):
  One workflow file runs BOTH the MAD debate and the 11:13 grounding-watch, so a run list shows
  two kinds of run under one name. Distinguish by the presence of `ARB-FIT`, never by time
  alone. S84 adds a second, WEAKER distinguisher observed 8/8: elapsed time separates them
  cleanly (~18-21s watch vs 11-14m debate), and the job list shows `grounding-watch` skipping
  in `0s` on a debate run. Use elapsed as a hint, never as the authority. Promoted rather than
  carried a third time, per CONTRACT v5: a trap copied forward unchanged twice has become an
  unregistered rule.

## AMENDMENTS TO EXISTING RULES (no new numbers -- search before minting)

- R-S81-1 (AMENDED 2026-08-25): the rule says a zero-match indicts the pattern first, and that
  a filter returning nothing prints a blank line indistinguishable from a broken one. Amended:
  a REDIRECTED FAILURE is not silence, and is worse, because it produces a corpus.
  `gh run view --log > file 2>&1` writes the error message INTO the file, so the artifact
  exists, is non-empty, opens cleanly, and reads as valid text -- while every `grep -c` against
  it returns 0. S84 came one command away from reading "ARB-DRYRUN fired 0 times" off a
  one-line file containing a TLS handshake timeout, and would have gone looking for a bug in a
  correct instrument. `wc -l` BEFORE grep, on any cached or redirected artifact, always.

- R-S67-2 (AMENDED 2026-08-25): the rule says verify an instrument's RANGE (caps, truncation,
  short-circuits) before trusting its statistic. Amended: verify its EPOCH too. A cumulative
  counter and the data it counts can start at different times.
  `pg_stat_user_tables.stats_reset` read 2026-02-12 identically for every table in every schema
  -- the signature of a platform-side reset, not of first insert -- while `pipeline_articles`
  data began 2026-05-24, three hours after a TRUNCATE. Dividing live rows by the counter's
  192-day window instead of the data's own 92-day span understated growth by 2.1x and
  overstated the runway by 40%. A rate is rows divided by the DATA's span, never by the
  counter's.

- R-S85-1 (A lettered proposal without a lineage read is an opinion wearing a decision's clothes):
  R-S69-1 already said "read past session records before designing a fix for a lineage-bearing
  bug", and S85 skipped it TWICE in one session. The first skip cost a wrong story about a
  workflow env line. The second was worse: Claude proposed A/B/C on the arbitrator's context
  budget without reading [[gni-s83]], leaned option C (round-robin ordering), James chose C, and
  James then said in plain words that he chose it BECAUSE Claude urged it. DECISION S83-1 - which
  James himself had ruled - had already settled the direction as per-article COST and explicitly
  reasoned that ordering/allotment fixes CANNOT raise coverage because the share is already
  stable. So an unresearched lean overwrote an operator ruling, and the audit trail would have
  read "James chose C". The lesson is not "remember to read". It is that Claude's lean STEERS the
  ruling, so the read must happen BEFORE the proposal exists, and it must leave an artifact James
  can see is missing. Shipped as CONTRACT v7's LINEAGE-BEV gate with its `LINEAGE:` line.

- R-S85-2 (Grep human-facing COPY case-insensitively; grep code case-sensitively):
  The S85 census for stale model names ran `grep -rniE` on code identifiers but `grep -rn -e
  'llama'` on prose, and prose is where humans capitalise. `src/app/about/page.tsx:26` read
  `'Groq API (Llama 3)'` with a capital L, survived the census, and was the SECOND site named in
  S69 census flag F5 - a flag Claude had just finished reading. The site was fixed only because a
  re-run with `-i` found it. Identifiers are case-exact by nature; copy is not. When the target is
  something a reader will see, case-fold, and grep the SYNONYMS too (a model may be named as
  `llama-3.3-70b-versatile`, `Llama 3`, or `Llama 3 Local` on three different pages).

- R-S85-3 (An idempotency guard must test a string that exists ONLY in the patched state):
  An S85 patch guarded with `if replacement in data: ABORT` fired immediately - not because the
  file was patched, but because the replacement text `{ name: 'Groq API', role: 'Cloud AI` already
  existed on the NEXT LINE as pre-existing content. The guard asserted the anchor was unique and
  never asserted the sentinel was. Correct shape: the ANCHOR's absence is the proof of a completed
  patch (`if count == 0: already patched`), because the anchor is the thing the patch destroys.
  A sentinel drawn from the new text is only safe if it is asserted unique first, and if it is
  unique it is usually just the anchor's complement anyway.

- R-S85-4 (A finding folded into another arc's scope DIES when that arc is declared achieved):
  S69 census flag F5 named TWO stale model-name sites and was routed with "F5 -> CLIFF scope
  (CLIFF-DOC)". The CLIFF arc was formally DECLARED ACHIEVED WITH EVIDENCE at S81. F5 was not in
  that evidence; one of its two sites was still live on the public site five weeks later, and the
  flag had no home left to be unclosed in. A phase transition audits its own definition of done,
  never the items other arcs parked inside it. Therefore: a finding folded into another scope must
  ALSO exist as a numbered item in the order, or the fold is a deletion with extra steps. At any
  ACHIEVED declaration, grep the closing arc's name across the census/register files first.

- R-S85-5 (A register with no scheduled reader decays into an archive):
  `docs/DEBT_REGISTER_S69.md` was built by conversation_search archaeology across every GNI record,
  carries 131 lines, D-1..D-11, V-1..V-3 and a 13-row James-deferral ledger, received S70 and S74
  status appends - and then stopped on 2026-07-17. Ten sessions later no handoff, order file or
  contract referenced it, and S85 discovered it by accident while running a lineage grep. Its own
  text predicted this: "debt without an instrument decays into fact". The register WAS the
  instrument; nothing was the instrument for reading the register. A document that no prompt, gate
  or template ever opens is not a register, and creating one is not the same as closing the debt.
  Corollary: this is why LINEAGE-BEV greps `docs/` rather than naming files - the grep finds
  registers nobody remembered to cite.

- R-S85-6 (State the FAILURE TEST in the commit that ships the change):
  The S85 arbitrator fix went out with five pre-registered predictions and one explicit failure
  test ("GROUNDING SHADOW arb_hits must NOT rise; a rise means breadth did not buy grounding and
  the depth call was wrong") written into the commit body. This is the S82/S84 instrument
  discipline applied to a BEHAVIOUR change rather than a measurement: R-S83-4 says a cert on
  mechanics has not certified the instrument, and the only defence is to name, before the run
  exists, the observation that would refute the ruling. A cert that cannot fail is a ceremony.

- R-S86-1 (A baseline drawn from the most recent runs is not a baseline):
  S86 nearly banked the arb_hits baseline from the four S85 runs (mean 11.25). Widening to the
  twenty debates of Aug 17-26 gave mean 8.3, because the last four days were already running
  ~3.5 above the sixteen before them, for reasons still unknown. Had the narrow window been
  used, a post-change reading of 11 would have scored as "no rise" while sitting three points
  above the true centre. A pre-registered threshold inherits every drift inside its window:
  state the window's SPAN and check its head against its tail before the threshold is fixed.

- R-S86-2 (Two instruments printing the same word may not be counting the same thing):
  GNI publishes arbitrator grounding hits twice. The per-run line prints
  `len(grounding_shadow['arb_hits'])`, and `mad_protocol.py:753` extends that bucket with
  `_g['hits']` ENTIRE - dialect spans included. `check_grounding`'s own `hit_count` (L299)
  excludes dialect, and the watch digest excludes it per GT-1. S86 called the two figures'
  near-equality a cross-instrument confirmation; it was a coincidence of scales. Before
  comparing two numbers that share a name, read the code that produces each. Near-agreement
  between differently-computed numbers is a FINDING about the difference, never corroboration.

- R-S86-3 (A conditional that never evaluates False is not a conditional):
  `mad_protocol.py:989`'s `_high_escalation` gates a hard-constraint block onto the Arbitrator
  prompt "for HIGH/CRITICAL only". Escalation is pinned CRITICAL on 109/110 scored reports, so
  the branch fired 6/6 across three measured days with zero variance, and the False path has
  never executed in production - nor in the selftest, whose fixture hardcodes
  `'escalation_level': 'CRITICAL'`. A feature described as conditional must have its branch
  RATE measured before it is reasoned about as a condition, and an untaken branch is untested
  code however old it is.

- R-S86-4 (A prompt is instantiated from the file's bytes, never from a chat transcript):
  S86 found the repo's PART D still headed `v3` while the file was v5, and still saying "The
  handoff is ATTACHED" while James's own paste said "The S84 close set is ATTACHED". Two agreed
  corrections from the S84 close had never reached the file, so the paste was AHEAD of the repo
  - the inverse of the drift Protocol v3 was built to stop, and invisible from either side
  alone. Therefore: at every open, PART D is copied from the highest-numbered protocol file and
  instantiated by substituting the session numbers; it is never copied from a chat, and a
  chat-authored amendment is never carried forward. Corollary of R-S82-4: when a close changes
  a prompt, the sweep is not done until the FILE holds the change.

- R-S86-5 (A refuted prediction may be naming a missing condition, not a wrong fix):
  `228634c` shipped five predictions. The first post-change run refuted three of them; the
  second satisfied all five exactly. The two runs differed in one measured variable -
  `assembled` 43 versus 39 - so the predictions were true within a boundary they had failed to
  state. Before a refuted prediction is read as a wrong ruling, diff the runs for the variable
  that moved; if one exists and explains the split, the finding is a missing CONDITION and
  belongs in the order as a trigger, not in the wrongness ledger as a bad call. This does not
  soften R-S83-4: the failure test must still be pre-registered, and a test that cannot fail is
  still a ceremony.

- R-S86-6 (Commit subjects carry intent that docs/ and conversation records do not):
  S86 read an always-on constraint block, found it enforced only the two pessimistic agents, and
  called it a bias defect. `git log -S 'NN-5' --oneline` returned one line - "hard correction
  channel - Black Swan + Ostrich enforced at code level for HIGH/CRITICAL" - which showed the
  asymmetry was deliberate and moved the defect to the stuck switch. `docs/` did not hold that
  design and the conversation search had not surfaced it. LINEAGE-BEV therefore has a third
  stage after `docs/` and `conversation_search`: `git log -S '<symbol>'` on the symbol about to
  be judged. Use it whenever the question is "why is this code shaped like this", because a
  commit subject is the only lineage written by the person who made the change.

- R-S87-1 (An ABSOLUTE threshold cannot measure a PRE-SELECTED set):
  `escalation_scorer` counts danger words in the 22 articles the funnel already chose as the
  most escalatory available. The question "are these tense?" is answered by the selection, not
  by the world, so the score saturates whatever the weights are. Replayed over 192 stored runs,
  THREE designs failed identically: Mar-24 Fix-2 (`base=min(sum,7)`) 192/192 CRITICAL, an
  actor-word tier 0 runs changed, a rupture-word tier 187/192. Before tuning weights or lists,
  ask WHO SELECTED THE SET BEING SCORED. If selection precedes scoring, only a relative or an
  uncapped-magnitude reading can carry information.

- R-S87-2 (A cap that is always at its limit is censorship, not a safety rail):
  Production wrote `raw_score 19` and published `10`. Across 192 runs the uncapped range is
  10.3-26.8 (median 19.2) and every published value is 10.0. The correct diagnosis of a stuck
  instrument is "the outputs are too UNIFORM", not "too HIGH" - the first is repaired by
  removing the clamp, the second by lowering the scale, and S87 proved the second repair does
  nothing. A cap only earns its name if it is reached sometimes.

- R-S87-3 (A single-regime corpus cannot be calibrated, only resolved):
  `pipeline_articles` begins 2026-05-24; the Hormuz crisis began in February. 100% of the
  measurable history sits inside one regime, so there is no pre-crisis baseline and a constant
  like "normal = 4-6" cannot be derived - hardcoding it would write the crisis in as normal and
  fail inverted when the world calms. Before fixing any constant, ask: WHAT IN MY DATA WOULD
  FALSIFY THIS NUMBER? If nothing could, it is a belief. Relative shape within the regime is
  still measurable; absolute levels are not.

- R-S87-4 (A shipped patch is not a wired feature - verify the CONSUMER CHAIN, not the edit):
  March 2026 added `score_breakdown` and `factors` to the scorer's return under GNI-R-117; the
  patch applied, `py_compile` passed, and the same session promised two front-end consumers.
  Five months later the fields were in the scorer's bytes, absent from `src/` entirely, and
  present in 0 of 191 database rows, because `main.py` copied 3 of the 7 returned fields into
  `report`. Producer + patch-applied proves nothing. Grep every consumer and check the store.

- R-S87-5 (MSYS/MINGW translates ARGUMENTS, not string literals - two proven bites):
  (a) `python - <<'PY'` with `open('/tmp/x')` inside fails while `wc -l < /tmp/x` in the same
  block succeeds: bash translates the redirect, the heredoc text is passed through untouched and
  Windows Python reads `C:\tmp`. Use paths relative to the repo (`../x.tsv`). (b) PROMOTED TRAP:
  `grep` silently ignores `--include` when the command also expands an unquoted variable of
  `--exclude-dir` flags; pass explicit PATHS on any census that matters.

- R-S87-6 (PROMOTED TRAP - scheduler lateness is a measured PROPERTY of the free tier, not an
  event): S86 recorded "the MAD schedule moved ~9.5h on Aug 27, cause unknown" and carried it as
  a trap. Measured over 133 scheduled runs since the Jun-23 cron move (`b27474e`, whose own
  subject reads "to reduce GHA scheduler drift"): median lateness 243 min in June, 177 in July,
  61 in August, tail past 10 hours - IMPROVING, not degrading - and ZERO runs missed in 67 days.
  Delivery is reliable; timing is not. Never infer run identity, novelty or ordering from the
  clock; use RUN ID, and for MAD use `ARB-FIT` to tell debate from grounding-watch.
  AMENDED 2026-08-30 (S88, promoting the S87 spacing trap on its second carry): where TWO
  schedulers lag INDEPENDENTLY, the GAP between them is a distribution, not the constant its
  cron comments claim. Measured over 8 pairs: real gap = 30 min designed MINUS (pipeline
  lateness - MAD lateness), median 15m02s, and on 2026-08-30 MAD `33318313852` STARTED at
  14:58:17Z while pipeline `33318041130` finished at 14:58:20Z - the order INVERTED by 3
  seconds with nothing raised. Pipeline duration is stable (6m02-6m35 over 12 runs), so the
  inversion law is exact: it flips whenever the lateness difference exceeds ~23m45s.

- R-S87-7 (PROMOTED TRAP - name the DENOMINATOR at the print site):
  `_arb_asm` prints `fits=N/assembled` and never against `available`, so a ratio read from the
  log answers a different question than the reader assumes; `check_grounding` computes
  `checked_spans` and discards it at the print (F-86-2); the per-run shadow line and the watch
  digest count hits on different scales with the same word (7.4). Three instances, one defect:
  a printed ratio whose denominator is not named at the call site cannot be compared to anything,
  and near-equality between two such numbers is a coincidence, not corroboration.

- R-S88-1 (SQL and shell must never share a paste block - `->` IS a redirection):
  A JSON-path query pasted into bash does not fail; bash reads `->` as `> file` and `->>` as
  `>> file` and CREATES those files. S88 produced two 0-byte files named `raw_score` and
  `score_breakdown-` this way. With a real filename in the path the same paste TRUNCATES that
  file to zero, silently, with exit status 0. Every SQL block is labelled SQL EDITOR ONLY and
  is delivered in its own message, never adjacent to a runnable shell block.

- R-S88-2 (A gate written for you is read LITERALLY; narrowing its scope is not judgement):
  The S87 LOAD CHECK said `design_bench.py` runs before any scorer OPINION. S88 reasoned that
  8.6 touched no threshold and therefore needed no bench - which was itself a scorer opinion.
  A gate's wording is the operator's instrument for catching exactly the reasoning that would
  skip it, so the moment a case for an exception feels sound is the moment to run the gate.

- R-S88-3 (Absence from the LIVE file is not a dropped item - read the generations between):
  S88 asserted that 5.1/5.2/5.3 and a whole retire roster had been silently dropped, because
  they were missing from generation 7 and no disposition appeared in it. One grep across
  `GNI_TARGET_AND_ORDER_S8*.md` showed S84 had closed all three explicitly and PROMOTED 5.2's
  fallback half to 1.10. The order is regenerated, not cumulative: disposition lives in the
  CHANGED THIS REGENERATION of the generation that made it, and nowhere else. Never charge the
  retire clause from the live file alone.

- R-S88-4 (Design the EXTRACTION for the question, or the command answers a different one):
  Three instrument failures in one session, all mine: `gh run view --log | head -60` returned
  60 lines of runner boilerplate and zero application output; `git log --oneline` was asked a
  question about DATES and carries none; `npm run build | tail -20` cut off the 40/40 page
  count the CONTRACT requires as the receipt. Name the FIELD the question needs and select it
  (`--json`, `--pretty='%h %ad %s'`, `grep -E 'Generating static'`); positional truncation is
  a guess about where the answer lives.

- R-S88-5 (A pillar at its CAP cannot be moved by editing its word list):
  8.7 proposed removing `ceasefire` from `GEO_SIGNALS` because it scores de-escalation as
  escalation. Replayed over 196 runs the change moved 0 runs, because GEO hits are min 8 /
  median 14 / max 19 against a cap of 5 - roughly half the 27-word list could be deleted with
  no arithmetic effect. Measure the pillar's headroom BEFORE proposing any list edit; where
  headroom is zero the only honest claims left are about the PUBLISHED evidence strings
  (`factors`, `signals_found`), not about the score. Extends R-S87-1 from thresholds to caps.
