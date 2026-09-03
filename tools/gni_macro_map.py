#!/usr/bin/env python3
"""GNI MACRO MAP -- the time-series gap measurement (S96, DECISION S93-2 row 4).

X = session number.  Y = White Paper layer.  Z = vision -> executable.

Reads ONLY committed bytes and names its source, file:line, for every point.
A point with no source is printed ABSENT and is never interpolated.

Sources (the LIVE file is the HIGHEST session number, Protocol PART A):
  docs/GNI_RULES_S{N}.md         -- Z: one **CHECKABLE: yes|no** marker per rule
  docs/GNI_ARCHITECTURE_S{N}.md  -- Y: the ROADMAP TO LAYER 2 table

The register is NOT uniformly formatted: rule entries appear in at least five
shapes, and some markers sit BELOW the section heading that follows their rule.
So a marker is bound to the nearest entry-start ABOVE it, never to a fixed
offset, and every marker that cannot be bound to a unique rule is reported in
an AMBIGUOUS bucket rather than silently attributed.

Exit codes match tools/gni_state.py and tools/gni_rule_checks.py:
  0  map generated
  1  a self-assertion about the map failed
  2  the INSTRUMENT refused -- never read as a pass
"""

import hashlib
import os
import re
import sys

DOCS = "docs"
OUT = "docs/GNI_MACRO_MAP_S%d.md"

ID = r"(?:R-S\d+-\d+|GNI-R-\d+|LR-\d+|NN-PHI-[A-Za-z0-9-]+)"
# an entry-start is an ID at the head of a line followed by a DEFINITION
# separator. A body line that merely opens with a cited id ("R-S91-4 cited
# ...") is not an entry and must not capture the marker below it.
OWN_PAT = re.compile(r"^(?:#{1,6}\s+)?(?:[-*]\s+)?\*{0,2}(" + ID +
                     r")(?:\*\*|\s*[:\u2014\u2013(]|\s+-\s|\s*$)")
MARK_PAT = re.compile(r"\*\*CHECKABLE: (yes|no)\*\*")
SESSION_PAT = re.compile(r"^R-S(\d+)-\d+$")
ROW_PAT = re.compile(r"^\|\s*S(\d+)\s*\|(.*)\|(.*)\|\s*$")
LAYER_PAT = re.compile(r"Layer\s+([0-3])\b")


def refuse(msg):
    sys.stderr.write("REFUSED: %s\n" % msg)
    sys.exit(2)


def live(prefix):
    if not os.path.isdir(DOCS):
        refuse("no %s/ directory -- run me from the repo root" % DOCS)
    pat = re.compile(r"^" + re.escape(prefix) + r"_S(\d+)\.md$")
    best, bestn = None, -1
    for name in sorted(os.listdir(DOCS)):
        m = pat.match(name)
        if m and int(m.group(1)) > bestn:
            best, bestn = name, int(m.group(1))
    if best is None:
        refuse("no %s_S*.md found in %s/" % (prefix, DOCS))
    # build with "/" so the ARTIFACT is byte-identical on Windows and POSIX.
    # os.path.join emitted "docs\\..." on Windows and "docs/..." here, which made
    # the same inputs produce two different files. Windows open() takes "/".
    return DOCS + "/" + best, bestn


def _session_arg():
    """M4 (item 5.27): the artifact is named for the SESSION that produced it,
    never for the register generation it read. "Highest number = live" is law
    (Protocol PART A); a file named after its INPUT sits outside that law and
    was invisible at S96 because register and session happened to coincide."""
    argv = sys.argv[1:]
    if len(argv) == 2 and argv[0] == "--session":
        try:
            return int(argv[1])
        except ValueError:
            refuse("--session takes an integer, got %r" % argv[1])
    refuse("usage: gni_macro_map.py --session <N>")


def norm_md5(raw):
    """EOL- and BOM-invariant md5. A raw hash disagrees between a Windows
    worktree (CRLF) and a CI checkout (LF) for byte-identical content. 5.21 is
    still unshipped, so no published checksum may depend on how git handed the
    file over. Hash what the content IS, not how it was delivered."""
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    return hashlib.md5(raw.replace(b"\r\n", b"\n")).hexdigest()


def read(path):
    """Binary read -> (raw, lines). Immune to LF / CRLF / mixed (S95 trap)."""
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError as e:
        refuse("cannot read %s: %s" % (path, e))
    try:
        return raw, raw.decode("utf-8").splitlines()
    except UnicodeDecodeError as e:
        refuse("%s is not utf-8: %s" % (path, e))


def parse_rules(path):
    raw, lines = read(path)
    bound, unbound = [], []
    for i, ln in enumerate(lines):
        m = MARK_PAT.search(ln)
        if not m:
            continue
        owner = None
        for j in range(i, -1, -1):
            o = OWN_PAT.search(lines[j])
            if o:
                owner = (o.group(1), j + 1)
                break
        if owner is None:
            unbound.append((m.group(1), i + 1))
        else:
            bound.append((owner[0], m.group(1), owner[1], i + 1))
    if not bound:
        refuse("%s: no CHECKABLE marker could be bound to a rule -- the "
               "register's shape changed" % path)
    return raw, bound, unbound


def parse_roadmap(path):
    raw, lines = read(path)
    start = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("## ROADMAP TO LAYER"):
            start = i
            break
    if start is None:
        refuse("%s: no '## ROADMAP TO LAYER' heading" % path)
    out = {}
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            break
        m = ROW_PAT.match(lines[j])
        if m:
            out[int(m.group(1))] = (m.group(3).strip(), j + 1)
    if not out:
        refuse("%s: ROADMAP table parsed to zero rows" % path)
    return raw, out


def main():
    session = _session_arg()
    rules_path, rules_n = live("GNI_RULES")
    arch_path, arch_n = live("GNI_ARCHITECTURE")
    rules_raw, bound, unbound = parse_rules(rules_path)
    arch_raw, roadmap = parse_roadmap(arch_path)

    total_markers = len(bound) + len(unbound)

    # a rule id claimed by more than one marker is AMBIGUOUS: the register's
    # format does not say which marker is whose. Never guess.
    claims = {}
    for rid, verdict, oline, mline in bound:
        claims.setdefault(rid, []).append((verdict, oline, mline))
    resolved = {k: v[0] for k, v in claims.items() if len(v) == 1}
    ambiguous = {k: v for k, v in claims.items() if len(v) > 1}
    amb_markers = sum(len(v) for v in ambiguous.values())

    # --- assertions computed BEFORE the write (R-S95-1) ---
    accounted = len(resolved) + amb_markers + len(unbound)
    problems = []
    if accounted != total_markers:
        problems.append("marker accounting lost rows: %d accounted vs %d found"
                        % (accounted, total_markers))

    by_session, unplaceable = {}, []
    for rid, (verdict, oline, mline) in sorted(resolved.items()):
        m = SESSION_PAT.match(rid)
        if m:
            d = by_session.setdefault(int(m.group(1)),
                                      {"yes": 0, "no": 0, "lines": []})
            d[verdict] += 1
            d["lines"].append(oline)
        else:
            unplaceable.append((rid, verdict, oline))

    ryes = sum(1 for v in resolved.values() if v[0] == "yes")
    rno = len(resolved) - ryes
    tyes = sum(1 for b in bound if b[1] == "yes") + \
        sum(1 for u in unbound if u[0] == "yes")
    tno = total_markers - tyes

    lo = min(by_session) if by_session else 0
    hi = max([max(by_session) if by_session else 0,
              max(roadmap) if roadmap else 0, rules_n])

    L = []
    a = L.append
    a("# GNI MACRO MAP -- S%d" % session)
    a("")
    a("GENERATED by `tools/gni_macro_map.py`. Do not hand-edit; the next run overwrites it.")
    a("No clock is written into this file, so an unchanged input reproduces it byte-identically.")
    a("")
    a("| axis | meaning | source |")
    a("|---|---|---|")
    a("| X | session number | rule ids of the form `R-S##-#` |")
    a("| Y | White Paper layer | `%s`, ROADMAP table |" % arch_path)
    a("| Z | vision -> executable | `**CHECKABLE:**` markers in `%s` |" % rules_path)
    a("")
    a("INPUT `%s` md5 `%s` (EOL-normalised)" % (rules_path, norm_md5(rules_raw)))
    a("INPUT `%s` md5 `%s` (EOL-normalised)" % (arch_path, norm_md5(arch_raw)))
    a("GENERATED from `%s` -- %d CHECKABLE markers, register generation %d."
      % (rules_path, total_markers, rules_n))
    a("")
    a("## TOTALS")
    a("")
    a("- CHECKABLE markers in the register: **%d** -- **%d** yes, **%d** no -- "
      "Z = **%.1f%%**" % (total_markers, tyes, tno, 100.0 * tyes / total_markers))
    a("- bound to exactly one rule id: **%d**" % len(resolved))
    a("- AMBIGUOUS (one id claimed by several markers, %d markers over %d ids): "
      "**%d**" % (amb_markers, len(ambiguous), amb_markers))
    a("- bound to no rule at all: **%d**" % len(unbound))
    a("- placeable on X: **%d** rules across **%d** sessions (S%d-S%d); "
      "NOT placeable: **%d** (`GNI-R-###`, `LR-###`, `NN-PHI-*` carry no session)"
      % (sum(d["yes"] + d["no"] for d in by_session.values()), len(by_session),
         lo, max(by_session) if by_session else 0, len(unplaceable)))
    a("- Y: **%d** of the **%d** sessions on this axis name a layer"
      % (sum(1 for s in roadmap if LAYER_PAT.search(roadmap[s][0])), hi - lo + 1))
    a("")
    a("## THE SERIES")
    a("")
    a("ABSENT means no source in the repo says anything. It is never interpolated,")
    a("and it is not a zero.")
    a("")
    a("| X | rules | Z yes | Z no | Z ratio | Y layer | source (file:line) |")
    a("|---|---|---|---|---|---|---|")
    rb = rules_path.rsplit("/", 1)[-1]
    ab = arch_path.rsplit("/", 1)[-1]
    for s in range(lo, hi + 1):
        ycell, ysrc = "ABSENT", ""
        if s in roadmap:
            lm = LAYER_PAT.search(roadmap[s][0])
            ycell = "Layer %s" % lm.group(1) if lm else "row, no layer named"
            ysrc = "%s:%d" % (ab, roadmap[s][1])
        d = by_session.get(s)
        if d:
            tot = d["yes"] + d["no"]
            src = "%s:%d-%d" % (rb, min(d["lines"]), max(d["lines"]))
            if ysrc:
                src += " + " + ysrc
            a("| S%d | %d | %d | %d | %.0f%% | %s | %s |"
              % (s, tot, d["yes"], d["no"], 100.0 * d["yes"] / tot, ycell, src))
        else:
            a("| S%d | ABSENT | ABSENT | ABSENT | ABSENT | %s | %s |"
              % (s, ycell, ysrc if ysrc else "none"))
    a("")
    a("## AMBIGUOUS -- the register cannot say which marker belongs to which rule (%d)"
      % amb_markers)
    a("")
    if ambiguous:
        a("| id claimed | markers | verdicts | marker lines |")
        a("|---|---|---|---|")
        for rid in sorted(ambiguous):
            v = ambiguous[rid]
            a("| `%s` | %d | %s | %s |"
              % (rid, len(v), ", ".join(x[0] for x in v),
                 ", ".join("%s:%d" % (rb, x[2]) for x in v)))
    else:
        a("None.")
    a("")
    a("## NOT PLACEABLE ON X (%d)" % len(unplaceable))
    a("")
    a("| id | Z | source |")
    a("|---|---|---|")
    for rid, verdict, oline in sorted(unplaceable):
        a("| `%s` | %s | %s:%d |" % (rid, verdict, rb, oline))
    a("")
    a("## WHAT THIS MAP CANNOT SAY")
    a("")
    a("- Z measures whether a rule COULD be checked by a script, not whether a check")
    a("  EXISTS. Five checks exist (`tools/gni_rule_checks.py`); the rest of the yes")
    a("  column is potential, not shipped.")
    a("- Y is nearly empty by MEASUREMENT, not by oversight: only the ROADMAP table")
    a("  binds a session to a layer, and only some of its rows name one. That emptiness")
    a("  IS the gap this map was asked to measure.")
    a("- A session with no rule minted is ABSENT on Z, not zero.")
    a("- The AMBIGUOUS bucket is a property of the REGISTER's formatting, not of the")
    a("  rules. It shrinks when the register is regularised, not when this tool is.")
    a("")

    body = ("\n".join(L) + "\n").encode("utf-8")
    if b"\\" in body:
        problems.append("a backslash reached the artifact -- a platform path "
                        "separator leaked and the output is not portable")

    if problems:
        for p in problems:
            sys.stderr.write("ASSERTION FAILED: %s\n" % p)
        return 1

    out = OUT % session
    with open(out, "wb") as f:
        f.write(body)
    sys.stdout.write("wrote %s -- %d bytes, %d markers, %d bound, %d ambiguous, "
                     "%d sessions, Z=%.1f%%\n"
                     % (out, len(body), total_markers, len(resolved),
                        amb_markers, len(by_session), 100.0 * tyes / total_markers))
    return 0


if __name__ == "__main__":
    sys.exit(main())
