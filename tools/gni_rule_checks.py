#!/usr/bin/env python3
"""tools/gni_rule_checks.py - S95, sixth check added S98. Layer 0 detector
for DOCUMENT law.

Converts six GNI engineering rules from prose into executable checks.

  C1  R-S90-2   every rule ID cited by a live doc is registered, or carries a
                status row in the PART 0 UNREGISTERED MANIFEST
  C2  R-S91-5   workflow/trigger counts derived from .github/workflows/*.yml
                equal the counts stated in ARCHITECTURE section 7.1
  C3  R-S92-2   no selection by absolute position into a growing collection
  C4  R-S62-3   no direct createClient under src/app/api/ (no-store only)
  C5  R-S81-5   self-lint: no check may hold a hand-written expected integer,
      R-S81-1   and every check must prove its input was non-empty first
  C6  R-S95-4   the macro map's stamped marker count AND the register's
                EOL-normalised md5 both match the live register (item 5.26)

CONSTRAINTS THIS SCRIPT HONOURS, ON PURPOSE:
  - stdlib only. No pip install step is needed or wanted (item 6.9).
  - NO SECRETS. Inherits gni_ci_harness.yml's hard boundary.
  - NO git history. actions/checkout defaults to fetch-depth 1; every check
    reads the working tree only.

EXIT CODES -- three, matching tools/gni_state.py:
  0  all checks passed
  1  a check FAILED (a rule is being violated)
  2  INSTRUMENT ERROR: an input was missing or a control probe failed.
     Nothing is reported as passing. A missing input must never read as zero
     violations (R-S81-1).
"""
import ast
import os
import re
import sys

LIVE_STEMS = (
    "CONTRACT",
    "GNI_RULES",
    "GNI_Session_Transfer_Protocol",
    "GNI_TARGET_AND_ORDER",
    "HANDOFF",
    "GNI_ARCHITECTURE",
)
ID_RE = re.compile(r"R-S\d+-\d+|LR-\d+|GNI-R-\d+|NN-PHI-\d+")
MANIFEST_MARKER = "UNREGISTERED ID MANIFEST"
MANIFEST_STATUSES = {
    "DANGLING-LAW", "UNMIGRATED-DOCX", "DEFINED-IN-CONTRACT", "DISCUSSION-ONLY",
}


class InstrumentError(Exception):
    """Raised when an input is missing. Never reported as a passing check."""


def require_nonempty(label, value):
    """R-S81-1: a zero result must first prove the instrument saw data."""
    if not value:
        raise InstrumentError("empty input: " + label)
    return value


def read(path):
    if not os.path.isfile(path):
        raise InstrumentError("missing file: " + path)
    with open(path, "rb") as fh:
        # utf-8-sig: six files in ai_engine/ carry a BOM. Decoding as plain
        # utf-8 leaves U+FEFF in the text and silently breaks any parser.
        return fh.read().decode("utf-8-sig", "replace")


def live_docs(root):
    """Highest session number per family. Selected by RELATION (R-S92-2),
    parsed as an integer -- never by lexical sort, never by list position."""
    docs = os.path.join(root, "docs")
    if not os.path.isdir(docs):
        raise InstrumentError("missing dir: " + docs)
    names = os.listdir(docs)
    out = {}
    for stem in LIVE_STEMS:
        pat = re.compile(r"^" + re.escape(stem) + r"_S(\d+)\.md$")
        gens = [(int(m.group(1)), n) for n in names for m in [pat.match(n)] if m]
        if not gens:
            raise InstrumentError("no generation found for family: " + stem)
        out[stem] = os.path.join(docs, max(gens)[1])
    return require_nonempty("live docs", out)


def registered_ids(rules_text):
    """Definitions only. PART 1 and PART 2 are an index and a cluster map;
    their mentions are citations, not definitions. Boundaries are found by
    heading text, never by line number (R-S92-2)."""
    lines = rules_text.split("\n")
    def heading(prefix):
        for i, ln in enumerate(lines):
            if ln.startswith(prefix):
                return i
        raise InstrumentError("heading not found: " + prefix)
    skip_from, skip_to = heading("# PART 1"), heading("# PART 3")
    d = re.compile(r"^\s{0,2}(?:-\s*)?(?:\*\*)?(" + ID_RE.pattern +
                   r")(?:\*\*)?\s*(?:[:\u2014-]|\()")
    h = re.compile(r"^##\s*(" + ID_RE.pattern + r")\b")
    found = set()
    for i, ln in enumerate(lines):
        if skip_from <= i < skip_to:
            continue
        m = d.match(ln) or h.match(ln)
        if m:
            found.add(m.group(1))
    return require_nonempty("registered ids", found)


def manifest_ids(rules_text):
    """PART 0 manifest. Absent marker is an INSTRUMENT ERROR, never an empty
    allowlist -- a renamed section must not silently pass every citation."""
    if MANIFEST_MARKER not in rules_text:
        raise InstrumentError("manifest marker absent: " + MANIFEST_MARKER)
    tail = rules_text.split(MANIFEST_MARKER, 1)[1]
    rows = {}
    for ln in tail.split("\n"):
        if not ln.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip().strip("`") for c in ln.strip("|").split("|")]
        if len(cells) < 2:
            continue
        m = ID_RE.fullmatch(cells[0])
        if m and cells[1] in MANIFEST_STATUSES:
            rows[cells[0]] = cells[1]
    return require_nonempty("manifest rows", rows)


def trigger_block(body):
    """The `on:` block: from a top-level `on:` line to the next top-level key.
    Found by structure, not by an assumed neighbour -- a workflow whose first
    line is `on:` is legal YAML, and splitting on "\non:" silently misses it."""
    lines, out, inside = body.split("\n"), [], False
    for ln in lines:
        if re.match(r"^on:", ln):
            inside = True
            continue
        if inside:
            if ln.strip() and not ln[:1].isspace():
                break
            out.append(ln)
    return "\n".join(out)


def check_c1_citations(ctx):
    """R-S90-2. No inline escape exists: `GNI-R-114` is backticked AND
    load-bearing, so backticks cannot mean 'not a citation'."""
    docs = require_nonempty("live docs", ctx["docs"])
    reg = registered_ids(read(docs["GNI_RULES"]))
    man = manifest_ids(read(docs["GNI_RULES"]))
    known = reg | set(man)
    bad, seen = {}, set()
    for stem, path in sorted(docs.items()):
        if stem == "GNI_RULES":
            continue
        # R-S81-1 applies to the INPUT, not the finding: a doc that cites no
        # rule at all is a legitimate observation. An unreadable doc is not.
        cited = set(ID_RE.findall(require_nonempty("text of " + stem, read(path))))
        seen |= cited
        for rid in sorted(cited - known):
            bad.setdefault(rid, []).append(stem)
    require_nonempty("citations across all live docs", seen)
    if bad:
        det = "; ".join("%s cited by %s" % (r, ",".join(s)) for r, s in sorted(bad.items()))
        return False, "unregistered and unmanifested: " + det
    return True, "%d registered + %d manifested cover every citation" % (len(reg), len(man))


def check_c2_workflow_counts(ctx):
    """R-S91-5. Derived from YAML, compared against the GENERATED section 7.1
    line. Prose elsewhere is not scanned: a doc that records a wrong count as
    a finding must not be indistinguishable from a doc that makes it."""
    wf_dir = os.path.join(ctx["root"], ".github", "workflows")
    if not os.path.isdir(wf_dir):
        raise InstrumentError("missing dir: " + wf_dir)
    files = require_nonempty("workflow files",
                             sorted(f for f in os.listdir(wf_dir)
                                    if f.endswith((".yml", ".yaml"))))
    sched = push = dispatch_only = 0
    for f in files:
        body = read(os.path.join(wf_dir, f))
        on = trigger_block(body)
        has_s, has_p = "schedule:" in on, re.search(r"^\s+push:", on, re.M) is not None
        sched += has_s
        push += has_p
        dispatch_only += (not has_s and not has_p)
    arch = read(ctx["docs"]["GNI_ARCHITECTURE"])
    m = re.search(r"\*\*(\d+) workflows:\s*(\d+) scheduled\s*.\s*(\d+) on push\s*.\s*"
                  r"(\d+) dispatch-only", arch)
    if not m:
        raise InstrumentError("section 7.1 count line not found in ARCHITECTURE")
    stated = tuple(int(g) for g in m.groups())
    derived = (len(files), sched, push, dispatch_only)
    if stated != derived:
        return False, "section 7.1 states %s; YAML derives %s -- generator is stale" % (
            stated, derived)
    return True, "section 7.1 %s matches YAML" % (derived,)


AMEND_MARKERS = ("AMENDMENT", "AMENDED", "INSTANCE")


def definition_lines(rules_text):
    """Every definition line in the register, in file order, with its ID.
    PART 1 and PART 2 are an index and a cluster map; boundaries are located by
    heading text, never by line number."""
    lines = rules_text.split("\n")
    def heading(prefix):
        for i, ln in enumerate(lines):
            if ln.startswith(prefix):
                return i
        raise InstrumentError("heading not found: " + prefix)
    skip_from, skip_to = heading("# PART 1"), heading("# PART 3")
    d = re.compile(r"^\s{0,2}(?:-\s*)?(?:\*\*)?(" + ID_RE.pattern +
                   r")(?:\*\*)?\s*(?:[:\u2014-]|\()")
    h = re.compile(r"^##\s*(" + ID_RE.pattern + r")\b")
    out = []
    for i, ln in enumerate(lines):
        if skip_from <= i < skip_to:
            continue
        m = d.match(ln) or h.match(ln)
        if m:
            out.append((m.group(1), i + 1, ln))
    return require_nonempty("definition lines", out)


def check_c3_register_uniqueness(ctx):
    """R-S74-1. A registry append asserts ID-uniqueness against FILE BYTES.
    The register became load-bearing the moment C1 started reading it: a
    silently duplicated ID would redefine law without anyone noticing. A
    repeated ID is legal ONLY when the later line declares itself an
    amendment or a further instance."""
    docs = require_nonempty("live docs", ctx["docs"])
    defs = definition_lines(read(docs["GNI_RULES"]))
    first, bad = {}, []
    for rid, lineno, text in defs:
        if rid not in first:
            first[rid] = lineno
        elif not any(mark in text for mark in AMEND_MARKERS):
            bad.append("%s redefined at line %d (first at %d) with no amendment marker"
                       % (rid, lineno, first[rid]))
    if bad:
        return False, "; ".join(bad)
    return True, "%d ids across %d definition lines; every repeat is declared" % (
        len(first), len(defs))


def check_c4_nostore_client(ctx):
    """R-S62-3. Server-side Supabase reads go through createNoStoreClient."""
    api = os.path.join(ctx["root"], "src", "app", "api")
    if not os.path.isdir(api):
        raise InstrumentError("missing dir: " + api)
    files = require_nonempty("api route files",
                             [os.path.join(dp, f) for dp, _, fs in os.walk(api)
                              for f in fs if f.endswith((".ts", ".tsx"))])
    rx = re.compile(r"\bcreateClient\b")
    hits = ["%s:%d" % (p, n) for p in files
            for n, ln in enumerate(read(p).split("\n"), 1)
            if rx.search(ln) and "createNoStoreClient" not in ln]
    if hits:
        return False, "direct createClient in: " + "; ".join(hits)
    return True, "no direct createClient across %d route files" % len(files)


def check_c5_self_lint(ctx):
    """R-S81-5 + R-S81-1, applied to this file. Counting a code literal is an
    AST job, never a regex one (R-S75-1)."""
    src = read(require_nonempty("self path", ctx["self_path"]))
    tree = ast.parse(src)
    problems = []
    checks = [n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name.startswith("check_")]
    require_nonempty("check functions", checks)
    for fn in checks:
        calls = {c.func.id for c in ast.walk(fn)
                 if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)}
        if "require_nonempty" not in calls:
            problems.append("%s never proves its input is non-empty" % fn.name)
        for node in ast.walk(fn):
            if isinstance(node, ast.Constant) and isinstance(node.value, int) \
                    and not isinstance(node.value, bool) and node.value > 1:
                problems.append("%s holds hand-written integer %d" % (fn.name, node.value))
    if problems:
        return False, "; ".join(problems)
    return True, "%d checks derive every expected value" % len(checks)


def check_c6_macro_map_fresh(ctx):
    """Item 5.26 (C6). The macro map is GENERATED from the register, and until
    now nothing went red when the register moved underneath it: S96 committed a
    map reading 159 markers and closed the same session with 164 registered.
    Count alone will not do -- a constant count is not a constant state
    (R-S95-4) -- so the register's EOL-normalised md5 is compared as well,
    using the generator's OWN parse_rules and norm_md5. A second parser here
    would be a second opinion, not a check (R-S96-3)."""
    import gni_macro_map as gm
    docs = os.path.join(ctx["root"], "docs")
    if not os.path.isdir(docs):
        raise InstrumentError("missing dir: " + docs)
    pat = re.compile(r"^GNI_MACRO_MAP_S(\d+)\.md$")
    gens = [(int(m.group(1)), n) for n in os.listdir(docs) for m in [pat.match(n)] if m]
    require_nonempty("macro map generations", gens)
    map_path = os.path.join(docs, max(gens)[-1])
    body = require_nonempty("macro map text", read(map_path))
    reg_path = require_nonempty("live register", ctx["docs"]["GNI_RULES"])
    stamp = re.search(r"GENERATED from `(?P<src>[^`]+)` -- (?P<n>\d+) CHECKABLE "
                      r"markers, register generation (?P<gen>\d+)\.", body)
    if not stamp:
        raise InstrumentError("no GENERATED-from stamp in " + map_path)
    md5line = re.search(r"INPUT `" + re.escape(stamp.group("src")) +
                        r"` md5 `(?P<h>[0-9a-f]+)`", body)
    if not md5line:
        raise InstrumentError("no INPUT md5 line for the register in " + map_path)
    try:
        raw, bound, unbound = gm.parse_rules(reg_path)
    except SystemExit:
        raise InstrumentError("the generator's own parser refused " + reg_path)
    live_n = len(bound) + len(unbound)
    live_h = gm.norm_md5(raw)
    problems = []
    if os.path.basename(stamp.group("src")) != os.path.basename(reg_path):
        problems.append("map generated from %s; live register is %s"
                        % (stamp.group("src"), reg_path))
    if int(stamp.group("n")) != live_n:
        problems.append("map stamps %s markers; register holds %d"
                        % (stamp.group("n"), live_n))
    if md5line.group("h") != live_h:
        problems.append("register md5 %s; map stamped %s" % (live_h, md5line.group("h")))
    if problems:
        return False, "; ".join(problems)
    return True, "%s stamps %d markers and the register md5 matches" % (
        os.path.basename(map_path), live_n)


CHECKS = (
    ("C1 R-S90-2  rule citations", check_c1_citations),
    ("C2 R-S91-5  workflow counts", check_c2_workflow_counts),
    ("C3 R-S74-1  register uniqueness", check_c3_register_uniqueness),
    ("C4 R-S62-3  no-store client", check_c4_nostore_client),
    ("C5 R-S81-5  self-lint", check_c5_self_lint),
    ("C6 R-S95-4  macro map fresh", check_c6_macro_map_fresh),
)


def build_ctx(root, self_path):
    return {"root": root, "self_path": self_path, "docs": live_docs(root)}


def control_probe(root):
    """R-S93-1: the instrument checks its own expectations before it reports.
    A manifest whose marker was renamed must halt, not pass silently."""
    rules = read(live_docs(root)["GNI_RULES"])
    try:
        manifest_ids(rules.replace(MANIFEST_MARKER, "XX-RENAMED-XX"))
    except InstrumentError:
        return
    raise InstrumentError("control probe FAILED: a renamed manifest still parsed")


def main(argv):
    root = argv[1] if len(argv) > 1 else "."
    self_path = os.path.abspath(__file__)
    try:
        control_probe(root)
        ctx = build_ctx(root, self_path)
    except InstrumentError as exc:
        print("INSTRUMENT ERROR: %s" % exc)
        print("Nothing checked. This is not a pass.")
        return 2
    failed = 0
    for name, fn in CHECKS:
        try:
            ok, detail = fn(ctx)
        except InstrumentError as exc:
            print("[ERROR] %-32s %s" % (name, exc))
            return 2
        print("[%s] %-32s %s" % ("PASS" if ok else "FAIL", name, detail))
        failed += not ok
    print("RESULT: %d checked, %d failed" % (len(CHECKS), failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
