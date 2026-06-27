# -*- coding: utf-8 -*-
# ============================================================
# mad_budget_solver -- pre-call depth solver for the MAD protocol.
#
# WHAT IT DOES
#   Given N (the number of scored articles destined for the MAD news context),
#   pick the single free variable D (the per-article summary slice depth, in
#   characters) so that the estimated per-run token cost lands on a target
#   token budget. N is SACRED -- the solver never reduces the article count;
#   depth D is the only lever it moves. Pure arithmetic, zero Groq calls,
#   meant to run PRE-CALL (R-S48-3).
#
# COST MODEL  (linear in N, linear in D)
#   cost(n, d) = FIXED + n * (PER_A_BASE + PER_A_PER_CHAR * d)
#   carried by the 10 scored-block calls of the real 21-call MAD run.
#
# PROVENANCE
#   Constants verified in P3-SOLVER validation against the P3-2D direct-harness
#   grid built from real Supabase run 7db741c6 (186 scored rows; pillars
#   geo:136 / fin:49 / tech:1). Least-squares per-N fit; FIXED recalibrated
#   35700->57300 at S52 from two live billed runs (N=34->89372, N=39->94212;
#   back-solve 57257/57374, <0.1% err). Held-constant bump, not a fresh joint
#   fit -- per-N slope re-validated ~0.1%.
#   Model reproduces the 4x4 (N=[15,30,45,60] x D=[100,200,300,400]) grid to
#   within <= 2.73% max error.
#
# CAVEAT (soft spot)
#   The fit is conservative (slightly high) at the depth extremes but is
#   ~1-1.5% OPTIMISTIC (model under-estimates) in the D=200 region. Treat
#   near-ceiling estimates around D~200 as a touch low; the HARD band and the
#   FLOOR_HIT alert exist precisely so a small under-estimate cannot silently
#   push a real run over the red line.
#
# *** NOT WIRED -- live flip gated on the dip per R-S49-3. ***
#   This module is ARMED BUT UNWIRED: built and self-tested, but its output
#   MUST NOT be consumed by any live MAD run until the V2 dip clears the gate.
#   Do not import this into mad_protocol.py or any live path yet.
# ============================================================

# --- verified constants (P3-SOLVER, run 7db741c6 grid, <= 2.73% error) ---
FIXED          = 57300
PER_A_BASE     = 397.25
PER_A_PER_CHAR = 1.3683

# --- settings (James-gated) ---
TARGET      = 85000   # aim per-run token budget
HARD        = 90000   # hard band ceiling before we floor the depth
D_MAX       = 400     # real-summary ceiling (stored summaries cap ~400-425 chars)
D_FLOOR_AIM = 300     # preferred minimum depth (quality floor we try to hold)
D_FLOOR_MIN = 250     # absolute minimum depth before we raise FLOOR_HIT


def cost(n, d):
    """Estimated per-run MAD token cost for n scored articles at depth d chars."""
    return FIXED + n * (PER_A_BASE + PER_A_PER_CHAR * d)


def compute_depth(n_articles, target=TARGET, hard=HARD, d_max=D_MAX,
                  d_floor_aim=D_FLOOR_AIM, d_floor_min=D_FLOOR_MIN):
    """Return (depth:int, est_cost:int, status:str). N is sacred -- never reduced.
       D is the only free variable. Pure arithmetic, zero Groq, pre-call (R-S48-3).

       status:
         OK         -- depth >= d_floor_aim while at/under target (healthy)
         DRIFT      -- had to dip below target / hold the floor to stay <= hard
         FLOOR_HIT  -- even d_floor_min exceeds hard; ALERT, do not silently ship
    """
    # deepest D that hits a given token ceiling, for the current (fixed) N
    def solve(ceiling):
        return (ceiling - FIXED - n_articles * PER_A_BASE) / (n_articles * PER_A_PER_CHAR)

    d = solve(target)
    if d >= d_max:          return d_max, int(cost(n_articles, d_max)), "OK"
    if d >= d_floor_aim:    return int(d), int(cost(n_articles, int(d))), "OK"
    # target needs sub-300 depth -> try to HOLD 300 within the hard band
    if cost(n_articles, d_floor_aim) <= hard:
        return d_floor_aim, int(cost(n_articles, d_floor_aim)), "DRIFT"
    # 300 won't fit hard -> dial down toward floor_min against the hard ceiling
    d2 = solve(hard)
    if d2 >= d_floor_min:   return int(d2), int(cost(n_articles, int(d2))), "DRIFT"
    # even floor_min exceeds hard -> alert, never silently ship garbage-shallow
    return d_floor_min, int(cost(n_articles, d_floor_min)), "FLOOR_HIT"


if __name__ == "__main__":
    # ============================================================
    # SELF-TEST -- reproduce the P3-SOLVER validated table and prove the
    # dormant guardrail branches fire when pushed out of spec.
    # Asserts the EXACT integer outputs the spec'd code produces.
    # ============================================================
    _fails = []

    def check(label, cond, detail=""):
        ok = bool(cond)
        print(("  [PASS] " if ok else "  [FAIL] ") + label + (("  -- " + detail) if detail else ""))
        if not ok:
            _fails.append(label)

    print("=" * 64)
    print("  mad_budget_solver self-test (ARMED BUT UNWIRED -- R-S49-3)")
    print("=" * 64)

    # ---- validated table: (n, expected_D, expected_status, doc_label_cost) ----
    # doc_label_cost = the human-rounded target from P3-SOLVER; we assert the
    # EXACT code output (int(cost(n,D))) and report the delta to the doc label.
    print("\n(1) validated table  [n -> D / est_cost / status]")
    # Re-derived @ FIXED=57300 (S52). At the higher fixed overhead the curve hits
    # the bands far sooner: trimming begins ~N=30, OK->DRIFT at N=35, FLOOR_HIT at
    # N>=45. doc_cost = exact int(cost(n,D)) for the chosen D (delta 0, tol kept @2).
    table = [
        # n,  expD, expStatus,   doc_cost, doc_tol
        (15,  400,  "OK",        71468,    2),
        (30,  384,  "OK",        84980,    2),
        (34,  305,  "OK",        84995,    2),
        (39,  300,  "DRIFT",     88801,    2),  # hold-300 band
        (45,  250,  "FLOOR_HIT", 90569,    2),  # was OK/400 pre-recalibration
        (60,  250,  "FLOOR_HIT", 101659,   2),  # was OK/310 pre-recalibration
        (31,  362,  "OK",        84969,    2),  # today's real run (re-derived)
    ]
    for n, expD, expS, doc_cost, doc_tol in table:
        d, est, st = compute_depth(n)
        # exact: depth, status, and internal cost-consistency at the chosen int D
        check(f"N={n}: D == {expD}", d == expD, f"got D={d}")
        check(f"N={n}: status == {expS}", st == expS, f"got {st}")
        check(f"N={n}: est == int(cost(n,D)) (self-consistent)",
              est == int(cost(n, d)), f"est={est} vs int(cost)={int(cost(n,d))}")
        check(f"N={n}: est ~ {doc_cost} (+/-{doc_tol})",
              abs(est - doc_cost) <= doc_tol, f"est={est}, delta={est-doc_cost}")

    # ---- guardrails fire when pushed out of spec (@ FIXED=57300) ----
    print("\n(2) dormant guardrail branches activate under pressure")
    # N=42: target needs sub-300 depth and cost(42,300) busts hard -> dial down
    # toward floor against the hard ceiling -> DRIFT at D=int(solve(hard))=278.
    d, est, st = compute_depth(42)
    check("N=42: status == DRIFT (sub-300 hard-ceiling dial-down)", st == "DRIFT", f"D={d}, est={est}, st={st}")
    check("N=42: D == 278", d == 278, f"got D={d}")
    # N=65: even d_floor_min exceeds hard -> FLOOR_HIT alert. NOTE: this INVERTS vs
    # pre-recalibration, where N=65 held 300/DRIFT; the higher fixed overhead floors it.
    d, est, st = compute_depth(65)
    check("N=65: status == FLOOR_HIT (floored at d_floor_min)", st == "FLOOR_HIT", f"D={d}, est={est}, st={st}")
    check("N=65: D == D_FLOOR_MIN (250)", d == D_FLOOR_MIN, f"got D={d}")
    # N=80: deeper into FLOOR_HIT territory -- still floored at 250.
    d, est, st = compute_depth(80)
    check("N=80: status == FLOOR_HIT (floored at d_floor_min)", st == "FLOOR_HIT", f"D={d}, est={est}, st={st}")
    check("N=80: D == D_FLOOR_MIN (250)", d == D_FLOOR_MIN, f"got D={d}")

    # ---- N is sacred: compute_depth never returns or reduces N ----
    print("\n(3) N is sacred -- only D moves")
    n_in = 31
    out = compute_depth(n_in)
    check("output is (depth, cost, status) -- no N field returned", len(out) == 3, str(out))
    # depth is a function of N and never equals/reduces N's role; prove monotonic:
    # larger N -> shallower or equal chosen depth (D drops, N untouched).
    d_small, _, _ = compute_depth(20)
    d_large, _, _ = compute_depth(60)
    check("larger N yields shallower-or-equal D (N untouched, D absorbs the load)",
          d_large <= d_small, f"D(20)={d_small} vs D(60)={d_large}")

    print("\n" + "=" * 64)
    if _fails:
        print(f"  FIRST FAILURE: {_fails[0]}   ({len(_fails)} total)")
    else:
        print("  ALL PASS")
    print("=" * 64)
    import sys
    sys.exit(0 if not _fails else 1)
