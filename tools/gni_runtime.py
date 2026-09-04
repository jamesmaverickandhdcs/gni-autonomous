#!/usr/bin/env python3
"""tools/gni_runtime.py -- GENERATOR for GNI ARCHITECTURE section 6 (RUNTIME VIEW).

Born S99. Scope is SECTION 6 ONLY.

THE BOUNDARY, decided in writing before the first line was written (DECISION S99-1):
  section 7 = what is DECLARED   -- source: .github/workflows/*.yml + `gh secret list`
  section 6 = what ACTUALLY RAN  -- source: GitHub Actions run history
  section 5 = what is WRITTEN    -- source: the AST of *.py   (S100)
Section 6 does NOT answer "what calls what". `gni_state.py` already reserves that for
section 5 at its own line 233, and section 5's planned contents name `who calls it`.
Two sections answering one question is a routing error (CONTRACT ROUTING).

WHY THE HARVEST IS SPLIT FROM THE RENDER. Section 6's evidence changes every 30 minutes,
and roadmap 2's completion test requires a generator to reproduce byte-identically on an
UNCHANGED TREE. So the harvest is a separate, explicit, network-touching step that writes a
git-tracked snapshot, and the render reads ONLY that snapshot. The snapshot is part of the
tree; therefore "unchanged tree -> identical output" holds exactly, and "flip one source
fact -> the output moves" holds too. `gni_state.py` puts `datetime.now()` inside its
generated stamp and therefore FAILS this test on its own account -- measured at S99, run
twice two seconds apart, md5 differs on that one line. Do not copy that pattern.

R-S93-1: the instrument checks its own expectations BY THE SCRIPT, with a control probe,
before it reads anything real. The probe covers every cron form this repo actually uses,
plus a step form it does not use, plus two negatives.

R-S81-5 / C5: no expected value in this file is hand-written. The lateness band, the
measurability threshold and the window are all DERIVED from the snapshot.

R-S98-3: every hash this file publishes is computed after stripping BOM and folding CRLF.

Usage:
    python tools/gni_runtime.py --harvest --session 99   # calls gh, writes the snapshot
    python tools/gni_runtime.py --session 99             # snapshot -> docs/GNI_ARCHITECTURE_S99.md
    python tools/gni_runtime.py --session 99 --stdout    # print section 6, write nothing
Exit codes: 0 ok - 2 the INSTRUMENT refused (bad args, control probe, unusable window)
            3 an input is missing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):          # item 5.22: cp1252 consoles kill the run
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                  # derived from HERE: the working directory does not matter
WF_DIR = ROOT / ".github" / "workflows"
DOCS = ROOT / "docs"
SCHEMA = 1
HARVEST_LIMIT = 300

# The cron line regex is deliberately a COPY of the one in gni_state.py rather than an
# import: section 6 must not break when section 7's generator is refactored, and one
# 60-character regex is a smaller risk than a coupling between two generated sections.
CRON_RE = re.compile(r"^\s*-\s*cron:\s*['\"]([^'\"]+)['\"]")
NAME_RE = re.compile(r"^name:\s*(.+?)\s*$")


# --------------------------------------------------------------------------- cron

def _field(spec: str, lo: int, hi: int) -> set[int]:
    """Expand ONE cron field. Raises on anything it does not understand -- an
    unparsed field must not silently become an empty slot set."""
    out: set[int] = set()
    for part in spec.split(","):
        step = 1
        if "/" in part:
            part, raw = part.split("/", 1)
            step = int(raw)
            if step < 1:
                raise ValueError("step < 1 in %r" % spec)
        if part == "*":
            a, b = lo, hi
        elif "-" in part.lstrip("-"):
            lhs, rhs = part.split("-", 1)
            a, b = int(lhs), int(rhs)
        else:
            a = b = int(part)
            if step != 1:
                b = hi                      # cron's "5/10" means 5, 15, 25 ... not just 5
        if a < lo or b > hi or a > b:
            raise ValueError("field %r out of range [%d,%d]" % (spec, lo, hi))
        out.update(range(a, b + 1, step))
    if not out:
        raise ValueError("field %r expanded to nothing" % spec)
    return out


def slots_on(expr: str, day: date) -> int:
    """How many times this cron expression fires on this UTC calendar day."""
    parts = expr.split()
    if len(parts) != 5:
        raise ValueError("cron %r does not have 5 fields" % expr)
    mi, ho, dom, mon, dow = parts
    if day.month not in _field(mon, 1, 12):
        return 0
    # POSIX: when BOTH day-of-month and day-of-week are restricted, cron ORs them.
    cron_dow = day.isoweekday() % 7                       # Mon=1..Sat=6, Sun=0
    dow_set = {d % 7 for d in _field(dow, 0, 7)}          # 7 is also Sunday
    dom_ok = day.day in _field(dom, 1, 31)
    dow_ok = cron_dow in dow_set
    if dom.strip() == "*" and dow.strip() == "*":
        day_ok = True
    elif dom.strip() == "*":
        day_ok = dow_ok
    elif dow.strip() == "*":
        day_ok = dom_ok
    else:
        day_ok = dom_ok or dow_ok
    if not day_ok:
        return 0
    return len(_field(mi, 0, 59)) * len(_field(ho, 0, 23))


def min_spacing_min(exprs: list[str], day: date) -> int | None:
    """Smallest gap in MINUTES between consecutive declared slots on this day,
    across all of a workflow's cron lines. None when fewer than two slots fire."""
    marks: set[int] = set()
    for expr in exprs:
        parts = expr.split()
        if len(parts) != 5 or slots_on(expr, day) == 0:
            continue
        for h in sorted(_field(parts[1], 0, 23)):
            for m in sorted(_field(parts[0], 0, 59)):
                marks.add(h * 60 + m)
    if not marks:
        return None                                       # does not fire on this day
    if len(marks) == 1:
        return 1440                                       # one slot a day IS a 24h spacing
    ordered = sorted(marks)
    gaps = [b - a for a, b in zip(ordered, ordered[1:])]
    gaps.append(1440 - ordered[-1] + ordered[0])          # wrap to the next day
    return min(gaps)


def slot_marks(exprs: list[str], day: date) -> list[datetime]:
    marks: set[datetime] = set()
    for expr in exprs:
        parts = expr.split()
        if len(parts) != 5 or slots_on(expr, day) == 0:
            continue
        for h in sorted(_field(parts[1], 0, 23)):
            for m in sorted(_field(parts[0], 0, 59)):
                marks.add(datetime(day.year, day.month, day.day, h, m, tzinfo=timezone.utc))
    return sorted(marks)


def pair_lateness(marks: list[datetime], runs: list[datetime]) -> tuple[list[int], str]:
    """Pair declared slots to observed runs IN ORDER. Returns ([], reason) unless every
    declared slot produced a run -- see the long note in analyse() for why the obvious
    nearest-slot alternative is bounded by the very spacing it must be independent of."""
    if not marks:
        return [], "no declared slot in the window"
    if len(runs) != len(marks):
        return [], "delivered %d of %d slots -- runs cannot be paired to slots" % (
            len(runs), len(marks))
    paired = [int((r - s).total_seconds() // 60)
              for s, r in zip(sorted(marks), sorted(runs))]
    if any(x < 0 for x in paired):
        return [], "ordered pairing produced a run BEFORE its slot at the window edge"
    return sorted(paired), ""


def control_probe() -> tuple[list[str], int]:
    """Assert the instrument's own expectations before trusting any real reading.
    Returns (failures, number of assertions actually made). The count is COUNTED, never
    written down: C5 / R-S81-5 forbids a check that holds a hand-written integer, and a
    probe that says 22/22 while making 23 assertions is the disease this file is
    about -- that literal was in this file and was wrong by one when counted."""
    fails: list[str] = []
    n = 0
    mon = date(2026, 8, 31)          # a Monday
    sat = date(2026, 9, 5)           # a Saturday
    sun = date(2026, 9, 6)           # a Sunday
    cases = [
        ("0,30 * * * *", mon, 48, "list form"),
        ("*/30 * * * *", mon, 48, "step form"),
        ("*/15 * * * *", mon, 96, "step form not used by this repo"),
        ("43 2 * * *", mon, 1, "single slot"),
        ("0 14 * * 1-5", mon, 1, "weekday range, on a weekday"),
        ("0 14 * * 1-5", sat, 0, "NEGATIVE: weekday range, on a Saturday"),
        ("0 14 * * 1-5", sun, 0, "NEGATIVE: weekday range, on a Sunday"),
        ("0 6 * * 0", sun, 1, "dow 0 is Sunday"),
        ("0 6 * * 7", sun, 1, "dow 7 is Sunday too"),
    ]
    for expr, day, want, label in cases:
        n += 1
        try:
            got = slots_on(expr, day)
        except Exception as exc:                                   # noqa: BLE001
            fails.append("%s: %r raised %s" % (label, expr, exc))
            continue
        if got != want:
            fails.append("%s: %r on %s gave %d, expected %d" % (label, expr, day, got, want))

    # spacing: the whole measurability rule rests on this number being right
    n += 1
    if min_spacing_min(["0,30 * * * *"], mon) != 30:
        fails.append("min_spacing wrong for the 30-minute form")
    n += 1
    if min_spacing_min(["43 2 * * *", "43 10 * * *", "13 11 * * *"], mon) != 30:
        fails.append("min_spacing wrong across multiple cron lines (2:43/10:43/11:13 -> 30)")
    n += 1
    if min_spacing_min(["13 2 * * *", "13 10 * * *"], mon) != 480:
        fails.append("min_spacing wrong for the 8-hour pair")
    n += 1
    if min_spacing_min(["0 6 * * *"], mon) != 1440:
        fails.append("min_spacing must be 1440 when exactly one slot fires per day")
    n += 1
    if min_spacing_min(["0 14 * * 1-5"], sat) is not None:
        fails.append("min_spacing must be None on a day the cron does not fire")

    # THE BUG THIS TOOL WAS BUILT AROUND, probed by the script every run (R-S93-1).
    # A run 365 minutes after its slot, on a 30-minute cron. The nearest-preceding-slot
    # method returns 5. Ordered matching must return 365, and must REFUSE when a slot is
    # missing rather than return a small confident number.
    day = date(2026, 9, 2)
    marks = slot_marks(["0,30 * * * *"], day)
    runs_ok = [t + timedelta(minutes=365) for t in marks]
    got, why = pair_lateness(marks, runs_ok)
    n += 1
    if not got or max(got) != 365 or min(got) != 365:
        fails.append("pair_lateness lost a 365-min lag on a 30-min cron: %r %s" % (got[:3], why))
    naive = min(int((runs_ok[0] - x).total_seconds() // 60) for x in marks if x <= runs_ok[0])
    n += 1
    if naive >= 365:
        fails.append("the probe itself is wrong: the naive method was supposed to UNDERSTATE")
    got, why = pair_lateness(marks, runs_ok[:5])
    n += 1
    if got or "cannot be paired" not in why:
        fails.append("NEGATIVE: incomplete delivery must refuse, got %r / %r" % (got, why))
    got, why = pair_lateness(marks, [t - timedelta(minutes=1) for t in marks])
    n += 1
    if got or "BEFORE its slot" not in why:
        fails.append("NEGATIVE: a run before its slot must refuse, got %r / %r" % (got, why))

    # a malformed expression must RAISE, never return a plausible number
    for bad in ("0 6 * *", "0 99 * * *", "x 6 * * *"):
        n += 1
        try:
            slots_on(bad, mon)
            fails.append("NEGATIVE: %r was accepted" % bad)
        except Exception:                                          # noqa: BLE001
            pass

    n += 1
    if norm_md5(b"a\r\nb\r\n") != norm_md5(b"a\nb\n"):
        fails.append("norm_md5 is not EOL-invariant (R-S98-3)")
    n += 1
    if norm_md5(b"\xef\xbb\xbfa\n") != norm_md5(b"a\n"):
        fails.append("norm_md5 does not strip the BOM (R-S98-3)")
    return fails, n


# --------------------------------------------------------------------------- io

def norm_md5(raw: bytes) -> str:
    """R-S98-3: hash what the content IS, not how git handed it over."""
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    return hashlib.md5(raw.replace(b"\r\n", b"\n")).hexdigest()


def sh(args: list[str]) -> tuple[int, str]:
    try:
        p = subprocess.run(args, cwd=str(ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=180)
        return p.returncode, p.stdout or ""
    except Exception as exc:                                       # noqa: BLE001
        return 1, "<%s: %s>" % (type(exc).__name__, exc)


def read_workflows() -> dict:
    if not WF_DIR.is_dir():
        return {}
    out = {}
    for path in sorted(WF_DIR.glob("*.yml")):
        crons, name = [], path.stem
        for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
            m = CRON_RE.match(raw)
            if m:
                crons.append(m.group(1).strip())
            n = NAME_RE.match(raw)
            if n and name == path.stem:
                name = n.group(1).strip().strip("'\"")
        out[path.name] = {"display_name": name, "crons": crons}
    return out


def harvest(session: int) -> int:
    wfs = read_workflows()
    if not wfs:
        print("MISSING: %s" % WF_DIR, file=sys.stderr)
        return 3
    rc, head = sh(["git", "rev-parse", "--short", "HEAD"])
    snap = {"schema": SCHEMA,
            "harvested_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "harvested_head": head.strip() or "unknown",
            "harvest_limit": HARVEST_LIMIT,
            "workflows": {}}
    for fname, meta in wfs.items():
        rc, out = sh(["gh", "run", "list", "--workflow", fname, "--limit", str(HARVEST_LIMIT),
                      "--json", "databaseId,createdAt,event,conclusion,status"])
        if rc != 0:
            print("gh failed for %s -- refusing to write a partial snapshot" % fname,
                  file=sys.stderr)
            print(out[:400], file=sys.stderr)
            return 2
        try:
            runs = json.loads(out or "[]")
        except json.JSONDecodeError as exc:
            print("gh returned unparseable JSON for %s: %s" % (fname, exc), file=sys.stderr)
            return 2
        sched = [r for r in runs if r.get("event") == "schedule"]
        snap["workflows"][fname] = {
            "display_name": meta["display_name"],
            "crons": meta["crons"],
            "fetched": len(runs),
            "truncated": len(runs) >= HARVEST_LIMIT,
            "runs": sorted(({"createdAt": r["createdAt"],
                             "conclusion": r.get("conclusion") or "none"} for r in sched),
                           key=lambda r: r["createdAt"]),
        }
        print("  %-26s %4d scheduled of %4d fetched%s"
              % (fname, len(sched), len(runs), "  [TRUNCATED]" if len(runs) >= HARVEST_LIMIT else ""))
    path = DOCS / ("gni_runtime_snapshot_S%d.json" % session)
    DOCS.mkdir(exist_ok=True)
    text = json.dumps(snap, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")
    print("WROTE  : %s  (%d bytes)" % (path.relative_to(ROOT), len(text)))
    print("md5    : %s  (EOL-normalised)" % norm_md5(text.encode("utf-8")))
    print("NEXT   : python tools/gni_runtime.py --session %d" % session)
    return 0


# --------------------------------------------------------------------------- analysis

def _dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def analyse(snap: dict) -> dict:
    """Everything published below is derived here. No threshold is hand-written."""
    wfs = {k: v for k, v in snap["workflows"].items() if v["crons"]}
    if not wfs:
        raise ValueError("the snapshot holds no scheduled workflow")

    # WINDOW. Each workflow's history is capped by --limit, so a workflow's oldest run is
    # the earliest date IT can speak to. The window every workflow covers is therefore
    # bounded by the LATEST of those, and only whole UTC days are counted.
    oldest = []
    newest = []
    for v in wfs.values():
        if not v["runs"]:
            continue
        oldest.append(_dt(v["runs"][0]["createdAt"]))
        newest.append(_dt(v["runs"][-1]["createdAt"]))
    if not oldest:
        raise ValueError("the snapshot holds no scheduled runs")
    start = (max(oldest) + timedelta(days=1)).date()      # first COMPLETE day
    end = (max(newest)).date() - timedelta(days=1)        # last COMPLETE day
    if end < start:
        raise ValueError("no complete UTC day is covered by every workflow")
    days = [start + timedelta(days=i) for i in range((end - start).days + 1)]

    rows = {}
    for fname, v in sorted(wfs.items()):
        declared = sum(slots_on(c, d) for d in days for c in v["crons"])
        runs = [_dt(r["createdAt"]) for r in v["runs"]
                if start <= _dt(r["createdAt"]).date() <= end]
        spacings = [s for s in (min_spacing_min(v["crons"], d) for d in days) if s is not None]
        spacing = min(spacings) if spacings else None

        # LATENESS BY ORDERED MATCHING, and only when delivery is complete.
        # The obvious instrument -- "distance back to the nearest slot at or before the run"
        # -- is WRONG and was measured to be wrong before this line was written: on a
        # 30-minute cron a run 365 minutes late reads as 5 minutes late, because a slot is
        # never more than 30 minutes behind anything. That instrument is bounded by the
        # spacing it is supposed to be independent of, so it reports its smallest possible
        # answer exactly where the truth is largest. Ordered matching has no such bound: if
        # every declared slot produced a run, the k-th run IS the k-th slot, whatever the
        # lag. If any slot did not, no pairing is defensible and nothing is published.
        marks = [t for d in days for t in slot_marks(v["crons"], d)]
        late, why = pair_lateness(marks, runs)

        # ATTRIBUTION. A run is evidence about the SLOT it served, not about the calendar day
        # it happened to start on. With 12 hours of lateness a Friday 20:00 slot lands on
        # Saturday, and counting by creation day then reports 8 runs against 7 declared slots
        # -- 114%, which is not noise, it is incoherent, and it reads as a defect in the system
        # rather than in the arithmetic. Wherever the pairing succeeded the slot is known
        # exactly, so attribute there; only where no pairing exists is creation day used, and
        # that fallback is named in the output rather than left for the reader to discover.
        if late:
            by_slot_day: dict[date, int] = {}
            for slot, _run in zip(sorted(marks), sorted(runs)):
                by_slot_day[slot.date()] = by_slot_day.get(slot.date(), 0) + 1
            per_day = [(d, sum(slots_on(c, d) for c in v["crons"]), by_slot_day.get(d, 0))
                       for d in days]
            attribution = "slot"
        else:
            per_day = [(d, sum(slots_on(c, d) for c in v["crons"]),
                        sum(1 for r in runs if r.date() == d)) for d in days]
            attribution = "created"
        outcomes: dict[str, int] = {}
        for r in v["runs"]:
            if start <= _dt(r["createdAt"]).date() <= end:
                outcomes[r["conclusion"]] = outcomes.get(r["conclusion"], 0) + 1
        rows[fname] = {"display_name": v["display_name"], "crons": v["crons"],
                       "declared": declared, "delivered": len(runs), "spacing": spacing,
                       "late": late, "why": why, "measurable": bool(late),
                       "outcomes": outcomes, "truncated": v["truncated"],
                       "per_day": per_day, "attribution": attribution,
                       "day_ratios": sorted(got / dec for _, dec, got in per_day if dec)}

    # The band is DERIVED (R-S81-5) from the workflows whose delivery was complete -- the
    # only ones whose lateness could be measured at all. It is published so a later session
    # can compare it against R-S87-6's recorded band instead of recalling one.
    measured = sorted(f for f, r in rows.items() if r["measurable"])
    band = max((rows[f]["late"][-1] for f in measured), default=None)
    return {"start": start, "end": end, "days": days, "rows": rows,
            "band": band, "consistent": measured}


def pct(n: int, d: int) -> str:
    return "—" if not d else "%.0f%%" % (100.0 * n / d)


def quantf(xs: list[float], q: float) -> float:
    return xs[min(len(xs) - 1, max(0, int(round(q * (len(xs) - 1)))))]


def quant(xs: list[int], q: float) -> int:
    return xs[min(len(xs) - 1, max(0, int(round(q * (len(xs) - 1)))))]


# --------------------------------------------------------------------------- render

def render(snap: dict, a: dict, snap_name: str, snap_md5: str) -> str:
    o: list[str] = []
    rows, band = a["rows"], a["band"]
    o.append("## §6 RUNTIME VIEW — **GENERATED**")
    o.append("")
    o.append("**GENERATED by `tools/gni_runtime.py` from `docs/%s` — harvested %s at HEAD `%s`, "
             "snapshot md5 `%s` (EOL-normalised, R-S98-3). Window: %s to %s UTC, %d complete "
             "days. This section carries NO clock of its own: re-rendering an unchanged "
             "snapshot reproduces these bytes exactly. Do not hand-edit — the next run "
             "overwrites it. If this section is absent, the generator failed and that absence "
             "is the signal.**"
             % (snap_name, snap["harvested_at"], snap["harvested_head"], snap_md5,
                a["start"], a["end"], len(a["days"])))
    o.append("")
    o.append("**Section 6 is what ACTUALLY RAN. Section 7 is what is DECLARED; section 5 is what "
             "is WRITTEN. \"What calls what\" is section 5's question, not this one.**")
    o.append("")

    # 6.1 ------------------------------------------------------------------
    o.append("### 6.1 Declared cadence vs delivered runs")
    o.append("")
    o.append("Scheduled runs only — `workflow_dispatch` and `push` are excluded, because a "
             "manual run is not evidence about a schedule.")
    o.append("")
    o.append("| workflow | cron (nominal UTC) | declared slots | delivered | window delivery "
             "| per-day min · median · max |")
    o.append("|---|---|---|---|---|---|")
    for f, r in sorted(rows.items(), key=lambda kv: (kv[1]["declared"] and
                                                     kv[1]["delivered"] / kv[1]["declared"], kv[0])):
        crons = "<br>".join("`%s`" % c for c in r["crons"]) or "—"
        dr = r["day_ratios"]
        spread = "—" if not dr else "%.0f%% · %.0f%% · %.0f%%" % (
            100 * dr[0], 100 * quantf(dr, 0.5), 100 * dr[-1])
        if r["attribution"] == "created" and dr and dr[-1] > 1.0:
            spread += " ⚠"
        o.append("| `%s` | %s | %d | %d | **%s** | %s |"
                 % (f, crons, r["declared"], r["delivered"],
                    pct(r["delivered"], r["declared"]), spread))
    o.append("")
    tot_d = sum(r["declared"] for r in rows.values())
    tot_r = sum(r["delivered"] for r in rows.values())
    o.append("**Total: %d of %d declared slots delivered (%s) across %d complete days.**"
             % (tot_r, tot_d, pct(tot_r, tot_d), len(a["days"])))
    o.append("")
    o.append("**The per-day spread sits beside every window figure, and it is not decoration.** "
             "A window ratio is an average, and DECISION S90-3 put average-across-a-boundary in "
             "the GRAVEYARD after a published token figure proved reproducible from no window at "
             "all. Where min and max sit far apart the window figure describes no day that "
             "happened, and 6.4 is the row-by-row record.")
    o.append("")
    fell_back = sorted(f for f, r in rows.items() if r["attribution"] == "created")
    o.append("**Attribution.** A run is evidence about the SLOT it served, not about the day it "
             "started on. Where every declared slot produced a run the slot is known exactly and "
             "the per-day figures are attributed to it. Where slots are missing no pairing "
             "exists, and the creation day is used as a fallback: %s. Under lateness a run can "
             "then cross midnight, so a fallback day can borrow a run from its neighbour; a "
             "column marked ⚠ exceeded 100%% on at least one day for that reason and is a "
             "property of the attribution, not of the system. Partial days at both ends of the "
             "window are dropped for the same reason."
             % (", ".join("`%s`" % f for f in fell_back) if fell_back else "no workflow"))
    o.append("")

    # 6.2 ------------------------------------------------------------------
    o.append("### 6.2 Slot lateness — published only where it CAN be measured")
    o.append("")
    o.append("Lateness is measured against the SLOT, never against the previous run "
             "(R-S87-6, second amendment) — and it is published **only where delivery was "
             "complete**. When every declared slot produced a run, the k-th run is the k-th "
             "slot and the lag is exact at any size. When slots are missing, no pairing is "
             "defensible and this section prints the reason instead of a number.")
    o.append("")
    o.append("**The instrument that was REJECTED, and why, because it is the obvious one:** "
             "\"distance back to the nearest declared slot at or before the run\". On a "
             "30-minute cron a slot is never more than 30 minutes behind anything, so a run "
             "365 minutes late reads as **5 minutes** late. That method is bounded by the very "
             "spacing it is supposed to be independent of, and it returns its smallest possible "
             "answer exactly where the truth is largest. The generator's control probe "
             "re-proves this on every run: it builds a 365-minute lag on a 30-minute cron and "
             "asserts the nearest-slot number understates it while ordered matching does not.")
    o.append("")
    if band is None:
        o.append("**NOT MEASURABLE ANYWHERE in this window** — no workflow delivered every "
                 "declared slot, so no band is derived and no lateness figure is published.")
    else:
        o.append("Derived band: **%d min** (%.1f h) — the maximum over the %d workflow(s) with "
                 "complete delivery: %s. Compare against R-S87-6's recorded band; do not "
                 "recall one."
                 % (band, band / 60.0, len(a["consistent"]),
                    ", ".join("`%s`" % f for f in a["consistent"])))
    o.append("")
    o.append("| workflow | min slot spacing | lateness | median | p90 | max |")
    o.append("|---|---|---|---|---|---|")
    for f, r in sorted(rows.items()):
        sp = "—" if r["spacing"] is None else "%d min" % r["spacing"]
        if r["measurable"]:
            L = r["late"]
            o.append("| `%s` | %s | measured | %d min | %d min | %d min |"
                     % (f, sp, quant(L, 0.5), quant(L, 0.9), L[-1]))
        else:
            o.append("| `%s` | %s | **NOT MEASURABLE** — %s | — | — | — |" % (f, sp, r["why"]))
    o.append("")

    # 6.3 ------------------------------------------------------------------
    o.append("### 6.3 Outcome distribution of the runs that DID happen")
    o.append("")
    kinds = sorted({k for r in rows.values() for k in r["outcomes"]})
    o.append("| workflow | " + " | ".join(kinds) + " |")
    o.append("|---" * (len(kinds) + 1) + "|")
    for f, r in sorted(rows.items()):
        o.append("| `%s` | " % f + " | ".join(str(r["outcomes"].get(k, 0)) for k in kinds) + " |")
    o.append("")
    o.append("**A green conclusion says the job exited zero. It does not say the slot fired, and "
             "6.1 is where that question is answered.**")
    o.append("")

    # 6.4 ------------------------------------------------------------------
    o.append("### 6.4 Delivery by day")
    o.append("")
    o.append("| day | " + " | ".join("`%s`" % f.replace(".yml", "") for f in sorted(rows)) + " |")
    o.append("|---" * (len(rows) + 1) + "|")
    for i, d in enumerate(a["days"]):
        cells = []
        for f in sorted(rows):
            _, dec, got = rows[f]["per_day"][i]
            cells.append("%d/%d" % (got, dec) if dec else "—")
        o.append("| %s | " % d + " | ".join(cells) + " |")
    o.append("")

    # 6.5 ------------------------------------------------------------------
    o.append("### 6.5 What §6 does not answer")
    o.append("")
    o.append("- **Why** a slot did not fire. This section measures delivery; it does not "
             "diagnose the scheduler.")
    o.append("- **Job level.** `gni_mad.yml` carries both the debate and the grounding-watch "
             "and they are separable only by reading each run's jobs (one API call per run). "
             "This generator is workflow-level by design; the job-level split is filed, not "
             "silently skipped.")
    o.append("- **What calls what.** Section 5.")
    o.append("- **A known edge, disclosed here at ship time rather than found later.** The "
             "pairing in 6.2 compares slots on complete days against runs created on those same "
             "days. When lateness is large enough to push a slot's run past midnight "
             "consistently, the two sets disagree at the window edges and the pairing REFUSES "
             "even though delivery was complete -- measured deliberately against a synthetic "
             "12-hour uniform lag, which returns \"a run BEFORE its slot at the window edge\". "
             "The failure direction is safe: the section says NOT MEASURABLE instead of "
             "publishing a wrong lag. Widening the run collection past the window end without "
             "letting the previous day's runs leak in is the fix, and it is filed, not done.")
    truncated = [f for f, r in rows.items() if r["truncated"]]
    if truncated:
        o.append("- **Fetch truncation.** %s hit the %d-run fetch limit. The window above is "
                 "already bounded so that every workflow covers it, so the figures stand — but "
                 "a longer window needs a larger limit."
                 % (", ".join("`%s`" % f for f in sorted(truncated)), snap["harvest_limit"]))
    o.append("")
    return "\n".join(o)


def splice(src_text: str, section: str) -> str:
    lines = src_text.splitlines()
    start = end = None
    for i, ln in enumerate(lines):
        if start is None and ln.startswith("## §6"):
            start = i
        elif start is not None and ln.startswith("## §7"):
            end = i
            break
    if start is None or end is None:
        raise ValueError("could not locate the §6..§7 boundary in the source document")
    return "\n".join(lines[:start] + section.splitlines() + lines[end:]) + "\n"


# --------------------------------------------------------------------------- main

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--session", type=int, required=True,
                    help="session number; names the snapshot AND the output document")
    ap.add_argument("--harvest", action="store_true", help="call gh and write the snapshot")
    ap.add_argument("--snapshot", default=None)
    ap.add_argument("--src", default=None)
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args(argv)

    fails, n_probe = control_probe()
    if fails:
        print("CONTROL PROBE FAILED -- nothing written. The instrument is wrong, "
              "not the repo:", file=sys.stderr)
        for f in fails:
            print("  - " + f, file=sys.stderr)
        return 2
    print("CONTROL PROBE: %d/%d pass (cron forms, weekday negatives, spacing, "
          "ordered pairing incl. the 365-min case, EOL hashing)" % (n_probe, n_probe))

    if args.harvest:
        return harvest(args.session)

    path = Path(args.snapshot) if args.snapshot else \
        DOCS / ("gni_runtime_snapshot_S%d.json" % args.session)
    if not path.is_file():
        print("MISSING: %s\nRun --harvest first." % path, file=sys.stderr)
        return 3
    raw = path.read_bytes()
    snap = json.loads(raw.decode("utf-8-sig"))
    if snap.get("schema") != SCHEMA:
        print("SCHEMA MISMATCH: snapshot %r, this tool speaks %r"
              % (snap.get("schema"), SCHEMA), file=sys.stderr)
        return 2
    try:
        a = analyse(snap)
    except ValueError as exc:
        print("REFUSING: %s" % exc, file=sys.stderr)
        return 2
    section = render(snap, a, path.name, norm_md5(raw))

    if args.stdout:
        print(section)
        return 0
    if args.src:
        src = Path(args.src)
    else:
        cands = sorted(DOCS.glob("GNI_ARCHITECTURE_S*.md"),
                       key=lambda p: int(re.sub(r"\D", "", p.stem) or 0))
        if not cands:
            print("MISSING: no GNI_ARCHITECTURE_S*.md under %s" % DOCS, file=sys.stderr)
            return 3
        src = cands[-1]
    if not src.is_file():
        print("MISSING: %s" % src, file=sys.stderr)
        return 3
    out = DOCS / ("GNI_ARCHITECTURE_S%d.md" % args.session)
    try:
        text = splice(src.read_text(encoding="utf-8"), section)
    except ValueError as exc:
        print("REFUSING: %s (source: %s)" % (exc, src), file=sys.stderr)
        return 2
    out.write_text(text, encoding="utf-8", newline="\n")
    print("SOURCE : %s" % src.name)
    print("WROTE  : %s  (%d bytes)" % (out.relative_to(ROOT), len(text)))
    print("§6 covers %d workflows over %d complete days; lateness measurable for %d of them"
          % (len(a["rows"]), len(a["days"]), sum(1 for r in a["rows"].values() if r["measurable"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
