#!/usr/bin/env python3
"""tools/patch_s103_c6.py -- item 5.50.

Widens C6 from "the register's INPUT line" to "EVERY INPUT line the map
declares", adds a third control probe, and adds three fixture families.

DISCIPLINE THIS SCRIPT HONOURS:
  GNI-L-001   binary mode throughout; ship-to-file, never a heredoc.
  R-S95-1  every verification is computed BEFORE the write, not after.
  R-S81-5  the C5 self-lint is REPRODUCED here against the new source, so a
           patch that would make the detector fail itself never gets written.
  S95 trap line endings are detected PER FILE and mixed endings abort.
  idempotency the NEW content is asserted ABSENT before writing, not merely
           that the anchor appears once (a re-paste must be safe).

Run from the repo root:  python tools/patch_s103_c6.py
"""
import ast
import io
import os
import sys

ROOT = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHECKS = os.path.join(ROOT, "tools", "gni_rule_checks.py")
FIXTURE = os.path.join(ROOT, "tools", "gni_rule_checks_fixture.py")


def die(msg):
    print("ABORT: %s" % msg)
    sys.exit(1)


def load(path):
    """Binary read + per-file line-ending detection. Mixed endings abort: a
    multi-line anchor built from the wrong NL matches nothing and a script that
    then 'finds no anchor' looks like a missing feature, not a byte problem."""
    if not os.path.isfile(path):
        die("missing file: " + path)
    with open(path, "rb") as fh:
        data = fh.read()
    crlf = data.count(b"\r\n")
    lf = data.count(b"\n") - crlf
    if crlf and lf:
        die("%s has MIXED line endings (%d CRLF, %d LF); refusing to patch"
            % (path, crlf, lf))
    nl = b"\r\n" if crlf else b"\n"
    print("  read %-34s %6d bytes  nl=%s" % (os.path.basename(path), len(data),
                                             "CRLF" if crlf else "LF"))
    return data, nl


def enc(text, nl):
    """A \\n-authored block re-expressed in the file's own line ending."""
    return text.encode("utf-8").replace(b"\n", nl)


def splice(data, nl, start_text, end_text, new_text, label):
    """Replace everything from start_text up to (but not including) end_text.
    Blank-line counts between the two therefore do not have to be guessed."""
    a, b = enc(start_text, nl), enc(end_text, nl)
    if data.count(a) != 1:
        die("%s: start anchor appears %d times, need exactly 1" % (label, data.count(a)))
    if data.count(b) != 1:
        die("%s: end anchor appears %d times, need exactly 1" % (label, data.count(b)))
    i, j = data.index(a), data.index(b)
    if i >= j:
        die("%s: start anchor is not before end anchor" % label)
    print("  splice %-30s %6d bytes -> %d bytes" % (label, j - i, len(enc(new_text, nl))))
    return data[:i] + enc(new_text, nl) + data[j:]


def replace_once(data, nl, old_text, new_text, label):
    o = enc(old_text, nl)
    if data.count(o) != 1:
        die("%s: anchor appears %d times, need exactly 1" % (label, data.count(o)))
    print("  replace %-29s ok" % label)
    return data.replace(o, enc(new_text, nl))


# --------------------------------------------------------------------------
# 1. tools/gni_rule_checks.py
# --------------------------------------------------------------------------

DOC_OLD = """  C6  R-S95-4   the macro map's stamped marker count AND the register's
                EOL-normalised md5 both match the live register (item 5.26)
"""

DOC_NEW = """  C6  R-S95-4   EVERY `INPUT ... md5` line the macro map declares resolves
                to the LIVE file of its family and matches that file's bytes,
                and the stamped marker count matches the live register. Until
                S103 only the register's line was read (items 5.26 + 5.50)
"""

C6_NEW = '''INPUT_RE = re.compile(
    r"^INPUT `(?P<src>[^`]+)` md5 `(?P<h>[0-9a-f]+)` \\(EOL-normalised\\)", re.M)
STAMP_RE = re.compile(
    r"GENERATED from `(?P<src>[^`]+)` -- (?P<n>\\d+) CHECKABLE "
    r"markers, register generation (?P<gen>\\d+)\\.")
MAP_RE = re.compile(r"^GNI_MACRO_MAP_S(\\d+)\\.md$")


def live_map_path(root):
    """The highest-numbered macro map. The map is not in LIVE_STEMS because it
    is GENERATED rather than authored, so it is resolved here -- by the same
    RELATION rule, never by lexical sort and never by list position
    (R-S92-2)."""
    docs = os.path.join(root, "docs")
    if not os.path.isdir(docs):
        raise InstrumentError("missing dir: " + docs)
    gens = [(int(m.group(1)), n) for n in os.listdir(docs)
            for m in [MAP_RE.match(n)] if m]
    require_nonempty("macro map generations", gens)
    return os.path.join(docs, max(gens)[-1])


def map_inputs(body):
    """Every `INPUT ... md5` line the map DECLARES, in the order written. Zero
    is an INSTRUMENT ERROR and never an empty list: a renamed INPUT format must
    halt, not report a map with nothing left to check (R-S81-1)."""
    rows = [(m.group("src"), m.group("h")) for m in INPUT_RE.finditer(body)]
    return require_nonempty("map INPUT lines", rows)


def stem_of(name):
    """`docs/GNI_RULES_S102.md` -> `GNI_RULES`. Matched against LIVE_STEMS by
    RELATION. A name belonging to no live family returns None and is refused by
    the caller rather than silently skipped."""
    base = os.path.basename(name)
    for stem in LIVE_STEMS:
        if re.match(r"^" + re.escape(stem) + r"_S\\d+\\.md$", base):
            return stem
    return None


def check_c6_macro_map_fresh(ctx):
    """Items 5.26 and 5.50 (C6). The macro map declares one `INPUT ... md5`
    line per source it read. Until S103 this check built the INPUT pattern from
    the map's own `GENERATED from` stamp, and that stamp names the REGISTER by
    construction -- so the ARCHITECTURE line was never read, and an
    architecture that had moved underneath the map was SILENT. S102
    demonstrated that four times in one session, twice by accident.

    Every declared INPUT is now checked, and no count of inputs is written
    anywhere in this file. Each is compared against the LIVE file of its
    family, NOT against the file the line names: a hash re-read from the named
    path always agrees with itself, and the failure S102 actually suffered was
    a RENAME, where the named file still exists and still hashes correctly
    while no longer being the live one.

    The generator's own read, parse_rules and norm_md5 are imported. A second
    parser here would be a second opinion, not a check (R-S96-3).

    KNOWN LIMIT, disclosed rather than hidden: this checks what the map
    DECLARES. A generator that reads a source and emits no INPUT line for it is
    invisible to this check, and to every other check in this file."""
    import gni_macro_map as gm
    docs = require_nonempty("live docs", ctx["docs"])
    map_path = live_map_path(ctx["root"])
    body = require_nonempty("macro map text", read(map_path))
    inputs = map_inputs(body)
    problems = []
    for src, stamped in inputs:
        stem = stem_of(src)
        if stem is None:
            raise InstrumentError("INPUT names no live family: " + src)
        live_path = docs[stem]
        if os.path.basename(src) != os.path.basename(live_path):
            problems.append("map read %s; the live %s is %s"
                            % (os.path.basename(src), stem,
                               os.path.basename(live_path)))
            continue
        try:
            raw = gm.read(live_path)[0]
        except SystemExit:
            raise InstrumentError("the generator's own reader refused " + live_path)
        live_h = gm.norm_md5(raw)
        if stamped != live_h:
            problems.append("%s md5 %s; map stamped %s" % (stem, live_h, stamped))
    stamp = STAMP_RE.search(body)
    if not stamp:
        raise InstrumentError("no GENERATED-from stamp in " + map_path)
    reg_path = docs["GNI_RULES"]
    if os.path.basename(stamp.group("src")) != os.path.basename(reg_path):
        problems.append("map generated from %s; live register is %s"
                        % (stamp.group("src"), reg_path))
    try:
        raw, bound, unbound = gm.parse_rules(reg_path)
    except SystemExit:
        raise InstrumentError("the generator's own parser refused " + reg_path)
    live_n = len(bound) + len(unbound)
    if int(stamp.group("n")) != live_n:
        problems.append("map stamps %s markers; register holds %d"
                        % (stamp.group("n"), live_n))
    if problems:
        return False, "; ".join(problems)
    return True, "%s: %d INPUT lines resolve live and match, %d markers" % (
        os.path.basename(map_path), len(inputs), live_n)


'''

PROBE_NEW = '''def _probe_halts(what, fn, arg):
    """A probe passes only when the parser RAISES. A parser that returned an
    empty result on perturbed bytes would report a clean tree built from
    nothing, which is the failure R-S81-1 exists to prevent."""
    try:
        fn(arg)
    except InstrumentError:
        return
    raise InstrumentError("control probe FAILED: " + what)


def control_probe(root):
    """R-S93-1: the instrument checks its own expectations before it reports.
    Each probe perturbs the REAL tree's bytes in memory (R-S100-1) and asserts
    the parser HALTS rather than passing silently. Added at S103: the map's
    INPUT format became load-bearing when C6 widened to every INPUT line, so a
    renamed INPUT must halt exactly as a renamed manifest does."""
    rules = read(live_docs(root)["GNI_RULES"])
    _probe_halts("a renamed manifest still parsed", manifest_ids,
                 rules.replace(MANIFEST_MARKER, "XX-RENAMED-XX"))
    body = read(live_map_path(root))
    _probe_halts("a renamed INPUT line still parsed", map_inputs,
                 body.replace("INPUT `", "XX-RENAMED-XX `"))


'''

# --------------------------------------------------------------------------
# 2. tools/gni_rule_checks_fixture.py
# --------------------------------------------------------------------------

MAPTEXT_NEW = '''def _map_text(reg_path, arch_path, n_delta=0):
    """Built from the register AND the architecture AS WRITTEN, so the fixture
    is self-consistent on any platform: open(mode="w") emits CRLF on Windows
    and LF elsewhere, and the stamped md5s must survive that. Uses the
    generator's own functions.

    TWO INPUT lines from S103, because the production map declares two and C6
    now reads every one of them (item 5.50). With one line the fixture could
    not have gone red on a stale architecture stamp, which is why no family
    covered that case for four closes."""
    import gni_macro_map as gm
    raw, bound, unbound = gm.parse_rules(reg_path)
    n = len(bound) + len(unbound) + n_delta
    arch_raw = gm.read(arch_path)[0]
    return ("# GNI MACRO MAP -- S94\\n\\n"
            "INPUT `%s` md5 `%s` (EOL-normalised)\\n"
            "INPUT `%s` md5 `%s` (EOL-normalised)\\n"
            "GENERATED from `%s` -- %d CHECKABLE markers, register generation 94.\\n"
            % (reg_path, gm.norm_md5(raw),
               arch_path, gm.norm_md5(arch_raw),
               reg_path, n))


'''

BASE_OLD_A = '''    if map_present:
        w(root + "/docs/GNI_MACRO_MAP_S94.md",
          _map_text(root + "/docs/GNI_RULES_S94.md", map_n_delta))
    w(root + "/ai_engine/monitoring_pipeline.py", watcher)
'''

BASE_NEW_A = '''    w(root + "/ai_engine/monitoring_pipeline.py", watcher)
'''

BASE_OLD_B = '''    ap(root + "/docs/GNI_ARCHITECTURE_S94.md",
       _slo_block(slo_bound,
                  slo_from if slo_from else SLO_FAST[0],
                  slo_to if slo_to else SLO_FAST[-1]))
    return root
'''

BASE_NEW_B = '''    ap(root + "/docs/GNI_ARCHITECTURE_S94.md",
       _slo_block(slo_bound,
                  slo_from if slo_from else SLO_FAST[0],
                  slo_to if slo_to else SLO_FAST[-1]))
    # LAST, and the order is load-bearing: the map stamps the architecture's
    # md5, and the SLO block above APPENDS to the architecture. Stamping before
    # that append would leave every family red on a hash the fixture itself had
    # just invalidated -- the check would look alive while measuring nothing.
    if map_present:
        w(root + "/docs/GNI_MACRO_MAP_S94.md",
          _map_text(root + "/docs/GNI_RULES_S94.md",
                    root + "/docs/GNI_ARCHITECTURE_S94.md", map_n_delta))
    return root
'''

CASES_NEW = '''# S103, item 5.50. 19 is what the DoD asked for; 20 and 21 go beyond it.
# 20 is the DISCRIMINATOR (R-S90-1): a check that compared only hashes passes
# it, because the file the map names still exists and still hashes correctly.
# That is precisely the failure S102 suffered and could not see.
CASES["19-map-stale-arch-md5"] = lambda r: (
    base(r), ap(r + "/docs/GNI_ARCHITECTURE_S94.md",
                "\\nprose line carrying no id and no marker\\n"), r)[-1]
CASES["20-map-arch-renamed"] = lambda r: (
    base(r), shutil.copyfile(r + "/docs/GNI_ARCHITECTURE_S94.md",
                             r + "/docs/GNI_ARCHITECTURE_S95.md"), r)[-1]
CASES["21-map-third-input"] = lambda r: (
    base(r), ap(r + "/docs/GNI_MACRO_MAP_S94.md",
                "INPUT `%s/docs/CONTRACT_S94.md` md5 `%s` (EOL-normalised)\\n"
                % (r, "0" * 32)), r)[-1]

'''

EXPECT_OLD = '''    "17-standdown-absent": 0, "18-standdown-reinstated": 1,
}
'''

EXPECT_NEW = '''    "17-standdown-absent": 0, "18-standdown-reinstated": 1,
    "19-map-stale-arch-md5": 1, "20-map-arch-renamed": 1,
    "21-map-third-input": 1,
}
'''


def c5_self_lint(src, path):
    """R-S81-5 and R-S81-1 reproduced against the NEW source, before the write.
    If the patched detector would fail its own C5, nothing is written."""
    tree = ast.parse(src)
    fns = [n for n in ast.walk(tree)
           if isinstance(n, ast.FunctionDef) and n.name.startswith("check_")]
    if not fns:
        die("C5 pre-check: no check_ functions found in " + path)
    bad = []
    for fn in fns:
        calls = {c.func.id for c in ast.walk(fn)
                 if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)}
        if "require_nonempty" not in calls:
            bad.append("%s never proves its input is non-empty" % fn.name)
        for node in ast.walk(fn):
            if isinstance(node, ast.Constant) and isinstance(node.value, int) \
                    and not isinstance(node.value, bool) and node.value > 1:
                bad.append("%s holds hand-written integer %d" % (fn.name, node.value))
    if bad:
        die("C5 pre-check FAILED: " + "; ".join(bad))
    print("  C5 pre-check   %d check functions, 0 problems" % len(fns))


def main():
    print("PATCH S103 / item 5.50 -- C6 reads every INPUT line")
    print("root: %s" % ROOT)

    # ---- gni_rule_checks.py -------------------------------------------------
    print("\n[1] tools/gni_rule_checks.py")
    data, nl = load(CHECKS)
    if b"map_inputs" in data:
        die("already patched (map_inputs present) -- nothing written")
    data = replace_once(data, nl, DOC_OLD, DOC_NEW, "module docstring C6")
    data = splice(data, nl,
                  "def check_c6_macro_map_fresh(ctx):",
                  "SLO_KEYS = (",
                  C6_NEW, "C6 + helpers")
    data = splice(data, nl,
                  "def control_probe(root):",
                  "def main(argv):",
                  PROBE_NEW, "control_probe")
    src = data.decode("utf-8")
    try:
        ast.parse(src)
    except SyntaxError as exc:
        die("patched gni_rule_checks.py does not parse: %s" % exc)
    print("  ast.parse    OK")
    c5_self_lint(src, CHECKS)
    for token in ("INPUT_RE", "live_map_path", "map_inputs", "stem_of",
                  "_probe_halts", "a renamed INPUT line still parsed"):
        if src.count(token) < 1:
            die("post-splice grep failed for: " + token)
    print("  element grep 6/6")
    checks_out = data

    # ---- gni_rule_checks_fixture.py ----------------------------------------
    print("\n[2] tools/gni_rule_checks_fixture.py")
    fdata, fnl = load(FIXTURE)
    if b"21-map-third-input" in fdata:
        die("already patched (family 21 present) -- nothing written")
    fdata = splice(fdata, fnl, "def _map_text(reg_path", "def ap(p, s):",
                   MAPTEXT_NEW, "_map_text")
    fdata = replace_once(fdata, fnl, BASE_OLD_A, BASE_NEW_A, "base(): drop early map")
    fdata = replace_once(fdata, fnl, BASE_OLD_B, BASE_NEW_B, "base(): map written LAST")
    fdata = replace_once(fdata, fnl, "# Expected verdict per family.",
                         CASES_NEW + "# Expected verdict per family.",
                         "three new families")
    fdata = replace_once(fdata, fnl, EXPECT_OLD, EXPECT_NEW, "EXPECT rows")
    fsrc = fdata.decode("utf-8")
    try:
        ast.parse(fsrc)
    except SyntaxError as exc:
        die("patched fixture does not parse: %s" % exc)
    print("  ast.parse    OK")
    for name in ("19-map-stale-arch-md5", "20-map-arch-renamed", "21-map-third-input"):
        if fsrc.count('"%s"' % name) != 2:
            die("%s must appear exactly twice (CASES + EXPECT), found %d"
                % (name, fsrc.count('"%s"' % name)))
    print("  CASES/EXPECT pairing  3/3")

    # ---- write, both or neither --------------------------------------------
    print("\n[3] WRITE")
    with open(CHECKS, "wb") as fh:
        fh.write(checks_out)
    print("  WROTE %-34s %6d bytes" % (os.path.basename(CHECKS), len(checks_out)))
    with open(FIXTURE, "wb") as fh:
        fh.write(fdata)
    print("  WROTE %-34s %6d bytes" % (os.path.basename(FIXTURE), len(fdata)))
    print("\nDONE. Next: py_compile, then the fixture, then the live tree.")


if __name__ == "__main__":
    main()
