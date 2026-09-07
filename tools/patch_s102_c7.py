# S102 / order item 6.12 -- C7 must ASK the tree whether the watcher still
# stands down, instead of assuming it does. Without this the bound cannot
# fall when the standdown is removed, and cannot rise if it is reinstated.
# Binary mode (LR-078); EOL detected, never assumed.
import hashlib, sys

P = 'tools/gni_rule_checks.py'
with open(P, 'rb') as fh:
    b = fh.read()
eol = b'\r\n' if b'\r\n' in b else b'\n'
J = lambda *L: eol.join(L)

EDITS = []

# 1. new predicate, inserted immediately before in_protection()
EDITS.append((
    J(b"def in_protection(when, windows):", b""),
    J(b"def heartbeat_stands_down(root):",
      b'    """Does the watcher still consult its own protection windows?',
      b"    Until S102 it did, and a run inside a window returned before it",
      b"    opened a connection while still reporting success (order item 6.12).",
      b"    `GNI-R-122` was amended at S102 to bind ADAPTIVE and MANUAL runs, so",
      b"    the call set IS the rule's subject test -- asked of the tree, never",
      b"    assumed here, because an assumption cannot go red when it stops being",
      b'    true. The window table itself is still read: adaptive still uses it."""',
      b'    path = os.path.join(root, "ai_engine", "monitoring_pipeline.py")',
      b"    if not os.path.isfile(path):",
      b'        raise InstrumentError("missing watcher: " + path)',
      b"    for node in ast.walk(ast.parse(read(path))):",
      b"        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)",
      b'                and node.func.id == "is_protection_window"):',
      b"            return True",
      b"    return False",
      b"", b"",
      b"def in_protection(when, windows):", b""),
))

# 2. the effective_gaps docstring is now FALSE. Fix it in the same commit.
EDITS.append((
    J(b'    """The gap between CHECKS, not between runs: a run inside a protection',
      b'    window returns before it opens a connection and checks nothing."""'),
    J(b'    """The gap between CHECKS, not between runs. Pass windows=[] when the',
      b"    watcher no longer stands down: every run then performs its check, so",
      b'    the check gap and the run gap are the same number."""'),
))

# 3. the caller decides from the tree, not from the presence of a window table
EDITS.append((
    J(b'    windows = protection_windows(ctx["root"])',
      b"    gaps = effective_gaps(runs, windows, frm, to)"),
    J(b'    windows = protection_windows(ctx["root"])   # must exist: adaptive uses it',
      b'    if not heartbeat_stands_down(ctx["root"]):',
      b"        windows = []",
      b"    gaps = effective_gaps(runs, windows, frm, to)"),
))

if b"def heartbeat_stands_down" in b:
    sys.stderr.write("ALREADY PATCHED -- refusing to write\n")
    raise SystemExit(2)

out = b
for i, (old, new) in enumerate(EDITS, 1):
    n = out.count(old)
    if n != 1:
        sys.stderr.write("EDIT %d MATCHED %d TIMES -- refusing to write\n" % (i, n))
        raise SystemExit(2)
    out = out.replace(old, new)

# R-S95-1: verified before the write.
assert out.count(b"def heartbeat_stands_down") == 1
assert out.count(b"def protection_windows") == 1, "the window reader must survive"
assert b"windows = []" in out
assert out[:3] == b[:3] and (b'\r\n' in out) == (b'\r\n' in b)
with open(P, 'wb') as fh:
    fh.write(out)
print("PATCHED  %s" % P)
print("  md5 before %s  %d bytes" % (hashlib.md5(b).hexdigest(), len(b)))
print("  md5 after  %s  %d bytes" % (hashlib.md5(out).hexdigest(), len(out)))
