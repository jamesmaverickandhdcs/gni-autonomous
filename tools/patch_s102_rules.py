# S102 / order item 6.12 -- register the GNI-R-122 amendment.
# Creates docs/GNI_RULES_S102.md from S101's bytes. S101 is NEVER touched.
# The amendment is a CONTINUATION of the existing bullet, exactly like the
# INSTANCE (S101) block above it: the id is not re-declared, so C3 sees no
# duplicate definition. NO second **CHECKABLE:** marker is added -- the entry
# already carries `yes`, and a second marker would put GNI-R-122 in the macro
# map's AMBIGUOUS bucket without adding a fact.
import hashlib, os, sys

SRC = 'docs/GNI_RULES_S101.md'
DST = 'docs/GNI_RULES_S102.md'

if os.path.exists(DST):
    sys.stderr.write("%s ALREADY EXISTS -- refusing to write\n" % DST)
    raise SystemExit(2)
with open(SRC, 'rb') as fh:
    b = fh.read()
eol = b'\r\n' if b'\r\n' in b else b'\n'
J = lambda *L: eol.join(L)

OLD = J(b"  `success`. A rule applied outside its subject. See ARCHITECTURE section 10 SLO-1 and",
        b"  order item 6.8.")

NEW = J(b"  `success`. A rule applied outside its subject. See ARCHITECTURE section 10 SLO-1 and",
        b"  order item 6.8.",
        b"  **AMENDMENT (S102, 2026-09-07):** the windows bind the runs this rule's own purpose",
        b"  clause names -- an ADAPTIVE or MANUAL run. The heartbeat is neither: it is cron",
        b"  `0,30 * * * *`, and `GNI-R-114` says it spends zero Groq, so it cannot collide on the",
        b"  tokens this rule exists to protect. The standdown was removed from",
        b"  `ai_engine/monitoring_pipeline.py:317-321` at S102 (order item 6.12). The `:317-320`",
        b"  cited in the INSTANCE above stops one line short of the `return True` that was the",
        b"  mechanism; the range is 317-321. SUBJECT TEST, countable and AST-readable: the callers",
        b"  of `is_protection_window` in `ai_engine/` are exactly {`adaptive_pipeline.py:226`}.",
        b"  A third caller is a change to this rule and must be registered here first. `C7`'s",
        b"  `heartbeat_stands_down()` reads that caller set, so the published freshness bound",
        b"  falls when the call goes and rises if it returns; fixture families",
        b"  `17-standdown-absent` and `18-standdown-reinstated` differ by that one call and by",
        b"  nothing else. `GNI-R-118`'s blackout windows are UNTOUCHED, as is the March-2026",
        b"  sentence above, which is preserved verbatim.")

n = b.count(OLD)
if n != 1:
    sys.stderr.write("ANCHOR MATCHED %d TIMES -- refusing to write\n" % n)
    raise SystemExit(2)
out = b.replace(OLD, NEW)

# R-S95-1: verified before the write.
assert out.count(b"**CHECKABLE:") == b.count(b"**CHECKABLE:"), "marker count must not change"
assert out.count(b"**AMENDMENT (S102, 2026-09-07):**") == 1
assert out.count(b"- **GNI-R-122** -") == 1, "the id must not be re-declared (C3)"
assert b"starved of tokens by an adaptive or manual run" in out, "verbatim sentence lost"
assert (b'\r\n' in out) == (b'\r\n' in b) and out[:3] == b[:3]
with open(DST, 'wb') as fh:
    fh.write(out)
print("WROTE    %s   (%s untouched)" % (DST, SRC))
print("  src md5 %s  %d bytes" % (hashlib.md5(b).hexdigest(), len(b)))
print("  dst md5 %s  %d bytes" % (hashlib.md5(out).hexdigest(), len(out)))
print("  CHECKABLE markers: %d before, %d after" % (b.count(b"**CHECKABLE:"), out.count(b"**CHECKABLE:")))
