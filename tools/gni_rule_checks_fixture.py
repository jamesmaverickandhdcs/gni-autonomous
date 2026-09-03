import os, shutil, sys, tempfile

def w(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(s)

RULES = """# GNI RULES
# PART 0 - RECOVERED IDS

### UNREGISTERED ID MANIFEST
| id | status | reason |
|---|---|---|
| `GNI-R-076` | UNMIGRATED-DOCX | lives in the un-migrated DOCX register |
| `GNI-R-233` | DEFINED-IN-CONTRACT | CONTRACT defines it inline; routing debt |
| `GNI-R-180` | DISCUSSION-ONLY | named only while describing the drift defect |

# PART 1 - ACTIVE RULES BY TRIGGER
- R-S90-2 appears here as an INDEX line and must not count as a definition
- LR-092 appears here too

# PART 2 - CLUSTERS
- R-S92-2 index mention

# PART 3 - HISTORICAL REGISTER
- R-S90-2: an ID cited by a live doc is law only if the register contains it
**CHECKABLE: yes**
- R-S92-2: select on a relation, never a position
**CHECKABLE: yes**
- LR-092: py_compile every modified file before commit
**CHECKABLE: no**
**R-S81-1** - a zero result indicts the instrument first
"""

ARCH_OK = """## §7 DEPLOYMENT VIEW
### 7.1 Workflow inventory
**2 workflows: 1 scheduled · 1 on push · 0 dispatch-only.**
## §8 CROSSCUTTING
"""

def _map_text(reg_path, n_delta=0):
    """Built from the register AS WRITTEN, so the fixture is self-consistent on
    any platform: open(mode="w") emits CRLF on Windows and LF elsewhere, and
    the stamped md5 must survive that. Uses the generator's own functions."""
    import gni_macro_map as gm
    raw, bound, unbound = gm.parse_rules(reg_path)
    n = len(bound) + len(unbound) + n_delta
    return ("# GNI MACRO MAP -- S94\n\n"
            "INPUT `%s` md5 `%s` (EOL-normalised)\n"
            "GENERATED from `%s` -- %d CHECKABLE markers, register generation 94.\n"
            % (reg_path, gm.norm_md5(raw), reg_path, n))


def ap(p, s):
    with open(p, "a", encoding="utf-8") as fh:
        fh.write(s)


def base(root, arch=ARCH_OK, rules=RULES, contract=None,
         map_n_delta=0, map_present=True):
    if os.path.isdir(root):
        shutil.rmtree(root)
    w(root + "/docs/GNI_RULES_S94.md", rules)
    w(root + "/docs/GNI_RULES_S93.md", "superseded, must be ignored: R-S99-9\n")
    w(root + "/docs/GNI_ARCHITECTURE_S94.md", arch)
    w(root + "/docs/CONTRACT_S94.md",
      contract if contract is not None else "law: R-S90-2 and `GNI-R-076` apply\n")
    w(root + "/docs/GNI_Session_Transfer_Protocol_S94.md", "see R-S92-2\n")
    w(root + "/docs/GNI_TARGET_AND_ORDER_S94.md", "queue: LR-092\n")
    w(root + "/docs/HANDOFF_S94.md", "state: R-S81-1\n")
    w(root + "/.github/workflows/a.yml", "on:\n  schedule:\n    - cron: '0 2 * * *'\njobs:\n  x:\n")
    w(root + "/.github/workflows/b.yml", "on:\n  push:\njobs:\n  y:\n")
    w(root + "/ai_engine/ok.py", "rows = q.order('created_at', desc=True).execute().data\n")
    w(root + "/src/app/api/r/route.ts", "const s = createNoStoreClient()\n")
    if map_present:
        w(root + "/docs/GNI_MACRO_MAP_S94.md",
          _map_text(root + "/docs/GNI_RULES_S94.md", map_n_delta))
    return root

CASES = {}
CASES["0-clean"] = lambda r: base(r)
CASES["1-dangling-law"] = lambda r: base(
    r, contract="law: R-S90-2 and `GNI-R-114` contradicts the rationale\n")
CASES["2-wrong-home-def"] = lambda r: base(
    r, contract="- GNI-R-999: FAMILIAR = THE TELL. defined right here in law.\n")
CASES["3-discussion-only"] = lambda r: base(
    r, contract="law: R-S90-2. The S90 defect named GNI-R-064 as an example.\n")
CASES["4-backticked-is-still-checked"] = lambda r: base(
    r, contract="law: R-S90-2 and `GNI-R-777` is cited here\n")
CASES["5-stale-generator"] = lambda r: base(r, arch=ARCH_OK.replace(
    "**2 workflows: 1 scheduled · 1 on push · 0 dispatch-only.**",
    "**3 workflows: 2 scheduled · 1 on push · 0 dispatch-only.**"))
CASES["6-family-stem-missing"] = lambda r: (
    base(r), os.remove(r + "/docs/GNI_ARCHITECTURE_S94.md"), r)[-1]
CASES["7-manifest-marker-renamed"] = lambda r: base(
    r, rules=RULES.replace("UNREGISTERED ID MANIFEST", "OLD SECTION NAME"))
CASES["10-undeclared-duplicate"] = lambda r: base(r, rules=RULES.replace(
    "**R-S81-1** - a zero result indicts the instrument first",
    "**R-S81-1** - a zero result indicts the instrument first\n- R-S90-2: quietly redefined here"))
CASES["11-declared-amendment"] = lambda r: base(r, rules=RULES.replace(
    "**R-S81-1** - a zero result indicts the instrument first",
    "**R-S81-1** - a zero result indicts the instrument first\n**R-S90-2** - AMENDMENT (S95): widened"))
CASES["12-map-stale-count"] = lambda r: base(r, map_n_delta=1)
CASES["13-map-stale-md5"] = lambda r: (
    base(r), ap(r + "/docs/GNI_RULES_S94.md",
                "\nprose line carrying no id and no marker\n"), r)[-1]
CASES["14-map-missing"] = lambda r: base(r, map_present=False)
CASES["9-direct-createClient"] = lambda r: (
    base(r), w(r + "/src/app/api/z/route.ts", "const s = createClient(url, key)\n"), r)[-1]

# Expected verdict per family. The fixture is not scaffolding: it is the
# discriminating evidence for tools/gni_rule_checks.py, and it asserts its own
# expectations (R-S93-1). A fixture nobody runs is a dead harness (item 5.14).
EXPECT = {
    "0-clean": 0, "1-dangling-law": 1, "2-wrong-home-def": 1,
    "3-discussion-only": 1, "4-backticked-is-still-checked": 1,
    "5-stale-generator": 1, "6-family-stem-missing": 2,
    "7-manifest-marker-renamed": 2, "9-direct-createClient": 1,
    "10-undeclared-duplicate": 1, "11-declared-amendment": 0,
    "12-map-stale-count": 1, "13-map-stale-md5": 1, "14-map-missing": 2,
}

if __name__ == "__main__":
    import subprocess
    here = os.path.dirname(os.path.abspath(__file__))
    tool = os.path.join(here, "gni_rule_checks.py")
    if not os.path.isfile(tool):
        sys.exit("INSTRUMENT ERROR: %s not found" % tool)
    if set(EXPECT) != set(CASES):
        sys.exit("INSTRUMENT ERROR: EXPECT and CASES disagree on family names")
    tmp = tempfile.mkdtemp(prefix="gni_fixture_")
    bad = []
    for name, fn in sorted(CASES.items()):
        root = fn(os.path.join(tmp, name))
        rc = subprocess.run([sys.executable, tool, root],
                            capture_output=True, text=True).returncode
        want = EXPECT[name]
        mark = "ok" if rc == want else "MISMATCH"
        print("%-32s want=%d got=%d  %s" % (name, want, rc, mark))
        if rc != want:
            bad.append(name)
    shutil.rmtree(tmp, ignore_errors=True)
    print("%d families, %d mismatches" % (len(CASES), len(bad)))
    sys.exit(1 if bad else 0)
