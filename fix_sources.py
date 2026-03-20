import re
content = open('ai_engine/collectors/rss_collector.py', encoding='utf-8').read()
old = """    {
        "name": "South China Morning Post",
        "url": "https://www.scmp.com/rss/91/feed",
        "bias": "Asian Perspective"
    },
    {
        "name": "The Hindu",
        "url": "https://www.thehindu.com/news/international/feeder/default.rss",
        "bias": "Asian Perspective"
    },"""
new = """    {
        "name": "Wired",
        "url": "https://www.wired.com/feed/rss",
        "bias": "Technology"
    },
    {
        "name": "MIT Technology Review",
        "url": "https://www.technologyreview.com/feed/",
        "bias": "Technology"
    },"""
result = content.replace(old, new)
open('ai_engine/collectors/rss_collector.py', 'w', encoding='utf-8').write(result)
print('Done - replacements:', content.count(old))
