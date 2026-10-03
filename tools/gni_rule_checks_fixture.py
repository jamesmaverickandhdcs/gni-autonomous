import os, re, shutil, sys, tempfile

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
- GNI-L-003 appears here too

# PART 2 - CLUSTERS
- R-S92-2 index mention

# PART 3 - HISTORICAL REGISTER
- R-S90-2: an ID cited by a live doc is law only if the register contains it
**CHECKABLE: yes**
- R-S92-2: select on a relation, never a position
**CHECKABLE: yes**
- GNI-L-003: py_compile every modified file before commit
**CHECKABLE: no**
- R-S98-3: a published hash is EOL-normalised or it is platform noise
**R-S81-1** - a zero result indicts the instrument first
"""

ARCH_OK = """## §7 DEPLOYMENT VIEW
### 7.1 Workflow inventory
**2 workflows: 1 scheduled · 1 on push · 0 dispatch-only.**
## §8 CROSSCUTTING
"""

SLO_FAST = ("2026-01-01", "2026-01-02")
SLO_SLOW = ("2026-01-03", "2026-01-04")
WATCHER = ("# synthetic watcher -- C7 reads this by AST, never by regex\n"
           "PROTECTION_WINDOWS = [\n"
           "    (23, 0, 1, 30),\n"
           "]\n")
# The pre-S102 shape: the watcher consulted its own windows and a run
# inside one returned before it opened a connection. Restored here as a
# perturbation, not invented -- this is the body removed at S102.
WATCHER_STANDDOWN = WATCHER + ("\n\ndef run_monitoring_pipeline(now):\n"
                               "    if is_protection_window(now):\n"
                               "        return True\n"
                               "    return True\n")
SLO_PW = ("2026-02-01", "2026-02-05")


def _snap_text():
    """A run history with TWO regimes: two days at one run an hour, then two
    days at one run every three hours. Written out rather than harvested, so
    the fixture needs no network and no clock."""
    import json
    runs = []
    for d in SLO_FAST:
        for h in range(2, 23):
            runs.append("%sT%02d:00:00Z" % (d, h))
    for d in SLO_SLOW:
        for h in range(2, 21, 3):
            runs.append("%sT%02d:00:00Z" % (d, h))
    return json.dumps({
        "harvest_limit": 300, "harvested_at": "2026-01-05T00:00:00Z", "schema": 1,
        "workflows": {"a.yml": {"crons": ["0 * * * *"], "fetched": len(runs),
                                "truncated": False,
                                "runs": [{"conclusion": "success", "createdAt": t}
                                         for t in runs]}}})


def _snap_pw_text():
    """A history that ENTERS the protection window. _snap_text never does
    -- its runs start at 02:00 -- so until S102 no family exercised the
    window argument of effective_gaps at all. A run every three hours from
    00:00 puts exactly one run per day inside 23:00-01:30: 39 gaps and a
    3 h bound when every run checks, 34 gaps and 6 h when they do not."""
    import json
    days = ["2026-02-0%d" % i for i in range(1, 6)]
    runs = ["%sT%02d:00:00Z" % (d, h) for d in days for h in range(0, 24, 3)]
    return json.dumps({
        "harvest_limit": 300, "harvested_at": "2026-02-06T00:00:00Z", "schema": 1,
        "workflows": {"a.yml": {"crons": ["0 */3 * * *"], "fetched": len(runs),
                                "truncated": False,
                                "runs": [{"conclusion": "success", "createdAt": t}
                                         for t in runs]}}})


def _slo_block(bound, frm, to):
    """The SLO-CFG lines C7 parses. The bound is STATED here and DERIVED by the
    check: over the fast window the history yields 1 h, over both regimes 3 h.
    A family that states anything else must go red."""
    return ("\n### 10.3 SLO\n\n"
            "- SLO-CFG BOUND_HOURS: `%s`\n"
            "- SLO-CFG EXCEEDANCE_MAX: `0.10`\n"
            "- SLO-CFG WINDOW_FROM: `%s`\n"
            "- SLO-CFG WINDOW_TO: `%s`\n"
            "- SLO-CFG SPLIT_RATIO: `2.0`\n"
            "- SLO-CFG WORKFLOW: `a.yml`\n"
            "- SLO-CFG SNAPSHOT: `docs/gni_runtime_snapshot_S94.json`\n"
            % (bound, frm, to))


def _map_text(reg_path, arch_path, n_delta=0):
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
    return ("# GNI MACRO MAP -- S94\n\n"
            "INPUT `%s` md5 `%s` (EOL-normalised)\n"
            "INPUT `%s` md5 `%s` (EOL-normalised)\n"
            "GENERATED from `%s` -- %d CHECKABLE markers, register generation 94.\n"
            % (reg_path, gm.norm_md5(raw),
               arch_path, gm.norm_md5(arch_raw),
               reg_path, n))


def _git_index(root):
    """C8 reads section five's fingerprint through gni_blocks.collect, which
    lists the git INDEX. A tempfile tree is not a repository, so without this
    every family returns 2 on an instrument error and the fixture measures
    nothing. One commit, so HEAD resolves too; identity is passed with -c
    rather than written, so no global git config is touched."""
    import subprocess
    def run(*args):
        subprocess.run(("git",) + args, cwd=root, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    run("init", "-q")
    run("add", "-A")
    run("-c", "user.email=fixture@local", "-c", "user.name=fixture",
        "commit", "-q", "-m", "fixture tree")


def _gen_stamps(root):
    """The three GENERATED-section stamps C8 reads. Every fingerprint is
    computed from the tree AS BUILT, using the generator's own hasher -- the
    discipline _map_text already follows, and the reason the fixture survives
    CRLF on Windows. A hard-coded md5 here would make the families agree with
    the fixture's memory instead of with the tree.

    The HEAD and count fields are deliberately junk: C8 reads neither, and
    writing plausible values would invite a later reader to believe they are
    checked. Section five's HEAD field CANNOT be checked from a working tree
    -- committing the document that carries it advances HEAD -- and that is
    DECISION S104-1, recorded here where it would otherwise be assumed."""
    from pathlib import Path
    import gni_blocks as gb
    import gni_runtime as gr
    import gni_state as gs
    snap = Path(root) / "docs" / "gni_runtime_snapshot_S94.json"
    wfs = sorted((Path(root) / ".github" / "workflows").glob("*.yml"))
    return ("\n## \u00a75 BUILDING BLOCK VIEW\n\n"
            "**GENERATED by `tools/gni_blocks.py` from the AST of ? tracked `*.py` "
            "at HEAD `unchecked` \u2014 source manifest md5 `%s` "
            "(EOL-normalised, R-S98-3).**\n\n"
            "## \u00a76 RUNTIME VIEW\n\n"
            "**GENERATED by `tools/gni_runtime.py` from "
            "`docs/gni_runtime_snapshot_S94.json` \u2014 snapshot md5 `%s` "
            "(EOL-normalised, R-S98-3).**\n\n"
            "**GENERATED by `tools/gni_state.py` from HEAD `unchecked` \u2014 "
            "? workflow files, manifest md5 `%s` (EOL-normalised, R-S98-3).**\n"
            % (gb.collect(Path(root))["manifest_md5"],
               gr.norm_md5(snap.read_bytes()),
               gs.workflow_manifest(wfs)))


ESC_LIB_OK = ("export function formatEscalation(s, raw) {\n"
              "  return raw != null ? s + '/10 raw ' + raw : s + '/10'\n}\n")
ESC_PAGE_OK = ("import { formatEscalation } from '@/lib/escalation'\n"
               "const t = formatEscalation(r.escalation_score, r.escalation_score_raw)\n")
ORIGIN_OK = "# origin\nS94 recorded the fixture tree.\n"


def _glossary_text(root, drop_check=None, session_rows=""):
    """S106. The glossary C9 and C10 read, built from the tree AS WRITTEN by
    the detector's OWN collector -- the discipline _map_text follows. Every
    candidate the tree yields is declared NOT an abbreviation, so the clean
    family passes by construction and a family goes red only on what it adds
    afterwards. A hand-typed list here would agree with the fixture's memory
    instead of with the tree."""
    import gni_rule_checks as rc
    english = rc.english_words(root)
    docs = rc.live_docs(root)
    docs["GNI_ORIGIN"] = rc.origin_path(root)
    cands = set()
    for path in docs.values():
        cands |= rc.candidate_tokens(rc.read(path), english)
    ns = (r"S\d+", r"C\d+")
    words = sorted(t for t in cands if not any(re.fullmatch(p, t) for p in ns))
    checks = [n.split()[0] for n, _ in rc.CHECKS if n.split()[0] != drop_check]
    return ("# GNI GLOSSARY -- S94\n\n## DEFINED\n| term | definition |\n|---|---|\n"
            "| GNI | the fixture's system |\n\n"
            "## NOT ABBREVIATIONS\n| word | why |\n|---|---|\n"
            + "".join("| %s | fixture |\n" % t for t in words) +
            "\n## NAMESPACES\n| pattern | meaning |\n|---|---|\n"
            + "".join("| `%s` | fixture |\n" % p for p in ns) +
            "\n## SESSION INDEX\n| session | record | status |\n|---|---|---|\n"
            + session_rows +
            "\n## CHECKS\n| check | meaning |\n|---|---|\n"
            + "".join("| %s | fixture |\n" % c for c in checks))


# S107, roadmap 3 row R3-2. A one-line White Paper and one page carrying one
# claim; the verdicts and the claims document are built from the tree AS
# WRITTEN by the tool's own extractor and renderer (the _map_text discipline).
WP_OK = "# white paper\n\n---\n\nThe fixture system answers every query in plain words.\n"
CLAIM_TEXT = "GNI checks every source twice daily."
CLAIM_KEPT = "GNI publishes every report for free."
# S107 R3-3: one claim a fitness function can measure. F-ROUTES counts route.ts
# files under src/app/api; the base tree has one, so this claim starts
# SUPPORTED. Not F-PAGES: several older families add a page, and a measured
# page count would turn them red on C13 for a reason they do not test.
CLAIM_PAGES = "GNI exposes 1 API endpoint to readers."
PAGES_FRAG = "1 API endpoint"
CLAIM_PAGE = ("export default function P() { return <div><p>%s</p>\n<p>%s</p>\n<p>%s</p></div> }\n"
              % (CLAIM_TEXT, CLAIM_KEPT, CLAIM_PAGES))
CLAIM_NEW = "GNI verifies every forecast after seven days."


def _verdict_row(gcl, text, verdict, kind="-", cid="-"):
    return "\t".join((gcl.key_of(text), verdict, kind, cid, text))


def _claims_files(root, claim_texts=(CLAIM_TEXT, CLAIM_KEPT, CLAIM_PAGES)):
    """Every manual unit the tree yields gets a verdict: the named texts are
    CLAIMs, everything else UI. Then the claims document is rendered."""
    import gni_claims as gcl
    rows, binds, seen, n = [], [], set(), 0
    for _, _, kind, t in gcl.candidates(root):
        k = gcl.key_of(t)
        if k in seen or gcl.tier(kind, t) != "manual":
            continue
        seen.add(k)
        if t in claim_texts:
            n += 1
            cid = "CLM-%03d" % n
            rows.append(_verdict_row(gcl, t, "CLAIM", "STATE", cid))
            binds.append("%s\tF-ROUTES\t%s" % (cid, PAGES_FRAG) if t == CLAIM_PAGES
                         else "%s\tUNMEASURED\tUNREVIEWED" % cid)
        else:
            rows.append(_verdict_row(gcl, t, "UI"))
    w(root + "/docs/GNI_CLAIM_VERDICTS_S94.tsv", "# fixture verdicts\n" + "\n".join(rows) + "\n")
    w(root + "/docs/GNI_CLAIM_BINDINGS_S94.tsv", "# fixture bindings\n" + "\n".join(binds) + "\n")
    _claims_doc(root)


def _claims_doc(root):
    import gni_claims as gcl
    w(root + "/docs/GNI_CLAIMS_S94.md", gcl.render(root, 94))


# The base tree's two modules nothing imports and no workflow names.
BUCKETS_OK = (("ai_engine/ok.py", "DECLARE", "fixture module"),
              ("ai_engine/monitoring_pipeline.py", "DECLARE", "fixture watcher"))
ORPHAN = {"ai_engine/orphan.py": "def lonely():\n    return 1\n"}


def ap(p, s):
    with open(p, "a", encoding="utf-8") as fh:
        fh.write(s)


def base(root, arch=ARCH_OK, rules=RULES, contract=None,
         map_n_delta=0, map_present=True,
         slo_bound="1", slo_from=None, slo_to=None,
         watcher=WATCHER, snap=None, extra_arch=None, web_bound=None, web=True,
         origin_extra="", gloss_drop=None, session_rows="", extra_py=None, buckets=None):
    if os.path.isdir(root):
        shutil.rmtree(root)
    w(root + "/docs/GNI_RULES_S94.md", rules)
    w(root + "/docs/GNI_RULES_S93.md", "superseded, must be ignored: R-S99-9\n")
    w(root + "/docs/GNI_ARCHITECTURE_S94.md", arch)
    w(root + "/docs/CONTRACT_S94.md",
      contract if contract is not None else "law: R-S90-2 and `GNI-R-076` apply\n")
    w(root + "/docs/GNI_Session_Transfer_Protocol_S94.md", "see R-S92-2\n")
    w(root + "/docs/GNI_TARGET_AND_ORDER_S94.md", "queue: GNI-L-003\n")
    w(root + "/docs/HANDOFF_S94.md", "state: R-S81-1\n")
    w(root + "/.github/workflows/a.yml", "on:\n  schedule:\n    - cron: '0 2 * * *'\njobs:\n  x:\n")
    w(root + "/.github/workflows/b.yml", "on:\n  push:\njobs:\n  y:\n")
    w(root + "/ai_engine/ok.py", "rows = q.order('created_at', desc=True).execute().data\n")
    w(root + "/src/app/api/r/route.ts", "const s = createNoStoreClient()\n")
    # S106: C11 needs the lib and one page that formats through it.
    w(root + "/src/lib/escalation.ts", ESC_LIB_OK)
    w(root + "/src/app/brief/page.tsx", ESC_PAGE_OK)
    w(root + "/ai_engine/monitoring_pipeline.py", watcher)
    # S107 R3-3: extra modules go in BEFORE the git index and the section-5
    # stamp, so a family that adds one is red on C14 and not also on C8.
    for rel, body in (extra_py or {}).items():
        w(root + "/" + rel, body)
    w(root + "/docs/GNI_MODULE_BUCKETS_S94.tsv", "# fixture buckets\n" + "".join(
        "%s\t%s\t%s\n" % r for r in (BUCKETS_OK if buckets is None else buckets)))
    w(root + "/docs/gni_runtime_snapshot_S94.json",
      snap if snap is not None else _snap_text())
    ap(root + "/docs/GNI_ARCHITECTURE_S94.md",
       _slo_block(slo_bound,
                  slo_from if slo_from else SLO_FAST[0],
                  slo_to if slo_to else SLO_FAST[-1]))
    if web:   # S105: the public constant mirrors SLO-CFG unless a family says otherwise
        w(root + "/src/lib/freshness.ts",
          "export const FRESHNESS_BOUND_HOURS = %s\n"
          "export const FRESHNESS_EXCEEDANCE_MAX = 0.10\n"
          "export const FRESHNESS_WINDOW_FROM = '%s'\n"
          "export const FRESHNESS_WINDOW_TO = '%s'\n"
          % (web_bound if web_bound else slo_bound,
             slo_from if slo_from else SLO_FAST[0], slo_to if slo_to else SLO_FAST[-1]))
    # The index must exist before the stamps: section five's fingerprint is
    # `git ls-files '*.py'` under the hood, and an untracked tree hashes to a
    # value no generator would ever publish.
    _git_index(root)
    ap(root + "/docs/GNI_ARCHITECTURE_S94.md", _gen_stamps(root))
    if extra_arch:
        ap(root + "/docs/GNI_ARCHITECTURE_S94.md", extra_arch)
    # LAST, and the order is load-bearing: the map stamps the architecture's
    # md5, and the SLO and STAMP blocks above APPEND to the architecture.
    # Stamping before those appends would leave every family red on a hash the
    # fixture itself had just invalidated -- the check would look alive while
    # measuring nothing.
    if map_present:
        w(root + "/docs/GNI_MACRO_MAP_S94.md",
          _map_text(root + "/docs/GNI_RULES_S94.md",
                    root + "/docs/GNI_ARCHITECTURE_S94.md", map_n_delta))
    # S106: ORIGIN before the glossary, because C9 scans ORIGIN too and the
    # glossary is derived from everything C9 scans.
    # S107: the claims files before the glossary, because the glossary's
    # English corpus is every .md under docs/ and these are two of them.
    w(root + "/docs/GNI_WHITE_PAPER_S94.md", WP_OK)
    w(root + "/src/app/claims/page.tsx", CLAIM_PAGE)
    _claims_files(root)
    w(root + "/docs/GNI_ORIGIN.md", ORIGIN_OK + origin_extra)
    w(root + "/docs/GNI_GLOSSARY_S94.md",
      _glossary_text(root, drop_check=gloss_drop, session_rows=session_rows))
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
CASES["15-slo-bound-not-derived"] = lambda r: base(r, slo_bound="2")
CASES["16-slo-window-spans-regimes"] = lambda r: base(
    r, slo_bound="3", slo_from=SLO_FAST[0], slo_to=SLO_SLOW[-1])
CASES["17-standdown-absent"] = lambda r: base(
    r, watcher=WATCHER, snap=_snap_pw_text(),
    slo_bound="3", slo_from=SLO_PW[0], slo_to=SLO_PW[-1])
CASES["18-standdown-reinstated"] = lambda r: base(
    r, watcher=WATCHER_STANDDOWN, snap=_snap_pw_text(),
    slo_bound="3", slo_from=SLO_PW[0], slo_to=SLO_PW[-1])

# S103, item 5.50. 19 is what the DoD asked for; 20 and 21 go beyond it.
# 20 is the DISCRIMINATOR (R-S90-1): a check that compared only hashes passes
# it, because the file the map names still exists and still hashes correctly.
# That is precisely the failure S102 suffered and could not see.
CASES["19-map-stale-arch-md5"] = lambda r: (
    base(r), ap(r + "/docs/GNI_ARCHITECTURE_S94.md",
                "\nprose line carrying no id and no marker\n"), r)[-1]
CASES["20-map-arch-renamed"] = lambda r: (
    base(r), shutil.copyfile(r + "/docs/GNI_ARCHITECTURE_S94.md",
                             r + "/docs/GNI_ARCHITECTURE_S95.md"), r)[-1]
CASES["21-map-third-input"] = lambda r: (
    base(r), ap(r + "/docs/GNI_MACRO_MAP_S94.md",
                "INPUT `%s/docs/CONTRACT_S94.md` md5 `%s` (EOL-normalised)\n"
                % (r, "0" * 32)), r)[-1]

# S104, item 5.54. One family per failure shape C8 can detect. 24 is the
# DISCRIMINATOR against C2 (R-S90-1): C2 counts workflows and passes, because
# the counts did not move; only the bytes did. 23 is the liveness shape C6
# learned at S103 -- the named file still exists and still hashes correctly.
CASES["22-sec5-stale-manifest"] = lambda r: (
    base(r), ap(r + "/ai_engine/ok.py", "extra = 1\n"), r)[-1]
CASES["23-sec6-snapshot-renamed"] = lambda r: (
    base(r), shutil.copyfile(r + "/docs/gni_runtime_snapshot_S94.json",
                             r + "/docs/gni_runtime_snapshot_S95.json"), r)[-1]
CASES["24-sec7-workflow-edited"] = lambda r: (
    base(r), ap(r + "/.github/workflows/a.yml",
                "# fixture edit: bytes move, counts do not\n"), r)[-1]
CASES["25-arch-unknown-generator"] = lambda r: base(
    r, extra_arch="\n**GENERATED by `tools/gni_future.py` from HEAD `x` "
                  "\u2014 manifest md5 `%s` (EOL-normalised).**\n" % ("0" * 32))

CASES["26-web-bound-stale"] = lambda r: base(r, web_bound="12")
CASES["27-web-constant-missing"] = lambda r: base(r, web=False)

# S106, roadmap 3 row R3-1. One family per shape C9 and C10 can detect, and a
# DISCRIMINATOR beside each red one (R-S90-1): 36 proves C9 does not flag every
# capitalised word, 33 proves C10 honours a declared CHAT-ONLY session.
CASES["28-glossary-undefined-term"] = lambda r: (
    base(r), ap(r + "/docs/HANDOFF_S94.md", "state: QZXV broke it\n"), r)[-1]
CASES["29-glossary-check-row-missing"] = lambda r: base(r, gloss_drop="C1")
CASES["30-glossary-missing"] = lambda r: (
    base(r), os.remove(r + "/docs/GNI_GLOSSARY_S94.md"), r)[-1]
CASES["31-glossary-section-renamed"] = lambda r: (
    base(r), w(r + "/docs/GNI_GLOSSARY_S94.md",
               open(r + "/docs/GNI_GLOSSARY_S94.md", encoding="utf-8").read()
               .replace("## NAMESPACES", "## NAME SPACES")), r)[-1]
CASES["32-origin-session-unrecorded"] = lambda r: base(r, origin_extra="S53 designed it.\n")
CASES["33-origin-chat-only-declared"] = lambda r: base(
    r, origin_extra="S53 designed it.\n", session_rows="| S53 | chat | CHAT-ONLY |\n")
CASES["34-origin-hash-cited"] = lambda r: base(r, origin_extra="shipped in af010a2.\n")
CASES["35-origin-missing"] = lambda r: (
    base(r), os.remove(r + "/docs/GNI_ORIGIN.md"), r)[-1]
CASES["36-emphasis-word-passes"] = lambda r: (
    base(r), ap(r + "/docs/HANDOFF_S94.md", "state: RECORDED\n"), r)[-1]

# S106, item 9.22(c) / DoD D2. 39 is the DISCRIMINATOR for 37 (R-S90-1): the
# uncapped field rendered directly is not the capped score, and must pass.
CASES["37-escalation-direct-render"] = lambda r: (
    base(r), w(r + "/src/app/x/page.tsx", "<b>{r.escalation_score.toFixed(1)}/10</b>\n"), r)[-1]
CASES["38-escalation-lib-missing"] = lambda r: (
    base(r), os.remove(r + "/src/lib/escalation.ts"), r)[-1]
CASES["39-escalation-raw-field-passes"] = lambda r: (
    base(r), w(r + "/src/app/x/page.tsx", "<b>{r.escalation_score_raw.toFixed(1)}</b>\n"), r)[-1]
CASES["40-escalation-capped-average"] = lambda r: (
    base(r), w(r + "/src/app/x/page.tsx", "<b>avg {c.avg_escalation_score?.toFixed(1)}/10</b>\n"), r)[-1]

# S107, roadmap 3 row R3-2. The row's DONE asks the fixture to prove a claim
# added is counted and a claim removed is not: 41/42 and 43. 42 is the
# DISCRIMINATOR for 41 (R-S90-1): the same added claim passes once the
# document is regenerated, so 41 fails on staleness, not on the claim. 45 is
# the KNOWN LIMIT of DECISION S107-3 carried as a family: a claim of under four
# words with no lexicon word is filed UI by rule and the check cannot see it.
def _add_claim(r, regenerate):
    import gni_claims as gcl
    base(r)
    w(r + "/src/app/claims2/page.tsx", "export default function Q() { return <p>%s</p> }\n" % CLAIM_NEW)
    ap(r + "/docs/GNI_CLAIM_VERDICTS_S94.tsv",
       _verdict_row(gcl, CLAIM_NEW, "CLAIM", "PROMISE", "CLM-900") + "\n")
    ap(r + "/docs/GNI_CLAIM_BINDINGS_S94.tsv", "CLM-900\tUNMEASURED\tPROMISE\n")
    if regenerate:
        _claims_doc(r)
    return r


def _forge_key(r):
    import gni_claims as gcl
    base(r)
    ap(r + "/docs/GNI_CLAIM_VERDICTS_S94.tsv",
       "\t".join(("0" * 10, "UI", "-", "-", "a row whose key is not its text")) + "\n")
    return r


CASES["41-claim-added-not-regenerated"] = lambda r: _add_claim(r, False)
CASES["42-claim-added-regenerated"] = lambda r: _add_claim(r, True)
CASES["43-claim-removed"] = lambda r: (
    base(r), w(r + "/src/app/claims/page.tsx", CLAIM_PAGE.replace("<p>%s</p>\n" % CLAIM_TEXT, "")),
    r)[-1]
CASES["44-literal-unclassified"] = lambda r: (
    base(r), w(r + "/src/app/claims3/page.tsx",
               "export default function R() { return <p>GNI never sleeps at night.</p> }\n"), r)[-1]
CASES["45-short-claim-escapes-known-limit"] = lambda r: (
    base(r), w(r + "/src/app/claims3/page.tsx",
               "export default function R() { return <p>Runs itself.</p> }\n"), r)[-1]
CASES["46-claims-doc-missing"] = lambda r: (
    base(r), os.remove(r + "/docs/GNI_CLAIMS_S94.md"), r)[-1]
CASES["47-verdict-key-forged"] = _forge_key

# S107, roadmap 3 row R3-3. The row's cert: flip one claim wired -> unwired and
# the verdict must flip (48). 49 flips the MEASUREMENT instead: one more route
# file and "1 API endpoint" is defeated, while the document still says SUPPORTED. 50
# is the DISCRIMINATOR for 49 (R-S90-1): regenerated, the same tree passes with
# a DEFEATED claim on record, so 49 fails on an underived status and not on the
# defeat. 51 is a status typed by hand. Each of 48, 49, 51 is red on C13 alone.
# 49 flips the measurement with one more route file (a no-store one, so C4
# stays green).
def _bindings(r):
    return r + "/docs/GNI_CLAIM_BINDINGS_S94.tsv"


def _unwire(r):
    base(r)
    text = open(_bindings(r), encoding="utf-8").read()
    w(_bindings(r), "\n".join(l for l in text.split("\n") if "\tF-ROUTES\t" not in l))
    return r


def _extra_page(r, regenerate):
    base(r)
    w(r + "/src/app/api/extra/route.ts", "const s = createNoStoreClient()\n")
    if regenerate:
        _claims_doc(r)
    return r


def _hand_typed(r):
    base(r)
    doc = r + "/docs/GNI_CLAIMS_S94.md"
    text = open(doc, encoding="utf-8").read()
    w(doc, text.replace("| STATE | SUPPORTED | F-ROUTES", "| STATE | DEFEATED | F-ROUTES"))
    return r


def _fragment_forged(r):
    base(r)
    text = open(_bindings(r), encoding="utf-8").read()
    w(_bindings(r), text.replace("\tF-ROUTES\t%s" % PAGES_FRAG, "\tF-ROUTES\t9 API endpoint"))
    return r


CASES["48-claim-unwired"] = _unwire
CASES["49-measurement-flips"] = lambda r: _extra_page(r, False)
CASES["50-measurement-flips-regenerated"] = lambda r: _extra_page(r, True)
CASES["51-status-hand-typed"] = _hand_typed
CASES["52-fragment-not-verbatim"] = _fragment_forged

# S107, roadmap 3 row R3-3, check `dead symbols`. 53 is the DET-DEAD shape: a
# module nothing imports and no bucket names. 54 is its DISCRIMINATOR
# (R-S90-1): the same module, bucketed, passes. 55 is a row that rotted.
CASES["53-dead-module-unbucketed"] = lambda r: base(r, extra_py=ORPHAN)
CASES["54-dead-module-bucketed"] = lambda r: base(
    r, extra_py=ORPHAN, buckets=BUCKETS_OK + (("ai_engine/orphan.py", "DELETE", "serves no claim"),))
CASES["55-bucket-row-stale"] = lambda r: base(
    r, buckets=BUCKETS_OK + (("ai_engine/gone.py", "DELETE", "already deleted"),))
CASES["56-bucket-wire-without-claim"] = lambda r: base(
    r, extra_py=ORPHAN, buckets=BUCKETS_OK + (("ai_engine/orphan.py", "WIRE", "serves something"),))

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
    "15-slo-bound-not-derived": 1, "16-slo-window-spans-regimes": 1,
    "17-standdown-absent": 0, "18-standdown-reinstated": 1,
    "19-map-stale-arch-md5": 1, "20-map-arch-renamed": 1,
    "21-map-third-input": 1,
    "22-sec5-stale-manifest": 1, "23-sec6-snapshot-renamed": 1,
    "24-sec7-workflow-edited": 1, "25-arch-unknown-generator": 2,
    "26-web-bound-stale": 1, "27-web-constant-missing": 1,
    "28-glossary-undefined-term": 1, "29-glossary-check-row-missing": 1,
    "30-glossary-missing": 2, "31-glossary-section-renamed": 2,
    "32-origin-session-unrecorded": 1, "33-origin-chat-only-declared": 0,
    "34-origin-hash-cited": 1, "35-origin-missing": 2,
    "36-emphasis-word-passes": 0,
    "37-escalation-direct-render": 1, "38-escalation-lib-missing": 2,
    "39-escalation-raw-field-passes": 0, "40-escalation-capped-average": 1,
    "41-claim-added-not-regenerated": 1, "42-claim-added-regenerated": 0,
    "43-claim-removed": 1, "44-literal-unclassified": 1,
    "45-short-claim-escapes-known-limit": 0, "46-claims-doc-missing": 2,
    "47-verdict-key-forged": 2,
    "48-claim-unwired": 1, "49-measurement-flips": 1,
    "50-measurement-flips-regenerated": 0, "51-status-hand-typed": 1,
    "52-fragment-not-verbatim": 2,
    "53-dead-module-unbucketed": 1, "54-dead-module-bucketed": 0,
    "55-bucket-row-stale": 1, "56-bucket-wire-without-claim": 2,
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
