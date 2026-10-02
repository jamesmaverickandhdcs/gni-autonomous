#!/usr/bin/env python3
"""tools/patch_s103_row4.py -- item 5.50's last DoD clause.

Updates roadmap 2's completion-test status table in the LIVE architecture from
BYTES: what S103 closed, what it did not, and the reason roadmap 2 is not four
of four (DECISION S103-1).

Pure ASCII source; the section sign is a byte constant (GNI-L-015 discipline, and
the shape S102's own patches used). Binary mode throughout (GNI-L-001). Every
anchor must match exactly once or nothing is written (R-S95-1). Re-running is
refused rather than duplicated.

Run from the repo root:  python tools/patch_s103_row4.py
"""
import hashlib
import os
import re
import sys

S = b"\xc2\xa7"
DOCS = "docs"


def die(msg):
    print("ABORT: %s" % msg)
    sys.exit(1)


def live_architecture():
    """Highest generation, selected by RELATION and never by lexical sort
    (R-S92-2) -- the same rule the detector's live_docs uses."""
    pat = re.compile(r"^GNI_ARCHITECTURE_S(\d+)\.md$")
    gens = [(int(m.group(1)), n) for n in os.listdir(DOCS)
            for m in [pat.match(n)] if m]
    if not gens:
        die("no GNI_ARCHITECTURE_S*.md under %s/" % DOCS)
    return os.path.join(DOCS, max(gens)[1])


OLD_HEAD = (b"### STATUS OF THE COMPLETION TEST AT THE S102 CLOSE "
            b"(three of four rows hold)")

NEW_HEAD = (b"### STATUS OF THE COMPLETION TEST AT THE S103 CLOSE "
            b"(three of four; row four is half closed)")

OLD_ROW4 = (
    b"| 4 | **PARTIAL - THE ONLY ROW LEFT** | `rule_checks` exits 0 on a clean "
    b"tree and goes RED on a stale " + S + b"7 (C2, family `5-stale-generator`) "
    b"and on a stale macro map (C6, families `12-map-stale-count` and "
    b"`13-map-stale-md5`). But C6 reads ONLY the register's `INPUT` line: the "
    b"map declares one for the register and one for this document, and an "
    b"architecture that has moved underneath the map is SILENT. Demonstrated "
    b"four times at S102, twice by accident. There is no staleness check for "
    + S + b"5 or " + S + b"6 at all. Item **5.50** is what closes this row. |")

NEW_ROW4 = (
    b"| 4 | **PARTIAL - THE MAP HALF IS CLOSED, THE SECTION HALF IS NOT** | "
    b"`rule_checks` exits 0 on a clean tree and goes RED on a stale " + S + b"7 "
    b"(C2, family `5-stale-generator`) and on the macro map in BOTH of its "
    b"failure shapes (C6, rewritten at S103 for item **5.50**): a stamped md5 "
    b"that no longer matches the live file, AND a source RENAMED out from under "
    b"the map while the file it names still exists and still hashes to exactly "
    b"the stamped value. C6 now loops over every `INPUT ... md5` line the map "
    b"declares, resolves each to the LIVE file of its family rather than to the "
    b"file the line names, and holds no count of inputs anywhere; families "
    b"`19-map-stale-arch-md5`, `20-map-arch-renamed` and `21-map-third-input` "
    b"cover it. Certified against real commits, not invented trees: at "
    b"`b7eaab4` the old check reports PASS and 7 checked 0 failed on the same "
    b"tree where the new one reports the architecture md5 `a4fb9fce` against "
    b"the map's stamped `0d944f64`, and at `3268c14` the new one reports a "
    b"RENAME with no md5 in it at all. **" + S + b"5 and " + S + b"6 still have "
    b"NO staleness check of any kind.** That is measured, not hypothetical: "
    + S + b"5 shipped at the S102 close stamping `86 tracked *.py` while the "
    b"tree at that close held 89, wrong by three from the moment it was "
    b"published, and seen by nothing until S103 re-ran the generator. Item "
    b"**5.54** is what closes the remaining half. |")

OLD_TAIL = (
    b"The failing rows are named, which is the point of the test. **Roadmap 2 "
    b"is 3 of 4**, and the one\nremaining row names the item that closes it. "
    b"This table was the S98 table for four closes while two\nof its rows had "
    b"quietly become true; a scoreboard nobody re-runs is a claim, not a "
    b"measurement.")

NEW_TAIL = (
    b"The failing rows are named, which is the point of the test. **Roadmap 2 "
    b"is 3 of 4**, and row four is\nstill the one left. S103 closed the half of "
    b"it that item 5.50 named and did NOT close the row.\n\n"
    b"**DECISION S103-1 (James), ruled at the S103 open, before the work:** the "
    b"row is read AS WRITTEN. It\nnames four surfaces - " + S + b"5, " + S +
    b"6, " + S + b"7 and the macro map - and the S98 status table recorded "
    + S + b"5 and\n" + S + b"6 as ABSENT rather than as excluded, so the row "
    b"was waiting for them rather than ignoring them.\nThe row's own published "
    b"command settles it without interpretation: flip a " + S + b"5 figure "
    b"today and\n`rule_checks` still exits 0. Reading the row narrowly would "
    b"have bought a fourth row by\ninterpretation - which is the one way this "
    b"scoreboard has never yet been wrong, and the reason it\nwas wrong for "
    b"four closes is that nobody re-ran it, not that anybody argued with it.")


def main():
    path = live_architecture()
    print("live architecture: %s" % path)
    with open(path, "rb") as fh:
        b = fh.read()
    print("  read %d bytes  nl=%s" % (len(b), "CRLF" if b"\r\n" in b else "LF"))

    if b"5.54" in b or b"THE MAP HALF IS CLOSED" in b:
        die("already patched -- nothing written")

    out = b
    for i, (old, new) in enumerate(
            ((OLD_HEAD, NEW_HEAD), (OLD_ROW4, NEW_ROW4), (OLD_TAIL, NEW_TAIL)), 1):
        n = out.count(old)
        if n != 1:
            die("edit %d matched %d times, need exactly 1" % (i, n))
        out = out.replace(old, new)
        print("  edit %d ok  (%d -> %d bytes)" % (i, len(old), len(new)))

    # verification BEFORE the write (R-S95-1)
    checks = [
        (out.count(b"Roadmap 2\nis 3 of 4") + out.count(b"**Roadmap 2 is 3 of 4**") == 1,
         "the 3-of-4 figure must appear exactly once"),
        (b"AT THE S102 CLOSE" not in out, "the S102 heading must be gone"),
        (b"THE ONLY ROW LEFT" not in out, "the old row-four verdict must be gone"),
        (out.count(b"DECISION S103-1") == 1, "the ruling must be recorded once"),
        (out.count(b"**5.54**") == 1, "the item that closes the remaining half"),
        ((b"\r\n" in out) == (b"\r\n" in b), "line endings must be unchanged"),
        (len(out) > len(b), "the patch only adds"),
    ]
    for ok, what in checks:
        if not ok:
            die("post-edit assertion FAILED: " + what)
    print("  assertions %d/%d" % (len(checks), len(checks)))

    with open(path, "wb") as fh:
        fh.write(out)
    print("PATCHED %s" % path)
    print("  md5 before %s" % hashlib.md5(b.replace(b"\r\n", b"\n")).hexdigest())
    print("  md5 after  %s" % hashlib.md5(out.replace(b"\r\n", b"\n")).hexdigest())
    print("\nNEXT, and the order is load-bearing: regenerate the macro map LAST.")


if __name__ == "__main__":
    main()
