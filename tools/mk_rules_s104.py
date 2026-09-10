#!/usr/bin/env python3
"""tools/mk_rules_s104.py - PART C step 9: append only what S104 EARNED.

Reads the LIVE register by RELATION (R-S92-2), never by name, and writes it
forward as `docs/GNI_RULES_S104.md`. Four rules, each with an ID, no number
gaps, each one thing this session paid for rather than a restatement.

BEFORE ANY OF IT: the register is CRLF and has been since S99 deliberately
declined to convert 1556 line endings inside a docs commit (item 5.21). The
appended block is written CRLF to match, and the script REFUSES if the file it
read is not CRLF - a mixed-ending register would move its own md5 for a reason
that is not its content, which is the NINTH CARRY in the handoff.

It also refuses if any of the four ids is already defined, which is the
before-minting search PART C step 9 asks for, done by the program rather than
by the reader.

    python tools/mk_rules_s104.py
"""
import os
import re
import sys

RULES_RE = re.compile(r"^GNI_RULES_S(\d+)\.md$")
OUT = "docs/GNI_RULES_S104.md"
NEW_IDS = ["R-S104-1", "R-S104-2", "R-S104-3", "R-S104-4"]

BLOCK = """
- R-S104-1 - A GENERATED SECTION'S DECLARED FINGERPRINT IS RECOMPUTED FROM THE LIVE TREE BY THE
  GENERATOR'S OWN CODE, AND THE NUMBER OF SECTIONS IS NEVER WRITTEN DOWN. Every generated artefact
  here publishes the fingerprint of what it read - a source manifest md5, a snapshot md5, a
  workflow manifest md5 - and until S104 nothing read any of them except the macro map's. Measured
  across twenty-four commits: section five's declared value disagreed with its own tree at ELEVEN
  of them, and the nine that agreed did so because no tracked module moved in those sessions, not
  because anything checked. The recomputation imports the generator's own function rather than
  reimplementing it (R-S96-3), and the dispatch is keyed on the GENERATOR that wrote the stamp, so
  a stamp naming a generator with no rule is an INSTRUMENT ERROR and never a silent skip - a fourth
  generated section must announce itself. Writing the count of sections anywhere would be R-S103-1
  in a different coat: it makes the instrument agree with its author's belief about how many things
  exist rather than with what the document declares.
  **CHECKABLE: yes** - assert every generated stamp in the live architecture resolves to a
  fingerprint rule, and that no such rule is selected by count or by position.

- R-S104-2 - A GUARD PROVES NOTHING UNLESS IT TESTS THE FAILURE MODE IT IS GUARDING AGAINST. S104
  built two certifications for one claim and both passed on nothing. The first compared two renders
  of a generator that had exited 2 on a missing required argument: both files were empty, and two
  empty files compare identical. The second added a non-empty guard; the generator then died
  mid-write on a console encoding error, left the same 68 bytes in each file, and the guard passed
  again. The claim under test was "these bytes are identical". The guards asked "is this file
  non-empty". Neither asked the question that could have come back wrong. A cert reads the EXIT
  CODE of every program it runs, states the minimum output size that proves the run reached the
  region under test, and carries a NEGATIVE control that MUST fail. This is the fixture's own
  disease one level up - a green result on ground the instrument never walked - and it appeared
  twice in one session in the tooling built to certify the check that fixes it.
  **CHECKABLE: yes** - assert every published cert command captures and prints the exit code of
  each program it runs.

- R-S104-3 - A PROGRAM THAT IDENTIFIES ITSELF FROM `__file__` CANNOT BE CERTIFIED AGAINST A RENAMED
  COPY. `gni_state.py` derives `SELF` from its own filename so that it never counts its own source
  as a consumer of a secret. A cert that recovered the pre-patch version as `gni_state_PRE.py`
  therefore rendered a section 23 bytes LONGER - the real `gni_state.py` had become a consumer in
  the copy's eyes - and the difference had nothing to do with the change under test. The shape that
  works is two worktrees of one commit, each holding the file under its real name, with only the
  content differing. It generalises past this file: any comparison of two versions of a program
  must hold the program's IDENTITY constant, and a filename is part of identity the moment the
  program reads it.
  **CHECKABLE: no** - it constrains how a cert is built, not what any file contains.

- R-S104-4 - A TRAP NAMES AN EXAMPLE, NOT ITS EXTENT: READ THE FAMILY. The S103 handoff carried
  "`gni_runtime.py --stdout` needs `PYTHONIOENCODING=utf-8` on Windows". `gni_state.py --stdout`
  has exactly the same defect, is named by an order item that had already measured it, and cost
  S104 a false certification anyway - because the trap named one tool and was read as being about
  that tool. A carried warning is written from the instance that produced it; its subject is the
  CLASS. Before acting on a trap, ask which other members of its family share the mechanism, and
  treat the named one as the first instance rather than the only one. Kin of R-S103-1: both are
  about reading what a document SAYS rather than what its author happened to be looking at when
  they wrote it.
  **CHECKABLE: no** - it constrains reading, not bytes.
"""


def fail(msg):
    print("REFUSED: %s" % msg)
    print("Nothing written.")
    sys.exit(2)


def main():
    docs = "docs"
    gens = [(int(m.group(1)), n) for n in os.listdir(docs)
            for m in [RULES_RE.match(n)] if m]
    if not gens:
        fail("no register under " + docs)
    for g, n in sorted(gens)[-3:]:
        print("  generation S%d: %s" % (g, n))
    live = os.path.join(docs, max(gens)[-1])
    print("LIVE (by RELATION): %s" % live)
    if os.path.abspath(live) == os.path.abspath(OUT):
        fail("%s is already the live register; this close has already run" % OUT)
    if os.path.exists(OUT):
        fail("%s already exists" % OUT)

    raw = open(live, "rb").read()
    lf = raw.count(b"\n")
    crlf = raw.count(b"\r\n")
    print("EOL: %d lines, %d CRLF" % (lf, crlf))
    if crlf != lf:
        fail("the register is not uniformly CRLF (%d of %d); appending LF would "
             "move its md5 for a reason that is not its content" % (crlf, lf))

    text = raw.decode("utf-8")
    for rid in NEW_IDS:
        if re.search(r"^\s*-?\s*\*{0,2}" + re.escape(rid) + r"\*{0,2}\s*[-\u2014:(]",
                     text, re.M):
            fail("%s is already defined; amend it instead of re-minting "
                 "(PART C step 9)" % rid)
    print("SEARCH: none of %s is already defined" % ", ".join(NEW_IDS))

    block = BLOCK.replace("\n", "\r\n").encode("utf-8")
    if not raw.endswith(b"\r\n"):
        raw += b"\r\n"
    out = raw + block
    open(OUT, "wb").write(out)

    check = out.decode("utf-8")
    missing = [r for r in NEW_IDS if ("- " + r + " -") not in check]
    if missing:
        fail("wrote the file but %s is not in it" % missing)
    print("WROTE %s  %d bytes  (+%d appended)" % (OUT, len(out), len(block)))
    print("  all four ids present in the written bytes")
    print("\nNEXT, in this order - the map reads the register (PART C step 9a):")
    print("  git add tools/ docs/GNI_RULES_S104.md")
    print("  python tools/gni_macro_map.py --session 104")
    print("  python tools/gni_rule_checks.py .        # expect 0 failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
