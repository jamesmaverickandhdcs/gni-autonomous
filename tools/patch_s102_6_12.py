# S102 / order item 6.12 -- remove the GNI-R-122 standdown from the heartbeat.
# Binary mode throughout (LR-078): the file carries a BOM and this must not
# decode/re-encode it. EOL is detected from the bytes, never assumed.
import hashlib, sys

P = 'ai_engine/monitoring_pipeline.py'
with open(P, 'rb') as fh:
    b = fh.read()

eol = b'\r\n' if b'\r\n' in b else b'\n'

OLD = eol.join([
    b"    # -- Check protection window first (GNI-R-122)",
    b"    if is_protection_window(now):",
    b"        print('PROTECTION WINDOW ACTIVE -- suspending all checks')",
    b"        print('Sacred pipeline run imminent -- heartbeat standing down')",
    b"        return True",
    b"",
    b"",
])

NEW = eol.join([
    b"    # -- GNI-R-122 standdown REMOVED (S102, order item 6.12).",
    b"    #    The windows bind ADAPTIVE and MANUAL runs; the heartbeat is",
    b"    #    neither, and spends zero Groq (GNI-R-114). Suppressing it",
    b"    #    produced a run that performed no check and still exited 0.",
    b"    #    PROTECTION_WINDOWS and is_protection_window() are UNCHANGED:",
    b"    #    adaptive_pipeline.py:26,226 still imports and calls them.",
    b"",
    b"",
])

n = b.count(OLD)
if n != 1:
    sys.stderr.write("ANCHOR MATCHED %d TIMES -- refusing to write\n" % n)
    raise SystemExit(2)

out = b.replace(OLD, NEW)

# R-S95-1: verification computed BEFORE the write.
assert b"is_protection_window(now)" not in out.split(b"def run_monitoring_pipeline")[1], \
    "standdown still reachable in run_monitoring_pipeline"
assert b"PROTECTION_WINDOWS = [" in out, "PROTECTION_WINDOWS lost -- C7 would break"
assert b"def is_protection_window" in out, "function lost -- adaptive_pipeline import would break"
assert out[:3] == b[:3], "BOM changed"
assert (b'\r\n' in out) == (b'\r\n' in b), "EOL regime changed"

with open(P, 'wb') as fh:
    fh.write(out)

print("PATCHED  %s" % P)
print("  md5 before %s  %d bytes" % (hashlib.md5(b).hexdigest(), len(b)))
print("  md5 after  %s  %d bytes" % (hashlib.md5(out).hexdigest(), len(out)))
