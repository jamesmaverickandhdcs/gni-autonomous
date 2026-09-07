# S102 / order item 6.12 -- fixture families 17 and 18.
# The existing snapshot has ZERO runs inside 23:00-01:30, so no family has
# ever exercised the window argument of effective_gaps. These two do: one
# tree without the standdown, one with it, everything else byte-identical.
import hashlib, sys

P = 'tools/gni_rule_checks_fixture.py'
with open(P, 'rb') as fh:
    b = fh.read()
eol = b'\r\n' if b'\r\n' in b else b'\n'
J = lambda *L: eol.join(L)

if b"WATCHER_STANDDOWN" in b:
    sys.stderr.write("ALREADY PATCHED -- refusing to write\n")
    raise SystemExit(2)

EDITS = [
 (J(b'WATCHER = ("# synthetic watcher -- C7 reads this by AST, never by regex\\n"',
    b'           "PROTECTION_WINDOWS = [\\n"',
    b'           "    (23, 0, 1, 30),\\n"',
    b'           "]\\n")'),
  J(b'WATCHER = ("# synthetic watcher -- C7 reads this by AST, never by regex\\n"',
    b'           "PROTECTION_WINDOWS = [\\n"',
    b'           "    (23, 0, 1, 30),\\n"',
    b'           "]\\n")',
    b"# The pre-S102 shape: the watcher consulted its own windows and a run",
    b"# inside one returned before it opened a connection. Restored here as a",
    b"# perturbation, not invented -- this is the body removed at S102.",
    b'WATCHER_STANDDOWN = WATCHER + ("\\n\\ndef run_monitoring_pipeline(now):\\n"',
    b'                               "    if is_protection_window(now):\\n"',
    b'                               "        return True\\n"',
    b'                               "    return True\\n")',
    b'SLO_PW = ("2026-02-01", "2026-02-05")')),

 (J(b"def _slo_block(bound, frm, to):"),
  J(b"def _snap_pw_text():",
    b'    """A history that ENTERS the protection window. _snap_text never does',
    b"    -- its runs start at 02:00 -- so until S102 no family exercised the",
    b"    window argument of effective_gaps at all. A run every three hours from",
    b"    00:00 puts exactly one run per day inside 23:00-01:30: 39 gaps and a",
    b'    3 h bound when every run checks, 34 gaps and 6 h when they do not."""',
    b"    import json",
    b'    days = ["2026-02-0%d" % i for i in range(1, 6)]',
    b'    runs = ["%sT%02d:00:00Z" % (d, h) for d in days for h in range(0, 24, 3)]',
    b"    return json.dumps({",
    b'        "harvest_limit": 300, "harvested_at": "2026-02-06T00:00:00Z", "schema": 1,',
    b'        "workflows": {"a.yml": {"crons": ["0 */3 * * *"], "fetched": len(runs),',
    b'                                "truncated": False,',
    b'                                "runs": [{"conclusion": "success", "createdAt": t}',
    b"                                         for t in runs]}}})",
    b"", b"",
    b"def _slo_block(bound, frm, to):")),

 (J(b"         slo_bound=\"1\", slo_from=None, slo_to=None):"),
  J(b"         slo_bound=\"1\", slo_from=None, slo_to=None,",
    b"         watcher=WATCHER, snap=None):")),

 (J(b'    w(root + "/ai_engine/monitoring_pipeline.py", WATCHER)',
    b'    w(root + "/docs/gni_runtime_snapshot_S94.json", _snap_text())'),
  J(b'    w(root + "/ai_engine/monitoring_pipeline.py", watcher)',
    b'    w(root + "/docs/gni_runtime_snapshot_S94.json",',
    b"      snap if snap is not None else _snap_text())")),

 (J(b'CASES["16-slo-window-spans-regimes"] = lambda r: base(',
    b'    r, slo_bound="3", slo_from=SLO_FAST[0], slo_to=SLO_SLOW[-1])'),
  J(b'CASES["16-slo-window-spans-regimes"] = lambda r: base(',
    b'    r, slo_bound="3", slo_from=SLO_FAST[0], slo_to=SLO_SLOW[-1])',
    b'CASES["17-standdown-absent"] = lambda r: base(',
    b"    r, watcher=WATCHER, snap=_snap_pw_text(),",
    b'    slo_bound="3", slo_from=SLO_PW[0], slo_to=SLO_PW[-1])',
    b'CASES["18-standdown-reinstated"] = lambda r: base(',
    b"    r, watcher=WATCHER_STANDDOWN, snap=_snap_pw_text(),",
    b'    slo_bound="3", slo_from=SLO_PW[0], slo_to=SLO_PW[-1])')),

 (J(b'    "15-slo-bound-not-derived": 1, "16-slo-window-spans-regimes": 1,',
    b"}"),
  J(b'    "15-slo-bound-not-derived": 1, "16-slo-window-spans-regimes": 1,',
    b'    "17-standdown-absent": 0, "18-standdown-reinstated": 1,',
    b"}")),
]

out = b
for i, (old, new) in enumerate(EDITS, 1):
    n = out.count(old)
    if n != 1:
        sys.stderr.write("EDIT %d MATCHED %d TIMES -- refusing to write\n" % (i, n))
        raise SystemExit(2)
    out = out.replace(old, new)

assert out.count(b"WATCHER_STANDDOWN") == 2   # definition + family 18
assert out.count(b"_snap_pw_text") == 3
assert out.count(b'"17-standdown-absent"') == 2
assert out.count(b'"18-standdown-reinstated"') == 2
assert out[:3] == b[:3] and (b'\r\n' in out) == (b'\r\n' in b)
with open(P, 'wb') as fh:
    fh.write(out)
print("PATCHED  %s" % P)
print("  md5 before %s  %d bytes" % (hashlib.md5(b).hexdigest(), len(b)))
print("  md5 after  %s  %d bytes" % (hashlib.md5(out).hexdigest(), len(out)))
