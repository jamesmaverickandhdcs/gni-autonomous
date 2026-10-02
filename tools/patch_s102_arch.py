# S102 / order item 6.12 -- publish the fall.
# Creates docs/GNI_ARCHITECTURE_S102.md from S101's bytes. S101 is NEVER
# touched: freezing it keeps S102-F1 (the macro map's stale ARCHITECTURE
# stamp) reproducible instead of erasing the evidence with a regeneration.
# Pure ASCII source (GNI-L-015); the em dash is a byte constant.
import hashlib, os, sys

SRC = 'docs/GNI_ARCHITECTURE_S101.md'
DST = 'docs/GNI_ARCHITECTURE_S102.md'
EM  = b"\xe2\x80\x94"

if os.path.exists(DST):
    sys.stderr.write("%s ALREADY EXISTS -- refusing to write\n" % DST)
    raise SystemExit(2)
with open(SRC, 'rb') as fh:
    b = fh.read()
eol = b'\r\n' if b'\r\n' in b else b'\n'
J = lambda *L: eol.join(L)

EDITS = [
 (b"- SLO-CFG BOUND_HOURS: `12`",
  b"- SLO-CFG BOUND_HOURS: `8`"),

 (b"| **POST** | **2026-08-27 .. 09-03** | **41** | **29** | **12** | **5.33 h** | **11.05 h** | **30.61 h** |",
  J(b"| **POST** | **2026-08-27 .. 09-03** | **41** | **29** | **12** | **5.33 h** | **11.05 h** | **30.61 h** |",
    b"| **POST, S102 CODE** | **2026-08-27 .. 09-03** | **41** | **41** | **0** | **4.34 h** | **7.31 h** | **11.30 h** |")),

 (J(b"figures IS the SLO-1 violation, published rather than described.**"),
  J(b"figures IS the SLO-1 violation, published rather than described.**",
    b"",
    b"**At S102 that distance went to zero for POST.** Every run now performs its check, so",
    b"the third row's check figures ARE the run figures. That row is DERIVED from measured",
    b"timestamps under the shipped watcher, not observed " + EM + b" see SLO-1.")),

 (J(b'for lo, hi, tag in [("2026-08-19","2026-08-26","PRE "),',
    b'                    ("2026-08-27","2026-09-03","POST")]:',
    b'    run = [t for t in ts if lo <= t.strftime("%Y-%m-%d") <= hi]',
    b"    eff = [t for t in run if not in_pw(t)]"),
  J(b'for lo, hi, tag, sd in [("2026-08-19","2026-08-26","PRE       ", True),',
    b'                        ("2026-08-27","2026-09-03","POST      ", True),',
    b'                        ("2026-08-27","2026-09-03","POST S102 ", False)]:',
    b'    run = [t for t in ts if lo <= t.strftime("%Y-%m-%d") <= hi]',
    b"    eff = [t for t in run if not (sd and in_pw(t))]")),

 (J(b"**SLO-1 " + EM + b" DECLARED, MEASURED, AND CURRENTLY VIOLATED.**",
    b"`monitoring_pipeline.py:317-320` returns `True` before `_get_supabase_client()`, so a run",
    b"inside a protection window performs no divergence check, no consensus check and no",
    b"escalation delta read, and reports `success`."),
  J(b"**SLO-1 " + EM + b" DECLARED, MEASURED, VIOLATED, AND REMOVED AT S102.**",
    b"`monitoring_pipeline.py:317-321` returned `True` before `_get_supabase_client()`, so a run",
    b"inside a protection window performed no divergence check, no consensus check and no",
    b"escalation delta read, and reported `success`. The earlier citation here read `:317-320`,",
    b"which stopped one line short of the `return True` that was the mechanism.")),

 (J(b"The rule was applied outside its subject."),
  J(b"The rule was applied outside its subject.",
    b"",
    b"**REMOVED at S102 (order item 6.12).** The standdown is gone from the watcher;",
    b"`PROTECTION_WINDOWS` and the window helper remain, because `adaptive_pipeline.py:26,226`",
    b"still uses them and `GNI-R-122`, amended at S102, still binds adaptive and manual runs.",
    b"`C7` no longer assumes the standdown exists: `heartbeat_stands_down()` asks the tree by",
    b"AST, so the bound falls when that call goes and rises again if it returns. Fixture",
    b"families `17-standdown-absent` and `18-standdown-reinstated` differ by that one call and",
    b"by nothing else.",
    b"",
    b"**SLO-1 REMAINS UNWIRED, AND IS UNMEASURED AFTER THE FIX.** No heartbeat run has yet",
    b"executed the new code. Runs that used to stand down will now open a connection and can",
    b"therefore FAIL where they used to report `success`; that is the promise working, not a",
    b"regression. First post-fix measurement is owed.")),

 (J(b"**SLO-2 " + EM + b" PUBLISHED FRESHNESS BOUND: 12 hours.**",
    b"Derived, not chosen: current-regime check p90 is 11.05 h, and the bound is that value",
    b"rounded up to the next whole hour. **GNI's view of the world is no more than 12 hours old,",
    b"nine times out of ten.** Every public page stating a monitoring cadence states THIS number",
    b"with THIS window, never `0,30 * * * *`. The bound falls when SLO-1 is fixed; publishing it",
    b"is what makes that visible."),
  J(b"**SLO-2 " + EM + b" PUBLISHED FRESHNESS BOUND: 8 hours.**",
    b"Derived, not chosen: `C7` walks whole hours upward and stops at the first whose exceedance",
    b"is inside the budget. Before S102 that was 12 h over 28 check gaps; with the standdown gone",
    b"the same window yields 41 checks, 40 gaps, and 8 h. **GNI's view of the world is no more",
    b"than 8 hours old, nine times out of ten.** Every public page stating a monitoring cadence",
    b"states THIS number with THIS window, never `0,30 * * * *`. The bound FELL because SLO-1 was",
    b"fixed; publishing it is what made that visible.")),

 (J(b"At the published bound, 2 of the 28 POST check gaps exceed 12 h " + EM + b" **7.1%, inside the 10%",
    b"budget**. At 11 h, 4 of 28 exceed " + EM + b" **14.3%, outside it**. One hour of difference flips the",
    b"verdict, which is what makes the check discriminating rather than decorative."),
  J(b"At the published bound, 4 of the 40 POST check gaps exceed 8 h " + EM + b" **10.0%**. At 7 h, 6 of",
    b"40 exceed " + EM + b" **15.0%, outside the budget**. One hour of difference flips the verdict, which",
    b"is what makes the check discriminating rather than decorative.",
    b"",
    b"**DISCLOSED: this bound has ZERO margin.** 10.0% is ON the budget, not inside it. `C7`",
    b"accepts it because its test is `> budget` and `0.10 * 40` is exactly `4.0` in IEEE754 " + EM + b" a",
    b"property of forty gaps, not of the promise. At 39 gaps the budget is 3.9 and the same four",
    b"exceedances would derive 10 h instead. The number is correct for THIS window and is",
    b"sensitive to the window's size at the boundary. A reader who sees it move should look at",
    b"the gap count before looking at the schedule.")),
]

out = b
for i, (old, new) in enumerate(EDITS, 1):
    n = out.count(old)
    if n != 1:
        sys.stderr.write("EDIT %d MATCHED %d TIMES -- refusing to write\n" % (i, n))
        raise SystemExit(2)
    out = out.replace(old, new)

# R-S95-1: verified before the write.
assert out.count(b"- SLO-CFG BOUND_HOURS: `8`") == 1
assert b"- SLO-CFG BOUND_HOURS: `12`" not in out
assert out.count(b"POST, S102 CODE") == 1
assert b"`monitoring_pipeline.py:317-320`" not in out   # the live citation, not the note about it
assert out.count(b"ZERO margin") == 1
assert (b'\r\n' in out) == (b'\r\n' in b), "EOL regime changed"
assert len(out) > len(b)
with open(DST, 'wb') as fh:
    fh.write(out)
print("WROTE    %s   (%s untouched)" % (DST, SRC))
print("  src md5 %s  %d bytes" % (hashlib.md5(b).hexdigest(), len(b)))
print("  dst md5 %s  %d bytes" % (hashlib.md5(out).hexdigest(), len(out)))
