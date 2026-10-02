#!/usr/bin/env python3
"""tools/patch_s104_protocol.py - PART C step 11, PROTOCOL v18.

Resolves the LIVE protocol by RELATION (R-S92-2) and writes it forward as
`docs/GNI_Session_Transfer_Protocol_S104.md`. PART A, PART B and PART D are
byte-identical to v17; PART C changes in one line.

WHAT CHANGED AND WHY IT IS NOT A BUMP. Step 9a printed `(expect 7 checked,
0 failed)`. That number is now 8. **This is the SECOND time.** The v16 log
records the first in its own words: "the step's own expected detector count
still said six after a seventh check shipped - the step written to catch
staleness had gone stale." v16 corrected the value. Correcting the value
guarantees a third occurrence, and the third is here.

A count is STATE. A template is LAW. The file's own LAW-VS-STATE TEST is
printed above PART C's prompt - if a template needs editing most sessions,
state has leaked into it - and this is that leak, measured twice. It is also
the identical defect R-S104-1 forbids inside a check, committed in prose one
document away from the check that forbids it. So the number is REMOVED rather
than raised, and the expectation is stated in the form that cannot go stale.

Binary mode (GNI-L-001); every anchor is pure ASCII (GNI-L-015).
    python tools/patch_s104_protocol.py
"""
import os
import re
import sys

PROTO_RE = re.compile(r"^GNI_Session_Transfer_Protocol_S(\d+)\.md$")
OUT = "docs/GNI_Session_Transfer_Protocol_S104.md"

NEW_STEP = (
    "      `python tools/gni_rule_checks.py .`      (expect 0 FAILED - the NUMBER of checks is "
    "state, not law, and is deliberately not written here; see the v18 log)"
)

V18 = """- **v18 - S104 (2026-09-10).** PART C step 9a, ONE LINE. PART A, PART B and PART D are
  byte-identical to v17. The step printed an expected detector count and that count went stale
  for the SECOND time - v16's own log records the first, when it "still said six after a seventh
  check shipped", and v16's remedy was to write seven. S104 shipped an eighth. Correcting the
  value is what guarantees the next occurrence, so the value is REMOVED: the step now expects
  ZERO FAILED and says why the number is absent. A count is STATE and this file is LAW, which is
  the LAW-VS-STATE TEST printed three paragraphs above the prompt itself; and it is the same
  defect R-S104-1 forbids inside a check, committed in prose one document away from the check
  that forbids it. The step written to catch staleness had gone stale twice, in a repository
  whose entire target is that published claims stay true. No CONTRACT bump: this removes a figure,
  not an authority.

"""


def fail(msg):
    print("REFUSED: %s" % msg)
    print("Nothing written.")
    sys.exit(2)


def main():
    gens = [(int(m.group(1)), n) for n in os.listdir("docs")
            for m in [PROTO_RE.match(n)] if m]
    if not gens:
        fail("no protocol under docs/")
    live = os.path.join("docs", max(gens)[-1])
    print("LIVE (by RELATION): %s" % live)
    if os.path.exists(OUT):
        fail("%s already exists" % OUT)

    blob = open(live, "rb").read()
    if b"\r\n" in blob:
        fail("%s holds CRLF; this patch assumes LF" % live)
    lines = blob.split(b"\n")

    edits = [
        (b"# GNI SESSION TRANSFER PROTOCOL v17",
         b"# GNI SESSION TRANSFER PROTOCOL v18", "the version heading"),
        (b"      `python tools/gni_rule_checks.py .`      (expect ",
         NEW_STEP.encode("utf-8"), "step 9a's expected count"),
    ]
    for prefix, new, label in edits:
        hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
        if len(hits) != 1:
            fail("prefix for %r matches %d lines" % (label, len(hits)))
        print("  ok  %s  (line %d)" % (label, hits[0] + 1))
        print("      was: %s" % lines[hits[0]].decode("utf-8").strip()[:88])
        lines[hits[0]] = new

    log = [i for i, l in enumerate(lines) if l.startswith(b"## VERSION LOG")]
    if len(log) != 1:
        fail("found %d version logs" % len(log))
    at = log[0] + 2
    lines[at:at] = V18.rstrip("\n").encode("utf-8").split(b"\n") + [b""]
    print("  ok  v18 log entry  (after line %d)" % (log[0] + 1))

    out = b"\n".join(lines)
    if b"\r\n" in out:
        fail("this patch introduced CRLF")
    open(OUT, "wb").write(out)
    print("WROTE %s  %d bytes  (was %d)" % (OUT, len(out), len(blob)))

    txt = out.decode("utf-8")
    if re.search(r"expect \d+ checked", txt):
        fail("a hard-coded check count survived the patch")
    print("  no `expect N checked` survives anywhere in the file")
    return 0


if __name__ == "__main__":
    sys.exit(main())
