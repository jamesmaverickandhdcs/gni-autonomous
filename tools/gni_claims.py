#!/usr/bin/env python3
"""tools/gni_claims.py - S107, roadmap 3 row R3-2 (absorbs item 9.21).

STAGE 1 (S107): the deterministic CANDIDATE extractor. It lists
every human-readable SENTENCE the public surface renders, verbatim, anchored at
file:line, keyed by the hash of its whitespace-normalised text.
STAGE 2 (S107): the verdict file docs/GNI_CLAIM_VERDICTS_S<N>.tsv and the
generated docs/GNI_CLAIMS_S<N>.md; the detector check labelled
`claims resolve` (C12) reads both.
STAGE 3 (S111): roadmap 4 row R4-1. The STATUS line also prints UNREVIEWED
and NUMBERS UNDERIVED (ratchet_counts); the check labelled
`unreviewed ratchet` holds them below the previous generation.

SURFACE: src/app/**/page.tsx, src/components/**/*.tsx, and the frozen White
Paper docs/GNI_WHITE_PAPER_S<N>.md (DECISION S107-2). ABSENT FROM IT, named
(R-S106-4): layout.tsx, API routes, and runtime strings that come from the DB.

  python tools/gni_claims.py --candidates [root]   one TSV row per candidate
  python tools/gni_claims.py --summary [root]      counts and tiers
  python tools/gni_claims.py --todo [path-part]    manual units with no verdict
  python tools/gni_claims.py --write <session>     generate docs/GNI_CLAIMS_S<N>.md

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
# S111 (roadmap 4, finding "JSX text that touches a {expression} escapes the harvest"):
# JSX_TEXT_RE refuses any run holding a brace, so "Short Focus predictions are verified
# after {n} days." was never a claim - 60 such sentences on 20 pages, measured S111.
# A second pass takes runs WITH balanced {expressions} (two levels of nesting) and
# rewrites each as a template interpolation ${...}, which is_machine, sentences and
# tier already read as code around a literal. Runs that open with '=' or carry an
# object-literal shape are TypeScript (a generic's '>' then '= {...}'), not JSX text.
# Fixture families 82-84.
_BR = r"\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}"
JSX_BRACE_RUN_RE = re.compile(r">((?:[^<>{}]|" + _BR + r")*)<")
JSX_EXPR_RE = re.compile(_BR)
INTERP_RE = re.compile(r"\$" + _BR)
OBJ_SHAPE_RE = re.compile(r"""['"`]\s*[,:}\])]|[,{]\s*\w+\s*:\s*['"`]""")
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
    # S111: split on a copy whose ${...} interpolations are masked, so the '?' of
    # `${a ? 'x' : 'y'}` does not end a sentence; cut the raw text at the same
    # offsets. A raw without interpolations splits exactly as before.
    masked = INTERP_RE.sub(lambda m: "_" * len(m.group(0)), raw)
    out, start = [], 0
    bounds = [(m.start(), m.end()) for m in SENT_RE.finditer(masked)] + [(len(raw), len(raw))]
    for s, e in bounds:
        part = raw[start:s]
        lead = len(part) - len(part.lstrip())
        if part.strip():
            out.append((start + lead, norm(part)))
        start = e
    return out


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def tsx_candidates(path, rel):
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8-sig", "replace").replace("\r\n", "\n")
    out = []
    taken = []
    for m in JSX_TEXT_RE.finditer(text):
        t = m.group(1)
        if norm(t) and not is_machine(t):
            for off, sent in sentences(t):
                if not is_machine(sent):
                    out.append((rel, line_of(text, m.start(1) + off), "jsx", sent))
        taken.append((m.start(1), m.end(1)))
    for m in JSX_BRACE_RUN_RE.finditer(text):
        t = m.group(1)
        if "{" not in t:
            continue  # the brace-free run JSX_TEXT_RE already took
        lit = JSX_EXPR_RE.sub(" ", t)
        if not re.search(r"[A-Za-z]", lit) or lit.lstrip().startswith("=") or OBJ_SHAPE_RE.search(lit):
            continue
        t = JSX_EXPR_RE.sub(lambda e: "$" + e.group(0), t)
        if norm(t) and not is_machine(t):
            for off, sent in sentences(t):
                if not is_machine(sent):
                    # offsets index the rewritten run; each '$' added before `off`
                    # shifts it by one, so count them back out for the line number
                    out.append((rel, line_of(text, m.start(1) + off - t[:off].count("${")
                                         + m.group(1)[:off].count("${")), "jsx", sent))
        # not added to `taken`: string literals inside the {expressions} stay claims
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


# TIERS (DECISION S107-3). A TSX unit gets a verdict BY RULE in two cases, and
# by a recorded human/AI verdict otherwise. The White Paper is always manual.
#   DATA by rule: the unit is a fragment of JavaScript the JSX regex caught.
#   UI by rule:   fewer than 4 words AND no CLAIM_LEXICON hit.
# LIMIT, written down: the lexicon is hand-made. A claim of under 4 words with
# no lexicon word in it is filed UI by rule - the short end of a keyword
# filter's blind spot. The fixture carries that case as a known limit.
# S111: `\)\.` matched every sentence that closes a parenthesis and then ends
# ("... (SUM).") and filed it DATA by rule, so 24 prose sentences were never
# harvested as claims. A method call after a paren is `).name`, so a letter,
# `_` or `$` must follow the dot (fixture families 80 and 81).
CODE_RE = re.compile(r"\b(?:const|let|return|useState|useEffect|await|async|function|null|undefined)\b"
                     r"|=>|\)\.(?=[A-Za-z_$])|\.length|&&|\|\||\?\s*['\"`]|===|!==|<div|</")
CLAIM_LEXICON = re.compile(
    r"\b(?:daily|twice|hourly|weekly|real[- ]?time|24/7|always|never|every|autonomous\w*|"
    r"automatic\w*|self[- ]\w+|minutes?|min|hours?|interval|frequency|free|forever|live|"
    r"continuous\w*|instant\w*|verified|accura\w*|zero|no human|guarantee\w*|first|only|"
    r"open[- ]source|unlimited|all)\b|%|\$|\d", re.I)


def tier(kind, text):
    """'manual', or the verdict a rule gives: 'DATA' / 'UI'."""
    if kind == "wp":
        return "manual"
    # S111: judge the literal around ${...} interpolations, as is_machine does - an
    # `&&` inside `${a && b}` is the expression's code, not the sentence's.
    lit = INTERP_RE.sub(" ", text)
    if CODE_RE.search(lit):
        return "DATA"
    if len(WORD_RE.findall(lit)) < 4 and not CLAIM_LEXICON.search(lit):
        return "UI"
    return "manual"


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
        # EOL-normalised: a Windows checkout (and the fixture, which writes in
        # text mode) gives CRLF, and "---\r" is not the body marker.
        lines = fh.read().decode("utf-8").replace("\r\n", "\n").split("\n")
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


VERDICT_RE = re.compile(r"^GNI_CLAIM_VERDICTS_S(\d+)\.tsv$")


def verdict_keys(root):
    docs = os.path.join(root, "docs")
    gens = [(int(m.group(1)), n) for n in os.listdir(docs) for m in [VERDICT_RE.match(n)] if m]
    if not gens:
        return set()
    with open(os.path.join(docs, max(gens)[1]), "rb") as fh:
        lines = fh.read().decode("utf-8").split("\n")
    return {ln.split("\t", 1)[0] for ln in lines if ln and not ln.startswith("#")}


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


CLAIMS_RE = re.compile(r"^GNI_CLAIMS_S(\d+)\.md$")
VERDICTS = ("CLAIM", "DATA", "UI")
KINDS = ("STATE", "PROMISE", "MIXED")
STATUSES = ("SUPPORTED", "DEFEATED", "UNMEASURED")
ID_RE = re.compile(r"^CLM-\d{3,}$")


def live(root, regex, what):
    docs = os.path.join(root, "docs")
    gens = [(int(m.group(1)), n) for n in os.listdir(docs) for m in [regex.match(n)] if m]
    if not gens:
        raise InstrumentError("no %s under docs/" % what)
    return os.path.join(docs, max(gens)[1])


def norm_md5(path):
    with open(path, "rb") as fh:
        return hashlib.md5(fh.read().replace(b"\r\n", b"\n")).hexdigest()


def load_verdicts(root):
    """{key: (verdict, kind, id, text)}. Every row is validated: a key that
    is not the hash of its own text, an unknown verdict, a CLAIM without a
    kind or an id, or an id used twice halts the tool - a verdict file that
    cannot be trusted is not read as a partial one."""
    path = live(root, VERDICT_RE, "claim verdict file")
    with open(path, "rb") as fh:
        lines = fh.read().decode("utf-8").replace("\r\n", "\n").split("\n")
    out, ids = {}, set()
    for n, ln in enumerate(lines, 1):
        if not ln or ln.startswith("#"):
            continue
        parts = ln.split("\t")
        if len(parts) != 5:
            raise InstrumentError("verdict row %d has %d columns, not 5" % (n, len(parts)))
        k, v, kind, cid, text = parts
        if key_of(text) != k:
            raise InstrumentError("verdict row %d: key %s is not the hash of its text" % (n, k))
        if v not in VERDICTS:
            raise InstrumentError("verdict row %d: unknown verdict %r" % (n, v))
        if v == "CLAIM":
            if kind not in KINDS or not ID_RE.match(cid) or cid in ids:
                raise InstrumentError("verdict row %d: CLAIM needs a kind and an unused id" % n)
            ids.add(cid)
        elif kind != "-" or cid != "-":
            raise InstrumentError("verdict row %d: only a CLAIM carries a kind or an id" % n)
        if k in out:
            raise InstrumentError("verdict row %d: key %s appears twice" % (n, k))
        out[k] = (v, kind, cid, text)
    if not out:
        raise InstrumentError("verdict file has no rows: " + path)
    return path, out


def build(root):
    """The claim set the tree and the verdicts imply, plus what is missing."""
    vpath, verdicts = load_verdicts(root)
    rows, todo, seen = [], [], set()
    for rel, ln, kind, t in candidates(root):
        k = key_of(t)
        if tier(kind, t) == "manual" and k not in verdicts:
            todo.append((rel, ln, t))
            continue
        v = verdicts.get(k)
        if v and v[0] == "CLAIM" and (rel, ln, t) not in seen:
            seen.add((rel, ln, t))
            rows.append((v[2], v[1], rel, ln, t))
    rows.sort(key=lambda r: (int(r[0][4:]), r[2], r[3]))
    return vpath, rows, todo


BIND_RE = re.compile(r"^GNI_CLAIM_BINDINGS_S(\d+)\.tsv$")


def load_bindings(root, claim_text, minted):
    """{id: [(fitness, fragment)] or [('UNMEASURED', reason)]}. Validated: a
    binding to an id that is not a claim, an unknown fitness id or reason, a
    fragment that is not verbatim in its claim, or UNMEASURED mixed with a
    fitness row halts the tool. Every claim having a row is C13's to judge."""
    import gni_fitness as gf
    path = live(root, BIND_RE, "claim binding file")
    with open(path, "rb") as fh:
        lines = fh.read().decode("utf-8").replace("\r\n", "\n").split("\n")
    out = {}
    for n, ln in enumerate(lines, 1):
        if not ln or ln.startswith("#"):
            continue
        parts = ln.split("\t")
        if len(parts) != 3:
            raise InstrumentError("binding row %d has %d columns, not 3" % (n, len(parts)))
        cid, fid, arg = parts
        if cid not in minted:
            raise InstrumentError("binding row %d: %s was never minted as a claim id" % (n, cid))
        if cid not in claim_text:
            continue   # a retired claim: its text left the surface; C12 sees that
        if fid == "UNMEASURED":
            if arg not in gf.UNMEASURED_REASONS:
                raise InstrumentError("binding row %d: unknown reason %r" % (n, arg))
        elif fid not in gf.FITNESS:
            raise InstrumentError("binding row %d: unknown fitness function %s" % (n, fid))
        elif arg not in claim_text[cid]:
            raise InstrumentError("binding row %d: fragment %r is not in %s's text" % (n, arg, cid))
        out.setdefault(cid, []).append((fid, arg))
    for cid, rows in out.items():
        if any(f == "UNMEASURED" for f, _ in rows) and len(rows) > 1:
            raise InstrumentError("%s is UNMEASURED and also bound" % cid)
    return path, out


def statuses(root, ids_text):
    """{id: (status, evidence)} for every claim id given; BLANK when unbound.
    DEFEATED if any bound fitness function defeats it, SUPPORTED if all bear
    it out, UNMEASURED when declared so (SACM needsSupport)."""
    import gni_fitness as gf
    _, verdicts = load_verdicts(root)
    minted = {v[2] for v in verdicts.values() if v[0] == "CLAIM"}
    bpath, binds = load_bindings(root, ids_text, minted)
    cache, out = {}, {}
    for cid in ids_text:
        rows = binds.get(cid)
        if not rows:
            out[cid] = ("BLANK", "-")
        elif rows[0][0] == "UNMEASURED":
            out[cid] = ("UNMEASURED", rows[0][1])
        else:
            res = []
            for fid, frag in rows:
                try:
                    st, claimed, measured = gf.derive(root, fid, frag, cache)
                except gf.FitnessError as exc:
                    raise InstrumentError("%s %s: %s" % (cid, fid, exc))
                res.append((st, "%s claims %s, measured %s" % (fid, fmt(claimed), fmt(measured))))
            st = "DEFEATED" if any(r[0] == "DEFEATED" for r in res) else "SUPPORTED"
            out[cid] = (st, "; ".join(r[1] for r in res))
    return bpath, out


# Roadmap 4 row R4-1 (S111). The two counts the ratchet holds. A reason in
# REVIEW_EXEMPT excuses a number from being derived: the claim is about the
# past (HISTORICAL) or about who made GNI (PROVENANCE), and neither is a fact
# the tree can be asked about today. RUNTIME, EXTERNAL and QUALITATIVE do not
# excuse a number - a runtime number still waits for a fitness function that
# reads a committed snapshot (ARCHITECTURE, ROADMAP 4, row R4-3).
REVIEW_EXEMPT = ("HISTORICAL", "PROVENANCE")
# S111: a number written as a word is still a number. S111's own rewrites showed
# the hole - "up to two hundred", "the newest ten", "three rounds" passed the
# digit test and so escaped NUMBERS UNDERIVED. Cardinals two..billion and
# "dozen" count; "one" does not ("no one", "one of") and neither do ordinals
# ("first"), which name a position, not a quantity. Fixture families 85-86.
NUMBER_WORDS = ("two three four five six seven eight nine ten eleven twelve thirteen fourteen "
                "fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty "
                "seventy eighty ninety hundred thousand million billion dozen").split()
NUMBER_RE = re.compile(r"\d|\b(?:%s)\b" % "|".join(NUMBER_WORDS), re.I)
# S112 (DECISION S112-2): an HTML character reference (&#9888; &#x1F4B0;) is how a page
# writes a symbol, and the reader sees the symbol, never its digits. Until S112 the
# warning sign of CLM-373 and the money bag of CLM-1094 each sat in NUMBERS UNDERIVED
# on their markup alone. Removed before the test, as an interpolation is; a digit the
# reader sees - in a name, a version, a date - still counts. Fixture families 87-88.
CHARREF_RE = re.compile(r"&#(?:\d+|[xX][0-9A-Fa-f]+);")


def ratchet_counts(locations):
    """(UNREVIEWED, NUMBERS UNDERIVED), each a count of DISTINCT claim ids.
    `locations`: (id, kind, rel, text, status, evidence), one per place a claim
    appears - the claims document's rows, or the tree's rows with their derived
    status. Ids, never rows: a claim on three pages is one claim to review, and
    the binding file keeps rows for retired claims (S110 measured 427 rows for
    415 claims). UNREVIEWED: UNMEASURED with reason UNREVIEWED. NUMBERS
    UNDERIVED: a STATE or MIXED claim with a location under src/, a digit in
    its text, not SUPPORTED, and not excused by a reason in REVIEW_EXEMPT. A
    digit inside a name (SHA-256, L7, PHI-003) counts: the definition is the
    one roadmap 4 published with 139 at S110, and it is not narrowed here. S111
    WIDENED it to cardinal number words (NUMBER_RE); C18 re-derives the previous
    generation with the same function, so the comparison stays like for like.
    A digit inside a ${...} interpolation is the code's (a fallback `|| 14`), not
    the sentence's, and does not count; nor does one inside an HTML character
    reference (S112), which the reader sees as a symbol."""
    unrev, under = set(), set()
    for cid, kind, rel, text, status, evidence in locations:
        if status == "UNMEASURED" and evidence == "UNREVIEWED":
            unrev.add(cid)
        if (kind in ("STATE", "MIXED") and rel.startswith("src/")
                and NUMBER_RE.search(CHARREF_RE.sub(" ", INTERP_RE.sub(" ", text)))
                and status != "SUPPORTED"
                and not (status == "UNMEASURED" and evidence in REVIEW_EXEMPT)):
            under.add(cid)
    return len(unrev), len(under)


def fmt(v):
    return "+".join(v) if isinstance(v, list) else str(v)


def cell(text):
    return text.replace("\\", "\\\\").replace("|", "\\|")


def uncell(text):
    return re.sub(r"\\(.)", r"\1", text)


def render(root, session):
    vpath, rows, todo = build(root)
    if todo:
        raise InstrumentError("%d manual units have no verdict; first: %s:%d" % (
            len(todo), todo[0][0], todo[0][1]))
    ids, texts = {}, {}
    for cid, kind, _, _, t in rows:
        ids[cid] = kind
        texts[cid] = t
    by = {k: sum(v == k for v in ids.values()) for k in KINDS}
    files = len({r[2] for r in rows})
    vrel = os.path.relpath(vpath, root).replace(os.sep, "/")
    bpath, st = statuses(root, texts)
    blank = [c for c, v in st.items() if v[0] == "BLANK"]
    if blank:
        raise InstrumentError("%d claims have no binding row; first %s" % (len(blank), blank[0]))
    sc = {k: sum(v[0] == k for v in st.values()) for k in STATUSES}
    measured = sc["SUPPORTED"] + sc["DEFEATED"]
    brel = os.path.relpath(bpath, root).replace(os.sep, "/")
    unrev, under = ratchet_counts((cid, kind, rel, t, st[cid][0], st[cid][1])
                                  for cid, kind, rel, _, t in rows)
    head = [
        "# GNI CLAIMS -- S%d" % session,
        "",
        "GENERATED by `tools/gni_claims.py`. Do not hand-edit; the next run overwrites it.",
        "No clock is written into this file, so an unchanged input reproduces it byte-identically.",
        "",
        "A CLAIM is a sentence on GNI's public surface that states something about GNI a reader",
        "could hold GNI to (DECISION S107-1; ISO/IEC/IEEE 15026-2:2022, assurance case). One id per",
        "claim; one row per place it appears. Roadmap 3 row R3-2. Status is row R3-3's, not this file's.",
        "",
        "STAMP verdicts `%s` md5 `%s` (EOL-normalised) -- **%d claims** (%d STATE, %d PROMISE, "
        "%d MIXED) at **%d locations** in %d files; 0 unclassified."
        % (vrel, norm_md5(vpath), len(ids), by["STATE"], by["PROMISE"], by["MIXED"], len(rows), files),
        "",
        "STATUS bindings `%s` md5 `%s` (EOL-normalised) -- **COVERAGE %d/%d = %.1f%%** "
        "(%d SUPPORTED, %d DEFEATED, %d UNMEASURED); **UNREVIEWED %d**, **NUMBERS UNDERIVED %d** "
        "- a ratchet: neither may exceed what the previous claims generation derives (roadmap 4 "
        "row R4-1). Status is DERIVED by `tools/gni_fitness.py`, "
        "never typed (roadmap 3 row R3-3; SACM: UNMEASURED = needsSupport, DEFEATED = defeated)."
        % (brel, norm_md5(bpath), measured, len(ids), 100.0 * measured / len(ids),
           sc["SUPPORTED"], sc["DEFEATED"], sc["UNMEASURED"], unrev, under),
        "",
        "| id | kind | status | evidence | where | claim |",
        "|---|---|---|---|---|---|",
    ]
    body = ["| %s | %s | %s | %s | `%s:%d` | %s |" % (
        cid, kind, st[cid][0], cell(st[cid][1]), rel, ln, cell(t))
        for cid, kind, rel, ln, t in rows]
    return "\n".join(head + body) + "\n"


STAMP_RE = re.compile(r"^STAMP verdicts `([^`]+)` md5 `([0-9a-f]{32})` \(EOL-normalised\) -- "
                      r"\*\*(\d+) claims\*\* .* at \*\*(\d+) locations\*\*", re.M)
ROW_RE = re.compile(r"^\| (CLM-\d+) \| (STATE|PROMISE|MIXED) \| (\w+) \| ((?:[^|\\]|\\.)*) \| "
                    r"`([^`]+):(\d+)` \| (.*) \|$")
STATUS_RE = re.compile(r"^STATUS bindings `([^`]+)` md5 `([0-9a-f]{32})` \(EOL-normalised\) -- "
                       r"\*\*COVERAGE (\d+)/(\d+) = [\d.]+%\*\* \((\d+) SUPPORTED, (\d+) DEFEATED, "
                       r"(\d+) UNMEASURED\)", re.M)


def parse_doc(path):
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8").replace("\r\n", "\n")
    m = STAMP_RE.search(text)
    if not m:
        raise InstrumentError("no STAMP line in " + path)
    rows = []
    for ln in text.split("\n"):
        r = ROW_RE.match(ln)
        if r:
            rows.append((r.group(1), r.group(2), r.group(5), int(r.group(6)), uncell(r.group(7)),
                         r.group(3), uncell(r.group(4))))
    return m.group(1), m.group(2), int(m.group(3)), int(m.group(4)), rows


def parse_status(path):
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8").replace("\r\n", "\n")
    m = STATUS_RE.search(text)
    if not m:
        raise InstrumentError("no STATUS line in " + path)
    g = m.groups()
    return g[0], g[1], tuple(int(x) for x in g[2:])


RATCHET_RE = re.compile(r"^STATUS bindings .*?\*\*UNREVIEWED (\d+)\*\*, "
                        r"\*\*NUMBERS UNDERIVED (\d+)\*\*", re.M)


def parse_ratchet(path):
    """(UNREVIEWED, NUMBERS UNDERIVED) as the document PRINTS them, or None for
    a document written before R4-1 (S110 and earlier). None is not zero."""
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8").replace("\r\n", "\n")
    m = RATCHET_RE.search(text)
    return (int(m.group(1)), int(m.group(2))) if m else None


def previous(root, regex, current):
    """The highest-numbered generation BELOW `current` in the same family, or
    None. Chosen by session number, never by position (R-S92-2). A session
    that writes no claims document leaves the live one live, so its previous
    generation does not move and the ratchet cannot be reset by skipping one."""
    m = regex.match(os.path.basename(current))
    if not m:
        raise InstrumentError("%s is not in its family" % current)
    docs = os.path.join(root, "docs")
    gens = [(int(g.group(1)), n) for n in os.listdir(docs) for g in [regex.match(n)]
            if g and int(g.group(1)) < int(m.group(1))]
    return os.path.join(docs, max(gens)[1]) if gens else None


def _unjsx(text):
    """The source spelling of a harvested JSX brace run: each `${` the harvester
    wrote for a JSX {expression} back to `{`, keeping the `${` of a template
    literal (inside backticks) as written."""
    out, in_tick, i = [], False, 0
    while i < len(text):
        ch = text[i]
        if ch == "`":
            in_tick = not in_tick
        if ch == "$" and text[i + 1:i + 2] == "{" and not in_tick:
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def resolves(root, rel, line, text):
    """Independent of the extractor: the claim's first word is on the line,
    and the whole claim is found from that line on (a JSX run may wrap)."""
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        return False
    with open(path, "rb") as fh:
        lines = fh.read().decode("utf-8-sig", "replace").replace("\r\n", "\n").split("\n")
    if not 1 <= line <= len(lines):
        return False
    window = norm(" ".join(lines[line - 1:line + 15]))
    # S111: a JSX run with {expressions} is harvested as `${...}` (JSX_BRACE_RUN_RE);
    # the source holds `{...}`, so that spelling is tried too.
    for cand in (text, _unjsx(text)):
        if cand.split(" ")[0] in norm(lines[line - 1]) and cand in window:
            return True
    return False


def main(argv):
    mode = argv[1] if len(argv) > 1 else "--summary"
    if mode == "--write":
        if len(argv) != 3 or not argv[2].isdigit():
            print("usage: gni_claims.py --write <session>")
            return 2
        try:
            out = render(".", int(argv[2]))
        except InstrumentError as exc:
            print("INSTRUMENT ERROR: %s" % exc)
            return 2
        dst = os.path.join("docs", "GNI_CLAIMS_S%s.md" % argv[2])
        with open(dst, "wb") as fh:
            fh.write(out.encode("utf-8"))
        print("wrote %s -- %s" % (dst, [l for l in out.split("\n") if l.startswith("STAMP")][0][6:]))
        return 0
    if mode == "--todo":
        # Manual units with no verdict yet: key, first location, text.
        # Optional third arg: a path substring to work one page at a time.
        root = "."
        want = argv[2] if len(argv) > 2 else ""
        try:
            rows = candidates(root)
            done = verdict_keys(root)
        except InstrumentError as exc:
            print("INSTRUMENT ERROR: %s" % exc)
            return 2
        seen = set()
        for rel, ln, kind, t in rows:
            k = key_of(t)
            if k in seen or k in done or tier(kind, t) != "manual" or want not in rel:
                continue
            seen.add(k)
            print("%s\t%s:%d\t%s" % (k, rel, ln, t))
        return 0
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
    t = {}
    for r in rows:
        t.setdefault(key_of(r[3]), tier(r[2], r[3]))
    done = verdict_keys(root)
    man = [k for k, v in t.items() if v == "manual"]
    print("  tiers: DATA by rule %d, UI by rule %d, manual %d (verdicts %d, todo %d)" % (
        sum(v == "DATA" for v in t.values()), sum(v == "UI" for v in t.values()),
        len(man), sum(k in done for k in man), sum(k not in done for k in man)))
    for k in sorted(by):
        print("  %-4s %d (unique %d)" % (k, len(by[k]), len({key_of(r[3]) for r in by[k]})))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
