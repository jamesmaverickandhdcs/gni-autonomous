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
