#!/usr/bin/env python3
"""tools/gni_output_sample.py - S114, roadmap 5 row R5-1.

Writes docs/gni_output_sample_S<N>.json from the ONE cell the operator copied out of the Supabase
SQL Editor after running tools/gni_output_sample.sql. The cell is kept unaltered under 'harvest';
this tool only checks it and wraps it, the S112 snapshot pattern (DECISION S112-4).

It REFUSES - exit 1, nothing written - when the copy cannot be the query's whole result:
  - the cell is not one JSON object, or lacks rows / window / outputs;
  - 'rows' differs from the number of outputs (a row was lost in the copy);
  - an output's md5, computed by Postgres over its five published texts, differs from the md5
    of the texts the file holds (a character was lost or changed in the copy);
  - an output lies outside the window, ids repeat, or the order by created_at is broken;
  - the empty-field counts differ from the outputs.
--selftest builds a cell, proves it is accepted, then proves each of five damages is refused
(R-S90-1: a cert that cannot fail certifies nothing).

usage:  python tools/gni_output_sample.py --session 114 --cell ../S114_cell.txt
        python tools/gni_output_sample.py --selftest
"""
import argparse
import hashlib
import json
import os
import sys

QUERY = "tools/gni_output_sample.sql"
TEXTS = ("title", "summary", "fff_what_is_happening", "fff_honest_analysis", "fff_human_path")
EMPTY = ("summary", "fff_what_is_happening", "fff_honest_analysis", "fff_human_path")


class Refused(Exception):
    pass


def row_md5(o):
    # The query's md5(concat_ws(chr(31), coalesce(...)...)): UTF-8 bytes, unit separator 0x1F.
    return hashlib.md5("\x1f".join((o.get(k) or "") for k in TEXTS).encode("utf-8")).hexdigest()


def ts(text):
    # Postgres JSON timestamps: '2026-09-01T02:49:00.123456+00:00'; parsed, never compared as text.
    from datetime import datetime
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def query_md5(root):
    # The same EOL-normalised md5 gni_fitness.py's _db_harvest checks a query against.
    with open(os.path.join(root, QUERY), "rb") as fh:
        return hashlib.md5(fh.read().replace(b"\r\n", b"\n")).hexdigest()


def check(cell):
    """Return the parsed harvest, or raise Refused naming the first damage found."""
    try:
        h = json.loads(cell)
    except ValueError as e:
        raise Refused("the cell is not JSON (%s) - copy the cell's value as text, not a CSV row" % e)
    if not isinstance(h, dict) or not all(k in h for k in ("rows", "window", "outputs", "empty")):
        raise Refused("the cell lacks rows, window, outputs or empty")
    outs, win = h["outputs"], h["window"]
    if h["rows"] != len(outs):
        raise Refused("rows says %s, the cell holds %d outputs" % (h["rows"], len(outs)))
    if not outs:
        raise Refused("the window holds no outputs")
    t0, t1 = ts(win["from"]), ts(win["to"])
    ids, prev = set(), None
    for i, o in enumerate(outs):
        if o.get("md5") != row_md5(o):
            raise Refused("output %d (%s): md5 differs from its texts - the copy changed it" % (i, o.get("id")))
        if o["id"] in ids:
            raise Refused("output %d: id %s repeats" % (i, o["id"]))
        ids.add(o["id"])
        at = ts(o["created_at"])
        if not (t0 <= at < t1):
            raise Refused("output %d: created_at %s outside [%s, %s)" % (i, o["created_at"], win["from"], win["to"]))
        if prev is not None and at < prev:
            raise Refused("output %d: out of created_at order" % i)
        prev = at
    for k in EMPTY:
        n = sum(1 for o in outs if not (o.get(k) or "").strip())
        if h["empty"].get(k) != n:
            raise Refused("empty.%s says %s, the outputs give %d" % (k, h["empty"].get(k), n))
    return h


def write(root, session, cell, harvested_by):
    h = check(cell)
    out = os.path.join(root, "docs", "gni_output_sample_S%d.json" % session)
    if os.path.exists(out):
        raise Refused("%s exists; a revised harvest takes a new session number, not an overwrite" % out)
    doc = {
        "about": ("GNI's published report texts (title, summary, the three Freedom from Fear sections) for a "
                  "closed window, harvested by one read-only query whose result is ONE cell, kept unaltered under "
                  "'harvest'. Roadmap 5 row R5-1 (docs/GNI_ROADMAP5_SPEC_S113.md). Each output carries the md5 "
                  "Postgres computed over its texts; tools/gni_output_sample.py refused the copy unless every one "
                  "matched and 'rows' equalled the outputs."),
        "query_file": QUERY,
        "query_md5": query_md5(root),
        "harvested_by": harvested_by,
        "harvest": h,
    }
    with open(out, "wb") as fh:
        fh.write((json.dumps(doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print("WROTE %s: %d outputs, window %s to %s, %d fallback events, empty %s, query_md5 %s" % (
        os.path.relpath(out, root), h["rows"], h["window"]["from"], h["window"]["to"],
        len(h.get("fallback_events") or []), json.dumps(h["empty"]), doc["query_md5"]))


def selftest():
    def out(i, path="Stay informed; talk to someone you trust."):
        o = {"id": "id-%d" % i, "created_at": "2026-09-%02dT02:49:00+00:00" % (i + 1),
             "title": "T%d" % i, "summary": "S \u2014 %d" % i, "fff_what_is_happening": "W%d" % i,
             "fff_honest_analysis": "A%d" % i, "fff_human_path": path}
        o["md5"] = row_md5(o)
        return o

    def cell(outs):
        return {"window": {"from": "2026-08-31T09:02:39+00:00", "to": "2026-10-14T00:00:00+00:00"},
                "rows": len(outs), "outputs": outs, "fallback_events": [],
                "empty": {k: sum(1 for o in outs if not (o.get(k) or "").strip()) for k in EMPTY}}

    good = cell([out(0), out(1, ""), out(2)])
    check(json.dumps(good, ensure_ascii=False))
    print("selftest: a whole cell is ACCEPTED")
    damages = {
        "a row lost in the copy": lambda c: c["outputs"].pop(),
        "a character lost in the copy": lambda c: c["outputs"][2].update(summary="S \u2014 "),
        "a row outside the window": lambda c: c["outputs"][2].update(created_at="2026-10-14T00:00:01+00:00"),
        "an empty count that lies": lambda c: c["empty"].update(fff_human_path=0),
        "a CSV-quoted copy": None,
    }
    bad = 0
    for name, hurt in damages.items():
        c = json.loads(json.dumps(good))
        if hurt is None:
            text = '"' + json.dumps(c).replace('"', '""') + '"'
        else:
            hurt(c)
            text = json.dumps(c, ensure_ascii=False)
        try:
            check(text)
            print("selftest: %s was ACCEPTED - FAIL" % name)
            bad += 1
        except Refused as e:
            print("selftest: %s REFUSED (%s)" % (name, e))
    print("selftest: %s" % ("PASS" if not bad else "FAIL"))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", type=int)
    ap.add_argument("--cell")
    ap.add_argument("--harvested-by", default="the operator (Supabase SQL Editor)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.session and a.cell):
        ap.error("--session and --cell are required")
    with open(a.cell, "rb") as fh:
        cell = fh.read().decode("utf-8-sig").strip()
    try:
        write(a.root, a.session, cell, "%s, S%d" % (a.harvested_by, a.session))
    except Refused as e:
        print("REFUSED: %s" % e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
