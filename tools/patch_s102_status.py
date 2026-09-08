# S102 (reopened at close) -- the roadmap 2 STATUS table has been the S98 table
# for four closes. Item 5.46. Re-run today: rows 2 and 3 hold, row 4 is the only
# one left and it names its own fix. Pure ASCII source (LR-101); the section
# sign is a byte constant.
import hashlib, sys
P = 'docs/GNI_ARCHITECTURE_S102.md'
S = b"\xc2\xa7"
with open(P, 'rb') as fh:
    b = fh.read()
E = [
 (b"### STATUS OF THE COMPLETION TEST AT THE S98 CLOSE (row 1 of roadmap 2 shipped)",
  b"### STATUS OF THE COMPLETION TEST AT THE S102 CLOSE (three of four rows hold)"),

 (b"| 2 | **NO** | " + S + b"6 is generated and byte-identical (`tools/gni_runtime.py`, S99, md5 `fb6e3f1e0e96e6a696af988b08bb6143` on two renders). " + S + b"5 is S100. **AND " + S + b"7 FAILS THIS ROW ON ITS OWN ACCOUNT** -- `gni_state.py` renders `datetime.now()` into its own stamp, so two runs two seconds apart differ (`06:14:00Z` vs `06:14:04Z`). Item **5.33**. The S98 status recorded this row as failing only because " + S + b"5 and " + S + b"6 were missing; that was incomplete. |",
  b"| 2 | **YES** | S102, measured rather than assumed: each generator was rendered TWICE two seconds apart and `cmp` reports the pair identical. `gni_blocks` md5 `8796c4c5522be2dd22db384e50b88531`, `gni_state` `480406a42d19a837f4d1f4ad2885db9c`, `gni_runtime` `e620e7e317ee6f72b9267e26566d8705`. The row flipped at S100, when item **5.33** removed `gni_state.py`'s own clock; nobody re-ran the test for four closes, which is exactly what item **5.46** is about. |"),

 (b"| 3 | **NO** | no SLO is written. S101. |",
  b"| 3 | **YES** | S101 wrote SLO-1, SLO-2 and SLO-3 into " + S + b"10 with an error budget. S102 republished SLO-2's measured value: bound 8 h, DERIVED as the smallest whole hour inside the budget rather than chosen, with the probe that produced it printed beside it in " + S + b"10.2 and its zero margin disclosed. |"),

 (b"| 4 | **PARTIAL** | `rule_checks` exits 0 clean and RED on a stale macro map (C6, item 5.26, `1d5bcab`) and on a stale " + S + b"7 (C2, fixture family `5-stale-generator`). " + S + b"5 and " + S + b"6 cannot be stale because they do not exist. |",
  b"| 4 | **PARTIAL - THE ONLY ROW LEFT** | `rule_checks` exits 0 on a clean tree and goes RED on a stale " + S + b"7 (C2, family `5-stale-generator`) and on a stale macro map (C6, families `12-map-stale-count` and `13-map-stale-md5`). But C6 reads ONLY the register's `INPUT` line: the map declares one for the register and one for this document, and an architecture that has moved underneath the map is SILENT. Demonstrated four times at S102, twice by accident. There is no staleness check for " + S + b"5 or " + S + b"6 at all. Item **5.50** is what closes this row. |"),

 (b"The failing rows are named, which is the point of the test. Roadmap 2 is **1 of 4**.",
  b"The failing rows are named, which is the point of the test. **Roadmap 2 is 3 of 4**, and the one\nremaining row names the item that closes it. This table was the S98 table for four closes while two\nof its rows had quietly become true; a scoreboard nobody re-runs is a claim, not a measurement."),
]
out = b
for i, (old, new) in enumerate(E, 1):
    n = out.count(old)
    if n != 1:
        sys.stderr.write("EDIT %d MATCHED %d TIMES -- refusing to write\n" % (i, n))
        raise SystemExit(2)
    out = out.replace(old, new)
assert out.count(b"Roadmap 2 is 3 of 4") == 1
assert b"AT THE S98 CLOSE" not in out
assert b"| 3 | **NO** |" not in out and b"| 2 | **NO** |" not in out
assert b"- SLO-CFG BOUND_HOURS: `8`" in out
assert (b'\r\n' in out) == (b'\r\n' in b)
with open(P, 'wb') as fh:
    fh.write(out)
print("PATCHED  %s" % P)
print("  md5 before %s" % hashlib.md5(b).hexdigest())
print("  md5 after  %s" % hashlib.md5(out).hexdigest())
