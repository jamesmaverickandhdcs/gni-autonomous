#!/bin/bash
# ============================================================
# GNI Autonomous (QS) — preflight.sh
# Run at session START before any work (GNI-R-206)
# All 6 files must show OK before proceeding
# ============================================================
echo "===== GNI AUTONOMOUS PRE-FLIGHT CHECKLIST ====="
echo ""

echo "1. File Identity Check:"
head -6 ai_engine/main.py                | grep -q "datetime"            && echo "   main.py OK"               || echo "   WRONG FILE! main.py"
head -3 ai_engine/mad_runner.py          | grep -q "MAD\|mad\|runner"    && echo "   mad_runner.py OK"         || echo "   WRONG FILE! mad_runner.py"
head -6 ai_engine/monitoring_pipeline.py | grep -q "monitoring_pipeline"  && echo "   monitoring_pipeline.py OK" || echo "   WRONG FILE! monitoring_pipeline.py"
head -6 ai_engine/quota_guard.py         | grep -q "quota_guard"          && echo "   quota_guard.py OK"        || echo "   WRONG FILE! quota_guard.py"
head -3 ai_engine/adaptive_pipeline.py   | grep -q "adaptive\|Adaptive"   && echo "   adaptive_pipeline.py OK"  || echo "   WRONG FILE! adaptive_pipeline.py"
head -6 ai_engine/notifications/telegram_notifier.py | grep -q "GNI Telegram" && echo "   telegram_notifier.py OK" || echo "   WRONG FILE! telegram_notifier.py"
echo ""

echo "2. Syntax Check:"
python -c "
import ast, sys
files = [
    'ai_engine/main.py',
    'ai_engine/mad_runner.py',
    'ai_engine/monitoring_pipeline.py',
    'ai_engine/quota_guard.py',
    'ai_engine/adaptive_pipeline.py',
    'ai_engine/notifications/telegram_notifier.py',
]
ok = True
for f in files:
    try:
        ast.parse(open(f, encoding='utf-8-sig').read())
        print(f'   SYNTAX OK: {f}')
    except SyntaxError as e:
        print(f'   SYNTAX ERROR: {f} -- {e}')
        ok = False
if not ok:
    sys.exit(1)
"
echo ""

echo "3. Model Names (Provider Check):"
echo "   Groq model (P3 Articles):"
grep -n "llama-3.3-70b-versatile" ai_engine/main.py | head -3 || echo "   WARNING: llama-3.3-70b-versatile not found in main.py"
echo "   Cerebras model (P4 MAD + Adaptive):"
grep -rn "llama3.1-8b" ai_engine/mad_runner.py ai_engine/adaptive_pipeline.py 2>/dev/null | head -3 || echo "   WARNING: llama3.1-8b not found"
echo "   NOT gpt-oss-120b (must be absent):"
grep -rn "gpt-oss-120b" ai_engine/*.py 2>/dev/null && echo "   WARNING: gpt-oss-120b found — wrong model!" || echo "   OK — gpt-oss-120b absent"
echo ""

echo "4. Telegram Routing Check (no old TELEGRAM_CHAT_ID):"
grep -rn "TELEGRAM_CHAT_ID" ai_engine/ --include="*.py" 2>/dev/null && echo "   WARNING: Old TELEGRAM_CHAT_ID found!" || echo "   OK — all renamed to TELEGRAM_QSChannel_ID"
echo ""

echo "5. YML Timeouts:"
grep -n "timeout-minutes" .github/workflows/gni_pipeline.yml .github/workflows/gni_mad.yml .github/workflows/gni_adaptive.yml .github/workflows/gni_heartbeat.yml .github/workflows/gni_selfcheck.yml
echo ""

echo "6. Git Status:"
git status
echo ""

echo "===== PRE-FLIGHT COMPLETE ====="
echo "All OK? → Proceed with session"
echo "Any WARN/ERROR? → Fix before touching any code!"
