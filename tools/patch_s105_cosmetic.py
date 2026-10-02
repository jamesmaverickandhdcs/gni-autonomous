#!/usr/bin/env python3
"""S105 cosmetic fix - two grammar defects left where two pseudonym rules stacked on one phrase.
Historical documents only; no check reads them. Binary mode, ASCII anchors (GNI-L-015), all or nothing.
usage: python tools/patch_s105_cosmetic.py [--apply]     (default: dry run)"""
import subprocess, sys

FIXES = [  # (anchor, replacement, files that must carry it exactly once each)
    (b"Partner B's a Partner B agent", b"a Partner B agent",
     ["docs/GNI_TARGET_AND_ORDER_S%d.md" % n for n in range(88, 96)]),
    (b"GNI_to_Partner B_", b"GNI_to_Partner_B_",
     ["docs/S47_Next_Session_Brief.md", "docs/S48_Next_Session_Brief.md"]),
]

def main():
    apply = "--apply" in sys.argv
    if subprocess.run(["git", "status", "--porcelain"], capture_output=True).stdout.strip():
        print("REFUSED: tree is not clean"); return 1
    found = subprocess.run(["git", "grep", "-l", "-F", "-e", FIXES[0][0].decode(), "-e", FIXES[1][0].decode(), "--", "docs/"],   # docs only: this script carries the anchors too
                           capture_output=True).stdout.decode().split()
    expected = sorted(f for _, _, fs in FIXES for f in fs)
    if sorted(found) != expected:
        print("REFUSED: anchors found in %s, expected exactly %s" % (sorted(found), expected)); return 1
    out = {}
    for old, new, files in FIXES:
        for f in files:
            b = out.get(f) or open(f, "rb").read()
            if b.count(old) != 1:
                print("REFUSED: %s carries the anchor %d times, expected 1" % (f, b.count(old))); return 1
            out[f] = b.replace(old, new)
    for f, b in sorted(out.items()):
        print("%-40s %s" % (f, "WRITTEN" if apply else "would change 1 line"))
        if apply:
            open(f, "wb").write(b)
    print("APPLIED %d files" % len(out) if apply else "DRY RUN - %d files, nothing written" % len(out))
    return 0

if __name__ == "__main__":
    sys.exit(main())
