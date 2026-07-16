# SRC-INTEGRITY BUILD SPEC -- S71 (2026-07-16) -- brief for Claude Code
Authority: docs/SRC_INTEGRITY_DESIGN.md (I-1..I-9) + S71 RATIFIED: R1-R4, bridge (a), window order.
Builder rules: BEV -- read ALL target files whole before editing. py_compile after every python edit.
One commit per section. Stage files explicitly (never add -A). James runs every git command.
DO NOT TOUCH: EMA formula/clamp, TIER_BONUS values, scoring/selection logic, outcome_verifier.py, main.py.

## COMMIT 1 -- single-writer + norm + seed (analysis/source_weights.py + analysis/credibility_model.py)
- source_weights.py: add helper `norm(source) = source.strip().lower()` near top.
- update_source_weight(): key rows by norm(source); get_source_weights(): cache keys via norm().
- __main__ (I-5): DELETE the two update_source_weight test calls -- read-only display.
- credibility_model.py rewrite of update_credibility_scores() (I-2/I-3):
  - calculate_credibility_scores() also returns REAL per-source wins/total (restructure return).
  - Upsert source_credibility with real wins/total; DELETE global outcomes re-fetch loop (51 fetches).
  - DELETE the source_weights upsert block entirely -- writer B never writes weights again (bridge (a)).
  - Key upserts by norm(source) (import from analysis.source_weights).
- Seeding (I-6): replace 13-source fossil in seed_initial_credibility -- seed BOTH tables from the
  collector's canonical 42-roster (import the list, don't copy it) at 1.0 weight / 0.75 cred, norm keys,
  insert-if-missing only.
- VERIFY: py_compile both; grep credibility_model.py for source_weights TABLE writes == 0; __main__ clean.

## COMMIT 2 -- TIER-TRUE (funnel/intelligence_funnel.py) [R2/R3 RATIFIED]
- 'New York Times': -> 'TIER1', delete its "# reserve source" comment only.
- ADD TIER1: 'Crisis Group', 'Amnesty International', 'ICIJ' -- verify exact roster spellings first + not already listed.
- DELETE ghosts (I-7, verify absent from 42-roster first): 'The Economist', 'Foreign Policy', 'Project Syndicate', 'Financial Times'.
- Fox News World: leave unlisted (TIER3 default) -- no tier ruling exists.
- Funnel weights reader: use norm() from analysis.source_weights.
- VERIFY: py_compile; per-edit grep count == 1.

## COMMIT 3 -- /health roster filter (frontend)
- Credibility board currently TOPPED by departed sources (MEE 0.929, Bloomberg 0.833) -- filter to live roster.
- Locate component + API route; filter where cheapest. npm run build 40/40 before commit.

## JAMES-ONLY -- one-time Supabase SQL at ship (AFTER commit 1 deployed)
- Dedupe case-dups in source_weights AND source_credibility -> norm keys, keep freshest timestamp.
- Archive-or-purge ex-roster rows (I-9): MEE, Bloomberg, Fox News, SCMP, Straits Times, The Hindu,
  Reuters-GN, Stimson + the 4 ghosts. Chat-Claude drafts exact SQL against live state at ship.

## NOTES
- I-8 CLOSED-BY-EVIDENCE: writer B periodic, landed 2026-07-16 11:56:24 batch and stomped writer A same-run
  (TRACE_S71_EVE). Cadence = main.py:252 call condition; harmless once weight-write removed.
- Reader nondeterminism (case-dup last-row-wins) dies with norm + dedupe SQL.
- SRC-PHI (NN-PHI-1) stays banked -- NOT in this build.
