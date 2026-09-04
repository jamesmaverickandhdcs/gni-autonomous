#!/usr/bin/env python3
"""S99 close: update ROADMAP 2's row and completion-test row 2 in docs/GNI_ARCHITECTURE_S99.md.

This is a PATCH SCRIPT, not a download, because that file holds the GENERATED section 6 that
only the repo has -- shipping a rebuilt copy would overwrite generated content with a guess.
Binary mode (LR-078). Anchors are UTF-8-encoded from readable text rather than typed as escapes,
because the target lines contain a section sign; LR-101's ASCII rule guards `python -c` command
lines, and this is a file. Asserts the NEW text is ABSENT first, so a double paste is safe.
"""
import sys

P = "docs/GNI_ARCHITECTURE_S99.md"
try:
    d = open(P, "rb").read()
except FileNotFoundError:
    print("MISSING: %s -- run this from the repo root" % P, file=sys.stderr)
    sys.exit(3)

if "roadmap 2 row 2 shipped at S99".encode("utf-8") in d:
    print("ALREADY PATCHED -- nothing written")
    sys.exit(0)

EDITS = [
    ("| S99 | ARCHITECTURE \u00a76 Runtime View, GENERATED | what calls what, without a grep |",
     "| S99 | \u2705 **DONE** -- `2bfef91`, CI run `33851242047` green at JOB level "
     "(roadmap 2 row 2 shipped at S99) | delivered cadence measured against declared cadence, "
     "regenerating byte-identically from a tracked snapshot |"),

    ("| 2 | **NO** | only \u00a77 is generated (`tools/gni_state.py`, S94). \u00a75 and \u00a76 are S100 and S99. |",
     "| 2 | **NO** | \u00a76 is generated and byte-identical (`tools/gni_runtime.py`, S99, md5 "
     "`fb6e3f1e0e96e6a696af988b08bb6143` on two renders). \u00a75 is S100. **AND \u00a77 FAILS THIS ROW ON "
     "ITS OWN ACCOUNT** -- `gni_state.py` renders `datetime.now()` into its own stamp, so two runs "
     "two seconds apart differ (`06:14:00Z` vs `06:14:04Z`). Item **5.33**. The S98 status recorded "
     "this row as failing only because \u00a75 and \u00a76 were missing; that was incomplete. |"),
]

for old, new in EDITS:
    ob, nb = old.encode("utf-8"), new.encode("utf-8")
    n = d.count(ob)
    if n != 1:
        print("ANCHOR matched %d times -- ABORT, nothing written:\n  %s" % (n, old[:76]),
              file=sys.stderr)
        sys.exit(2)
    d = d.replace(ob, nb)

open(P, "wb").write(d)
print("PATCHED %s (%d bytes, %d edits)" % (P, len(d), len(EDITS)))
