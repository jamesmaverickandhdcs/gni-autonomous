import hashlib, sys
P = 'ai_engine/monitoring_pipeline.py'
with open(P, 'rb') as fh:
    b = fh.read()
OLD = b"    #    PROTECTION_WINDOWS and is_protection_window() are UNCHANGED:"
NEW = b"    #    The window table and its helper are UNCHANGED; see line 122:"
n = b.count(OLD)
if n != 1:
    sys.stderr.write("ANCHOR MATCHED %d TIMES -- refusing to write\n" % n); raise SystemExit(2)
out = b.replace(OLD, NEW)
assert out.count(b"is_protection_window") == b.count(b"is_protection_window") - 1
assert out[:3] == b[:3] and (b'\r\n' in out) == (b'\r\n' in b)
with open(P, 'wb') as fh: fh.write(out)
print("PATCHED  %s" % P)
print("  md5 before %s" % hashlib.md5(b).hexdigest())
print("  md5 after  %s" % hashlib.md5(out).hexdigest())
