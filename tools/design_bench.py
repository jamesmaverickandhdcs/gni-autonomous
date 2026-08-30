# design_bench.py -- S87. Test ANY escalation-scorer design against stored history.
#
# READ-ONLY. No DB write, no Groq call. Run before proposing a design, not after.
#
# WHY THIS EXISTS: at S87, eight claims about this scorer died -- none to argument,
# all eight to measurement. A design that failed here in March survived five
# sessions because nothing could test it in under a week. Now it takes one command.
#
# HOW TO USE: write your design as a function raw(t) -> float, add it to CANDIDATES,
# run this file. The GRAVEYARD below is RECOMPUTED every run, never hardcoded --
# a banked number is a claim; a recomputed one is evidence.
#
# Usage: python tools/design_bench.py     (repo root, venv active)

import sys, os, collections
sys.path.insert(0, os.path.abspath('ai_engine'))
from analysis.escalation_scorer import (TECH_SIGNALS, GEO_SIGNALS, FIN_SIGNALS,
                                        CRITICAL_COMBOS)
from analysis.supabase_saver import get_client

P    = {'TECH': TECH_SIGNALS, 'GEO': GEO_SIGNALS, 'FIN': FIN_SIGNALS}
W    = {'TECH': 1.5, 'GEO': 1.0, 'FIN': 0.8}
CAP  = {'TECH': 5,   'GEO': 5,   'FIN': 4}
RUPTURE = set(['invasion','coup','blockade','nuclear','missile','attack','embargo',
 'war','market crash','bank run','banking crisis','credit crunch','debt default',
 'currency collapse','hyperinflation','devaluation','capital flight','commodity shock',
 'food crisis','liquidity crisis','crypto crash','energy crisis','economic crisis',
 'recession','chip ban','ransomware','hack','export control','tech war','debt trap'])
ACTORS  = set(['iran','russia','china','north korea','israel','taiwan','ukraine',
 'red sea','hormuz','malacca','south china sea','arctic','strait','huawei','nvidia',
 'tsmc','opec','federal reserve','dollar','gold','bitcoin','treasury','wheat'])

def hits(t, drop=frozenset()):
    return {p: [s for s in sig if s in t and s not in drop] for p, sig in P.items()}
def combo(t):
    return sum(b for kws, b in CRITICAL_COMBOS if all(k in t for k in kws))
def div(h, sub=None):
    a = sum(1 for p in P if (sub[p] if sub else h[p]))
    return (a - 1) * 1.5 if a > 1 else 0
def level(s):
    return ('CRITICAL' if s >= 9 else 'HIGH' if s >= 7 else 'ELEVATED' if s >= 5
            else 'MODERATE' if s >= 3 else 'LOW')

def d_live(t):
    h = hits(t); return sum(min(len(h[p])*W[p], CAP[p]) for p in P) + div(h) + combo(t)
def d_fix2(t):
    h = hits(t); b = sum(min(len(h[p])*W[p], CAP[p]) for p in P)
    return min(b, 7.0) + div(h) + combo(t)
def d_actor(t):
    h = hits(t, ACTORS); return sum(min(len(h[p])*W[p], CAP[p]) for p in P) + div(h) + combo(t)
def d_rupture(t):
    h = hits(t, frozenset(['ceasefire']))
    r = {p: [s for s in h[p] if s in RUPTURE] for p in P}
    b = sum(min(len(r[p])*1.5 + (len(h[p])-len(r[p]))*0.3, CAP[p]) for p in P)
    return b + div(h, r) + combo(t)

GRAVEYARD = [
    ("Mar-24 Fix-2   base=min(sum,7)",      d_fix2),
    ("actor-tier     drop iran/china/...",  d_actor),
    ("rupture-tier   invasion/war weighted", d_rupture),
]
# ---- ADD YOUR DESIGN HERE: ("my design", my_fn) ----------------------------
def d_nocease(t):
    h = hits(t, frozenset(['ceasefire']))
    return sum(min(len(h[p])*W[p], CAP[p]) for p in P) + div(h) + combo(t)
CANDIDATES = [("8.7 polarity   drop ceasefire ONLY", d_nocease)]

def load():
    c = get_client(); assert c, "NO CLIENT -- STOP"
    rows, step, off = [], 1000, 0
    while True:
        r = (c.table("pipeline_articles").select("run_id,title,summary,created_at")
              .eq("stage4_selected", True).order("created_at").range(off, off+step-1).execute())
        if not r.data: break
        rows += r.data
        if len(r.data) < step: break
        off += step
    runs = collections.defaultdict(list)
    for a in rows: runs[a["run_id"]].append(a)
    return runs

def q(v, p):
    v = sorted(v); return v[min(int(len(v)*p), len(v)-1)]

def report(tag, texts):
    raw = [f(t) for t in texts]
    cap = [round(min(v, 10.0), 1) for v in raw]
    lv  = collections.Counter(level(v) for v in cap)
    top, cnt = lv.most_common(1)[0]
    print("%-38s %4.1f %4.1f %4.1f | %s" % (tag, q(cap,.25), q(cap,.5), q(cap,.75),
                                            dict(lv.most_common())))
    print("%-38s uncapped %.1f - %.1f (median %.1f)" % ("", min(raw), max(raw), q(raw,.5)))
    if cnt / float(len(cap)) > 0.90:
        print("   !! %d%% land on %s. An ABSOLUTE threshold on a PRE-SELECTED set:" % (
            round(100.0*cnt/len(cap)), top))
        print("      the funnel already picked the 22 most escalatory articles.")
        print("      Weights and word lists do not fix this. Three designs died here.")

if __name__ == '__main__':
    runs = load()
    texts = [" ".join((a.get("title") or "")+" "+(a.get("summary") or "")
                      for a in arts).lower() for arts in runs.values()]
    dates = sorted(a[0]["created_at"][:10] for a in runs.values())
    print("CORPUS: %d runs, %s .. %s" % (len(runs), dates[0], dates[-1]))
    print("  !! NO pre-crisis baseline in this window. 'normal = 4-6' CANNOT be")
    print("     derived from this data. Do not hardcode a crisis as normal.\n")
    print("%-38s  p25  med  p75 | levels" % "design")
    for tag, f in [("LIVE (production)", d_live)] + GRAVEYARD + CANDIDATES:
        globals()['f'] = f
        report(tag if tag.startswith("LIVE") else "GRAVEYARD " + tag, texts)
    if not CANDIDATES:
        print("\n(no candidate design supplied -- add one to CANDIDATES and re-run)")
