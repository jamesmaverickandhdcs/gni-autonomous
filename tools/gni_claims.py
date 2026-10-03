#!/usr/bin/env python3
"""tools/gni_claims.py - S107, roadmap 3 row R3-2 (absorbs item 9.21).

STAGE 1 (this file, S107): the deterministic CANDIDATE extractor. It lists
every human-readable SENTENCE the public surface renders, verbatim, anchored at
file:line, keyed by the hash of its whitespace-normalised text. Stage 2 adds
the verdict file and generates docs/GNI_CLAIMS_S<N>.md; the detector check
labelled `claims resolve` reads both.

SURFACE: src/app/**/page.tsx, src/components/**/*.tsx, and the frozen White
Paper docs/GNI_WHITE_PAPER_S<N>.md (DECISION S107-2). ABSENT FROM IT, named
(R-S106-4): layout.tsx, API routes, and runtime strings that come from the DB.

  python tools/gni_claims.py --candidates [root]   one TSV row per candidate
  python tools/gni_claims.py --summary [root]      counts only

stdlib only (item 6.9). No git history (fetch-depth 1).
"""
import glob
import hashlib
import os
import re
import sys

PAGE_GLOBS = ("src/app/**/page.tsx", "src/components/**/*.tsx")
WP_RE = re.compile(r"^GNI_WHITE_PAPER_S(\d+)\.md$")
WP_BODY_MARK = "---"

# Attribute values that are machinery, never prose a reader sees.
MACHINE_ATTR_RE = re.compile(
    r"\b(?:className|href|src|key|id|type|style|rel|target|method|role|htmlFor|"
    r"viewBox|fill|stroke|d|xmlns|strokeWidth|strokeLinecap|strokeLinejoin)\s*=\s*\{?\s*$")
JSX_TEXT_RE = re.compile(r">([^<>{}]*[A-Za-z][^<>{}]*)<")
STR_RE = re.compile(r"'((?:[^'\\\n]|\\.)*)'|\"((?:[^\"\\\n]|\\.)*)\"|`((?:[^`\\]|\\.)*)`")
WORD_RE = re.compile(r"[A-Za-z]{2,}")
# A literal with no space that looks like code, a path, a URL, a class list
# or an identifier is machinery.
MACHINE_TOKEN_RE = re.compile(
    r"^(?:[\w./:@#?&=%+-]*[/._:@#=][\w./:@#?&=%+-]*|[a-z]+(?:[A-Z][a-z0-9]*)+|[a-z0-9_]+|[A-Z0-9_]+)$")
TW_RE = re.compile(r"(?:^|\s)-?(?:[a-z]+:)*(?:text|bg|p[xytrbl]?|m[xytrbl]?|flex|grid|gap|w|h|"
                   r"min|max|rounded|border|shadow|font|leading|tracking|items|justify|space|"
                   r"overflow|opacity|ring|hover|transition|duration|z|top|left|right|bottom|"
                   r"inset|col|row|truncate|block|inline|hidden|relative|absolute|fixed|"
                   r"sticky|cursor|select|whitespace|divide|animate|from|to|via)(?:-[\w./\[\]%#]+)*(?=\s|$)")


class InstrumentError(Exception):
    pass


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


def key_of(text):
    return hashlib.sha1(norm(text).encode("utf-8")).hexdigest()[:10]


def is_machine(text):
    # Interpolations are code; judge the literal around them.
    t = norm(re.sub(r"\$\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", " ", text))
    if not WORD_RE.search(t):
        return True
    if " " not in t and MACHINE_TOKEN_RE.match(t):
        return True
    toks = t.split(" ")
    if all(TW_RE.fullmatch(" " + x) or TW_RE.match(x) and TW_RE.match(x).end() == len(x) for x in toks):
        return True
    if len(toks) > 1 and sum(bool(TW_RE.fullmatch(" " + x)) or bool(TW_RE.match(x)) for x in toks) == len(toks):
        return True
    return False


# DECISION S107-4: the harvest unit is the SENTENCE. Measured S107: 61 of the
# White Paper's 200 paragraph lines hold more than one sentence, and roadmap 3
# row R3-3 derives ONE status per claim - a paragraph that is half true cannot
# carry one. A sentence is the smallest unit that stays VERBATIM. LIMIT,
# written down: one sentence can still hold several claims; splitting it
# further would need words that are not in the source.
SENT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")


def sentences(raw):
    """[(offset_in_raw, sentence)] - offsets index the UNnormalised text, so a
    sentence on the third line of a JSX run is anchored on that line."""
    out, pos = [], 0
    for part in SENT_RE.split(raw):
        at = raw.index(part, pos)
        pos = at + len(part)
        lead = len(part) - len(part.lstrip())
        if part.strip():
            out.append((at + lead, norm(part)))
    return out


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def tsx_candidates(path, rel):
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8-sig", "replace")
    out = []
    taken = []
    for m in JSX_TEXT_RE.finditer(text):
        t = m.group(1)
        if norm(t) and not is_machine(t):
            for off, sent in sentences(t):
                if not is_machine(sent):
                    out.append((rel, line_of(text, m.start(1) + off), "jsx", sent))
        taken.append((m.start(1), m.end(1)))
    for m in STR_RE.finditer(text):
        s, e = m.span()
        if any(a <= s < b for a, b in taken):
            continue
        before = text[max(0, s - 40):s]
        if MACHINE_ATTR_RE.search(before) or re.search(r"\b(?:import|from|require)\s*\(?\s*$", before):
            continue
        t = next(g for g in m.groups() if g is not None)
        if t and not is_machine(t):
            for off, sent in sentences(t):
                if not is_machine(sent):
                    out.append((rel, line_of(text, s + 1 + off), "str", sent))
    return out


def wp_path(root):
    docs = os.path.join(root, "docs")
    gens = [(int(m.group(1)), n) for n in os.listdir(docs) for m in [WP_RE.match(n)] if m]
    if not gens:
        raise InstrumentError("no frozen White Paper under docs/")
    return os.path.join(docs, max(gens)[1])


def wp_candidates(root):
    path = wp_path(root)
    rel = os.path.relpath(path, root).replace(os.sep, "/")
    with open(path, "rb") as fh:
        lines = fh.read().decode("utf-8").split("\n")
    if WP_BODY_MARK not in lines:
        raise InstrumentError("White Paper body marker not found: " + rel)
    start = lines.index(WP_BODY_MARK) + 1
    out = []
    for i, ln in enumerate(lines):
        if i < start or not norm(ln) or not WORD_RE.search(ln):
            continue
        # A table row is one unit: its cells only mean something together.
        units = [(0, norm(ln))] if ln.startswith("|") else sentences(ln)
        out += [(rel, i + 1, "wp", u) for _, u in units if WORD_RE.search(u)]
    return out


def candidates(root):
    out = []
    files = sorted({p for g in PAGE_GLOBS for p in glob.glob(os.path.join(root, g), recursive=True)})
    if not files:
        raise InstrumentError("no page or component files under " + root)
    for p in files:
        out += tsx_candidates(p, os.path.relpath(p, root).replace(os.sep, "/"))
    out += wp_candidates(root)
    if not out:
        raise InstrumentError("empty harvest")
    return out


def main(argv):
    mode = argv[1] if len(argv) > 1 else "--summary"
    root = argv[2] if len(argv) > 2 else "."
    try:
        rows = candidates(root)
    except InstrumentError as exc:
        print("INSTRUMENT ERROR: %s" % exc)
        return 2
    if mode == "--candidates":
        for rel, ln, kind, t in rows:
            print("%s\t%s:%d\t%s\t%s" % (key_of(t), rel, ln, kind, t))
        return 0
    by = {}
    for r in rows:
        by.setdefault(r[2], []).append(r)
    uniq = {key_of(r[3]) for r in rows}
    print("candidates %d (unique texts %d)" % (len(rows), len(uniq)))
    for k in sorted(by):
        print("  %-4s %d (unique %d)" % (k, len(by[k]), len({key_of(r[3]) for r in by[k]})))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
