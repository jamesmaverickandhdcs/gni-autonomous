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
