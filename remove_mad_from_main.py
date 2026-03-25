# -*- coding: utf-8 -*-
"""
Remove MAD protocol from main.py pipeline.
MAD is now handled by mad_runner.py (gni_mad.yml workflow).
GNI-R-110: Separate pipeline guarantees clean Groq TPM window.
"""
import py_compile
import os

FILE = os.path.join("ai_engine", "main.py")

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

# ── Remove MAD import ────────────────────────────────────────
OLD_IMPORT = "from analysis.mad_protocol import run_mad_protocol, _save_predictions"
NEW_IMPORT = "# MAD protocol moved to mad_runner.py (GNI-R-110 -- separate pipeline)\n# from analysis.mad_protocol import run_mad_protocol, _save_predictions"

# ── Replace MAD execution block with a comment ──────────────
OLD_MAD_BLOCK = """        # -- Step 3c: MAD Protocol ------------------------
        print("\\n???? Step 3c: Running Quadratic MAD Protocol...")
        t0 = time.time()
        # Quadratic MAD: pass ALL relevant articles (301) + report_id for prediction saving
        all_relevant = [a for a in trace if a.get('stage1_passed', False)]
        mad_result = run_mad_protocol(report, all_articles=all_relevant)
        # Unpack all Quadratic MAD fields
        report['mad_bull_case']             = mad_result.get('mad_bull_case', '')
        report['mad_bear_case']             = mad_result.get('mad_bear_case', '')
        report['mad_black_swan_case']        = mad_result.get('mad_black_swan_case', '')
        report['mad_ostrich_case']           = mad_result.get('mad_ostrich_case', '')
        report['mad_verdict']               = mad_result.get('mad_verdict', 'neutral')
        report['mad_confidence']            = mad_result.get('mad_confidence', 0.5)
        report['mad_blind_spot']            = mad_result.get('mad_blind_spot', '')
        report['mad_action_recommendation'] = mad_result.get('mad_action_recommendation', '')
        report['short_focus_threats']       = mad_result.get('short_focus_threats', '')
        report['long_shoot_threats']        = mad_result.get('long_shoot_threats', '')
        report['short_verify_days']         = mad_result.get('short_verify_days', 14)
        report['long_verify_days']          = mad_result.get('long_verify_days', 180)
        report['mad_round1_positions']      = mad_result.get('mad_round1_positions', {})
        report['mad_round2_positions']      = mad_result.get('mad_round2_positions', {})
        report['mad_round3_positions']      = mad_result.get('mad_round3_positions', {})
        report['mad_arb_feedbacks']         = mad_result.get('mad_arb_feedbacks', {})
        report['mad_historian_case']        = mad_result.get('mad_historian_case', '')
        report['mad_risk_case']             = mad_result.get('mad_risk_case', '')"""

NEW_MAD_BLOCK = """        # -- Step 3c: MAD Protocol (MOVED to mad_runner.py) ----
        # GNI-R-110: MAD runs as separate pipeline (gni_mad.yml)
        # 5 minutes after main pipeline -- clean Groq TPM window
        # mad_runner.py reads this report from Supabase and updates it
        print("\\n???? Step 3c: MAD Protocol running separately (gni_mad.yml)")
        print("   GNI-R-110: MAD will run in 5 min with clean Groq TPM window")
        t0 = time.time()
        # Set safe defaults -- mad_runner.py will overwrite these
        report['mad_bull_case']             = ''
        report['mad_bear_case']             = ''
        report['mad_black_swan_case']       = ''
        report['mad_ostrich_case']          = ''
        report['mad_verdict']               = 'pending'
        report['mad_confidence']            = 0.5
        report['mad_blind_spot']            = ''
        report['mad_action_recommendation'] = ''
        report['short_focus_threats']       = ''
        report['long_shoot_threats']        = ''
        report['short_verify_days']         = 14
        report['long_verify_days']          = 180
        report['mad_round1_positions']      = {}
        report['mad_round2_positions']      = {}
        report['mad_round3_positions']      = {}
        report['mad_arb_feedbacks']         = {}
        report['mad_historian_case']        = ''
        report['mad_risk_case']             = ''"""

# ── Remove _save_predictions call (now in mad_runner.py) ────
OLD_PREDICTIONS = """            # Save debate predictions now that we have real report_id
            _save_predictions(
                report_id=report_id,
                short=report.get('short_focus_threats', ''),
                long_s=report.get('long_shoot_threats', ''),
                short_days=report.get('short_verify_days', 14),
                long_days=report.get('long_verify_days', 180),
                round3=report.get('mad_round3_positions', {}),
            )"""

NEW_PREDICTIONS = """            # Predictions saved by mad_runner.py after MAD completes
            # GNI-R-110: mad_runner.py handles prediction saving"""

# ── Remove MAD timing from step_timings print ───────────────
OLD_MAD_TIMING = "        report['mad_reasoning']  = mad_result.get('mad_reasoning', '')\n"
NEW_MAD_TIMING = "        report['mad_reasoning']  = ''\n"

# ── Update MAD verdict print line ───────────────────────────
OLD_VERDICT_PRINT = """        step_timings["mad"] = round(time.time() - t0, 2)
        print(f"   ? MAD verdict: {report['mad_verdict']} ({report['mad_confidence']:.0%} confidence)")
        update_mad_confidence(prompt_version, report['mad_confidence'])"""

NEW_VERDICT_PRINT = """        step_timings["mad"] = round(time.time() - t0, 2)
        print("   ? MAD pending -- mad_runner.py will run in 5 minutes")"""

# ── Apply all fixes ──────────────────────────────────────────
fixes = [
    ("import",           OLD_IMPORT,          NEW_IMPORT),
    ("mad_block",        OLD_MAD_BLOCK,        NEW_MAD_BLOCK),
    ("predictions",      OLD_PREDICTIONS,      NEW_PREDICTIONS),
    ("mad_reasoning",    OLD_MAD_TIMING,       NEW_MAD_TIMING),
    ("verdict_print",    OLD_VERDICT_PRINT,    NEW_VERDICT_PRINT),
]

new_content = content
errors = []
for name, old, new in fixes:
    if old not in new_content:
        errors.append(name)
        print("NOT FOUND: " + name)
    else:
        new_content = new_content.replace(old, new, 1)
        print("OK  " + name)

if errors:
    print("")
    print("ERROR: " + str(len(errors)) + " block(s) not found: " + str(errors))
    print("The file may have changed. Show this error to Claude.")
    exit(1)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(new_content)
print("\nOK  Written: " + FILE)

try:
    py_compile.compile(FILE, doraise=True)
    print("OK  py_compile passed")
except py_compile.PyCompileError as e:
    print("FAIL: " + str(e))
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print("Original restored. Do NOT push.")
    exit(1)

print("")
print("=" * 60)
print("DONE. MAD removed from main.py pipeline.")
print("")
print("What changed:")
print("  - MAD import commented out")
print("  - MAD execution replaced with 'pending' defaults")
print("  - _save_predictions removed (now in mad_runner.py)")
print("  - Main pipeline now ~3 min (was ~6 min)")
print("  - MAD verdict shows 'pending' until mad_runner.py updates it")
print("")
print("Next steps:")
print("  1. Copy mad_runner.py to ai_engine/mad_runner.py")
print("  2. Copy gni_mad.yml to .github/workflows/gni_mad.yml")
print("  3. npm run build")
print("  4. git add -A")
print('  5. git commit -m "separate MAD pipeline -- GNI-R-110"')
print("  6. git push")
print("=" * 60)
