content = open('ai_engine/main.py', encoding='utf-8').read()
old = 'duplicate = check_recent_duplicate(top_articles, hours=2, overlap_threshold=0.7)'
new = 'duplicate = check_recent_duplicate(top_articles, hours=6, overlap_threshold=0.7)'
result = content.replace(old, new)
open('ai_engine/main.py', 'w', encoding='utf-8').write(result)
print('Done:', content.count(old))
