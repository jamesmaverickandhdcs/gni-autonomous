# SRC-INTEGRITY DESIGN — S70 (2026-07-16)
Status: DESIGN ONLY. Shifter — ships AFTER FT-GAP-A window closes (James re-ratifies order:
FT-GAP-A -> SRC-INTEGRITY -> FT-GAP-B -> DET-DEAD). All findings byte-verified S70.

## ROOT CAUSE (one line)
`source_weights.weight` has TWO writers with incompatible formulas — the L-CLIFF disease
(dual source of truth) in DB form. Whichever runs last erases the other's learning.

## FINDINGS (all verified in bytes, S70)
| # | Finding | Where | Class |
|---|---------|-------|-------|
| I-1 | EMA writer: w = 0.7*old + 0.3*factor(1.5/1.0/0.7), clamp 0.5-2.0 — memory-preserving | source_weights.py update_source_weight(), called outcome_verifier.py:473 (every GPVS verify, cron since S60) | writer A |
| I-2 | Overwrite writer: w = 0.5 + cred*1.5 — NO memory, clobbers A | credibility_model.py update_credibility_scores(), called main.py:252 (every pipeline run) | writer B |
| I-3 | gpvs_wins/gpvs_total stored per-source are GLOBAL counts: loop re-fetches ALL outcomes, total=count(all rows), wins=round(score*total). Real per-source stats computed in calculate_credibility_scores() then discarded | credibility_model.py update loop | data corruption, /health displays it |
| I-4 | Case split: A writes lowercase ("bbc"), B writes title-case ("BBC") -> dup rows per source; funnel reader lowercases into dict -> last-row-wins, order not guaranteed -> nondeterministic weight | both writers + intelligence_funnel.py:446-448 | R-S64 kin |
| I-5 | `__main__` test block MUTATES LIVE DB: update_source_weight("BBC",1.0) + ("Fox News",0.0) on every standalone run | source_weights.py L155-172 | landmine (source of the false "Fox soft-zeroed at :166" lineage) |
| I-6 | Roster drift: DEFAULT_WEIGHTS=6 (lowercase), seed_initial_credibility=13 (title-case, fossil roster: no NPR/NYT/AllAfrica/Fox News World), collector=42. ~30 live sources have no seeded row anywhere -> ride weights.get(src,1.0) | three files | census |
| I-7 | Tier-map ghosts: The Economist, Foreign Policy, Project Syndicate, Financial Times in SOURCE_TIERS but not in 42-roster. NYT commented "reserve source" but promoted primary S68 (a95bd67). Fox News World unlisted -> TIER3/0pts | intelligence_funnel.py:363-393 | cosmetic + re-rule |

## FIX (single-writer principle)
1. **weight column owned by EMA path ONLY** (writer A). Writer B stops touching source_weights
   entirely — credibility_model computes and writes source_credibility ONLY.
2. In credibility_model: keep the REAL per-source wins/total from calculate_credibility_scores()
   and store those (fixes I-3). Delete the global-recount loop.
3. **Name normalization**: one `norm(source) = source.strip().lower()` helper in source_weights.py,
   used by BOTH writers and the funnel reader. One-time DB dedupe SQL (James, Supabase):
   merge case-dup rows keeping the freshest last_updated.
4. **Roster seeding**: seed source_weights + source_credibility from the collector roster (42)
   at neutral (1.0 / 0.75) — DEFAULT_WEIGHTS shrinks to fallback-only or derives from roster.
5. **Kill I-5**: `__main__` becomes read-only display (drop the two update calls).
6. Bridge (design decision for James): should credibility still INFLUENCE weight? Options:
   (a) No — GPVS EMA is the only weight mover (cleanest, credibility = dashboard evidence);
   (b) Yes, via EMA — writer B feeds cred through the SAME EMA formula instead of overwriting.
   LEAN: (a). Both signals derive from the same GPVS outcomes — B is a re-derivation of A's
   input, so blending them double-counts the same evidence.
7. I-7 rides along: delete 4 ghost tier entries, fix NYT comment, tier ruling for Fox News World
   comes from SRC_REEXAM (not this commit).

## PHILOSOPHY VERDICT (the "upgrade?" question James asked)
- NN-PHI-2 PASS: weights learn from outcomes, never sentiment. No direction filtering.
- NN-PHI-6 PASS: filter-to-protect is GNI's deliberate side of the May 26 GNI/Lens divergence.
- NN-PHI-1 GAP (real): source trust learns EXCLUSIVELY from market-direction correctness
  (direction_correct_3d) — "markets are one lens, not the purpose." The S35/36 GPVS
  human-security track never reached the weight formula. -> banked as SRC-PHI (B option),
  gated on the human-security metric existing.
- PHI-001 threshold: admission-time process by design (Mar 23 policy, James: "it has to be",
  >=50%, six equal criteria). Display-only runtime = correct. Scores frozen since March —
  the re-exam (SRC_REEXAM_S70.md) is the unfreeze.

## VERIFY BEFORE SHIP (BEV at window-open)
- Supabase: SELECT source, weight, gpvs_contribution, last_updated FROM source_weights ORDER BY source;
  (expect case-dup rows + last-writer evidence)
- SELECT source, gpvs_wins, gpvs_total FROM source_credibility LIMIT 10; (expect identical
  global totals across sources = I-3 in the wild)
- Re-read both files at window-open (model/session re-audit ritual — this doc is a LEAD then).

## RULE CANDIDATE
R-S70-1: Shared DB state gets shared-route discipline (R-S55-1 kin): any table gaining a new
writer triggers a WRITERS census — name every function writing each column; two writers with
different formulas for one column is a design review, not a merge. Audit the seam, not the files.

## EVIDENCE ADDENDUM (Supabase live-state, 2026-07-16)
- I-3 CONFIRMED: gpvs_total identical across sources (86 current era / 290 fossil era) — global count as per-source stat, live on /health.
- I-4 CONFIRMED: full case-dup table; divergence example BBC 0.8793 (ema, fresh) vs 1.47 (cred, frozen) = -1.2 vs +4.7 pts nondeterministic.
- I-8 NEW: writer B frozen since 2026-07-08 05:33:43 (all Title-Case rows one batch instant; lowercase rows fresh thru Jul 15). Called every run (main.py:252) but not landing — silent-exception class. Root-cause trace at ship time. NYT (promoted post-Jul 8) exists only lowercase — consistent.
- I-9 NEW: fossil graveyard — Middle East Eye/Bloomberg/Fox News/SCMP/Straits Times/The Hindu/Reuters-GN/Stimson etc. still in both tables; /health credibility board TOPPED by departed sources (MEE 0.929, Bloomberg 0.833, Fox News 0.738). Departed sources still receive EMA updates when old predictions verify (stimson fresh Jul 15) — dedupe SQL must also archive-or-purge ex-roster rows, and /health display should filter to live roster.
