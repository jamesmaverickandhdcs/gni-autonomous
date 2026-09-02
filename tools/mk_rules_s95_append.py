#!/usr/bin/env python3
"""Append the five rules earned at S95 to docs/GNI_RULES_S95.md.

Each carries a CHECKABLE marker in S94's format. Verification is computed
BEFORE the write (R-S95-1, which this script is the first instance of).
"""
import os
import sys

P = "docs/GNI_RULES_S95.md"
UNIQUE = "# S95 APPENDIX"

BLOCK = """
# S95 APPENDIX (2026-09-03) — RULES EARNED

Five rules, all earned from instrument errors made inside this session. Six of
the seven were caught before the real tree; two reached the operator's terminal.

**R-S95-1 — VERIFICATION IS COMPUTED BEFORE THE WRITE, NEVER AFTER IT.** A patch
  script whose report runs after the mutation is not a report. S95's YAML patcher
  crashed on a `%`-precedence bug in its own `print` — AFTER the file was already
  written. The mutation succeeded and the verification died; had the mutation been
  wrong, the same crash would have hidden it. Compute the expected delta, compare
  it, refuse on mismatch, and only then open the file for writing. Kin to R-S55-3,
  which required confirming a patch RAN before trusting a verify; this requires
  confirming it will be CORRECT before it runs.
  **CHECKABLE: yes** — AST-lint patch scripts: no write call may precede the last assert

**R-S95-2 — ACCEPTING A CORRECTION REQUIRES READING A BYTE, NOT THE CORRECTOR'S
  CONFIDENCE.** S95 accepted a review's correction about `sort -V`, wrote a
  self-criticism, and was then told the correction had itself been a misreading.
  Four times in one session a review reasoned from an assumed tree rather than the
  live one — and each time it also carried something true, so neither deference nor
  dismissal was safe. R-S94-1 says a review is a lead; this says its CORRECTION is
  a lead too. Over-confession is as false as over-confidence and is harder to catch
  because it wears good manners.
  **CHECKABLE: no** — whether a byte was read before agreeing leaves no trace in any artifact

**R-S95-3 — A DOCUMENT THAT RECORDS A DEFECT IS INDISTINGUISHABLE, TO A DETECTOR,
  FROM ONE THAT COMMITS IT.** Item 9.16 records the wrong workflow count as a
  finding; a grep hunting wrong counts cannot tell it from a document making the
  claim. CONTRACT names `GNI-R-064` while describing the citation defect; a grep
  hunting dangling citations flags it. Every check that runs over DOCUMENTS needs a
  citation escape, or its remedy becomes "delete the record of the defect" — and
  GNI is built entirely on records of past defects. The escape must not be an
  inline convention: backticks were proposed and disproven within the hour, because
  `GNI-R-114` is backticked AND load-bearing. The escape is a MANIFEST with a
  status per id, in the register.
  **CHECKABLE: yes** — assert every document-scanning check declares an escape source

**R-S95-4 — A CONSTANT COUNT IS NOT A CONSTANT STATE.** S90 measured eight rule ids
  cited but unregistered. S95 measured eight. Four of S90's eight were fixed and
  four new ones accrued: the number held while HALF the membership rotated. A
  metric compared across sessions must be compared as a SET, not as an integer, or
  a fully-rotated population reads as stability. Kin to R-S54-2: the live byte beats
  the banked number, and here even a live number that MATCHES the banked one is
  concealing a change.
  **CHECKABLE: yes** — store the members, not the count, and diff the sets between generations

**R-S95-5 — THE TOOL THAT WRITES A FILE BECOMES THE INPUT TO EVERY TOOL THAT READS
  IT.** S95's marker script wrote `\\r\\r\\n` on every line of the register. All five
  new checks stayed GREEN, `git status` said nothing, markdown rendered identically
  — and `tools/gni_state.py` died with an `IndexError` that took three probes to
  trace back. One reader's green proves nothing about another reader's input. After
  any write to a shared artifact, run every tool that consumes it, not only the one
  that motivated the write.
  **CHECKABLE: yes** — CI runs every tool in tools/ against the tree after any docs/ change
"""

if not os.path.isfile(P):
    sys.exit("REFUSE: %s not found" % P)
with open(P, "rb") as fh:
    raw = fh.read()
text = raw.decode("utf-8-sig")
if UNIQUE in text:
    sys.exit("REFUSE: S95 appendix already present")
nl = "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") - raw.count(b"\r\n") else "\n"

block = nl.join(BLOCK.splitlines()) + nl
out = (nl.join(text.splitlines()) + nl + block).encode("utf-8")

# --- verification BEFORE the write (R-S95-1) ---
new_ids = ["R-S95-%d" % i for i in range(1, 6)]
for rid in new_ids:
    if text.count(rid) != 0:
        sys.exit("REFUSE: %s already appears in the register" % rid)
    if block.count("**" + rid + " \u2014") != 1:
        sys.exit("REFUSE: %s is not defined exactly once in the block" % rid)
if block.count("**CHECKABLE:") != len(new_ids):
    sys.exit("REFUSE: %d markers for %d rules" % (block.count("**CHECKABLE:"), len(new_ids)))
if b"\r\r" in out:
    sys.exit("REFUSE: \\r\\r produced - the R-S95-5 bug, again")

print("newline   : %r" % nl)
print("rules     : %d  (%s)" % (len(new_ids), ", ".join(new_ids)))
print("markers   : %d" % block.count("**CHECKABLE:"))
print("bytes     : %d -> %d (+%d)" % (len(raw), len(out), len(out) - len(raw)))

with open(P, "wb") as fh:
    fh.write(out)
print("WRITTEN")
