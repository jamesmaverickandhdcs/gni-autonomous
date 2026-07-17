# GT-5-ENFORCE BUILD SPEC -- for Claude Code (S73)
Repo: C:/HDCS_Project/03/GNI_Autonomous | HEAD at spec time: dc145b6
Design ratified S72: docs/GT5_ENFORCE_DESIGN.md (READ IT FULL FIRST -- it is authoritative;
this spec only operationalizes it). Memory: gt5-enforce-build.md is current.
Rules in force: GNI-R-076 (read full files before patching), LR-101 (ASCII anchors),
R-S72-1 (multi-line anchors join on DETECTED newline -- repo working copies are CRLF),
R-S59-1 (census every consumer before assuming one).

## PREREQUISITE (done by James before you run)
reports.mad_grounding_hits jsonb column EXISTS. Verify cheaply, do not assume.

## MISSION
Break the fabrication feedback loop (save->history->authority->repeat) and stop
ungrounded consultant text reaching agents. Reuses existing check_grounding from
ai_engine/analysis/mad_grounding_gate.py -- NO new extraction logic.

## BEV -- read IN FULL before any edit
- ai_engine/analysis/mad_protocol.py (whole file: _get_debate_history ~L293,
  _shadow_check ~L655, report save path -- line numbers are LEADS, re-grep)
- ai_engine/analysis/mad_grounding_gate.py (signature + basket field names;
  S61 memory says grounding matches title/summary/ENTITIES, not keywords -- confirm)
- The save path MUST have the basket in scope at save time. If it does not,
  STOP and report -- do not plumb the basket through new parameters without approval.
- Census: grep every writer of reports mad_*_case fields and every caller of
  _get_debate_history before assuming single sites.

## COMMIT 1 -- E-1a save-time scoring
At report save (basket in hand): run check_grounding on each mad_*_case field
(whitelist = report title + summary; location='save_<agent>'). Build
{"<field>": {"hit_count": n, "hits": [...]}} and write to mad_grounding_hits.
Fail-open: any exception in scoring -> log + save report WITHOUT the column value.
Zero change to report text or any other field.

## COMMIT 2 -- E-1b history skip-filter
_get_debate_history: when a row has mad_grounding_hits and the snippet's field
hit_count > 0 -> SKIP that snippet entirely (skip, not mask). NULL/absent
column value -> include (fail-open, old rows unscored = honest unknown).
/debate display and every other reader: UNTOUCHED.

## COMMIT 3 -- E-2 consultant gating
At each _shadow_check site (census them all): if reply hit_count >= T (module
const GROUNDING_GATE_T = 3), replace reply in downstream agent context with
'[consultant reply withheld: ungrounded]' and log 'GATED <label> <n> hits'.
No re-prompt ever (quota). Shadow logging itself stays intact.
Fail-open: gate exception -> pass reply through ungated + log.

## CONSTRAINTS (hard)
- $0, stdlib only, no new deps. No prompt rewrites. No re-prompting.
- No backfill of old reports. /debate display untouched.
- Three separate reviewable diffs (one per commit above); James commits/pushes.
  Do NOT run git add/commit/push. After each: python -m py_compile on touched files.
- If real code contradicts this spec or the design (shapes, field names, seam
  structure), STOP and report -- never improvise.

## ACCEPTANCE (self-verify, show output)
[ ] py_compile clean on every touched file, all 3 diffs
[ ] Synthetic test: fabricated span in a mad_*_case vs basket lacking it ->
    hit_count > 0 recorded; grounded field -> 0
[ ] History filter test: row with hits -> snippet absent; NULL row -> present
[ ] Gate test: reply with >=3 hits -> withheld marker + GATED log;
    2 hits -> passes untouched
[ ] grep proof: no writes to /debate render path, no prompt text changed
