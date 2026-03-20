content = open('ai_engine/main.py', encoding='utf-8').read()
old = "        report['mad_confidence'] = mad_result['mad_confidence']"
new = "        report['mad_confidence'] = mad_result['mad_confidence']\n        report['mad_reasoning']  = mad_result['mad_reasoning']"
result = content.replace(old, new)
open('ai_engine/main.py', 'w', encoding='utf-8').write(result)
print('Done - replacements:', content.count(old))
