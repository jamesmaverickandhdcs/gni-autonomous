content = open('ai_engine/analysis/supabase_saver.py', encoding='utf-8').read()
old = '            "mad_confidence": float(report.get("mad_confidence", 0.0)),'
new = '            "mad_confidence": float(report.get("mad_confidence", 0.0)),\n            "mad_reasoning": report.get("mad_reasoning", ""),'
result = content.replace(old, new)
open('ai_engine/analysis/supabase_saver.py', 'w', encoding='utf-8').write(result)
print('Done - replacements:', content.count(old))
