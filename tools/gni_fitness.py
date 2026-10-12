#!/usr/bin/env python3
"""tools/gni_fitness.py - S107, roadmap 3 row R3-3 (DECISION S107-5).

The FITNESS FUNCTIONS a claim can be bound to. Vocabulary from Ford, Parsons
and Kua, *Building Evolutionary Architectures*: a fitness function is any
mechanism performing an objective integrity assessment of some characteristic.
Status vocabulary from OMG SACM's AssertionDeclaration (needsSupport, defeated).

Each entry MEASURES the tree and PARSES the claim. A binding row names only the
claim, the fitness id and a verbatim fragment of the claim's own text; the
fitness function reads the claimed value out of that fragment with its own
parser. So neither the claimed value nor the status is ever typed by a human
(spec section 2: "no status may be typed by a human").

  SUPPORTED  - the measurement bears out the value the fragment states
               (equality for a count; a schedule holds when every named time
               is scheduled - see _scheduled)
  DEFEATED   - it does not (SACM `defeated`: invalidated by counter-evidence)
  UNMEASURED - declared in the binding file; no fitness function yet
               (SACM `needsSupport`)

LIMIT, written down: every function here measures the REPOSITORY. A claim
about what happens at runtime (cadence achieved, accuracy, cost, uptime) needs
the database or the run log, which CI cannot reach without secrets; those
claims stay UNMEASURED with reason RUNTIME until a fitness function can read a
committed snapshot of that data.

stdlib only (item 6.9). Measurements are lazy: only a bound function runs.
"""
import ast
import glob
import os
import re


class FitnessError(Exception):
    """The measurement could not be taken - an instrument error, never a status."""


INT_RE = re.compile(r"\d+")
HHMM_RE = re.compile(r"\b(\d{1,2}):(\d{2})\b")
CRON_RE = re.compile(r"cron:\s*['\"](\d+)\s+(\d+)\s")


def _first_int(fragment):
    m = INT_RE.search(fragment)
    if not m:
        raise FitnessError("no number in fragment %r" % fragment)
    return int(m.group(0))


def _ast_list_len(root, rel, name):
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise FitnessError("%s not found" % rel)
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == name for t in node.targets):
            if isinstance(node.value, (ast.List, ast.Tuple)):
                return len(node.value.elts)
    raise FitnessError("no top-level list %s in %s" % (name, rel))


def _count(root, pattern):
    return len(glob.glob(os.path.join(root, pattern), recursive=True))


# Myanmar Standard Time is UTC+06:30. Named here because a page states the
# schedule in it, and the parser must convert rather than guess.
TZ_OFFSET_MIN = (("UTC", 0), ("Myanmar", 390))


def _times_utc(fragment):
    offset = None
    for name, off in TZ_OFFSET_MIN:
        if name in fragment:
            offset = off
            break
    if offset is None:
        raise FitnessError("no known timezone in fragment %r" % fragment)
    out = set()
    for h, m in HHMM_RE.findall(fragment):
        t = (int(h) * 60 + int(m) - offset) % 1440
        out.add("%02d:%02d" % (t // 60, t % 60))
    if not out:
        raise FitnessError("no HH:MM in fragment %r" % fragment)
    return sorted(out)


def _cron(root, workflow):
    path = os.path.join(root, ".github", "workflows", workflow)
    if not os.path.isfile(path):
        raise FitnessError(".github/workflows/%s not found" % workflow)
    with open(path, "rb") as fh:
        crons = CRON_RE.findall(fh.read().decode("utf-8"))
    if not crons:
        raise FitnessError("no fixed-time cron line in %s" % workflow)
    return sorted("%02d:%02d" % (int(h), int(m)) for m, h in crons)


def _int_k(fragment):
    """'100K' -> 100000. A figure written in thousands is compared in units."""
    m = re.search(r"(\d+)\s*K\b", fragment)
    if not m:
        raise FitnessError("no <n>K figure in fragment %r" % fragment)
    return int(m.group(1)) * 1000


def _ast_int_const(root, rel, name):
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise FitnessError("%s not found" % rel)
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == name for t in node.targets):
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, int):
                return node.value.value
    raise FitnessError("no top-level integer %s in %s" % (name, rel))


LEVELS = ("CRITICAL", "HIGH", "ELEVATED", "MODERATE", "LOW")
GAP_RE = re.compile(r"\b(%s)\s+(\d+(?:\.\d+)?)\s*(min|h)\b" % "|".join(LEVELS))


def _hours(value):
    return ("%g" % value) + "h"


def _gap_claim(fragment):
    """'CRITICAL 30 min, HIGH 2 h' -> ['CRITICAL=0.5h', 'HIGH=2h']."""
    out = [lv + "=" + _hours(float(n) / 60 if unit == "min" else float(n))
           for lv, n, unit in GAP_RE.findall(fragment)]
    if not out:
        raise FitnessError("no LEVEL <n> min|h pair in fragment %r" % fragment)
    return out


def _adaptive_gaps(root):
    """The minimum gap the adaptive run enforces per level: interval_h in
    ESCALATION_MODES, adaptive_pipeline.py (AST). This table, not the frequency
    controller's, is what run_adaptive_pipeline compares hours_since against."""
    rel = "ai_engine/adaptive_pipeline.py"
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise FitnessError("%s not found" % rel)
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "ESCALATION_MODES"
                                                for t in node.targets):
            out = []
            for k, v in zip(node.value.keys, node.value.values):
                gap = [vv.value for kk, vv in zip(v.keys, v.values)
                       if getattr(kk, "value", None) == "interval_h"]
                if not gap:
                    raise FitnessError("ESCALATION_MODES[%r] has no interval_h" % k.value)
                out.append(k.value + "=" + _hours(float(gap[0])))
            return out
    raise FitnessError("no top-level ESCALATION_MODES in %s" % rel)


def _groq_refs(root):
    """Groq references in the heartbeat module (AST): imports of the groq
    package and calls to a name Groq. LIMIT, written down: imports are not
    followed - section 5 shows monitoring_pipeline imports no internal module,
    so at S111 there is nothing to follow; a new internal import moves that."""
    rel = "ai_engine/monitoring_pipeline.py"
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise FitnessError("%s not found" % rel)
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    n = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            n += sum(a.name.split(".")[0] == "groq" for a in node.names)
        elif isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] == "groq":
            n += 1
        elif isinstance(node, ast.Call) and getattr(node.func, "id", "") == "Groq":
            n += 1
    return n


def _func(root, rel, name):
    """The top-level FunctionDef `name` in `rel`, parsed (AST)."""
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise FitnessError("%s not found" % rel)
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise FitnessError("no function %s in %s" % (name, rel))


def _num(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) \
            and not isinstance(node.value, bool):
        return node.value
    raise FitnessError("expected a numeric literal at line %d" % getattr(node, "lineno", 0))


def _hash_claim(fragment):
    m = re.search(r"SHA-(\d+)", fragment)
    if not m:
        raise FitnessError("no SHA-<n> in fragment %r" % fragment)
    return int(m.group(1))


def _audit_hash(root):
    """Digest size of the audit chain: the hashlib.sha<N> call in
    audit_trail._compute_hash (AST). More than one size is an instrument error."""
    fn = _func(root, "ai_engine/analysis/audit_trail.py", "_compute_hash")
    sizes = {int(n.func.attr[3:]) for n in ast.walk(fn)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
             and re.fullmatch(r"sha\d+", n.func.attr)}
    if len(sizes) != 1:
        raise FitnessError("_compute_hash uses %d digest sizes, not one" % len(sizes))
    return sizes.pop()


def _temps_claim(fragment):
    m = re.search(r"temperatures ([\d.]+(?:(?:/|, )[\d.]+)+)", fragment)
    if not m:
        raise FitnessError("no 'temperatures a/b/c' or 'a, b, c' in fragment %r" % fragment)
    return ["%g" % v for v in sorted(float(x) for x in re.split(r"/|, ", m.group(1)))]


def _ci_temps(root):
    """Temperatures of the main pipeline's analysis: the 'temperature' value of
    _call_groq's request (the primary run) plus the list the CI loop in
    analyze() iterates (AST). Cerebras (the adaptive run) is not this path."""
    rel = "ai_engine/analysis/nexus_analyzer.py"
    prim = [_num(v) for n in ast.walk(_func(root, rel, "_call_groq")) if isinstance(n, ast.Dict)
            for k, v in zip(n.keys, n.values) if getattr(k, "value", None) == "temperature"]
    loops = [[_num(e) for e in n.iter.elts] for n in ast.walk(_func(root, rel, "analyze"))
             if isinstance(n, ast.For) and getattr(n.target, "id", "") == "temp"
             and isinstance(n.iter, (ast.List, ast.Tuple))]
    if len(set(prim)) != 1 or len(loops) != 1:
        raise FitnessError("expected one primary temperature and one CI loop, got %d and %d"
                           % (len(set(prim)), len(loops)))
    return ["%g" % v for v in sorted([float(prim[0])] + [float(x) for x in loops[0]])]


def _t_claim(fragment):
    """'t=4.303, n=3', 't=4.303 for n=3' or 'n=3' alone: whichever of the two
    the fragment states. The comparison is a subset, so a fragment naming only
    the run count is held to the run count."""
    out = ["t=%g" % float(x) for x in re.findall(r"\bt=([\d.]+)", fragment)]
    out += ["n=%d" % int(x) for x in re.findall(r"\bn=(\d+)", fragment)]
    if not out:
        raise FitnessError("no t=<x> or n=<k> in fragment %r" % fragment)
    return out


def _ci_t(root):
    """The run count the main pipeline aims for (the primary run plus the CI
    loop's temperatures, as F-CI-TEMPS reads them) and the t value
    _calculate_confidence_intervals uses for that count: the module-level
    _T95_TWO_SIDED table at df = n-1, which the function must read (AST).
    S111: was the `T if n == K else ...` expression, whose else branch gave
    every other run count the 99% normal z."""
    rel = "ai_engine/analysis/nexus_analyzer.py"
    with open(os.path.join(root, rel), "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    table = [n.value for n in tree.body if isinstance(n, ast.Assign)
             and any(getattr(t, "id", "") == "_T95_TWO_SIDED" for t in n.targets)]
    if len(table) != 1 or not isinstance(table[0], ast.Dict):
        raise FitnessError("expected one module-level _T95_TWO_SIDED dict in %s" % rel)
    t95 = {_num(k): _num(v) for k, v in zip(table[0].keys, table[0].values)}
    fn = _func(root, rel, "_calculate_confidence_intervals")
    if not any(isinstance(n, ast.Name) and n.id == "_T95_TWO_SIDED" for n in ast.walk(fn)):
        raise FitnessError("_calculate_confidence_intervals does not read _T95_TWO_SIDED")
    n = len(_ci_temps(root))
    if (n - 1) not in t95:
        raise FitnessError("_T95_TWO_SIDED has no entry for df=%d" % (n - 1))
    return ["t=%g" % float(t95[n - 1]), "n=%d" % n]


def _ci_t_two(root):
    """The t value _calculate_confidence_intervals uses when only two runs
    came back (one CI call failed): _T95_TWO_SIDED at df=1 (AST)."""
    rel = "ai_engine/analysis/nexus_analyzer.py"
    with open(os.path.join(root, rel), "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    table = [n.value for n in tree.body if isinstance(n, ast.Assign)
             and any(getattr(t, "id", "") == "_T95_TWO_SIDED" for t in n.targets)]
    if len(table) != 1 or not isinstance(table[0], ast.Dict):
        raise FitnessError("expected one module-level _T95_TWO_SIDED dict in %s" % rel)
    t95 = {_num(k): _num(v) for k, v in zip(table[0].keys, table[0].values)}
    if 1 not in t95:
        raise FitnessError("_T95_TWO_SIDED has no entry for df=1")
    return ["t=%g" % float(t95[1])]


_INSTR_RE = r"\b(SPY|GLD|USO)\b"


def _instr_claim(fragment):
    """The instruments a GPVS sentence says the direction is judged on."""
    out = sorted(set(re.findall(_INSTR_RE, fragment)))
    if not out:
        raise FitnessError("no SPY/GLD/USO in fragment %r" % fragment)
    return out


def _gpvs_dir_instr(root):
    """The instruments whose moves verify_pending_outcomes passes to its
    direction() helper - the prefix of each first argument, e.g. spy_3d -> SPY.
    A name that is not <ticker>_<window> fails the measure (AST)."""
    fn = _func(root, "ai_engine/analysis/outcome_verifier.py", "verify_pending_outcomes")
    seen = set()
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "direction" and n.args:
            name = getattr(n.args[0], "id", "")
            m = re.match(r"([a-z]{3})_\d+d$", name)
            if not m:
                raise FitnessError("direction() is passed %r, not <ticker>_<n>d" % name)
            seen.add(m.group(1).upper())
    if not seen:
        raise FitnessError("no direction() call in verify_pending_outcomes")
    return sorted(seen)


EMA_RE = (r"new = ([\d.]+) x old \+ ([\d.]+) x factor, where factor is ([\d.]+) for correct "
          r"predictions, ([\d.]+) for wrong, ([\d.]+) for partly correct")


def _ema_claim(fragment):
    m = re.search(EMA_RE, fragment)
    if not m:
        raise FitnessError("fragment %r is not the EMA sentence's grammar" % fragment)
    return ["%g" % float(x) for x in m.groups()]


def _ema(root):
    """[old coefficient, factor coefficient, correct, wrong, partly correct] from
    source_weights.update_source_weight (AST): the two products in the blended
    update, and the gpvs_factor the if / elif / else chain assigns - first
    branch correct (score >= 1.0), second partly correct, else wrong."""
    fn = _func(root, "ai_engine/analysis/source_weights.py", "update_source_weight")
    coef = {}
    for n in ast.walk(fn):
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mult) \
                and isinstance(n.right, ast.Name) and n.right.id in ("current", "gpvs_factor"):
            coef[n.right.id] = float(_num(n.left))
    chain = [n for n in ast.walk(fn) if isinstance(n, ast.If)
             and any(getattr(t, "id", "") == "gpvs_factor" for s in n.body
                     if isinstance(s, ast.Assign) for t in s.targets)]
    if len(coef) != 2 or not chain:
        raise FitnessError("update_source_weight: blended update or factor chain not found")
    top = min(chain, key=lambda n: n.lineno)
    vals = [float(_num(top.body[0].value))]
    orelse = top.orelse
    while orelse:
        node = orelse[0]
        if isinstance(node, ast.If):
            vals.append(float(_num(node.body[0].value)))
            orelse = node.orelse
        else:
            vals.append(float(_num(node.value)))
            orelse = []
    if len(vals) != 3:
        raise FitnessError("expected three gpvs_factor branches, got %d" % len(vals))
    correct, partly, wrong = vals
    return ["%g" % v for v in (coef["current"], coef["gpvs_factor"], correct, wrong, partly)]


def _bounds_claim(fragment):
    """'between 0.5 (...) and 2.0' -> both; 'up to 2.0' -> max; 'down to 0.5' -> min."""
    out = []
    m = re.search(r"between ([\d.]+)\b.*?\band ([\d.]+)", fragment)
    if m:
        out += ["min=%g" % float(m.group(1)), "max=%g" % float(m.group(2))]
    out += ["max=%g" % float(x) for x in re.findall(r"up to ([\d.]+)", fragment)]
    out += ["min=%g" % float(x) for x in re.findall(r"down to ([\d.]+)", fragment)]
    if not out:
        raise FitnessError("no bound in fragment %r" % fragment)
    return out


def _weight_bounds(root):
    """The clamp max(LO, min(x, HI)) in source_weights.update_source_weight (AST)."""
    fn = _func(root, "ai_engine/analysis/source_weights.py", "update_source_weight")
    hits = []
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "max" and len(n.args) == 2:
            inner = n.args[1]
            if isinstance(inner, ast.Call) and getattr(inner.func, "id", "") == "min":
                hits.append(["min=%g" % _num(n.args[0]), "max=%g" % _num(inner.args[1])])
    if len(hits) != 1:
        raise FitnessError("expected one max(lo, min(x, hi)) clamp, got %d" % len(hits))
    return hits[0]


def _bands_claim(fragment):
    out = ["%s>=%g" % (lv, float(n)) for lv, n in
           re.findall(r"\b(CRITICAL|HIGH|ELEVATED|MODERATE) from ([\d.]+)", fragment)]
    if not out:
        raise FitnessError("no '<LEVEL> from <n>' in fragment %r" % fragment)
    return out


def _esc_bands(root):
    """Lower bound of each escalation level: the `if final_score >= N: level =
    'X'` chain in escalation_scorer.score_escalation (AST)."""
    fn = _func(root, "ai_engine/analysis/escalation_scorer.py", "score_escalation")
    out = []
    for n in ast.walk(fn):
        if isinstance(n, ast.If) and isinstance(n.test, ast.Compare) \
                and getattr(n.test.left, "id", "") == "final_score" \
                and isinstance(n.test.ops[0], ast.GtE):
            lv = [s.value.value for s in n.body if isinstance(s, ast.Assign)
                  and any(getattr(t, "id", "") == "level" for t in s.targets)
                  and isinstance(s.value, ast.Constant)]
            if lv:
                out.append("%s>=%g" % (lv[0], _num(n.test.comparators[0])))
    if not out:
        raise FitnessError("no `if final_score >= n: level = ...` chain in score_escalation")
    return out


STATUS_CONFIG_RE = re.compile(r"const STATUS_CONFIG\b[^=]*=\s*\{(.*?)\n\}", re.S)


def _sh_states(root):
    """Keys of STATUS_CONFIG in the source-health page: the states it can show."""
    rel = "src/app/source-health/page.tsx"
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise FitnessError("%s not found" % rel)
    with open(path, "rb") as fh:
        m = STATUS_CONFIG_RE.search(fh.read().decode("utf-8"))
    if not m:
        raise FitnessError("no STATUS_CONFIG object in %s" % rel)
    keys = re.findall(r"^\s*'?([a-z][a-z-]*)'?\s*:\s*\{", m.group(1), re.M)
    if not keys:
        raise FitnessError("STATUS_CONFIG has no keys in %s" % rel)
    return len(keys)


WORD_NUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
            "eight": 8, "nine": 9, "ten": 10}


def _count_word(fragment):
    """The first count in the fragment, written as digits or as a word to ten."""
    m = re.search(r"\b(\d+|%s)\b" % "|".join(WORD_NUM), fragment)
    if not m:
        raise FitnessError("no count in fragment %r" % fragment)
    return int(m.group(1)) if m.group(1).isdigit() else WORD_NUM[m.group(1)]


def _secret_names(fragment):
    names = re.findall(r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b", fragment)
    if not names:
        raise FitnessError("no SECRET_NAME in fragment %r" % fragment)
    return sorted(set(names))


def _workflow_secrets(root):
    """Every `secrets.NAME` the workflow files read."""
    out = set()
    for path in glob.glob(os.path.join(root, ".github", "workflows", "*.yml")):
        with open(path, "rb") as fh:
            out |= set(re.findall(r"secrets\.([A-Z][A-Z0-9_]*)", fh.read().decode("utf-8")))
    if not out:
        raise FitnessError("no secrets.NAME in any workflow")
    return sorted(out)


def _src_cap(root):
    """max_per_source passed to run_funnel by the main pipeline (main.py, AST)."""
    path = os.path.join(root, "ai_engine", "main.py")
    if not os.path.isfile(path):
        raise FitnessError("ai_engine/main.py not found")
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    vals = [_num(k.value) for n in ast.walk(tree) if isinstance(n, ast.Call)
            and getattr(n.func, "id", "") == "run_funnel"
            for k in n.keywords if k.arg == "max_per_source"]
    if len(vals) != 1:
        raise FitnessError("expected one run_funnel(max_per_source=...) in main.py, got %d" % len(vals))
    return vals[0]


def _version_claim(fragment):
    """'Python 3.10+' or 'Next.js 14' -> the version as a tuple of ints."""
    m = re.search(r"(\d+(?:\.\d+)*)\+?", fragment)
    if not m:
        raise FitnessError("no version in fragment %r" % fragment)
    return tuple(int(x) for x in m.group(1).split("."))


def _at_least(claimed, measured):
    """'3.10+' holds when every measured version is at least the claimed one."""
    return all(tuple(v[:len(claimed)]) >= claimed for v in measured)


def _python_versions(root):
    """Every python-version the workflows set up (setup-python)."""
    out = []
    for path in glob.glob(os.path.join(root, ".github", "workflows", "*.yml")):
        with open(path, "rb") as fh:
            out += re.findall(r"python-version:\s*['\"]?(\d+(?:\.\d+)+)", fh.read().decode("utf-8"))
    if not out:
        raise FitnessError("no python-version in any workflow")
    # a tuple, not a list: gni_claims.fmt joins lists as strings
    return tuple(sorted({tuple(int(x) for x in v.split(".")) for v in out}))


def _next_major(root):
    """Major version of the `next` dependency in package.json."""
    import json
    path = os.path.join(root, "package.json")
    if not os.path.isfile(path):
        raise FitnessError("package.json not found")
    with open(path, "rb") as fh:
        deps = json.loads(fh.read().decode("utf-8")).get("dependencies", {})
    m = re.search(r"(\d+)", deps.get("next", ""))
    if not m:
        raise FitnessError("no next version in package.json dependencies")
    return (int(m.group(1)),)


def _major_equal(claimed, measured):
    return claimed[:1] == measured[:1]


def _py_names(fragment):
    names = re.findall(r"\b([a-z_][a-z0-9_]*\.py)\b", fragment)
    if not names:
        raise FitnessError("no <name>.py in fragment %r" % fragment)
    return sorted(set(names))


def _workflow_entrypoints(root):
    """Basenames of the python files the workflows run (`python <path>.py`)."""
    out = set()
    for path in glob.glob(os.path.join(root, ".github", "workflows", "*.yml")):
        with open(path, "rb") as fh:
            out |= {os.path.basename(x) for x in
                    re.findall(r"python3? ([\w./-]+\.py)", fh.read().decode("utf-8"))}
    if not out:
        raise FitnessError("no `python <file>.py` in any workflow")
    return sorted(out)


def _dedup_words(root):
    """How many title words the dedup key hashes: the slice bound in
    intelligence_funnel._get_dedup_key (AST)."""
    fn = _func(root, "ai_engine/funnel/intelligence_funnel.py", "_get_dedup_key")
    vals = [_num(n.slice.upper) for n in ast.walk(fn)
            if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Slice)
            and n.slice.lower is None and n.slice.upper is not None]
    if len(vals) != 1:
        raise FitnessError("expected one [:n] slice in _get_dedup_key, got %d" % len(vals))
    return vals[0]


def _sleeps_claim(fragment):
    m = re.search(r"(\d+)\s*s\b", fragment)
    if not m:
        raise FitnessError("no <n>s in fragment %r" % fragment)
    return ["%ds" % int(m.group(1))]


def _main_sleeps(root):
    """Every literal time.sleep(N) in the main pipeline (main.py, AST)."""
    path = os.path.join(root, "ai_engine", "main.py")
    if not os.path.isfile(path):
        raise FitnessError("ai_engine/main.py not found")
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    out = sorted({"%gs" % _num(n.args[0]) for n in ast.walk(tree) if isinstance(n, ast.Call)
                  and isinstance(n.func, ast.Attribute) and n.func.attr == "sleep"
                  and n.args and isinstance(n.args[0], ast.Constant)})
    if not out:
        raise FitnessError("no time.sleep(<literal>) in main.py")
    return out


def _quality_dims(root):
    """Dimensions of the report quality score: the keys of the breakdown dict
    quality_scorer.score_report builds (AST), counted."""
    fn = _func(root, "ai_engine/analysis/quality_scorer.py", "score_report")
    dicts = [n for n in ast.walk(fn) if isinstance(n, ast.Dict) and len(n.keys) > 1
             and all(isinstance(k, ast.Constant) and isinstance(v, ast.Call)
                     for k, v in zip(n.keys, n.values))]
    if len(dicts) != 1:
        raise FitnessError("expected one {name: score_fn(report)} dict in score_report, got %d" % len(dicts))
    return len(dicts[0].keys)


def _days_claim(fragment):
    m = re.search(r"(\d+) and (\d+) days", fragment)
    if not m:
        raise FitnessError("no '<n> and <m> days' in fragment %r" % fragment)
    return ["short=%d" % int(m.group(1)), "long=%d" % int(m.group(2))]


def _verify_days(root):
    """Default verify-by horizons of a debate's predictions: the fallback in
    mad_result.get('short_verify_days', N) and ('long_verify_days', M) in
    mad_runner.py (AST). Two different fallbacks for one key halt."""
    path = os.path.join(root, "ai_engine", "mad_runner.py")
    if not os.path.isfile(path):
        raise FitnessError("ai_engine/mad_runner.py not found")
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    found = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "get" \
                and len(n.args) == 2 and isinstance(n.args[0], ast.Constant) \
                and n.args[0].value in ("short_verify_days", "long_verify_days"):
            found.setdefault(n.args[0].value, set()).add(_num(n.args[1]))
    if set(found) != {"short_verify_days", "long_verify_days"} or any(len(v) != 1 for v in found.values()):
        raise FitnessError("verify-day defaults missing or inconsistent in mad_runner.py: %r" % found)
    return ["short=%d" % found["short_verify_days"].pop(), "long=%d" % found["long_verify_days"].pop()]


def _gpvs_days_claim(fragment):
    m = re.search(r"at ((?:\d+, )*\d+ and \d+) days", fragment)
    if not m:
        raise FitnessError("no 'at a, b and c days' in fragment %r" % fragment)
    return ["%dd" % x for x in sorted(int(x) for x in re.findall(r"\d+", m.group(1)))]


def _gpvs_days(root):
    """Windows the report-level GPVS check fetches SPY for: the literal day
    argument of fetch_price_change_with_fallback('SPY', N) in outcome_verifier.py (AST)."""
    path = os.path.join(root, "ai_engine", "analysis", "outcome_verifier.py")
    if not os.path.isfile(path):
        raise FitnessError("ai_engine/analysis/outcome_verifier.py not found")
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    out = sorted({_num(n.args[1]) for n in ast.walk(tree) if isinstance(n, ast.Call)
                  and getattr(n.func, "id", "") == "fetch_price_change_with_fallback"
                  and len(n.args) == 2 and getattr(n.args[0], "value", None) == "SPY"})
    if not out:
        raise FitnessError("no fetch_price_change_with_fallback('SPY', N) in outcome_verifier.py")
    return ["%dd" % x for x in out]


def _gpvs_window_claim(fragment):
    m = re.search(r"(\d+)-Day", fragment)
    if not m:
        raise FitnessError("no '<n>-Day' in fragment %r" % fragment)
    return ["%dd" % int(m.group(1))]



def _swan_claim(fragment):
    m = re.search(r"(\d+(?:\.\d+)?)% or more over the (\d+) hours", fragment)
    n = re.search(r"a fixed (\d+(?:\.\d+)?)", fragment)
    if not m or not n:
        raise FitnessError("no '<x>% or more over the <n> hours ... a fixed <s>' in %r" % fragment)
    return ["%g%%" % float(m.group(1)), "%gh" % float(m.group(2)), "%g" % float(n.group(1))]


def _black_swan(root):
    """The report check's black-swan rule in outcome_verifier.py (AST): the
    BLACK_SWAN_THRESHOLD constant; the window, BLACK_SWAN_HOURS, counted only if
    detect_black_swan uses it as wall-clock seconds (BLACK_SWAN_HOURS * 3600 - S111;
    before, a slice of hourly bars kept the whole 5-day range); and the score
    calculate_accuracy_score returns under `if black_swan or context_credit`."""
    rel = "ai_engine/analysis/outcome_verifier.py"
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise FitnessError("%s not found" % rel)
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    thr = [_num(n.value) for n in tree.body if isinstance(n, ast.Assign)
           and any(getattr(t, "id", "") == "BLACK_SWAN_THRESHOLD" for t in n.targets)]
    if len(thr) != 1:
        raise FitnessError("expected one BLACK_SWAN_THRESHOLD in %s" % rel)
    hours = [_num(n.value) for n in tree.body if isinstance(n, ast.Assign)
             and any(getattr(t, "id", "") == "BLACK_SWAN_HOURS" for t in n.targets)]
    if len(hours) != 1:
        raise FitnessError("expected one BLACK_SWAN_HOURS in %s" % rel)
    det = _func(root, rel, "detect_black_swan")
    wall = any(isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mult)
               and {getattr(n.left, "id", None), getattr(n.right, "value", None)} == {"BLACK_SWAN_HOURS", 3600}
               for n in ast.walk(det))
    acc = _func(root, rel, "calculate_accuracy_score")
    ret = [_num(s.value) for n in ast.walk(acc) if isinstance(n, ast.If) and isinstance(n.test, ast.BoolOp)
           and "black_swan" in {getattr(v, "id", "") for v in n.test.values}
           for s in n.body if isinstance(s, ast.Return)]
    if len(ret) != 1:
        raise FitnessError("expected one return under 'if black_swan or ...' in calculate_accuracy_score")
    return ["%g%%" % thr[0], ("%gh" % hours[0]) if wall else "bar-count window", "%g" % ret[0]]


def _ab_claim(fragment):
    m = re.search(r"(\d+) runs", fragment)
    n = re.search(r"(?:≥|by) (\d+(?:\.\d+)?)", fragment)
    if not m or not n:
        raise FitnessError("no '<n> runs' and '≥ <x>' in fragment %r" % fragment)
    return ["runs>=%d" % int(m.group(1)), "gap>=%g" % float(n.group(1))]


def _ab_promote(root):
    """The prompt A/B governor's promotion rule: the run_count >= N filter and the
    diff >= X test in prompt_manager._check_promotion (AST)."""
    fn = _func(root, "ai_engine/analysis/prompt_manager.py", "_check_promotion")
    runs, gaps = set(), set()
    for n in ast.walk(fn):
        if isinstance(n, ast.Compare) and len(n.ops) == 1 and isinstance(n.ops[0], ast.GtE) \
                and isinstance(n.comparators[0], ast.Constant):
            left = n.left
            if isinstance(left, ast.Subscript) and getattr(left.slice, "value", None) == "run_count":
                runs.add(_num(n.comparators[0]))
            elif getattr(left, "id", "") == "diff":
                gaps.add(_num(n.comparators[0]))
    if len(runs) != 1 or len(gaps) != 1:
        raise FitnessError("expected one run_count >= N and one diff >= X in _check_promotion")
    return ["runs>=%d" % runs.pop(), "gap>=%g" % gaps.pop()]


def _window_claim(fragment):
    out = re.findall(r"(\d+-\d+ (?:days|months))", fragment)
    if not out:
        raise FitnessError("no '<a>-<b> days|months' in fragment %r" % fragment)
    return sorted(out)


def _threat_windows(root):
    """Windows the Arbitrator is asked to name threats in: the JSON template's
    "short_focus_threats" and "long_shoot_threats" values in mad_protocol.py."""
    path = os.path.join(root, "ai_engine", "analysis", "mad_protocol.py")
    if not os.path.isfile(path):
        raise FitnessError("ai_engine/analysis/mad_protocol.py not found")
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8-sig")
    out = []
    for key in ("short_focus_threats", "long_shoot_threats"):
        got = set(re.findall(r'"%s": "[^"]*?(\d+-\d+ (?:days|months))"' % key, text))
        if len(got) != 1:
            raise FitnessError("expected one window for %s in mad_protocol.py, got %r" % (key, got))
        out.append(got.pop())
    return sorted(out)


def _accounts_claim(fragment):
    out = sorted(set(re.findall(r"\b(morning|evening)\b", fragment)))
    if not out:
        raise FitnessError("no morning/evening in fragment %r" % fragment)
    return out


def _mad_accounts(root):
    """Accounts the MAD workflow runs under: the quoted names on gni_mad.yml's
    GNI_MAD_ACCOUNT line. They count only if its GROQ_API_KEY line picks as many
    distinct secrets; otherwise the names share one key and this says so."""
    path = os.path.join(root, ".github", "workflows", "gni_mad.yml")
    if not os.path.isfile(path):
        raise FitnessError(".github/workflows/gni_mad.yml not found")
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8")
    acct = [l for l in text.splitlines() if l.strip().startswith("GNI_MAD_ACCOUNT:")]
    key = [l for l in text.splitlines() if l.strip().startswith("GROQ_API_KEY:")]
    if len(acct) != 1 or len(key) != 1:
        raise FitnessError("expected one GNI_MAD_ACCOUNT and one GROQ_API_KEY line in gni_mad.yml")
    names = sorted(set(re.findall(r"'([a-z]+)'", acct[0].split(":", 1)[1])))
    secrets = set(re.findall(r"secrets\.([A-Z0-9_]+)", key[0]))
    if len(secrets) != len(names):
        return ["%d names on %d key(s)" % (len(names), len(secrets))]
    return names


def _cap_claim(fragment):
    m = re.search(r"capped at (\d+(?:\.\d+)?)", fragment)
    if not m:
        raise FitnessError("no 'capped at <n>' in fragment %r" % fragment)
    return "%g" % float(m.group(1))


def _esc_cap(root):
    """The cap on the final escalation score: min(raw_score, N) in
    escalation_scorer.score_escalation (AST)."""
    fn = _func(root, "ai_engine/analysis/escalation_scorer.py", "score_escalation")
    caps = {_num(n.args[1]) for n in ast.walk(fn) if isinstance(n, ast.Call)
            and getattr(n.func, "id", "") == "min" and len(n.args) == 2
            and getattr(n.args[0], "id", "") == "raw_score"}
    if len(caps) != 1:
        raise FitnessError("expected one min(raw_score, N) in score_escalation, got %r" % caps)
    return "%g" % caps.pop()


def _delta_claim(fragment):
    m = re.search(r"delta (?:&gt;|>)= (\d+(?:\.\d+)?)", fragment)
    if not m:
        raise FitnessError("no 'delta >= <x>' in fragment %r" % fragment)
    return "%g" % float(m.group(1))


def _hb_delta(root):
    """The escalation delta at which the heartbeat triggers an adaptive run:
    DELTA_THRESHOLD in monitoring_pipeline.py (AST)."""
    path = os.path.join(root, "ai_engine", "monitoring_pipeline.py")
    if not os.path.isfile(path):
        raise FitnessError("ai_engine/monitoring_pipeline.py not found")
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    got = [_num(n.value) for n in tree.body if isinstance(n, ast.Assign)
           and any(getattr(t, "id", "") == "DELTA_THRESHOLD" for t in n.targets)]
    if len(got) != 1:
        raise FitnessError("expected one DELTA_THRESHOLD in monitoring_pipeline.py")
    return "%g" % got[0]


def _days_list_claim(fragment):
    out = sorted({int(x) for x in re.findall(r"(\d+)-day", fragment)})
    if not out:
        raise FitnessError("no '<n>-day' in fragment %r" % fragment)
    return ["%dd" % x for x in out]


def _corr_windows(root):
    """Windows the correlation engine writes: the spy_change_<n>d keys of the
    upsert in historical_correlations.save_correlation_table (AST)."""
    fn = _func(root, "ai_engine/analysis/historical_correlations.py", "save_correlation_table")
    keys = {m for n in ast.walk(fn) if isinstance(n, ast.Dict) for k in n.keys
            if isinstance(k, ast.Constant) and isinstance(k.value, str)
            for m in re.findall(r"^spy_change_(\d+)d$", k.value)}
    if not keys:
        raise FitnessError("no spy_change_<n>d key in save_correlation_table")
    return ["%dd" % x for x in sorted(int(k) for k in keys)]


def _min_claim(fragment):
    m = re.search(r"(\d+)\+", fragment)
    if not m:
        raise FitnessError("no '<n>+' in fragment %r" % fragment)
    return "%d" % int(m.group(1))


def _pattern_min(root):
    """Fewest outcomes a location or pillar pattern needs: every `if n < N:
    continue` in historical_correlations._save_patterns (AST); they must agree."""
    fn = _func(root, "ai_engine/analysis/historical_correlations.py", "_save_patterns")
    got = {_num(n.test.comparators[0]) for n in ast.walk(fn) if isinstance(n, ast.If)
           and isinstance(n.test, ast.Compare) and getattr(n.test.left, "id", "") == "n"
           and isinstance(n.test.ops[0], ast.Lt)}
    if len(got) != 1:
        raise FitnessError("expected one 'n < N' minimum in _save_patterns, got %r" % got)
    return "%d" % got.pop()


def _mat_claim(fragment):
    out = []
    m = re.search(r"f[ae]ll(?: of)? (\d+(?:\.\d+)?)% or more", fragment)
    if m:
        out.append("materialized<=-%g%%" % float(m.group(1)))
    n = re.search(r"above -(\d+(?:\.\d+)?)%", fragment)
    if n:
        out.append("not>=-%g%%" % float(n.group(1)))
    if not out:
        raise FitnessError("no 'fell <x>% or more' or 'above -<y>%' in fragment %r" % fragment)
    return out


def _materialized(root):
    """The debate check's verdict bands: MATERIALIZED_AT and NOT_MATERIALIZED_AT
    in debate_prediction_verifier.py (AST)."""
    path = os.path.join(root, "ai_engine", "analysis", "debate_prediction_verifier.py")
    if not os.path.isfile(path):
        raise FitnessError("ai_engine/analysis/debate_prediction_verifier.py not found")
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    val = {}
    for n in tree.body:
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if getattr(t, "id", "") in ("MATERIALIZED_AT", "NOT_MATERIALIZED_AT"):
                    v = n.value
                    if isinstance(v, ast.UnaryOp) and isinstance(v.op, ast.USub):
                        val[t.id] = -_num(v.operand)
                    else:
                        val[t.id] = _num(v)
    if set(val) != {"MATERIALIZED_AT", "NOT_MATERIALIZED_AT"}:
        raise FitnessError("MATERIALIZED_AT / NOT_MATERIALIZED_AT missing in debate_prediction_verifier.py")
    return ["materialized<=%g%%" % val["MATERIALIZED_AT"], "not>=%g%%" % val["NOT_MATERIALIZED_AT"]]


def _gpvs_version_claim(fragment):
    m = re.search(r"GPVS v(\d+\.\d+)", fragment)
    if not m:
        raise FitnessError("no 'GPVS v<x.y>' in fragment %r" % fragment)
    return "v" + m.group(1)


def _gpvs_version(root):
    """The GPVS version the report check announces: every 'GPVS v<x.y>' in
    outcome_verifier.py; more than one version halts."""
    path = os.path.join(root, "ai_engine", "analysis", "outcome_verifier.py")
    if not os.path.isfile(path):
        raise FitnessError("ai_engine/analysis/outcome_verifier.py not found")
    with open(path, "rb") as fh:
        got = set(re.findall(r"GPVS v(\d+\.\d+)", fh.read().decode("utf-8-sig")))
    if len(got) != 1:
        raise FitnessError("expected one GPVS version in outcome_verifier.py, got %r" % got)
    return "v" + got.pop()


def _of_claim(fragment):
    m = re.search(r"(\d+) of the (\d+)", fragment)
    if not m:
        raise FitnessError("no '<a> of the <b>' in fragment %r" % fragment)
    return "%d/%d" % (int(m.group(1)), int(m.group(2)))


def _pentest(root):
    """How many of the attack strings listed under the security page's Pentest
    Results match one of the funnel's INJECTION_PATTERNS today: the patterns read
    by AST, each string reduced as _normalize_text_funnel's last step does
    (printable ASCII), lowercased, then re.search'ed. Returns 'matched/listed'."""
    fpath = os.path.join(root, "ai_engine", "funnel", "intelligence_funnel.py")
    ppath = os.path.join(root, "src", "app", "security", "page.tsx")
    for p in (fpath, ppath):
        if not os.path.isfile(p):
            raise FitnessError("%s not found" % os.path.relpath(p, root))
    with open(fpath, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    pats = [e.value for n in tree.body if isinstance(n, ast.Assign)
            and any(getattr(t, "id", "") == "INJECTION_PATTERNS" for t in n.targets)
            for e in n.value.elts if isinstance(e, ast.Constant)]
    if not pats:
        raise FitnessError("no INJECTION_PATTERNS list in intelligence_funnel.py")
    with open(ppath, "rb") as fh:
        page = fh.read().decode("utf-8")
    at = page.find("Pentest Results")
    blk = page[at:]
    if at < 0 or "{[" not in blk or "].map" not in blk:
        raise FitnessError("no Pentest Results attack list in security/page.tsx")
    blk = blk[blk.index("{["):blk.index("].map")]
    atk = re.findall(r"'((?:[^'\\]|\\.)*)'", blk)
    if not atk:
        raise FitnessError("empty attack list in security/page.tsx")
    hit = 0
    for a in atk:
        t = "".join(ch for ch in a if ch.isascii() and (ch.isprintable() or ch == " ")).strip().lower()
        hit += any(re.search(p, t, re.IGNORECASE) for p in pats)
    return "%d/%d" % (hit, len(atk))


def _last_runs_claim(fragment):
    m = re.search(r"last (\d+) runs", fragment)
    if not m:
        raise FitnessError("no 'last <n> runs' in fragment %r" % fragment)
    return m.group(1)


def _sh_runs(root):
    """Runs per source the source-health API keeps: runs.length < N in its route."""
    return _route_int(root, "src/app/api/source-health/route.ts", r"runs\.length < (\d+)")


def _route_int(root, rel, rx):
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise FitnessError("%s not found" % rel)
    with open(path, "rb") as fh:
        got = set(re.findall(rx, fh.read().decode("utf-8")))
    if len(got) != 1:
        raise FitnessError("expected one match of %s in %s, got %r" % (rx, rel, got))
    return got.pop()


def _newest_claim(fragment):
    m = re.search(r"newest (\d+)", fragment)
    if not m:
        raise FitnessError("no 'newest <n>' in fragment %r" % fragment)
    return m.group(1)


def _alerts_limit(root):
    """Health alerts the alerts API returns: the .limit(N) on its health_alerts query."""
    return _route_int(root, "src/app/api/alerts/route.ts", r"from\('health_alerts'\)[^\n]*\.limit\((\d+)\)")


_NUMWORD = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
            "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "twenty": 20, "hundred": 100}


def _count_of(token):
    """An integer from digits or from the number words S111 writes ('two hundred')."""
    token = token.strip().lower()
    if token.isdigit():
        return int(token)
    words = token.split()
    if words and all(w in _NUMWORD for w in words):
        n = _NUMWORD[words[0]]
        for w in words[1:]:
            n = n * _NUMWORD[w] if w == "hundred" else n + _NUMWORD[w]
        return n
    raise FitnessError("not a count: %r" % token)


_COUNT_TOKEN = r"(\d+|(?:%s)(?: hundred)?)" % "|".join(sorted(_NUMWORD, key=len, reverse=True))


def _agents_claim(fragment):
    m = re.search(_COUNT_TOKEN + r"[- ](?:AI )?(?:agents?|quadrants?)\b", fragment, re.I)
    if not m:
        raise FitnessError("no '<n>-agent' / '<n> agents' / '<n> quadrants' in fragment %r" % fragment)
    return "%d" % _count_of(m.group(1))


def _mad_agents(root):
    """Debating agents: the quadrant prompts in mad_protocol.py, each opening
    'YOUR <word> -- THE <NAME>:' (the word is built below, not written here)."""
    path = os.path.join(root, "ai_engine", "analysis", "mad_protocol.py")
    if not os.path.isfile(path):
        raise FitnessError("ai_engine/analysis/mad_protocol.py not found")
    with open(path, "rb") as fh:
        names = set(re.findall(r"YOUR L[E]NS -- THE ([A-Z ]+?):", fh.read().decode("utf-8-sig")))
    if not names:
        raise FitnessError("no quadrant prompt ('YOUR <word> -- THE <NAME>:') in mad_protocol.py")
    return "%d" % len(names)


def _map_days_claim(fragment):
    m = re.search(r"last ((?:\d+, )*\d+,? or \d+) days", fragment)
    if not m:
        raise FitnessError("no 'last a, b, or c days' in fragment %r" % fragment)
    return ["%dd" % x for x in sorted(int(x) for x in re.findall(r"\d+", m.group(1)))]


def _map_days(root):
    """Day windows the map page offers: the literal list mapped into its filter buttons."""
    got = _route_int(root, "src/app/map/page.tsx", r"\{\[([\d, ]+)\]\.map\(d =>")
    return ["%dd" % x for x in sorted(int(x) for x in re.findall(r"\d+", got))]


def _every_min_claim(fragment):
    m = re.search(r"every (\d+) min", fragment)
    if not m:
        raise FitnessError("no 'every <n> min' in fragment %r" % fragment)
    return m.group(1)


def _mc_refresh(root):
    """Mission Control's refresh period: setInterval(runCheck, N * 60 * 1000)."""
    return _route_int(root, "src/app/mission-control/page.tsx", r"setInterval\(runCheck, (\d+) \* 60 \* 1000\)")


def _cats_claim(fragment):
    m = re.search(r"(\d+)-Category", fragment)
    if not m:
        raise FitnessError("no '<n>-Category' in fragment %r" % fragment)
    return m.group(1)


def _stock_cats(root):
    """Categories the market page offers: entries of its CATEGORIES list."""
    path = os.path.join(root, "src", "app", "stocks", "page.tsx")
    if not os.path.isfile(path):
        raise FitnessError("src/app/stocks/page.tsx not found")
    with open(path, "rb") as fh:
        text = fh.read().decode("utf-8")
    m = re.search(r"const CATEGORIES = \[(.*?)\n\]", text, re.S)
    if not m:
        raise FitnessError("no CATEGORIES list in stocks/page.tsx")
    return "%d" % len(re.findall(r"\{ key: '", m.group(1)))


def _rounds_claim(fragment):
    m = re.search(_COUNT_TOKEN + r" rounds?\b", fragment, re.I)
    if not m:
        raise FitnessError("no '<n> rounds' in fragment %r" % fragment)
    return "%d" % _count_of(m.group(1))


def _mad_rounds(root):
    """Debate rounds: the distinct 'ROUND <n>' markers the agents are sent in mad_protocol.py."""
    path = os.path.join(root, "ai_engine", "analysis", "mad_protocol.py")
    if not os.path.isfile(path):
        raise FitnessError("ai_engine/analysis/mad_protocol.py not found")
    with open(path, "rb") as fh:
        got = {int(x) for x in re.findall(r"ROUND (\d+)(?: FINAL)?:", fh.read().decode("utf-8-sig"))}
    if not got or got != set(range(1, max(got) + 1)):
        raise FitnessError("ROUND markers missing or not 1..n in mad_protocol.py: %r" % sorted(got))
    return "%d" % max(got)


def _upto_claim(fragment):
    m = re.search(r"(?:up to|newest) " + _COUNT_TOKEN + r"\b", fragment, re.I)
    if not m:
        raise FitnessError("no 'up to <n>' / 'newest <n>' in fragment %r" % fragment)
    return "%d" % _count_of(m.group(1))


def _runs_limit(root):
    """Main runs the pipeline-runs API returns: its .limit(N)."""
    return _route_int(root, "src/app/api/pipeline-runs/route.ts", r"\.limit\((\d+)\)")


def _reports_limit(root):
    """Reports the reports API lists: limit=N in its select=* query."""
    return _route_int(root, "src/app/api/reports/route.ts", r"select=\*&order=created_at\.desc&limit=(\d+)")


def _endpoints_claim(fragment):
    m = re.search(_COUNT_TOKEN + r" (?:REST )?endpoints?\b", fragment, re.I)
    if not m:
        raise FitnessError("no '<n> endpoints' in fragment %r" % fragment)
    return "%d" % _count_of(m.group(1))


def _export_routes(root):
    """Export endpoints: route.ts files under src/app/api/export."""
    got = glob.glob(os.path.join(root, "src", "app", "api", "export", "**", "route.ts"), recursive=True)
    if not got:
        raise FitnessError("no route.ts under src/app/api/export")
    return "%d" % len(got)


def _pillar_reports_claim(fragment):
    m = re.search(r"the " + _COUNT_TOKEN + r" (?:pillar )?reports\b", fragment, re.I)
    if not m:
        raise FitnessError("no 'the <n> reports' in fragment %r" % fragment)
    return "%d" % _count_of(m.group(1))


def _pillar_runs(root):
    """Pillar reports a main run attempts: the pillar list main.py enumerates for Step 4b."""
    got = _route_int(root, "ai_engine/main.py", r"enumerate\(\[((?:\"\w+\",? ?)+)\]\)")
    return "%d" % len(re.findall(r"\"\w+\"", got))


EXT_RE = re.compile(r"^gni_external_snapshot_S(\d+)\.json$")
EXT_FIELDS = ("id", "party", "statement", "source", "url", "read", "read_by", "phrases")


def _ext_claim(fragment):
    """The phrase itself: an external figure is stated, not computed."""
    if not fragment.strip():
        raise FitnessError("empty fragment for F-EXT")
    return fragment.strip()


def _ext_phrases(root):
    """Every phrase recorded in the highest-numbered docs/gni_external_snapshot_S<N>.json
    (S112, roadmap 4 row R4-3, DECISION S112-1). Each fact names its party, the
    statement read, the source, the day it was read and who read it; a fact with
    a field missing, a date not of the form YYYY-MM-DD, or a phrase claimed by two
    facts is an instrument fault. Returns {phrase: "<fact id> read <date>"}. LIMIT, written down: the snapshot records what a
    source said on the day it was read, so a figure that changes at its source
    stays SUPPORTED here until the source is read again."""
    import json
    docs = os.path.join(root, "docs")
    gen = sorted((int(m.group(1)), n) for n in (os.listdir(docs) if os.path.isdir(docs) else [])
                 for m in [EXT_RE.match(n)] if m)
    if not gen:
        raise FitnessError("no docs/gni_external_snapshot_S<N>.json")
    with open(os.path.join(docs, gen[-1][1]), "rb") as fh:
        facts = json.loads(fh.read().decode("utf-8-sig")).get("facts") or []
    if not facts:
        raise FitnessError("%s holds no facts" % gen[-1][1])
    owner = {}
    for f in facts:
        miss = [k for k in EXT_FIELDS if k not in f or (k != "url" and not f[k])]
        if miss:
            raise FitnessError("fact %r lacks %s" % (f.get("id"), ", ".join(miss)))
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", f["read"]):
            raise FitnessError("fact %r: read %r is not YYYY-MM-DD" % (f["id"], f["read"]))
        for ph in f["phrases"]:
            if ph in owner:
                raise FitnessError("phrase %r claimed by %s and %s" % (ph, owner[ph], f["id"]))
            owner[ph] = "%s read %s" % (f["id"], f["read"])
    return owner


def _recorded(claimed, measured):
    return claimed in measured


def _trend_claim(fragment):
    m = re.search(r"(\d+)-run\b|Last (\d+) Runs\b", fragment)
    if not m:
        raise FitnessError("no '<n>-run' / 'Last <n> Runs' in fragment %r" % fragment)
    return m.group(1) or m.group(2)


def _trend_runs(root):
    """Reports the escalation trend draws (S112): `reports.slice(0, N)` behind the
    trend on the home page and on /researcher. The two must agree; a page with no
    such slice, or two lengths, is an instrument fault."""
    got = set()
    for rel in ("src/app/page.tsx", "src/app/researcher/page.tsx"):
        got.add(_route_int(root, rel, r"const last7 = reports\.slice\(0, (\d+)\)"))
    if len(got) != 1:
        raise FitnessError("the two escalation trends draw different lengths: %r" % sorted(got))
    return got.pop()


def _neutral_claim(fragment):
    m = re.search(r"baseline of (\d+\.\d+)", fragment)
    if not m:
        raise FitnessError("no 'baseline of <x.y>' in fragment %r" % fragment)
    return m.group(1)


def _weight_neutral(root):
    """The weight a source starts at (S112): the 'weight' every roster source is
    seeded with in source_weights.py; more than one seeded value halts."""
    return _route_int(root, "ai_engine/analysis/source_weights.py", r"'weight': (\d+\.\d+),")


def _equal(claimed, measured):
    return claimed == measured


def _scheduled(claimed, measured):
    """A schedule claim names times at which runs happen. It holds when every
    named time is a scheduled time; a workflow may schedule more runs than a
    page names (gni_mad.yml adds an 11:13 watch beside its two debates)."""
    return set(claimed) <= set(measured)


# id: (what it measures, parser of the claim's fragment, measurement, comparison)
FITNESS = {
    "F-INJ": ("injection patterns in the funnel's INJECTION_PATTERNS list (AST)",
              _first_int,
              lambda r: _ast_list_len(r, "ai_engine/funnel/intelligence_funnel.py",
                                      "INJECTION_PATTERNS"), _equal),
    "F-RSS": ("RSS sources in the collector's SOURCES list (AST)",
              _first_int,
              lambda r: _ast_list_len(r, "ai_engine/collectors/rss_collector.py", "SOURCES"),
              _equal),
    "F-WF": ("workflow files under .github/workflows",
             _first_int, lambda r: _count(r, ".github/workflows/*.yml"), _equal),
    "F-PAGES": ("page.tsx files under src/app",
                _first_int, lambda r: _count(r, "src/app/**/page.tsx"), _equal),
    "F-ROUTES": ("route.ts files under src/app/api",
                 _first_int, lambda r: _count(r, "src/app/api/**/route.ts"), _equal),
    "F-CRON-PIPE": ("main pipeline schedule, UTC, from gni_pipeline.yml cron lines",
                    _times_utc, lambda r: _cron(r, "gni_pipeline.yml"), _scheduled),
    "F-CRON-MAD": ("MAD schedule, UTC, from gni_mad.yml cron lines",
                   _times_utc, lambda r: _cron(r, "gni_mad.yml"), _scheduled),
    # S110 (item 9.11): the per-account daily token limit GNI PLANS against. Not the provider's
    # limit - GNI has never measured that - which is why the page labels it as GNI's.
    "F-TPD": ("per-account daily Groq token limit GNI plans against: TPD_HARD_LIMIT in quota_guard.py (AST)",
              _int_k, lambda r: _ast_int_const(r, "ai_engine/quota_guard.py", "TPD_HARD_LIMIT"), _equal),
    "F-TPD-SAFE": ("per-account daily safe ceiling GNI plans against: TPD_SAFE_CEILING in quota_guard.py (AST)",
                   _int_k, lambda r: _ast_int_const(r, "ai_engine/quota_guard.py", "TPD_SAFE_CEILING"), _equal),
    # S111 (roadmap 4 row R4-2, /about/devops).
    "F-ADAPT-GAP": ("minimum gap per escalation level the adaptive run enforces: interval_h in "
                    "ESCALATION_MODES, adaptive_pipeline.py (AST)",
                    _gap_claim, _adaptive_gaps, _scheduled),
    "F-HB-GROQ": ("Groq imports and Groq() calls in the heartbeat module, monitoring_pipeline.py (AST)",
                  _first_int, _groq_refs, _equal),
    "F-AUDIT-HASH": ("digest size of the audit chain: hashlib.sha<N> in audit_trail._compute_hash (AST)",
                     _hash_claim, _audit_hash, _equal),
    "F-CI-TEMPS": ("main-pipeline analysis temperatures: _call_groq's request plus analyze()'s CI loop "
                   "(AST)", _temps_claim, _ci_temps, _equal),
    "F-CI-T-TWO": ("the t value nexus_analyzer._T95_TWO_SIDED gives a two-run interval, df=1 (AST)",
                   _t_claim, _ci_t_two, _scheduled),
    "F-GPVS-INSTR": ("instruments verify_pending_outcomes judges a report's direction on: the "
                     "first argument of each direction() call (AST)", _instr_claim, _gpvs_dir_instr, _equal),
    "F-CI-T": ("the planned run count and the t value nexus_analyzer._T95_TWO_SIDED gives it (AST)",
               _t_claim, _ci_t, _scheduled),
    "F-EMA": ("source-weight EMA coefficients and GPVS factors in source_weights.update_source_weight "
              "(AST)", _ema_claim, _ema, _equal),
    "F-WEIGHT-BOUNDS": ("source-weight clamp max(lo, min(x, hi)) in source_weights.update_source_weight (AST)",
                        _bounds_claim, _weight_bounds, _scheduled),
    "F-ESC-BANDS": ("lower bound of each escalation level in escalation_scorer.score_escalation (AST)",
                    _bands_claim, _esc_bands, _scheduled),
    "F-SH-STATES": ("states the source-health page can show: keys of its STATUS_CONFIG",
                    _count_word, _sh_states, _equal),
    "F-SECRETS": ("secret names the workflow files read (secrets.NAME); a claim's names must be among them",
                  _secret_names, _workflow_secrets, _scheduled),
    "F-SRC-CAP": ("per-source article cap the main pipeline passes to run_funnel (main.py, AST)",
                  _first_int, _src_cap, _equal),
    "F-PY-MIN": ("python versions the workflows set up; a claim 'X+' holds when every one is at least X",
                 _version_claim, _python_versions, _at_least),
    "F-NEXT": ("major version of the next dependency in package.json",
               _version_claim, _next_major, _major_equal),
    "F-ENTRY": ("python files the workflows run; a claim's file names must be among them",
                _py_names, _workflow_entrypoints, _scheduled),
    "F-DEDUP-WORDS": ("title words hashed by intelligence_funnel._get_dedup_key (AST slice bound)",
                      _first_int, _dedup_words, _equal),
    "F-PILLAR-WAIT": ("literal time.sleep waits in main.py; a claimed wait must be one of them",
                      _sleeps_claim, _main_sleeps, _scheduled),
    "F-QUALITY-DIMS": ("dimensions of the report quality score: the score_fn entries of the breakdown in "
                       "quality_scorer.score_report (AST)", _count_word, _quality_dims, _equal),
    "F-VERIFY-DAYS": ("default verify-by horizons of debate predictions: the .get fallbacks for "
                      "short_verify_days and long_verify_days in mad_runner.py (AST)",
                      _days_claim, _verify_days, _equal),
    "F-GPVS-DAYS": ("windows the report-level GPVS check fetches SPY for: fetch_price_change_with_fallback"
                    "('SPY', N) in outcome_verifier.py (AST)", _gpvs_days_claim, _gpvs_days, _equal),
    "F-GPVS-WINDOW": ("one window of the report-level GPVS check: a claimed '<n>-Day' must be one of "
                      "fetch_price_change_with_fallback('SPY', N) in outcome_verifier.py (AST)",
                      _gpvs_window_claim, _gpvs_days, _scheduled),
    "F-BLACK-SWAN": ("the report check's black-swan rule in outcome_verifier.py: BLACK_SWAN_THRESHOLD, "
                     "the range of detect_black_swan's chart URL, and the fixed score (AST)",
                     _swan_claim, _black_swan, _equal),
    "F-AB-PROMOTE": ("the prompt A/B governor's promotion rule: run_count >= N and diff >= X in "
                     "prompt_manager._check_promotion (AST)", _ab_claim, _ab_promote, _equal),
    "F-THREAT-WINDOWS": ("windows of the Arbitrator's short_focus_threats and long_shoot_threats in "
                         "mad_protocol.py's JSON template; a claimed window must be one of them",
                         _window_claim, _threat_windows, _scheduled),
    "F-MAD-ACCOUNTS": ("accounts the MAD workflow runs under: GNI_MAD_ACCOUNT names in gni_mad.yml, "
                       "counted only when GROQ_API_KEY picks as many secrets", _accounts_claim,
                       _mad_accounts, _equal),
    "F-ESC-CAP": ("the cap on the final escalation score: min(raw_score, N) in "
                  "escalation_scorer.score_escalation (AST)", _cap_claim, _esc_cap, _equal),
    "F-HB-DELTA": ("escalation delta at which the heartbeat triggers an adaptive run: DELTA_THRESHOLD in "
                   "monitoring_pipeline.py (AST)", _delta_claim, _hb_delta, _equal),
    "F-CORR-WINDOWS": ("windows the correlation engine writes: spy_change_<n>d keys in "
                       "historical_correlations.save_correlation_table (AST)",
                       _days_list_claim, _corr_windows, _equal),
    "F-PATTERN-MIN": ("fewest outcomes a location or pillar pattern needs: n < N in "
                      "historical_correlations._save_patterns (AST)", _min_claim, _pattern_min, _equal),
    "F-MATERIALIZED": ("the debate check's bands: MATERIALIZED_AT and NOT_MATERIALIZED_AT in "
                       "debate_prediction_verifier.py (AST); a claim names one or both",
                       _mat_claim, _materialized, _scheduled),
    "F-GPVS-VERSION": ("the GPVS version outcome_verifier.py announces ('GPVS v<x.y>')",
                       _gpvs_version_claim, _gpvs_version, _equal),
    "F-PENTEST": ("attack strings listed under the security page's Pentest Results that match one of "
                  "the funnel's INJECTION_PATTERNS today", _of_claim, _pentest, _equal),
    "F-SH-RUNS": ("runs per source the source-health API keeps (runs.length < N)",
                  _last_runs_claim, _sh_runs, _equal),
    "F-ALERTS-LIMIT": ("health alerts the alerts API returns (.limit on health_alerts)",
                       _newest_claim, _alerts_limit, _equal),
    "F-MAD-AGENTS": ("debating agents: the quadrant prompts in mad_protocol.py",
                     _agents_claim, _mad_agents, _equal),
    "F-MAP-DAYS": ("day windows the map page's filter offers", _map_days_claim, _map_days, _equal),
    "F-MC-REFRESH": ("Mission Control's refresh period in minutes (setInterval in its page)",
                     _every_min_claim, _mc_refresh, _equal),
    "F-STOCK-CATS": ("categories the market page offers (its CATEGORIES list)", _cats_claim, _stock_cats, _equal),
    "F-MAD-ROUNDS": ("debate rounds: distinct 'ROUND <n>' markers in mad_protocol.py",
                     _rounds_claim, _mad_rounds, _equal),
    "F-RUNS-LIMIT": ("main runs the pipeline-runs API returns (.limit)", _upto_claim, _runs_limit, _equal),
    "F-REPORTS-LIMIT": ("reports the reports API lists (limit= in its query)",
                        _upto_claim, _reports_limit, _equal),
    "F-EXPORTS": ("export endpoints: route.ts files under src/app/api/export",
                  _endpoints_claim, _export_routes, _equal),
    "F-PILLAR-RUNS": ("pillar reports a main run attempts: main.py's Step 4b pillar list",
                      _pillar_reports_claim, _pillar_runs, _equal),
    # S112 (roadmap 4 row R4-3): a figure of a party GNI does not control, bound to the
    # dated reading of its published source in docs/gni_external_snapshot_S<N>.json.
    # S112 (roadmap 4 row R4-3, round 2).
    "F-TREND-RUNS": ("reports the escalation trend draws: reports.slice(0, N) on the home page and "
                     "/researcher, which must agree", _trend_claim, _trend_runs, _equal),
    "F-WEIGHT-NEUTRAL": ("the weight a source is seeded with: 'weight' in source_weights.py's seed",
                         _neutral_claim, _weight_neutral, _equal),
    "F-EXT": ("phrases recorded in the highest-numbered docs/gni_external_snapshot_S<N>.json, "
              "each with its party, source and read date",
              _ext_claim, _ext_phrases, _recorded),
}

# Why a claim has no fitness function. Written down at S111 for the three that
# were accepted and defined nowhere (roadmap 4's OWED list); a reason without a
# definition is a status typed by hand.
# UNREVIEWED: nobody has yet looked for a fitness function for the claim - it
# says nothing about the claim, and it is the reason most claims carry at S107.
# RUNTIME: see the module docstring - the claim is about what happens when GNI
# runs, and waits for a fitness function that reads a committed snapshot.
# PROMISE: the claim states an intention, not a state (its kind is PROMISE).
# HISTORICAL: the claim states a past state of the system (the frozen March 2026
# White Paper's "current" figures); measuring today's tree against it would
# defeat a claim that was true when made.
# PROVENANCE: the claim states who made GNI, where, or in which programme - an
# authorship or credit line. It describes GNI's origin, not its behaviour.
# EXTERNAL: the claim states a fact about a party GNI does not control - a
# provider's free-tier terms, limits or billing, or an outside statistic. Only
# that party's published terms can bear it out (ARCHITECTURE section 4, SLM).
# QUALITATIVE: the claim describes GNI's design or behaviour with no count, rate,
# time or date in it, so no fitness function can bear it out or defeat it. The
# review that gives this reason has READ THE CODE the sentence describes and
# judged it true; the reviewing commit names the files read. A sentence judged
# false gets no reason: its copy is retired. WEAKNESS: this is a person's
# judgement and leaves no trace beyond that commit message.
# HISTORICAL and PROVENANCE excuse a number on the public pages (gni_claims
# REVIEW_EXEMPT, roadmap 4 row R4-3); the other reasons do not.
UNMEASURED_REASONS = ("UNREVIEWED", "RUNTIME", "PROMISE", "HISTORICAL", "QUALITATIVE",
                      "EXTERNAL", "PROVENANCE")


def _duplicate_defs():
    """Top-level function names this module defines more than once. Python keeps
    the LAST definition silently: at S111 a second `_version_claim` replaced
    F-PY-MIN's parser and only a halt elsewhere exposed it. A duplicate is an
    instrument fault, so derive() refuses to run while one exists."""
    with open(os.path.abspath(__file__), "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    seen, dup = set(), []
    for n in tree.body:
        if isinstance(n, ast.FunctionDef):
            if n.name in seen:
                dup.append(n.name)
            seen.add(n.name)
    return dup


_DUPLICATE_DEFS = _duplicate_defs()


def derive(root, fid, fragment, cache):
    """(status, claimed, measured). Raises FitnessError on an instrument fault."""
    if _DUPLICATE_DEFS:
        raise FitnessError("gni_fitness.py defines %s more than once; the later definition "
                           "silently replaces the earlier" % ", ".join(sorted(set(_DUPLICATE_DEFS))))
    if fid not in FITNESS:
        raise FitnessError("unknown fitness function %s" % fid)
    _, parse, measure, holds = FITNESS[fid]
    claimed = parse(fragment)
    if fid not in cache:
        cache[fid] = measure(root)
    measured = cache[fid]
    status = "SUPPORTED" if holds(claimed, measured) else "DEFEATED"
    if isinstance(measured, dict):
        # A measurement keyed by what is claimed (F-EXT) reports the one record that
        # bears the claim out, not every record it holds.
        measured = measured.get(claimed, "not recorded")
    return status, claimed, measured
