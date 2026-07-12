# GT-2 SPEC (frozen S67) - conditional alias corpus expansion + compound
# head-noun fix. 1 file: ai_engine/analysis/mad_grounding_gate.py. Shadow-only.

## 1. ALIAS_GROUPS (normalized forms; ALL 10 verified live in 513-article
## 24h corpus, S67 Supabase check - R-S66-2 satisfied)
ALIAS_GROUPS = [
  {'federal reserve','the fed','us federal reserve','fed'},
  {'treasury','us treasury','us treasury department','treasury department'},
  {'european union','eu'},
  {'united states','us','usa','u s'},
  {'us iran conflict','us iran','conflict between the us and iran','us iran war'},
  {'iran','iranian','iranians'},
  {'russia','russian','russians'},
  {'israel','israeli','israelis'},
  {'taiwan','taiwanese'},
  {'europe','european','europeans'},
]

## 2. CONDITIONAL EXPANSION (in check_grounding, after _basket_corpus)
For each group: if ANY member present in basket_norm as a whole token/phrase
(padded check: f' {member} ' in f' {basket_norm} ' -- basket_norm is already
space-normalized), append ALL members to basket_norm (space-joined).
CONDITIONAL BY DESIGN: a Fed span against a Fed-free basket must STILL fire.
Never expand unconditionally. Quantities unaffected (they use basket_raw).

## 3. COMPOUND HEAD-NOUN FIX
STOP_HEADS = {'between','and','of','with','to','in','on','for','that','which'}
After a _COMPOUND_RE match: if the optional trailing lowercase word is in
STOP_HEADS, strip it from the span before normalization.

## 4. SELFTESTS (append to __main__; all existing tests stay green)
a) Superstring: basket containing 'Federal Reserve' -> span 'US Federal
   Reserve' grounded (no hit).
b) Negative control: Fed-free basket -> span 'Federal Reserve' -> entity hit
   (conditional expansion did NOT fire).
c) Head fix: 'silo-gap between the agencies' -> candidate normalizes to
   'silo gap' (dialect-bucketed by GT-1, not 'silo gap between').

## RULES: stdlib only, shadow-only, no caller/schema changes, no extractor
## widening beyond item 3.
