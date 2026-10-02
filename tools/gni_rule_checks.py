#!/usr/bin/env python3
"""tools/gni_rule_checks.py - S95, seventh check added S101. Layer 0 detector
for DOCUMENT law.

Converts GNI engineering rules from prose into executable checks. The
CHECKS tuple at the foot of this file is the list; this header does not
count it, because a count written here went stale twice (protocol v18).

  C1  R-S90-2   every rule ID cited by a live doc is registered, or carries a
                status row in the PART 0 UNREGISTERED MANIFEST
  C2  R-S91-5   workflow/trigger counts derived from .github/workflows/*.yml
                equal the counts stated in ARCHITECTURE section 7.1
  C3  R-S74-1   no rule id is defined twice in the register unless the later
                line declares itself an amendment (this line said R-S92-2,
                position selection, until S106; no check implements that)
  C4  R-S62-3   no direct createClient under src/app/api/ (no-store only)
  C5  R-S81-5   self-lint: no check may hold a hand-written expected integer,
      R-S81-1   and every check must prove its input was non-empty first
  C6  R-S95-4   EVERY `INPUT ... md5` line the macro map declares resolves
                to the LIVE file of its family and matches that file's bytes,
                and the stamped marker count matches the live register. Until
                S103 only the register's line was read (items 5.26 + 5.50)
  C7  SLO-2+3   the freshness bound published in ARCHITECTURE section 10 is the
                smallest whole hour inside the error budget, and the published
                window holds ONE regime, not two averaged together
  C8  R-S104-1  the three GENERATED sections of ARCHITECTURE resolve live
                and match their inputs (S104; absent from this header until S106)
  C9  R3-1      every abbreviation a live doc or ORIGIN uses is in the
                glossary, and every check below has a glossary row (S106)
  C10 R3-1      every session ORIGIN cites has a record, and ORIGIN cites
                no commit hash (S106)
  C11 D2        no page under src/app formats an escalation score itself;
                src/lib/escalation.ts does, with its magnitude (S106)

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
ID_RE = re.compile(r"R-S\d+-\d+|GNI-L-\d+|GNI-R-\d+|NN-PHI-\d+")
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


INPUT_RE = re.compile(
    r"^INPUT `(?P<src>[^`]+)` md5 `(?P<h>[0-9a-f]+)` \(EOL-normalised\)", re.M)
STAMP_RE = re.compile(
    r"GENERATED from `(?P<src>[^`]+)` -- (?P<n>\d+) CHECKABLE "
    r"markers, register generation (?P<gen>\d+)\.")
MAP_RE = re.compile(r"^GNI_MACRO_MAP_S(\d+)\.md$")


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
        if re.match(r"^" + re.escape(stem) + r"_S\d+\.md$", base):
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


SNAP_RE = re.compile(r"^gni_runtime_snapshot_S(\d+)\.json$")
ARCH_STAMP_RE = re.compile(
    r"^\*\*GENERATED by `tools/(?P<tool>[A-Za-z0-9_]+\.py)`(?P<rest>[^\n]*)", re.M)
MD5_IN_STAMP = re.compile(r"md5 `([0-9a-f]+)`")
FROM_IN_STAMP = re.compile(r"from `([^`]+)`")


def live_snapshot_path(root):
    """The highest-numbered runtime snapshot. Same RELATION rule as live_docs
    and live_map_path: parsed as an integer, never a lexical sort and never a
    list position (R-S92-2)."""
    docs = os.path.join(root, "docs")
    if not os.path.isdir(docs):
        raise InstrumentError("missing dir: " + docs)
    gens = [(int(m.group(1)), n) for n in os.listdir(docs)
            for m in [SNAP_RE.match(n)] if m]
    require_nonempty("runtime snapshot generations", gens)
    return os.path.join(docs, max(gens)[-1])


def arch_stamps(body):
    """Every generated-section stamp the ARCHITECTURE declares, in the order
    written. Anchored at LINE START and on the literal `tools/` because the
    completion test's own prose contains the words GENERATED by and publishes
    md5s of its own: measured at S104, a loose pattern matches four stamps
    where three exist, and the fourth is the scoreboard that grades this check.
    A check must not derive its target from what the target names (R-S103-1).

    Zero is an INSTRUMENT ERROR and never an empty list: a renamed stamp format
    must halt, not report an architecture with nothing left to check
    (R-S81-1)."""
    rows = [(m.group("tool"), m.group("rest"))
            for m in ARCH_STAMP_RE.finditer(body)]
    return require_nonempty("architecture GENERATED stamps", rows)


def _blocks_fingerprint(ctx, rest):
    """§5. The generator's own collector, over the LIVE tree."""
    from pathlib import Path
    import gni_blocks as gb
    try:
        snap = gb.collect(Path(ctx["root"]))
    except ValueError as exc:
        raise InstrumentError("the generator's own collector refused: %s" % exc)
    return snap["manifest_md5"], None


def _runtime_fingerprint(ctx, rest):
    """§6. Two ways to be stale, and the second is the one S102 actually
    suffered on the macro map: the named snapshot still exists and still hashes
    to exactly its stamped value while no longer being the live one. Liveness
    is reported with no md5 in the message at all."""
    from pathlib import Path
    import gni_runtime as gr
    named = FROM_IN_STAMP.search(rest)
    if not named:
        raise InstrumentError("the gni_runtime stamp names no snapshot")
    live = live_snapshot_path(ctx["root"])
    if os.path.basename(named.group(1)) != os.path.basename(live):
        return None, "reads %s; the live snapshot is %s" % (
            os.path.basename(named.group(1)), os.path.basename(live))
    return gr.norm_md5(Path(live).read_bytes()), None


def _state_fingerprint(ctx, rest):
    """§7. KNOWN LIMIT, disclosed rather than hidden: this fingerprint covers
    WORKFLOW BYTES ONLY. Section 7.2 also renders `gh secret list`, whose
    source is outside the tree and unreachable from CI by this harness's own
    hard boundary -- a secret added or removed leaves the section stale with
    this value still green. DECISION S104-1 ruled that hole DISCLOSED and not
    closed here; it is item 5.58, and its home is the generator's stamp, not
    this check."""
    from pathlib import Path
    import gni_state as gs
    wf_dir = os.path.join(ctx["root"], ".github", "workflows")
    if not os.path.isdir(wf_dir):
        raise InstrumentError("missing dir: " + wf_dir)
    paths = sorted(Path(wf_dir).glob("*.yml"))
    require_nonempty("workflow files", paths)
    return gs.workflow_manifest(paths), None


ARCH_GENERATORS = {
    "gni_blocks.py": _blocks_fingerprint,
    "gni_runtime.py": _runtime_fingerprint,
    "gni_state.py": _state_fingerprint,
}


def check_c8_generated_sections_fresh(ctx):
    """Item 5.54 (C8), the other half of roadmap 2's row four. Every generated
    section of the ARCHITECTURE publishes the fingerprint of what it read.
    Until S104 nothing read any of them: C2 checked section seven's COUNTS
    against the YAML, C6 checked the macro map's declared inputs, and sections
    five and six had no check of any kind.

    That was never hypothetical. Measured at S104 across twenty-four commits:
    section five's declared value disagreed with the live tree at ELEVEN of
    them. It shipped wrong by six at `9e11f57`, correct at `8ce57fc`, wrong by
    three by the S102 close at `a923ad9` -- the same stamp, byte-identical, on
    two trees -- and wrong by one at `60af1a5`, the commit whose own purpose
    was to restamp it.

    HOW IT WORKS. Each stamp is resolved to a fingerprint RULE by the name of
    the generator that wrote it, and the rule recomputes the value from the
    live tree using the generator's own code. No count of sections is written
    anywhere in this file, and a stamp naming a generator with no rule is an
    INSTRUMENT ERROR rather than a silent skip: a fourth generated section must
    announce itself, not slip past.

    NOT CHECKED, and it cannot be: each stamp also names a HEAD. Committing the
    document that carries the stamp advances HEAD, so the field is one step
    behind by construction and no working-tree check can settle it. The
    fingerprints are unaffected -- none of the three takes HEAD as an input --
    so this check reads them and leaves the HEAD field alone. DECISION S104-1
    (IEEE 828 Annex D.3: limitations are recorded, not silently assumed)."""
    docs = require_nonempty("live docs", ctx["docs"])
    arch_path = docs["GNI_ARCHITECTURE"]
    body = require_nonempty("architecture text", read(arch_path))
    stamps = arch_stamps(body)
    problems = []
    for tool, rest in stamps:
        rule = ARCH_GENERATORS.get(tool)
        if rule is None:
            raise InstrumentError("no fingerprint rule for generator: " + tool)
        stamped = MD5_IN_STAMP.search(rest)
        if not stamped:
            raise InstrumentError("the %s stamp declares no md5" % tool)
        live_h, note = rule(ctx, rest)
        if note:
            problems.append("%s: %s" % (tool, note))
        elif stamped.group(1) != live_h:
            problems.append("%s: live md5 %s; section stamped %s"
                            % (tool, live_h, stamped.group(1)))
    if problems:
        return False, "; ".join(problems)
    return True, "%s: %d generated sections resolve live and match" % (
        os.path.basename(arch_path), len(stamps))


SLO_KEYS = ("BOUND_HOURS", "EXCEEDANCE_MAX", "WINDOW_FROM", "WINDOW_TO",
            "SPLIT_RATIO", "WORKFLOW", "SNAPSHOT")
SLO_RE = re.compile(r"^- SLO-CFG ([A-Z_]+): `([^`]+)`", re.M)
DAY_FMT = "%Y-%m-%d"


def slo_cfg(arch_text):
    """Section 10 IS the configuration. C5 forbids this file from holding the
    numbers (R-S81-5), so every constant is parsed out of the committed
    document and a missing key halts rather than defaults."""
    cfg = dict(SLO_RE.findall(require_nonempty("architecture text", arch_text)))
    missing = [k for k in SLO_KEYS if k not in cfg]
    if missing:
        raise InstrumentError("SLO-CFG missing: " + ", ".join(missing))
    return cfg


def protection_windows(root):
    """R-S96-3: the watcher's own bytes are the only source for its standdown.
    Read by AST, because counting a code literal is never a regex job
    (R-S75-1)."""
    path = os.path.join(root, "ai_engine", "monitoring_pipeline.py")
    if not os.path.isfile(path):
        raise InstrumentError("missing watcher: " + path)
    for node in ast.walk(ast.parse(read(path))):
        if not isinstance(node, ast.Assign):
            continue
        for tgt in node.targets:
            if isinstance(tgt, ast.Name) and tgt.id == "PROTECTION_WINDOWS":
                return [tuple(w) for w in ast.literal_eval(node.value)]
    raise InstrumentError("no PROTECTION_WINDOWS assignment in " + path)


def heartbeat_stands_down(root):
    """Does the watcher still consult its own protection windows?
    Until S102 it did, and a run inside a window returned before it
    opened a connection while still reporting success (order item 6.12).
    `GNI-R-122` was amended at S102 to bind ADAPTIVE and MANUAL runs, so
    the call set IS the rule's subject test -- asked of the tree, never
    assumed here, because an assumption cannot go red when it stops being
    true. The window table itself is still read: adaptive still uses it."""
    path = os.path.join(root, "ai_engine", "monitoring_pipeline.py")
    if not os.path.isfile(path):
        raise InstrumentError("missing watcher: " + path)
    for node in ast.walk(ast.parse(read(path))):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "is_protection_window"):
            return True
    return False


def in_protection(when, windows):
    now = (when.hour, when.minute)
    for oh, om, ch, cm in windows:
        lo, hi = (oh, om), (ch, cm)
        if lo <= hi:
            if lo <= now < hi:
                return True
        elif now >= lo or now < hi:
            return True
    return False


def effective_gaps(runs, windows, lo, hi):
    """The gap between CHECKS, not between runs. Pass windows=[] when the
    watcher no longer stands down: every run then performs its check, so
    the check gap and the run gap are the same number."""
    kept = [t for t in runs
            if lo <= t.strftime(DAY_FMT) <= hi and not in_protection(t, windows)]
    return sorted(kept[i + 1] - kept[i] for i in range(len(kept) - 1))


def check_c7_slo_freshness(ctx):
    """SLO-2 and SLO-3 of ARCHITECTURE section 10.

    (a) The published bound must be the smallest whole hour that keeps
        exceedance inside the published budget. Too low fails on exceedance;
        too high fails because a smaller hour would also have passed. A bound
        that is compared rather than derived can be padded until it is always
        green, which is the disease this whole section was written against.
    (b) The published window must hold one regime. A p90 across a step change
        describes no day that happened (DECISION S90-3). A split is only
        counted when both halves hold at least 1 / EXCEEDANCE_MAX gaps --
        derived, not chosen: below that a p90 does not exist and a one-gap
        half reports its own gap as a median.

    Constants come from the document, protection windows from the watcher's
    AST, the quantile from the section 6 generator rather than a second
    implementation (R-S96-3). A window the snapshot cannot cover raises
    INSTRUMENT ERROR: "this data cannot answer this question" is a different
    answer from "the promise was kept" (R-S81-1)."""
    import json
    from datetime import timedelta
    import gni_runtime as gr

    cfg = slo_cfg(read(require_nonempty("live architecture",
                                        ctx["docs"]["GNI_ARCHITECTURE"])))
    emax = float(cfg["EXCEEDANCE_MAX"])
    ratio = float(cfg["SPLIT_RATIO"])
    bound_h = float(cfg["BOUND_HOURS"])
    frm, to = cfg["WINDOW_FROM"], cfg["WINDOW_TO"]

    snap = os.path.join(ctx["root"], cfg["SNAPSHOT"])
    if not os.path.isfile(snap):
        raise InstrumentError("missing snapshot: " + snap)
    with open(snap, "rb") as fh:
        data = json.loads(fh.read().decode("utf-8"))
    wf = data.get("workflows", {}).get(cfg["WORKFLOW"])
    if not wf:
        raise InstrumentError("snapshot holds no " + cfg["WORKFLOW"])
    runs = sorted(gr._dt(r["createdAt"]) for r in wf["runs"])
    require_nonempty("runs in the snapshot", runs)

    span_lo, span_hi = runs[0].strftime(DAY_FMT), runs[-1].strftime(DAY_FMT)
    if span_lo > frm or span_hi < to:
        raise InstrumentError(
            "snapshot spans %s..%s; the published window is %s..%s"
            % (span_lo, span_hi, frm, to))

    windows = protection_windows(ctx["root"])   # must exist: adaptive uses it
    if not heartbeat_stands_down(ctx["root"]):
        windows = []
    gaps = effective_gaps(runs, windows, frm, to)
    require_nonempty("effective check gaps in the published window", gaps)
    floor = round(1 / emax)
    if len(gaps) < floor:
        raise InstrumentError(
            "%d gaps in %s..%s; a quantile at %.2f needs at least %d"
            % (len(gaps), frm, to, 1 - emax, floor))

    hour = timedelta(hours=1)
    budget = emax * len(gaps)
    steps = 1
    while sum(1 for g in gaps if g > hour * steps) > budget:
        steps += 1
    over = sum(1 for g in gaps if g > hour * bound_h)

    problems = []
    if steps != bound_h:
        problems.append(
            "BOUND_HOURS is %s; the smallest whole hour inside the budget is %d "
            "(%d of %d gaps exceed the published bound)"
            % (cfg["BOUND_HOURS"], steps, over, len(gaps)))

    days = sorted(set(t.strftime(DAY_FMT) for t in runs
                      if frm <= t.strftime(DAY_FMT) <= to))
    require_nonempty("days in the published window", days)
    worst, at = None, None
    for i in range(1, len(days)):
        early = effective_gaps(runs, windows, days[0], days[i - 1])
        late = effective_gaps(runs, windows, days[i], days[-1])
        if len(early) < floor or len(late) < floor:
            continue
        r = gr.quantf(late, 0.5) / gr.quantf(early, 0.5)
        if r < 1:
            r = 1 / r
        if worst is None or r > worst:
            worst, at = r, days[i]
    if worst is not None and worst >= ratio:
        problems.append(
            "window %s..%s spans a regime boundary at %s: check p50 ratio %.2f"
            % (frm, to, at, worst))

    # (c) S105, item 9.21: the public pages carry the bound through ONE constant that
    # mirrors SLO-CFG. A moved bound must redden here until the pages follow it.
    web = os.path.join(ctx["root"], "src", "lib", "freshness.ts")
    if not os.path.isfile(web):
        problems.append("no public freshness constant at src/lib/freshness.ts")
    else:
        with open(web, "rb") as fh:
            ts = fh.read().decode("utf-8")
        for key in ("BOUND_HOURS", "EXCEEDANCE_MAX", "WINDOW_FROM", "WINDOW_TO"):
            m = re.search(r"^export const FRESHNESS_%s = '?([^'\s]+)'?\s*$" % key, ts, re.M)
            seen = m.group(1) if m else None
            if key.startswith("WINDOW"):
                same = seen == cfg[key]
            else:
                same = seen is not None and float(seen) == float(cfg[key])
            if not same:
                problems.append("src/lib/freshness.ts FRESHNESS_%s is %s; SLO-CFG says %s"
                                % (key, seen, cfg[key]))

    if problems:
        return False, "; ".join(problems)
    return True, ("%s h is the smallest hour inside a %.2f budget; %d of %d gaps "
                  "exceed it; worst counted split %s"
                  % (cfg["BOUND_HOURS"], emax, over, len(gaps),
                     "none" if worst is None else "%.2f" % worst))

# ---- S106, ROADMAP 3 row R3-1: GLOSSARY + ORIGIN -----------------------
# C9 is C1 generalised (spec S102 section 3), with the one difference S106
# measured: an id has a grammar and an abbreviation does not. 593 distinct
# all-capitals tokens in the S105 live docs, most of them emphasis. So a
# token is a CANDIDATE only when no part of it is used as a lowercase word
# anywhere in docs/ prose, and the glossary must then define it, list it as
# NOT an abbreviation, or cover it with a NAMESPACES pattern. Every list the
# check consults lives in the glossary, never in this file (C1's manifest
# discipline).
# LIMITS, written down (IEEE 828 D.3), not discovered later:
#   - an abbreviation spelled like an English word used lowercase in docs/
#     (MAD, AI, EU, ARB, SHA, GEO at S106) is invisible to the filter; it is
#     defined because a human wrote it, not because the check forced it.
#   - fenced and inline code are not prose and are not scanned.
#   - a DEFINED row nobody uses any more is not detected.
GLOSSARY_RE = re.compile(r"^GNI_GLOSSARY_S(\d+)\.md$")
ORIGIN_NAME = "GNI_ORIGIN.md"
GLOSSARY_SECTIONS = ("DEFINED", "NOT ABBREVIATIONS", "NAMESPACES",
                     "SESSION INDEX", "CHECKS")
SESSION_STATUSES = {"CHAT-ONLY"}
FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_RE = re.compile(r"`[^`\n]*`")
TOKEN_RE = re.compile(r"(?<![\w./-])[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*(?![\w./]|-[A-Z0-9])")
LOWER_RE = re.compile(r"(?<![\w./-])[a-z]+(?![\w./-])")
SESSION_CITE_RE = re.compile(r"(?<![\w])S(\d+)(?![\w])")
RECORD_RE = re.compile(r"_S(\d+)\.[A-Za-z]+$")
SHA_RE = re.compile(r"(?<![\w])(?=[0-9a-f]*[0-9])(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}(?![\w])")


def prose(text):
    """Text with fenced and inline code removed. Code is not prose."""
    return INLINE_RE.sub(" ", FENCE_RE.sub(" ", text))


def glossary_paths(root):
    docs = os.path.join(root, "docs")
    if not os.path.isdir(docs):
        raise InstrumentError("missing dir: " + docs)
    return [(int(m.group(1)), os.path.join(docs, n))
            for n in os.listdir(docs) for m in [GLOSSARY_RE.match(n)] if m]


def live_glossary_path(root):
    """Highest session number, parsed as an integer (R-S92-2)."""
    gens = glossary_paths(root)
    if not gens:
        raise InstrumentError("no glossary generation found")
    return max(gens)[1]


def origin_path(root):
    return os.path.join(root, "docs", ORIGIN_NAME)


def glossary_sections(text):
    """Each section is found by its exact heading, exactly once. A renamed
    or doubled heading HALTS: an absent section must never read as an empty
    allowlist (the C1 manifest lesson)."""
    lines = text.split("\n")
    out = {}
    for sec in GLOSSARY_SECTIONS:
        idx = [i for i, ln in enumerate(lines) if ln.strip() == "## " + sec]
        if len(idx) != 1:
            raise InstrumentError("glossary section not found exactly once: " + sec)
        rows = []
        for ln in lines[idx[0] + 1:]:
            if ln.startswith("## "):
                break
            if not ln.startswith("|"):
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if set(cells[0]) <= set("-: "):
                continue
            rows.append(cells)
        out[sec] = rows[1:]
    return out


def first_cells(rows):
    return {r[0].strip("`* ") for r in rows if r[0].strip("`* ")}


def english_words(root):
    """Lowercase prose words of every .md under docs/, glossaries excluded:
    a definition's own words must not hide the term it defines."""
    skip = {os.path.abspath(p) for _, p in glossary_paths(root)}
    words = set()
    for dirpath, _, files in os.walk(os.path.join(root, "docs")):
        for n in sorted(files):
            p = os.path.join(dirpath, n)
            if n.endswith(".md") and os.path.abspath(p) not in skip:
                words |= set(LOWER_RE.findall(prose(read(p))))
    return require_nonempty("english corpus", words)


def candidate_tokens(text, english):
    """{token} a reader cannot decode from English, ids removed first (C1
    owns them). Single letters are not abbreviations."""
    out = set()
    for tok in TOKEN_RE.findall(ID_RE.sub(" ", prose(text))):
        if not tok[1:]:
            continue
        parts = [p for p in tok.split("-") if re.search(r"[A-Z]", p)]
        if parts and all(p.lower() in english for p in parts):
            continue
        out.add(tok)
    return out


def scanned_docs(ctx):
    out = dict(ctx["docs"])
    out["GNI_ORIGIN"] = origin_path(ctx["root"])
    return out


def check_c9_glossary(ctx):
    """R3-1. Every candidate token in a live doc or in ORIGIN is defined,
    declared not-an-abbreviation, or matched by a declared namespace; and
    every check this file runs has a row in the glossary's CHECKS section,
    so the check rows are verified against CHECKS rather than typed twice."""
    sec = glossary_sections(read(live_glossary_path(ctx["root"])))
    defined = require_nonempty("glossary DEFINED rows", first_cells(sec["DEFINED"]))
    allowed = defined | first_cells(sec["NOT ABBREVIATIONS"])
    try:
        pats = [re.compile(p) for p in first_cells(sec["NAMESPACES"])]
    except re.error as exc:
        raise InstrumentError("bad NAMESPACES pattern: %s" % exc)
    require_nonempty("glossary NAMESPACES rows", pats)
    english = english_words(ctx["root"])
    bad, seen = {}, set()
    for stem, path in sorted(scanned_docs(ctx).items()):
        cands = candidate_tokens(require_nonempty("text of " + stem, read(path)), english)
        seen |= cands
        for tok in sorted(cands):
            if tok in allowed or any(p.fullmatch(tok) for p in pats):
                continue
            bad.setdefault(tok, []).append(stem)
    require_nonempty("candidate tokens across live docs", seen)
    rows = first_cells(sec["CHECKS"])
    missing = [name.split()[0] for name, _ in CHECKS if name.split()[0] not in rows]
    problems = ["%s undefined (%s)" % (t, ",".join(s)) for t, s in sorted(bad.items())]
    problems += ["no CHECKS row for %s" % m for m in missing]
    if problems:
        return False, "; ".join(problems)
    return True, ("%d candidates resolve: %d defined, %d declared not abbreviations, "
                  "%d namespaces; every check has a row"
                  % (len(seen), len(defined), len(allowed - defined), len(pats)))


def check_c10_origin_citations(ctx):
    """R3-1. Every session ORIGIN cites has a record: a file under docs/
    carrying that session number, or a SESSION INDEX row declaring it
    CHAT-ONLY. Commit hashes are refused outright: ORIGIN is append-only and
    never regenerated, and the declared history rewrite changes every hash,
    so a hash cited there breaks by construction (DECISION S106-2)."""
    root = ctx["root"]
    text = read(origin_path(root))
    cited = {int(n) for n in SESSION_CITE_RE.findall(ID_RE.sub(" ", text))}
    require_nonempty("ORIGIN session citations", cited)
    docs = os.path.join(root, "docs")
    records = {int(m.group(1)) for n in os.listdir(docs) for m in [RECORD_RE.search(n)] if m}
    require_nonempty("session records under docs/", records)
    sec = glossary_sections(read(live_glossary_path(root)))
    chat = set()
    for r in sec["SESSION INDEX"]:
        m = SESSION_CITE_RE.fullmatch(r[0].strip("`* "))
        if m and r[-1].strip("`* ") in SESSION_STATUSES:
            chat.add(int(m.group(1)))
    unresolved = sorted(cited - records - chat)
    hashes = sorted(set(SHA_RE.findall(text)))
    problems = ["S%d has no record and no CHAT-ONLY row" % n for n in unresolved]
    problems += ["commit hash %s cited (rewrite-unsafe)" % h for h in hashes]
    if problems:
        return False, "; ".join(problems)
    return True, ("%d sessions cited: %d by a record under docs/, %d declared CHAT-ONLY"
                  % (len(cited), len(cited & records), len(cited - records)))


# ---- S106, order item 9.22(c) / definition-of-done line D2 ------------
# The S105 command for D2 grepped for FILES containing `escalation_score` and
# was blind both ways: it listed pages that only declare the field, and its
# pathspec could not see src/app/page.tsx - the home page, which rendered the
# capped score twice. This check reads RENDERING by grammar instead, the way
# C4 reads client construction: the identifier followed by `.toFixed(` or by
# `}/10`. LIMIT, written down: a score formatted through an intermediate
# variable (`const s = r.escalation_score; s.toFixed(1)`) is not seen.
ESC_LIB = os.path.join("src", "lib", "escalation.ts")
ESC_RENDER_RE = re.compile(
    r"(?<![\w])(?:avg_)?escalation_score(?![\w])[^\n;]{0,25}?\.toFixed\("
    r"|(?<![\w])(?:avg_)?escalation_score(?![\w])\s*\}\s*/10")


def check_c11_escalation_magnitude(ctx):
    """D2. Every escalation score a page shows goes through the one lib that
    shows its uncapped magnitude beside it (ICD 203 tradecraft 1 and 2)."""
    root = ctx["root"]
    lib = read(os.path.join(root, ESC_LIB))
    require_nonempty("formatEscalation exported by " + ESC_LIB,
                     "export function formatEscalation" in lib)
    app = os.path.join(root, "src", "app")
    pages = sorted(os.path.join(d, n) for d, _, fs in os.walk(app)
                   for n in fs if n.endswith(".tsx"))
    require_nonempty("page files under src/app", pages)
    bad, users = [], []
    for p in pages:
        text = read(p)
        if "@/lib/escalation" in text:
            users.append(p)
        for i, ln in enumerate(text.split("\n"), 1):
            if ESC_RENDER_RE.search(ln):
                bad.append("%s:%d" % (os.path.relpath(p, root), i))
    require_nonempty("pages importing @/lib/escalation", users)
    if bad:
        return False, "escalation score formatted outside the lib at " + ", ".join(bad)
    return True, "%d pages format escalation through %s; none format it directly" % (
        len(users), ESC_LIB)


CHECKS = (
    ("C1 R-S90-2  rule citations", check_c1_citations),
    ("C2 R-S91-5  workflow counts", check_c2_workflow_counts),
    ("C3 R-S74-1  register uniqueness", check_c3_register_uniqueness),
    ("C4 R-S62-3  no-store client", check_c4_nostore_client),
    ("C5 R-S81-5  self-lint", check_c5_self_lint),
    ("C6 R-S95-4  macro map fresh", check_c6_macro_map_fresh),
    ("C7 SLO-2+3  freshness bound", check_c7_slo_freshness),
    ("C8 R-S104-1 generated sections", check_c8_generated_sections_fresh),
    ("C9 R3-1     glossary", check_c9_glossary),
    ("C10 R3-1    origin citations", check_c10_origin_citations),
    ("C11 D2      escalation magnitude", check_c11_escalation_magnitude),
)


def build_ctx(root, self_path):
    return {"root": root, "self_path": self_path, "docs": live_docs(root)}


def _probe_halts(what, fn, arg):
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
    arch = read(live_docs(root)["GNI_ARCHITECTURE"])
    _probe_halts("a renamed GENERATED stamp still parsed", arch_stamps,
                 arch.replace("**GENERATED by `tools/", "XX-RENAMED-XX `tools/"))
    gloss = read(live_glossary_path(root))
    _probe_halts("a renamed glossary section still parsed", glossary_sections,
                 gloss.replace("## DEFINED", "## XX-RENAMED-XX", 1))


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
