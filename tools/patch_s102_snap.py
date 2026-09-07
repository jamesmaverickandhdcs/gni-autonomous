# S102 / order item 6.12, DoD clause 3 -- point C7 at a FRESHLY harvested
# snapshot. Two independent harvests three days apart agree exactly on the
# published window (41 runs, 40 gaps, p90 7.31, bound 8), so the bound is a
# property of the runs and not of the committed file. Also retires the S99
# snapshot's name/stamp/data disagreement (item 6.14) by not reading it.
import hashlib, sys

P = 'docs/GNI_ARCHITECTURE_S102.md'
with open(P, 'rb') as fh:
    b = fh.read()

OLD = b"- SLO-CFG SNAPSHOT: `docs/gni_runtime_snapshot_S99.json`"
NEW = b"- SLO-CFG SNAPSHOT: `docs/gni_runtime_snapshot_S102.json`"

n = b.count(OLD)
if n != 1:
    sys.stderr.write("ANCHOR MATCHED %d TIMES -- refusing to write\n" % n)
    raise SystemExit(2)
out = b.replace(OLD, NEW)

assert out.count(NEW) == 1 and OLD not in out
assert b"- SLO-CFG BOUND_HOURS: `8`" in out, "the bound must survive"
assert (b'\r\n' in out) == (b'\r\n' in b)
with open(P, 'wb') as fh:
    fh.write(out)
print("PATCHED  %s" % P)
print("  md5 before %s" % hashlib.md5(b).hexdigest())
print("  md5 after  %s" % hashlib.md5(out).hexdigest())
