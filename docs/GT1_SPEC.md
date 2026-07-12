# GT-1 SPEC (frozen S67) - dialect bucket, shadow-safe, 2 files

## LEXICON (normalized = lowercase, punctuation stripped; James may strike lines)
DIALECT_PREFIXES (span startswith):
  hidden pattern | second order | third order | invisible link | silo gap | far reaching
DIALECT_EXACT:
  invisible broker | cascading effects | knock on effects
ARB_LIST_NOUNS (single abstract nouns from arb list-style output, digest-proven;
strike this block if too broad):
  cascading | contagion | erosion | emergence | diversification | disruption |
  cooperation | potential | establishment
Provenance: prefixes+invisible broker = verbatim in mad_protocol.py prompt
constants (grep S67). far reaching / cascading / knock on / list-nouns = filler,
not prompt-induced, zero attribution content.

## GATE (ai_engine/analysis/mad_grounding_gate.py)
1. Module consts: DIALECT_PREFIXES tuple, DIALECT_EXACT set, ARB_LIST_NOUNS set
   (all normalized forms).
2. In grounding test loop, BEFORE grounding check: if kind=='entity' and
   (norm in DIALECT_EXACT or norm in ARB_LIST_NOUNS or
   norm.startswith(DIALECT_PREFIXES)): append
   {span, kind:'dialect', location} to hits, do NOT increment hit_count,
   do NOT affect grounded, continue. checked_spans still increments.
3. Selftest add: text 'The hidden-pattern connection implies second-order
   effects via an invisible broker.' vs specimen basket -> expect >=3 hits all
   kind=='dialect', hit_count==0, grounded==True. All existing specimens +
   quantity + zero-FP tests must stay green.

## WATCH (ai_engine/analysis/grounding_watch.py)
4. _aggregate: consultant_hits/arb_hits counts EXCLUDE kind=='dialect'; new
   dialect_cons/dialect_arb counters; separate dialect span Counter
   (top 5). arb_flagged and RED trigger use non-dialect hits only.
   Legacy rows (hits without kind) count as NON-dialect (fail-loud default).
5. _build_digest: add one line when any dialect seen:
   'Dialect (allowlisted): {dc} consultant / {da} arb - top: ...'

## RULES: shadow-only, zero LLM calls, stdlib only, no caller/schema changes.
