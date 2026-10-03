#!/usr/bin/env python3
"""tools/gni_lambda.py - S107, roadmap 3 row R3-4's OWED baseline (DECISION S107-7).

lambda = ARRIVALS PER CLOSE: the queue items a close adds. The specification
cited "~6.5 per session" at S102-S104 with no command; this file is the command.

  python tools/gni_lambda.py                     every generation, then lambda
  python tools/gni_lambda.py --window S102:S106  lambda over that window only

THE MEASUREMENT, from bytes only: for every docs/GNI_TARGET_AND_ORDER_S<N>.md,
the item ids are the order's OWN published scan - the bolded `**N.N` ids between
`## THE ORDER` and `## ARCHIVED` (R-S98-6's first counting command). Arrivals at
generation N are the ids present at N and absent from the generation before it;
departures are the reverse. A missing generation (S97) makes the next one's
arrivals span two closes, and the table says so.

LIMIT, written down: the published scan counts every bolded id in the queue,
and the order states "a closed id cited in the queue counts as a queue item".
So a renumbering or a citation can arrive without new work. The prose rho lines
count by hand and can differ; this command is the one that can be re-run.

stdlib only (item 6.9). No git: every generation since S84 is in the tree.
"""
import glob
import os
import re
import sys

GEN_RE = re.compile(r"GNI_TARGET_AND_ORDER_S(\d+)\.md$")
ID_RE = re.compile(r"\*\*(\d+\.\d+)")
WINDOW_RE = re.compile(r"^S(\d+):S(\d+)$")


def queue_ids(path):
    with open(path, "rb") as fh:
        lines = fh.read().decode("utf-8").replace("\r\n", "\n").split("\n")
    start = next((i for i, ln in enumerate(lines) if ln.startswith("## THE ORDER")), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ARCHIVED")),
               len(lines) - 1)
    return set(ID_RE.findall("\n".join(lines[start:end + 1])))


def table(root):
    gens = sorted((int(m.group(1)), p) for p in glob.glob(os.path.join(root, "docs", "*.md"))
                  for m in [GEN_RE.search(p)] if m)
    rows, prev, prev_n = [], None, None
    for n, path in gens:
        ids = queue_ids(path)
        if ids is None:
            continue
        if prev is not None:
            rows.append((n, len(ids), len(ids - prev), len(prev - ids), n - prev_n))
        prev, prev_n = ids, n
    return rows


def main(argv):
    root = "."
    lo, hi = None, None
    if len(argv) == 3 and argv[1] == "--window":
        m = WINDOW_RE.match(argv[2])
        if not m:
            print("usage: gni_lambda.py [--window S<a>:S<b>]")
            return 2
        lo, hi = int(m.group(1)), int(m.group(2))
    elif len(argv) != 1:
        print("usage: gni_lambda.py [--window S<a>:S<b>]")
        return 2
    rows = table(root)
    if not rows:
        print("INSTRUMENT ERROR: no order generations with a ## THE ORDER section")
        return 2
    print("| gen | items | arrivals | departures | closes spanned |")
    print("|---|---|---|---|---|")
    for n, items, arr, dep, span in rows:
        print("| S%d | %d | %d | %d | %d |" % (n, items, arr, dep, span))
    sel = [r for r in rows if (lo is None or r[0] >= lo) and (hi is None or r[0] <= hi)]
    if not sel:
        print("INSTRUMENT ERROR: no generation in the window")
        return 2
    closes = sum(r[4] for r in sel)
    arrivals = sum(r[2] for r in sel)
    print("lambda S%d:S%d = %d arrivals / %d closes = %.2f per close"
          % (sel[0][0], sel[-1][0], arrivals, closes, arrivals / closes))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
