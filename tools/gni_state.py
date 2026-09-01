#!/usr/bin/env python3
"""tools/gni_state.py -- GENERATOR for GNI ARCHITECTURE section 7 (DEPLOYMENT VIEW).

Born S94. Scope is SECTION 7 ONLY. Sections 5 and 6 are deliberately out of scope
(section 5 needs AST work; section 6 needs the measured lateness band, which must be
measured and never recalled -- see R-S87-6 third amendment).

WHY A GENERATOR (ARCHITECTURE 8.2): a hand-written inventory rots silently. Every
hand-measured inventory in this project has rotted. If this script fails, section 7
is ABSENT and that absence is visible -- which is the correct failure mode.

THE CHAIN. A secret does not reach code under its own name. A workflow maps it to an
ENV VAR:  GROQ_MODEL: ${{ secrets.GROQ_MODEL }}  and the code reads os.getenv('GROQ_MODEL').
So the consumer search runs over the secret name AND every env alias any workflow binds
it to. A generator that stops at "which workflow reads this secret" reproduces the trap
S93 spent a block undoing: GROQ_MODEL_FALLBACK is read by NO workflow and by SIX code files.

R-S93-1: the instrument checks its own expectations BY THE SCRIPT, with a control probe,
before it reads anything real. The probes include the exact regex bug that produced a
false finding at S94 open (a case-restricted class truncating TELEGRAM_QSChannel_ID).

Usage:
    python tools/gni_state.py                       # writes docs/GNI_ARCHITECTURE_S94.md
    python tools/gni_state.py --session 95
    python tools/gni_state.py --stdout              # print section 7, write nothing
    python tools/gni_state.py --no-gh               # skip `gh secret list`
Exit codes: 0 ok - 2 control probe failed (nothing written) - 3 input missing.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # derived from HERE: working directory does not matter
SELF = "tools/" + Path(__file__).name   # never count the generator's own source as a consumer
WF_DIR = ROOT / ".github" / "workflows"
DOCS = ROOT / "docs"

CODE_EXT = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".sh", ".yml_disabled"}

# --- patterns. Case class is [A-Za-z0-9_] ON PURPOSE. See control_probe(). ---------
SECRET_RE = re.compile(r"(?<![A-Za-z0-9_])secrets\.([A-Za-z_][A-Za-z0-9_]*)")
CRON_RE = re.compile(r"^\s*-\s*cron:\s*['\"]([^'\"]+)['\"]")
ENVMAP_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*\$\{\{\s*secrets\.([A-Za-z_][A-Za-z0-9_]*)\s*\}\}"
)
ENTRY_RE = re.compile(
    r"(?:python3?\s+-m\s+[A-Za-z0-9_.]+|python3?\s+[A-Za-z0-9_./-]+\.py|bash\s+[A-Za-z0-9_./-]+\.sh)"
)
GENDOC_RE = re.compile(r"docs/GNI_ARCHITECTURE_S\d+\.md$")
JOB_RE = re.compile(r"^  ([A-Za-z0-9_-]+):\s*$")
TOPKEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):")


def control_probe() -> list[str]:
    """Assert the instrument's own expectations before trusting any real reading."""
    fails = []

    # 1. POSITIVE, and the exact S94-open bug: a mixed-case secret name must survive whole.
    m = SECRET_RE.findall("        TG: ${{ secrets.TELEGRAM_QSChannel_ID }}")
    if m != ["TELEGRAM_QSChannel_ID"]:
        fails.append(f"SECRET_RE truncates mixed-case names: {m!r}")

    # 2. NEGATIVE: a word merely containing 'secrets.' must not match.
    if SECRET_RE.findall("mysecrets.FOO and secretsauce.BAR"):
        fails.append("SECRET_RE matches a non-boundary occurrence")

    # 3. cron with a trailing comment (every real GNI cron line has one).
    c = CRON_RE.match("    - cron: '43 2 * * *'   # 02:43 UTC -- pipeline + 30 min")
    if not c or c.group(1) != "43 2 * * *":
        fails.append("CRON_RE fails on a commented cron line")

    # 4. the env alias binding -- the link the whole chain rests on.
    e = ENVMAP_RE.match("          GROQ_MODEL: ${{ secrets.GROQ_MODEL }}")
    if not e or e.groups() != ("GROQ_MODEL", "GROQ_MODEL"):
        fails.append("ENVMAP_RE fails on a plain binding")
    e2 = ENVMAP_RE.match("          TELEGRAM_CHAT: ${{ secrets.TELEGRAM_ADMIN_ID }}")
    if not e2 or e2.groups() != ("TELEGRAM_CHAT", "TELEGRAM_ADMIN_ID"):
        fails.append("ENVMAP_RE fails when env name != secret name")

    # 5. NEGATIVE for the entrypoint: a pip line is not an entrypoint.
    if ENTRY_RE.search("          pip install --upgrade pip"):
        fails.append("ENTRY_RE matches a pip line")
    if not ENTRY_RE.search("        run: python ai_engine/mad_runner.py"):
        fails.append("ENTRY_RE misses a real entrypoint")
    return fails


def sh(args: list[str], cwd: Path = ROOT) -> tuple[int, str]:
    try:
        p = subprocess.run(args, cwd=str(cwd), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=60)
        return p.returncode, p.stdout or ""
    except Exception as exc:                                  # noqa: BLE001
        return 1, f"<{type(exc).__name__}: {exc}>"


def parse_workflow(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    wf: dict = {
        "file": path.name, "triggers": [], "crons": [], "jobs": [],
        "entrypoints": [], "pip": [], "secret_refs": {}, "env_alias": {},
    }
    in_on = in_jobs = False
    for i, raw in enumerate(lines, 1):
        line = raw.rstrip("\n")
        if TOPKEY_RE.match(line):
            key = TOPKEY_RE.match(line).group(1)
            in_on, in_jobs = key == "on", key == "jobs"
            continue
        if in_on:
            k = line.strip().rstrip(":")
            if k in ("schedule", "push", "pull_request", "workflow_dispatch", "workflow_call"):
                if k not in wf["triggers"]:
                    wf["triggers"].append(k)
            c = CRON_RE.match(line)
            if c:
                wf["crons"].append(c.group(1))
        if in_jobs:
            j = JOB_RE.match(line)
            if j:
                wf["jobs"].append(j.group(1))
        for name in SECRET_RE.findall(line):
            wf["secret_refs"].setdefault(name, []).append(i)
        em = ENVMAP_RE.match(line)
        if em:
            env, sec = em.groups()
            wf["env_alias"].setdefault(sec, set()).add(env)
        if "pip install" not in line:
            for hit in ENTRY_RE.findall(line):
                wf["entrypoints"].append((i, hit.strip()))
        if "pip install" in line and "--upgrade pip" not in line:
            pkgs, j = [], i - 1
            buf = line.split("pip install", 1)[1]
            while True:
                seg = buf.split("#", 1)[0].strip()
                cont = seg.endswith("\\")
                pkgs += seg.rstrip("\\").split()
                if not cont or j + 1 >= len(lines):
                    break
                j += 1
                buf = lines[j]
            wf["pip"].append([p for p in pkgs if p and not p.startswith("-")])
    return wf


def stored_secrets(use_gh: bool) -> tuple[list[str], str]:
    if not use_gh:
        return [], "SKIPPED (--no-gh)"
    rc, out = sh(["gh", "secret", "list"])
    if rc != 0 or not out.strip():
        return [], "UNAVAILABLE -- `gh secret list` did not return; this column is BLIND"
    rows = [ln for ln in out.strip().splitlines() if ln.split()]
    if rows and rows[0].split()[0].upper() == "NAME":
        rows = rows[1:]   # gh prints a header on a TTY and NONE through a pipe
    names = [ln.split()[0] for ln in rows]
    return sorted(names), f"{len(names)} read from `gh secret list`"


def code_consumers(names: set[str]) -> tuple[list[str], list[str]]:
    """Return (code hits, non-code hits) as 'path:line' for any of the given names."""
    code, other = [], []
    for name in sorted(names):
        rc, out = sh(["git", "grep", "-n", "-I", "-w", "-F", "--", name])
        if rc not in (0, 1):
            continue
        for ln in out.splitlines():
            path = ln.split(":", 1)[0]
            if (path.startswith(".github/workflows/") or path == SELF
                    or GENDOC_RE.match(path)):
                continue        # never count our own output: that count would grow every run
            (code if Path(path).suffix in CODE_EXT else other).append(ln.split(":", 2)[0]
                                                                     + ":" + ln.split(":", 2)[1])
    return sorted(set(code)), sorted(set(other))


def stored_cell(name: str, stored: list[str]) -> str:
    """GitHub folds secret names to upper case. Comparing by bytes invents defects:
    at S94 this cell reported TELEGRAM_QSChannel_ID as NOT STORED while
    TELEGRAM_QSCHANNEL_ID sat in the same table, stored, with no workflow."""
    if name.upper() == "GITHUB_TOKEN":
        return "runner"
    if not stored:
        return "?"          # the stored list is BLIND; absence here is not evidence
    return "yes" if name.upper() in {x.upper() for x in stored} else "**NOT STORED**"


def render(wfs: list[dict], stored: list[str], stored_note: str, head: str, session: int) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    o: list[str] = []
    o.append("## §7 DEPLOYMENT VIEW — **GENERATED**")
    o.append("")
    o.append(f"**GENERATED by `tools/gni_state.py` at {now} from HEAD `{head}`. "
             "Do not hand-edit: the next run overwrites it. If this section is absent, "
             "the generator failed and that absence is the signal.**")
    o.append("")

    # 7.1 -----------------------------------------------------------------
    o.append("### 7.1 Workflow inventory")
    o.append("")
    sched = [w for w in wfs if "schedule" in w["triggers"]]
    push = [w for w in wfs if "push" in w["triggers"]]
    disp_only = [w for w in wfs if w["triggers"] == ["workflow_dispatch"]]
    o.append(f"**{len(wfs)} workflows: {len(sched)} scheduled · {len(push)} on push · "
             f"{len(disp_only)} dispatch-only.** Cron times below are NOMINAL. Observed start "
             "times run hours later; the lateness band is measured, never recalled "
             "(R-S87-6 third amendment) and is NOT generated here — it belongs to §6.")
    o.append("")
    o.append("| workflow | triggers | cron (nominal UTC) | jobs | entrypoint | secret refs |")
    o.append("|---|---|---|---|---|---|")
    for w in wfs:
        crons = "<br>".join(f"`{c}`" for c in w["crons"]) or "—"
        eps = "<br>".join(f"`{e}` :{n}" for n, e in w["entrypoints"]) or "—"
        o.append(f"| `{w['file']}` | {', '.join(w['triggers']) or '—'} | {crons} | "
                 f"{len(w['jobs'])} | {eps} | {len(w['secret_refs'])} |")
    o.append("")

    # 7.2 -----------------------------------------------------------------
    o.append("### 7.2 The chain: secret → workflow (env alias) → code consumer")
    o.append("")
    o.append(f"Stored secrets: {stored_note}. `GITHUB_TOKEN` is runner-provided, never stored.")
    o.append("")
    o.append("| secret | stored | workflows | env alias(es) | code consumers | other files |")
    o.append("|---|---|---|---|---|---|")
    o.append("**Rows are the union of `gh secret list` and every `secrets.` reference in the "
             "workflows. A name that is neither stored nor referenced — an env var read only by "
             "code — is INVISIBLE HERE BY CONSTRUCTION. That blind spot is §5's job, not §7's.**")
    o.append("")
    referenced = sorted({s for w in wfs for s in w["secret_refs"]})
    groups: dict[str, set[str]] = {}
    for n in list(stored) + referenced:
        groups.setdefault(n.upper(), set()).add(n)
    for key in sorted(groups):
        spellings = groups[key]
        # display the spelling the WORKFLOWS use; fall back to the stored one
        in_wf = [sp for sp in sorted(spellings)
                 if any(sp in w["secret_refs"] for w in wfs)]
        name = in_wf[0] if in_wf else sorted(spellings)[0]
        users = sorted({w["file"] for w in wfs for sp in spellings if sp in w["secret_refs"]})
        aliases: set[str] = set()
        for w in wfs:
            for sp in spellings:
                aliases |= w["env_alias"].get(sp, set())
        code, other = code_consumers(spellings | aliases)
        cf = sorted({c.rsplit(":", 1)[0] for c in code})
        o.append(
            f"| `{name}` | {stored_cell(name, stored)} "
            f"| {', '.join(f'`{u}`' for u in users) or '**none**'} "
            f"| {', '.join(f'`{a}`' for a in sorted(aliases)) or '—'} "
            f"| {len(cf)} files, {len(code)} hits"
            f"{(' — ' + ', '.join('`' + f + '`' for f in cf[:6]) + (' …' if len(cf) > 6 else '')) if cf else ''} "
            f"| {len({o.split(':')[0] for o in other})} |")
    o.append("")
    o.append("**Read the `none` rows with the S93 ruling in hand: a secret read by no workflow "
             "is not dangling. `GROQ_MODEL_FALLBACK` is read by code only; `GROQ_TEST_ONLY` is a "
             "deliberately local probe account; `TELEGRAM_CHAT_ID` is a pre-rename remnant that "
             "`preflight.sh` GUARDS AGAINST — its mention is a negative reference, so a nonzero "
             "consumer count there is expected. `TELEGRAM_WEBHOOK_SECRET` is read by Vercel, not "
             "Actions. Nothing in this table is a deletion instruction.**")
    o.append("")

    # 7.3 -----------------------------------------------------------------
    o.append("### 7.3 Dependency lists — evidence for item 6.9")
    o.append("")
    manifests = [m for m in ("requirements.txt", "pyproject.toml", "setup.py", "Pipfile")
                 if (ROOT / m).exists()]
    o.append(f"Dependency manifest at repo root: **{', '.join(manifests) if manifests else 'NONE'}**. "
             "Each workflow therefore carries its own inline `pip install` list.")
    o.append("")
    o.append("| workflow | packages installed inline |")
    o.append("|---|---|")
    for w in wfs:
        if not w["pip"]:
            o.append(f"| `{w['file']}` | — |")
        for k, lst in enumerate(w["pip"], 1):
            tag = f"`{w['file']}` (list {k} of {len(w['pip'])})" if len(w["pip"]) > 1 else f"`{w['file']}`"
            o.append(f"| {tag} | {', '.join(f'`{p}`' for p in lst) or '—'} |")
    o.append("")
    allsets = {frozenset(lst) for w in wfs for lst in w["pip"]}
    nlists = sum(len(w["pip"]) for w in wfs)
    o.append(f"**{len(allsets)} distinct package sets across {nlists} install steps in "
             f"{len(wfs)} workflows. "
             "None is diffable against any other, because there is nothing to diff them against.**")
    o.append("")
    return "\n".join(o)


def splice(src_text: str, section: str) -> str:
    lines = src_text.splitlines()
    start = end = None
    for i, ln in enumerate(lines):
        if start is None and ln.startswith("## §7"):
            start = i
        elif start is not None and ln.startswith("## §8"):
            end = i
            break
    if start is None or end is None:
        raise ValueError("could not locate the §7..§8 boundary in the source document")
    return "\n".join(lines[:start] + section.splitlines() + lines[end:]) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", type=int, default=94)
    ap.add_argument("--src", default=None)
    ap.add_argument("--stdout", action="store_true")
    ap.add_argument("--no-gh", action="store_true")
    args = ap.parse_args()

    fails = control_probe()
    if fails:
        print("CONTROL PROBE FAILED -- nothing written. The instrument is wrong, "
              "not the repo:", file=sys.stderr)
        for f in fails:
            print("  - " + f, file=sys.stderr)
        return 2
    print(f"CONTROL PROBE: 7/7 pass (regex, boundary, cron, alias, entrypoint)")

    if not WF_DIR.is_dir():
        print(f"MISSING: {WF_DIR}", file=sys.stderr)
        return 3
    wfs = [parse_workflow(p) for p in sorted(WF_DIR.glob("*.yml"))]
    stored, note = stored_secrets(not args.no_gh)
    _, head = sh(["git", "rev-parse", "--short", "HEAD"])
    section = render(wfs, stored, note, head.strip() or "unknown", args.session)

    if args.stdout:
        print(section)
        return 0

    if args.src:
        src = Path(args.src)
    else:
        cands = sorted(DOCS.glob("GNI_ARCHITECTURE_S*.md"),
                       key=lambda p: int(re.sub(r"\D", "", p.stem) or 0))
        if not cands:
            print(f"MISSING: no GNI_ARCHITECTURE_S*.md under {DOCS}", file=sys.stderr)
            return 3
        src = cands[-1]
    out = DOCS / f"GNI_ARCHITECTURE_S{args.session}.md"
    text = splice(src.read_text(encoding="utf-8"), section)
    out.write_text(text, encoding="utf-8", newline="\n")
    print(f"SOURCE : {src.name}")
    print(f"WROTE  : {out.relative_to(ROOT)}  ({len(text)} bytes)")
    print(f"§7 has {len(wfs)} workflows, {len(stored)} stored secrets, "
          f"{sum(len(w['secret_refs']) for w in wfs)} secret references")
    return 0


if __name__ == "__main__":
    sys.exit(main())
