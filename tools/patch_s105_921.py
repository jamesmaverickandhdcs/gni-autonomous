#!/usr/bin/env python3
"""S105 item 9.21 - public pages state the MEASURED freshness bound, never the declared cron.

ARCHITECTURE section 10.3 (SLO-2) promises that every public page stating a monitoring cadence
states the bound with its window. A live read at S105 found 0 pages doing so. This patch:
  1. creates src/lib/freshness.ts - four literals that MIRROR the SLO-CFG lines;
  2. rewrites the heartbeat statements to use them, labels the self-check's */30 as a request,
     and drops "Real-time" from the site description;
  3. extends C7: the four literals must equal SLO-CFG, so a moved bound reddens the detector
     until the pages follow (the S102 lesson: a page that was accidentally right became wrong);
  4. adds fixture families 26 and 27 so the extension discriminates (R-S90-1).
Binary mode, ASCII-only anchors (GNI-L-015), every anchor must occur exactly once, all or nothing.
usage: python tools/patch_s105_921.py [--apply]     (default: dry run)"""
import os, subprocess, sys

EM = b"\xe2\x80\x94"   # em dash, written as bytes so this file stays ASCII

FRESHNESS_TS = b"""// Freshness wording for public pages - ARCHITECTURE section 10, SLO-2.
// The four FRESHNESS_ literals below MIRROR the SLO-CFG lines of the live architecture, and
// C7 compares them on every push: move the bound there and the detector stays red until this
// file follows. Never publish a workflow's declared cron as its cadence (section 10.1).
export const FRESHNESS_BOUND_HOURS = 8
export const FRESHNESS_EXCEEDANCE_MAX = 0.10
export const FRESHNESS_WINDOW_FROM = '2026-08-27'
export const FRESHNESS_WINDOW_TO = '2026-09-03'

const inTen = Math.round((1 - FRESHNESS_EXCEEDANCE_MAX) * 10)

// Table cells.
export const FRESHNESS_SHORT =
  `at most ${FRESHNESS_BOUND_HOURS} h old, ${inTen} times in 10 ` +
  `(measured ${FRESHNESS_WINDOW_FROM} to ${FRESHNESS_WINDOW_TO})`
// Prose.
export const FRESHNESS_LINE =
  `GNI's view of the world is at most ${FRESHNESS_BOUND_HOURS} hours old, ${inTen} times in 10 ` +
  `(measured ${FRESHNESS_WINDOW_FROM} to ${FRESHNESS_WINDOW_TO})`
// A workflow with no measured bound: its schedule is a request, not a rate.
export const SCHEDULE_REQUESTED_30 =
  'scheduled every 30 min (a request to GitHub Actions, not a measured rate)'
"""

PAGE = "src/app/%s/page.tsx"
REACT = b"import { useEffect, useState } from 'react'"
def imp(*names):
    return b"import { " + b", ".join(n.encode() for n in names) + b" } from '@/lib/freshness'"

# (file, old, new) - each old must occur exactly once in its file. "<EOL>" is the file's own.
EDITS = [
    (PAGE % "methodology",
     b"\xef\xbb\xbf'use client'<EOL>",
     b"\xef\xbb\xbf'use client'<EOL>" + imp("FRESHNESS_SHORT") + b"<EOL>"),
    (PAGE % "methodology",
     b"{ pipeline: 'gni_heartbeat', cron: 'Every 30 min',",
     b"{ pipeline: 'gni_heartbeat', cron: FRESHNESS_SHORT,"),

    (PAGE % "about/devops", REACT + b"<EOL>",
     REACT + b"<EOL>" + imp("FRESHNESS_LINE", "FRESHNESS_SHORT", "SCHEDULE_REQUESTED_30") + b"<EOL>"),
    (PAGE % "about/devops",
     b"{ name: 'gni_heartbeat', schedule: 'Every 30 min',",
     b"{ name: 'gni_heartbeat', schedule: FRESHNESS_SHORT,"),
    (PAGE % "about/devops",
     b"desc: 'Heartbeat monitors escalation delta every 30 minutes. Mission Control checks Supabase "
     b"connection, report freshness, quota ceiling, source health, pipeline recency. Telegram "
     b"CRITICAL/WARNING alerts with specific action recommendations.' },",
     b"desc: `Heartbeat monitors escalation delta; ${FRESHNESS_LINE}. Mission Control checks Supabase "
     b"connection, report freshness, quota ceiling, source health, pipeline recency. Telegram "
     b"CRITICAL/WARNING alerts with specific action recommendations.` },"),
    (PAGE % "about/devops",
     b"desc: 'Mission Control monitors 6 health dimensions every 30 minutes. Telegram alerts",
     b"desc: `Mission Control monitors 6 health dimensions, ${SCHEDULE_REQUESTED_30}. Telegram alerts"),
    (PAGE % "about/devops",
     b"triggers corrective pipelines autonomously. The system fixes itself.' },",
     b"triggers corrective pipelines autonomously. The system fixes itself.` },"),

    (PAGE % "adaptive-log", REACT + b"<EOL>", REACT + b"<EOL>" + imp("FRESHNESS_LINE") + b"<EOL>"),
    (PAGE % "adaptive-log",
     b"<span>Heartbeat runs every 30 min " + EM + b" zero Groq calls (GNI-R-114)</span>",
     b"<span>Heartbeat: {FRESHNESS_LINE} " + EM + b" zero Groq calls (GNI-R-114)</span>"),

    (PAGE % "developer-hub", REACT + b"<EOL>", REACT + b"<EOL>" + imp("SCHEDULE_REQUESTED_30") + b"<EOL>"),
    (PAGE % "developer-hub",
     b"Autonomous web-layer health monitoring that runs every 30 minutes. Checks",
     b"Autonomous web-layer health monitoring, {SCHEDULE_REQUESTED_30}. Checks"),

    (PAGE % "mission-control", REACT + b"<EOL>", REACT + b"<EOL>" + imp("SCHEDULE_REQUESTED_30") + b"<EOL>"),
    (PAGE % "mission-control",
     b"Auto-runs every 30 minutes. Checks:",
     b"Auto-runs: {SCHEDULE_REQUESTED_30}. Checks:"),

    ("src/app/layout.tsx",
     b"intelligence. Real-time analysis of global conflicts, market impact, escalation risk, and financial",
     b"intelligence. Analysis of global conflicts, market impact, escalation risk, and financial"),
    ("src/app/layout.tsx",
     b"intelligence. Real-time analysis of global conflicts, market impact, and escalation risk.",
     b"intelligence. Analysis of global conflicts, market impact, and escalation risk."),
    ("src/app/layout.tsx",
     b"'Real-time autonomous AI analysis of global conflicts and market impact. Free forever.'",
     b"'Autonomous AI analysis of global conflicts and market impact. Free forever.'"),

    ("tools/gni_rule_checks.py",
     b"    if problems:<EOL>        return False, \"; \".join(problems)<EOL>"
     b"    return True, (\"%s h is the smallest hour inside a %.2f budget; %d of %d gaps \"",
     b"    # (c) S105, item 9.21: the public pages carry the bound through ONE constant that<EOL>"
     b"    # mirrors SLO-CFG. A moved bound must redden here until the pages follow it.<EOL>"
     b"    web = os.path.join(ctx[\"root\"], \"src\", \"lib\", \"freshness.ts\")<EOL>"
     b"    if not os.path.isfile(web):<EOL>"
     b"        problems.append(\"no public freshness constant at src/lib/freshness.ts\")<EOL>"
     b"    else:<EOL>"
     b"        with open(web, \"rb\") as fh:<EOL>"
     b"            ts = fh.read().decode(\"utf-8\")<EOL>"
     b"        for key in (\"BOUND_HOURS\", \"EXCEEDANCE_MAX\", \"WINDOW_FROM\", \"WINDOW_TO\"):<EOL>"
     b"            m = re.search(r\"^export const FRESHNESS_%s = '?([^'\\s]+)'?\\s*$\" % key, ts, re.M)<EOL>"
     b"            seen = m.group(1) if m else None<EOL>"
     b"            if key.startswith(\"WINDOW\"):<EOL>"
     b"                same = seen == cfg[key]<EOL>"
     b"            else:<EOL>"
     b"                same = seen is not None and float(seen) == float(cfg[key])<EOL>"
     b"            if not same:<EOL>"
     b"                problems.append(\"src/lib/freshness.ts FRESHNESS_%s is %s; SLO-CFG says %s\"<EOL>"
     b"                                % (key, seen, cfg[key]))<EOL>"
     b"<EOL>"
     b"    if problems:<EOL>        return False, \"; \".join(problems)<EOL>"
     b"    return True, (\"%s h is the smallest hour inside a %.2f budget; %d of %d gaps \""),

    ("tools/gni_rule_checks_fixture.py",
     b"         watcher=WATCHER, snap=None, extra_arch=None):",
     b"         watcher=WATCHER, snap=None, extra_arch=None, web_bound=None, web=True):"),
    ("tools/gni_rule_checks_fixture.py",
     b"                  slo_to if slo_to else SLO_FAST[-1]))<EOL>",
     b"                  slo_to if slo_to else SLO_FAST[-1]))<EOL>"
     b"    if web:   # S105: the public constant mirrors SLO-CFG unless a family says otherwise<EOL>"
     b"        w(root + \"/src/lib/freshness.ts\",<EOL>"
     b"          \"export const FRESHNESS_BOUND_HOURS = %s\\n\"<EOL>"
     b"          \"export const FRESHNESS_EXCEEDANCE_MAX = 0.10\\n\"<EOL>"
     b"          \"export const FRESHNESS_WINDOW_FROM = '%s'\\n\"<EOL>"
     b"          \"export const FRESHNESS_WINDOW_TO = '%s'\\n\"<EOL>"
     b"          % (web_bound if web_bound else slo_bound,<EOL>"
     b"             slo_from if slo_from else SLO_FAST[0], slo_to if slo_to else SLO_FAST[-1]))<EOL>"),
    ("tools/gni_rule_checks_fixture.py",
     b"# Expected verdict per family.",
     b"CASES[\"26-web-bound-stale\"] = lambda r: base(r, web_bound=\"12\")<EOL>"
     b"CASES[\"27-web-constant-missing\"] = lambda r: base(r, web=False)<EOL>"
     b"<EOL># Expected verdict per family."),
    ("tools/gni_rule_checks_fixture.py",
     b"\"24-sec7-workflow-edited\": 1, \"25-arch-unknown-generator\": 2,",
     b"\"24-sec7-workflow-edited\": 1, \"25-arch-unknown-generator\": 2,<EOL>"
     b"    \"26-web-bound-stale\": 1, \"27-web-constant-missing\": 1,"),
]

def main():
    apply = "--apply" in sys.argv
    if subprocess.run(["git", "status", "--porcelain"], capture_output=True).stdout.strip():
        print("REFUSED: tree is not clean"); return 1
    if os.path.exists("src/lib/freshness.ts"):
        print("REFUSED: src/lib/freshness.ts already exists"); return 1
    out = {}
    for f, old, new in EDITS:
        b = out.get(f)
        if b is None:
            if not os.path.isfile(f):
                print("REFUSED: missing " + f); return 1
            b = open(f, "rb").read()
        eol = b"\r\n" if b"\r\n" in b else b"\n"
        o, n = old.replace(b"<EOL>", eol), new.replace(b"<EOL>", eol)
        if b.count(o) != 1:
            print("REFUSED: %s - anchor occurs %d times, expected 1:\n  %r" % (f, b.count(o), o[:90])); return 1
        out[f] = b.replace(o, n)
    print("%-36s %s" % ("src/lib/freshness.ts", "NEW" if not apply else "WRITTEN (new)"))
    for f in sorted(out):
        print("%-36s %s" % (f, "WRITTEN" if apply else "would change"))
    if not apply:
        print("DRY RUN - %d edits in %d files plus 1 new file, nothing written" % (len(EDITS), len(out))); return 0
    os.makedirs("src/lib", exist_ok=True)
    open("src/lib/freshness.ts", "wb").write(FRESHNESS_TS)
    for f, b in out.items():
        open(f, "wb").write(b)
    print("APPLIED %d edits in %d files plus src/lib/freshness.ts" % (len(EDITS), len(out)))
    return 0

if __name__ == "__main__":
    sys.exit(main())
