#!/usr/bin/env python3
"""tools/mk_rules_s95_markers.py - S95 mission deliverable.

Writes a CHECKABLE marker with a one-line reason under every rule definition in
docs/GNI_RULES_S95.md, and emits docs/GNI_RULE_CHECKABILITY_S95.tsv from the
SAME dict, so the prose and the table can never disagree.

THE STANDARD, stated so it can be argued with:
  yes = a command or assert can be NAMED in one line and would run TODAY against
        repo bytes, git working tree, workflow YAML, or the DB.
  no  = it cannot, and the reason says WHAT IS MISSING (no artifact, a
        counterfactual, or a fact about how a constant was derived).
"CHECKABLE" is not "important". R-S90-1, the most load-bearing rule GNI holds,
is `no`: asking what an output would look like had the change NOT shipped is a
counterfactual, and no script can evaluate it.

R-S92-2 is `no` and was `yes` for most of this session. Three designs died
against measurement. Recorded because the correction is the finding (R-S84-3).
"""
import os
import re
import sys

SRC = "docs/GNI_RULES_S95.md"
TSV = "docs/GNI_RULE_CHECKABILITY_S95.tsv"
ID_RE = re.compile(r"R-S\d+-\d+|LR-\d+|GNI-R-\d+|NN-PHI-\d+")
MARK = "CHECKABLE:"

C = {}
def y(rid, why): C[rid] = ("yes", why)
def n(rid, why): C[rid] = ("no", why)

# ---- shipped as executable checks this session -------------------------------
y("R-S90-2", "SHIPPED C1: cited ids diffed against registered + PART 0 manifest")
y("R-S91-5", "SHIPPED C2: workflow/trigger counts derived from YAML vs section 7.1")
y("R-S74-1", "SHIPPED C3: every repeated definition id must declare AMENDMENT/INSTANCE")
y("R-S62-3", "SHIPPED C4: git grep createClient under src/app/api must be empty")
y("R-S81-5", "SHIPPED C5: AST lint - no check function may hold a hand-written integer")

# ---- R-S54 .. R-S58 ----------------------------------------------------------
n("R-S54-1", "governs how a write is DELIVERED in chat; the repo records no delivery method")
n("R-S54-2", "a judgement about which source to trust when two disagree")
n("R-S54-3", "about terminal state after a paste; no committed artifact holds it")
n("R-S54-4", "chooses a verification tool for a human; nothing to assert against")
n("R-S54-5", "a cognitive tell - felt familiarity has no representation in bytes")
y("GNI-R-240", "grep ai_engine/mad_runner.py for the polling gate constants (60s, 25 attempts)")
y("GNI-R-241", "SQL: rows past Stage 1 with content_type IS NULL must be zero")
n("GNI-R-242", "governs when a claim may be CALLED done; the claim lives in prose")
n("LR-078", "patch scripts live in /tmp and are never committed - nothing to scan")
y("LR-091", "every os.getenv name must resolve to a stored secret or a workflow env (section 7.2 emits the join)")
y("LR-092", "python -m py_compile over changed .py files in CI")
n("LR-095", "governs how a human diagnoses an HTTP error, not the shape of code")
n("LR-096", "no truncation convention exists to assert prompt fields against")
y("LR-098", "every package in a workflow inline pip list must be imported by a reachable module")
n("LR-099", "an audit obligation on the agent; no artifact records whether it happened")
n("LR-102", "a cognitive tell; confidence is not stored anywhere")
n("LR-103", "governs the CHOICE of test input, which the test file does not record")
n("LR-104", "ranks candidate work by risk before it exists; no artifact to rank")
n("LR-105", "forbids cosmetic green; distinguishing cosmetic from real needs the intent")
y("LR-106", "AST: every _parse_json_response-class function's return paths yield dict or None")
n("LR-107", "governs trust in a prior session's claim; trust has no byte form")
n("NN-PHI-1", "a value statement about who GNI serves; no measurable predicate")
n("NN-PHI-2", "requires judging whether coverage is direction-balanced; needs a labelled corpus")
n("NN-PHI-3", "detecting manipulation in output requires reading the output for meaning")
y("NN-PHI-4", "SQL: reports rows with fff_human_path IS NULL must be zero (needs DB, not CI)")
n("NN-PHI-5", "OPEN since S37; 'coverage gap' has no operational definition to assert")
n("NN-PHI-6", "requires weighing a source's authority - a judgement about content")
n("NN-PHI-7", "a policy about when to reset data; the trigger is a human decision")
n("R-S55-1", "'all consumers of a shared route' has no mechanical boundary")
n("R-S55-2", "widening a pattern is an act of imagination; there is no wider-pattern oracle")
n("R-S55-3", "about the ORDER of two steps in a terminal session; no artifact")
n("R-S55-4", "bundling policy for model-coupled fixes; scope lives in the plan, not the tree")
n("R-S55-5", "records the adoption of Protocol v1 - a historical fact, not a predicate")
y("R-S56-1", "grep every Telegram send site: an HTML-mode send interpolating external text must call the escape helper")
n("R-S57-1", "governs patch scripts in /tmp; the repo keeps no copy of them")
n("R-S58-1", "same as R-S57-1 - the banned open() lives in uncommitted patch scripts")

# ---- R-S59 .. R-S80 ----------------------------------------------------------
n("R-S59-1", "'census before sweep' is an ordering of two human acts; no artifact")
n("R-S60-1", "about a browser hard-refresh before verifying; nothing in the repo")
n("R-S60-2", "a design principle: structure is not grounding. No predicate over bytes")
n("R-S60-3", "'ungrounded into grounded' requires knowing which layer is grounded - a judgement")
n("R-S62-1", "governs how a Claude Code task is handed over; no committed artifact")
n("R-S62-2", "placeholder marking lives in a chat message, not in the tree")
n("R-S63-1", "'reply-number maps to list POSITION' needs the consumer's semantics")
n("R-S63-2", "'guilty until verified' is a stance toward a resource, not a code shape")
n("R-S63-3", "requires proving a branch can be reached again - a reachability proof, not a grep")
y("R-S64-1", "grep audit/census scripts for .limit( - a whole-table audit may not truncate")
n("R-S64-2", "about what an aggregate CANNOT answer; absence of an answer is not greppable")
y("R-S64-3", "assert the fallback dedupe key is a parsed feed domain, not a display name")
n("R-S65-1", "'consult yield or serve-path' requires reading what a criterion MEANS")
n("R-S65-2", "chat clearance before a git trigger; the clearance is a chat turn")
y("R-S65-3", "assert no \\\\b wrapper is applied to entries in the stem keyword lists")
n("R-S66-1", "which census proves which claim - an epistemic distinction, not a byte one")
n("R-S66-2", "requires measuring what real signal entered through a bug - needs the corpus")
n("R-S66-3", "no in-code proxy-declaration convention exists to assert against")
n("R-S67-1", "numbered gates with the push first - about message structure")
n("R-S67-2", "verifying an instrument's RANGE means reasoning about caps and short-circuits")
y("R-S68-1", "grep workflow YAML and call-site literals for model-name strings not sourced from env")
n("R-S68-2", "a platform fact about log masking, not a rule the repo can violate")
n("R-S69-1", "'history says which side is canonical' - the evidence is conversation records")
n("R-S69-2", "requires deciding whether a queue row genuinely instruments a deferral")
y("R-S69-3", "assert every module under ai_engine/analysis is imported by an entrypoint-reachable module")
y("R-S70-1", "emit writers-per-table from the tree and fail when the set changes (snapshot)")
y("R-S70-2", "wc -l on disk against the expected count before first commit")
n("R-S71-1", "'the owning writer wins' requires knowing who owns a row")
n("R-S71-2", "'census the CLASS' - naming the class is the judgement being asked for")
n("R-S72-1", "patch-script rule; those scripts are never committed")
y("R-S73-1", "detect the same literal list or threshold defined in two files (duplicate-constant lint)")
n("R-S73-2", "requires knowing which consumers are feedback loops and which are exhibits")
y("R-S74-2", "compare TypeScript interface fields against information_schema.columns")
y("R-S74-3", "assert every cert record names the checkout SHA it was read from")
y("R-S75-1", "assert count guards over code literals derive expected values via ast, not regex")
n("R-S75-2", "'read the full call site' is an instruction to a reader, not a predicate")
y("R-S75-3", "grep funnel aggregates for counts conditioned on one stage flag only")
n("R-S76-1", "patch-script rule; not committed")
n("R-S76-2", "an oracle spec's fidelity to bytes is judged by comparing meanings")
n("R-S76-3", "an arithmetic tell about a suspicious table; needs the numbers in hand")
n("R-S77-1", "about chaining commands in a paste block; no artifact")
y("R-S77-2", "grep live docs for a bare numeric count that no generator emits")
n("R-S77-3", "verifying a label's ATTRIBUTION requires knowing what the system is called")
n("R-S78-1", "about a UI write interrupted by auth; the platform holds no record")
n("R-S78-2", "'which path served it' requires reading run logs for probe prints, per run")
n("R-S79-1", "about the deliverable form of an instruction in chat")
n("R-S79-2", "requires grepping live logs, which vary per run")
n("R-S80-1", "patch-script rule; not committed")
n("R-S80-2", "'the call-shape it holds' requires comparing a fixture's shape to production's")
n("R-S80-3", "labelling speculation at output seams needs to know which claims are speculative")

# ---- R-S81 .. R-S94 ----------------------------------------------------------
y("R-S81-1", "assert every guard proves its input was non-empty before reporting a zero")
y("R-S81-2", "grep budget assemblers for a paired INCLUDED-vs-AVAILABLE print")
y("R-S81-3", "grep budget code for a share computed from another consumer's remainder")
n("R-S81-4", "one load-bearing block per message - a property of a chat turn")
n("R-S81-6", "'contents vs agreement' requires knowing what was agreed")
y("R-S81-7", "assert no live doc states a cron time as a start time; the band must be emitted")
n("R-S81-8", "a fact about how Groq refills; violating it means holding a wrong mental model")
y("R-S82-1", "assert artifact searches grep a structural marker, not a phrase")
n("R-S82-2", "'the whole category' requires naming the category under test")
n("R-S82-3", "'a stopgap never closes a root' - classifying a fix as stopgap is judgement")
y("R-S82-4", "assert the Protocol's template fields match what the live HANDOFF contains")
y("R-S82-5", "git log: count sessions in which CONTRACT was edited over a window")
n("R-S83-1", "a disclosed limitation is a claim - trust level has no byte form")
n("R-S83-2", "novelty is identity; no artifact records which runs have been read")
n("R-S83-3", "about reading a clock inside the block that makes a claim")
n("R-S83-4", "distinguishing mechanics from instrument is the same counterfactual as R-S90-1")
n("R-S83-5", "requires the pasted opening prompt, which reaches no file")
n("R-S83-6", "flow vs stock - a modelling distinction, not a code shape")
n("R-S84-1", "'measure instead of deriving' - the choice happens before code exists")
n("R-S84-2", "which meter ENFORCES is a fact about the platform, not the repo")
y("R-S84-3", "assert every entry in a session's WRONG ledger has a home in a live doc")
y("R-S84-4", "assert MAD run classification keys on the ARB-FIT marker, never on run time")
y("R-S85-1", "grep every lettered proposal block in a close doc for a LINEAGE: line")
y("R-S85-2", "assert copy sweeps run case-insensitively and code sweeps case-sensitively")
n("R-S85-3", "the guard string must be unique to the PATCHED state - needs both states")
n("R-S85-4", "'folded into another arc' requires tracing a finding's routing history")
y("R-S85-5", "assert every docs/*REGISTER*.md is referenced by a live doc or a workflow")
y("R-S85-6", "git log: a feature commit's message must contain a FAILURE TEST line")
n("R-S86-1", "'recent runs are not a baseline' - window width is a statistical judgement")
n("R-S86-2", "two instruments printing one word - requires knowing what each counts")
y("R-S86-3", "measure over stored runs whether a conditional ever evaluated False")
n("R-S86-4", "a prompt from bytes not transcript - about where a human read from")
n("R-S86-5", "a refuted prediction naming a missing condition - interpretive")
n("R-S86-6", "commit subjects carry intent - intent is not checkable")
n("R-S87-1", "'pre-selected set' requires knowing the selection that produced the set")
y("R-S87-2", "measure over stored runs: a published metric constant at its cap")
n("R-S87-3", "'single-regime corpus' requires knowing the regimes in the data")
y("R-S87-4", "same detector as R-S69-3: a shipped field with no consumer in the chain")
n("R-S87-5", "MSYS argument translation - a shell fact, not a repo predicate")
y("R-S87-6", "same check as R-S81-7: lateness must be emitted from observation, not recalled")
y("R-S87-7", "grep ratio print sites and assert the denominator variable is named")
n("R-S88-1", "about paste blocks in chat")
n("R-S88-2", "'read a gate literally' - narrowing scope is a reading, not a byte")
n("R-S88-3", "requires reading the generations between two files to see what moved")
n("R-S88-4", "design the extraction for the question - about command design before running")
y("R-S88-5", "measure GEO pillar hits against its cap over stored runs")
y("R-S89-1", "same grep as R-S85-1, widened to every finding block")
y("R-S89-2", "before a deletion proposal, assert the column has zero consumers in src/")
y("R-S89-3", "DB: a rendered column must have at least one non-null row before its blank is read as a defect")
n("R-S90-1", "a counterfactual - what the output would look like had the change NOT shipped. No script can evaluate it, and it is the most load-bearing rule GNI holds")
n("R-S90-3", "'re-emit preconditions' - about how a revision is communicated")
n("R-S90-4", "binds a class of items within one session; the class is named by judgement")
y("R-S91-1", "the harness job already runs this: a wiring commit whose test callers were not swept fails on import")
n("R-S91-2", "verifying each item of a bundle separately - the bundling is a claim in prose")
y("R-S91-3", "lint count-producing greps: an ORed pattern may not be used as a count")
n("R-S91-4", "premise disproven at S91 (item 5.19); a classification grep's status is interpretive")
n("R-S92-1", "a deadline's originating evidence lives in session history, not beside the date")
n("R-S92-2", "position-decay lives in HOW the constant was derived, not in the call site. limit(1000) and limit(332) are byte-identical in shape and both carry .order(). Three check designs died against measurement this session")
y("R-S93-1", "assert every tool in tools/ has a control-probe or selftest path")
n("R-S94-1", "a review is a lead - trust level again, with no byte form")
y("R-S94-2", "assert identifier comparisons fold case the way the platform stores the name")
y("R-S94-3", "assert CLI parsers do not depend on TTY-only output shape (no header assumption)")
n("R-S94-4", "build against a fixture first - an ordering of two acts, not a repo state")


# S94 wrote three markers at line start and one mid-sentence. Searching
# only at line start finds 3 of 4 and silently duplicates the fourth, so the
# marker is located ANYWHERE in the line (R-S82-1: grep the structure).
MARKER_RE = re.compile(r"\*\*CHECKABLE:\s*(yes|no)\*\*")


def definition_lines(text):
    """Same locator tools/gni_rule_checks.py uses. PART 1 and PART 2 are an
    index and a cluster map; their mentions are citations, not definitions.
    Boundaries are found by heading text, never by line number."""
    # splitlines(), NOT split("\n"): on a CRLF file the latter leaves a \r on
    # every line, and re-joining with \r\n then writes \r\r\n everywhere.
    # Shipped that corruption once; the diff was the only witness.
    lines = text.splitlines()
    def heading(prefix):
        for i, ln in enumerate(lines):
            if ln.startswith(prefix):
                return i
        sys.exit("REFUSE: heading not found: " + prefix)
    a, b = heading("# PART 1"), heading("# PART 3")
    d = re.compile(r"^\s{0,2}(?:-\s*)?(?:\*\*)?(" + ID_RE.pattern +
                   r")(?:\*\*)?\s*(?:[:\u2014-]|\()")
    h = re.compile(r"^##\s*(" + ID_RE.pattern + r")\b")
    out = []
    for i, ln in enumerate(lines):
        if a <= i < b:
            continue
        m = d.match(ln) or h.match(ln)
        if m:
            out.append((m.group(1), i))
    return lines, out


def existing_markers(lines, defs):
    """S94 classified its own four rules one session early, in this exact
    format. Those verdicts are not re-stated; they are HONOURED, and a
    disagreement halts the script rather than quietly overwriting a published
    ruling."""
    starts = sorted(set(i for _, i in defs))
    owner = {}
    for rid, i in defs:
        owner.setdefault(rid, i)
    found = {}
    for rid, i in sorted(owner.items(), key=lambda kv: kv[1]):
        nxt = next((s for s in starts if s > i), len(lines))
        for ln in lines[i:nxt]:
            m = MARKER_RE.search(ln)
            if m:
                found[rid] = m.group(1)
                break
    return found


def main():
    if not os.path.isfile(SRC):
        sys.exit("REFUSE: %s not found" % SRC)
    with open(SRC, "rb") as fh:
        raw = fh.read()
    nl = "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") - raw.count(b"\r\n") else "\n"
    text = raw.decode("utf-8-sig")
    lines, defs = definition_lines(text)

    # Completeness both ways, before a single byte is written (R-S81-5, R-S55-3).
    ids = set(rid for rid, _ in defs)
    missing = sorted(ids - set(C))
    extra = sorted(set(C) - ids)
    if missing:
        sys.exit("REFUSE: %d registered ids have no classification: %s"
                 % (len(missing), missing[:8]))
    if extra:
        sys.exit("REFUSE: %d classified ids are not in the register: %s"
                 % (len(extra), extra[:8]))

    prior = existing_markers(lines, defs)
    # HANDOFF S94 states FOUR S94 rules carry a marker. A different number means
    # the locator is wrong, not that the file changed (R-S81-1).
    if len(prior) != len([r for r in prior if r.startswith("R-S94-")]) or len(prior) < 1:
        sys.exit("REFUSE: prior markers found outside R-S94: %s" % sorted(prior))
    clash = sorted(r for r, v in prior.items() if C[r][0] != v)
    if clash:
        sys.exit("REFUSE: verdict disagrees with an existing marker: %s" % clash)

    first = {}
    for rid, i in defs:
        first.setdefault(rid, i)
    # A rule's prose is hard-wrapped, so the marker goes AFTER the block's last
    # non-empty line, not after the first. Inserting after the definition line
    # splits a sentence in half.
    starts = sorted(set(i for _, i in defs))
    todo = {}
    for rid, i in first.items():
        if rid in prior:
            continue
        nxt = next((s for s in starts if s > i), len(lines))
        end = i
        for j in range(i, nxt):
            if lines[j].strip():
                end = j
        todo[rid] = end
    out = list(lines)
    for rid, end in sorted(todo.items(), key=lambda kv: kv[1], reverse=True):
        verdict, why = C[rid]
        out.insert(end + 1, "  **CHECKABLE: %s** \u2014 %s" % (verdict, why))

    body = nl.join(out).encode("utf-8")
    added = len(out) - len(lines)
    if added != len(todo):
        sys.exit("REFUSE: inserted %d markers, expected %d" % (added, len(todo)))
    yes = sum(1 for v, _ in C.values() if v == "yes")
    print("newline        : %r" % nl)
    print("ids            : %d  (definition lines %d)" % (len(first), len(defs)))
    print("markers already: %d  (agreed on all %d)" % (len(prior), len(prior)))
    print("markers written: %d" % added)
    print("CHECKABLE      : yes=%d  no=%d  of %d" % (yes, len(C) - yes, len(C)))
    print("bytes          : %d -> %d" % (len(raw), len(body)))

    with open(SRC, "wb") as fh:
        fh.write(body)
    rows = ["id\tcheckable\treason"]
    rows += ["%s\t%s\t%s" % (rid, C[rid][0], C[rid][1]) for rid in sorted(C)]
    with open(TSV, "wb") as fh:
        fh.write((nl.join(rows) + nl).encode("utf-8"))
    print("WROTE          : %s and %s" % (SRC, TSV))


if __name__ == "__main__":
    main()
