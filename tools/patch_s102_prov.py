# S102 -- section 10.2 still cites the S99 snapshot while SLO-CFG and section 6
# both read S102. The figures are unchanged (both files yield 41 runs / 40 gaps
# / p50 4.34 / p90 7.31 / max 11.30 on 08-27..09-03, verified this session);
# only the provenance was stale. A document citing two sources for one number
# is the shape item 6.13 names.
import hashlib, sys
P = 'docs/GNI_ARCHITECTURE_S102.md'
with open(P, 'rb') as fh:
    b = fh.read()
EDITS = [
 (b"**MEASURED from `docs/gni_runtime_snapshot_S99.json`, window 2026-08-19 .. 2026-09-03,",
  b"**MEASURED from `docs/gni_runtime_snapshot_S102.json`, window 2026-08-19 .. 2026-09-03,"),
 (b"d = json.load(open('docs/gni_runtime_snapshot_S99.json', encoding='utf-8'))",
  b"d = json.load(open('docs/gni_runtime_snapshot_S102.json', encoding='utf-8'))"),
]
out = b
for i, (old, new) in enumerate(EDITS, 1):
    n = out.count(old)
    if n != 1:
        sys.stderr.write("EDIT %d MATCHED %d TIMES -- refusing to write\n" % (i, n))
        raise SystemExit(2)
    out = out.replace(old, new)
assert b"gni_runtime_snapshot_S99" not in out, "no S99 citation may survive"
assert out.count(b"gni_runtime_snapshot_S102.json") == 4   # sec 6, 10.2 prose, 10.2 probe, SLO-CFG
assert b"- SLO-CFG BOUND_HOURS: `8`" in out
assert (b'\r\n' in out) == (b'\r\n' in b)
with open(P, 'wb') as fh:
    fh.write(out)
print("PATCHED  %s" % P)
print("  md5 before %s" % hashlib.md5(b).hexdigest())
print("  md5 after  %s" % hashlib.md5(out).hexdigest())
