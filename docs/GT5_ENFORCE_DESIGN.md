# GT-5-ENFORCE DESIGN (S72) -- recurrence break + consultant gating
Scope B ratified S72. Citation contract deferred -> banked as GT-6 (own arc, quality-monitored).
Evidence: TRACE_S71_EVE.md exhibits A/B, 7d digest 249c/68arb, Fed/DoE + Brazil-25% recurrence.

## PROBLEM (byte-verified S72)
History IS the saved report: _get_debate_history reads reports.mad_*_case last-3 [:150].
Loop: save(fabrication) -> next-run history -> prior authority -> Arbitrator repeats -> save again.
Two cut points: (1) snippet entering history, (2) consultant reply entering agent context.

## E-1 RECURRENCE BREAK (save-time scoring, read-time filtering)
- At report-save (basket in hand): run check_grounding per mad_*_case field
  (basket + report-title/summary whitelist, location='save_<agent>').
- Store per-field hits in reports.mad_grounding_hits (jsonb, additive column; NULL = unscored).
- _get_debate_history: skip snippet if its field hit_count > 0 (skip, not mask -- masked
  ellipses in [:150] snippets read as garbage to agents). Old NULL rows pass (fail-open).
- /debate display UNTOUCHED -- exhibits remain public; only the feedback loop is sanitized.

## E-2 CONSULTANT GATING (act on existing shadow verdicts)
- At each _shadow_check site: if reply hit_count >= T, exclude reply from downstream
  agent context; log 'GATED <label> <n> hits'. No re-prompt (quota 87%, cliff 31d).
- Excluded means replaced by neutral marker '[consultant reply withheld: ungrounded]'
  so round structure survives. Arbitrator never sees the fabricated text.
- T tuning: start T=3 (shadow data shows dialect excluded already; storm chatter ~1-2).
  One week observation via grounding_watch digest before considering T=2.

## NON-GOALS
- No prompt rewrites (S48/S49 regime-change dip). No re-prompting. No display changes.
- No backfill scoring of old reports (basket gone; NULL = honest unknown).

## BUILD PLAN (Claude Code, next session, spec to follow)
1. SQL: ALTER TABLE reports ADD COLUMN mad_grounding_hits jsonb;  (James)
2. Commit 1: save-time scoring + column write (mad_protocol save path).
3. Commit 2: _get_debate_history skip-if-hits filter.
4. Commit 3: _shadow_check gating + threshold const + GATED log line.
Self-certifies: next storm run shows 'GATED' lines and/or history excludes flagged
snippets; Fed/DoE lineage dies when its source reports age out of last-3.

## RISKS
- Over-gating in storms (agents starved) -> T=3 floor + fail-open on gate exception.
- check_grounding cost x4 fields at save: trivial (deterministic, no LLM).
- jsonb column additive -> zero migration risk; rollback = stop writing it.
