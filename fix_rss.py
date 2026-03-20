content = open('ai_engine/collectors/rss_collector.py', encoding='utf-8').read()
old = '    {\n        "name": "DW News",\n        "url": "https://rss.dw.com/xml/rss-en-world",\n        "bias": "Western Liberal"\n    },\n]'
new = '''    {
        "name": "DW News",
        "url": "https://rss.dw.com/xml/rss-en-world",
        "bias": "Western Liberal"
    },
    {
        "name": "Reuters",
        "url": "https://feeds.reuters.com/reuters/worldNews",
        "bias": "Western Liberal"
    },
    {
        "name": "AP News",
        "url": "https://feeds.apnews.com/rss/apf-topnews",
        "bias": "Western Liberal"
    },
    {
        "name": "South China Morning Post",
        "url": "https://www.scmp.com/rss/91/feed",
        "bias": "Asian Perspective"
    },
    {
        "name": "The Hindu",
        "url": "https://www.thehindu.com/news/international/feeder/default.rss",
        "bias": "Asian Perspective"
    },
    {
        "name": "France 24",
        "url": "https://www.france24.com/en/rss",
        "bias": "Western Liberal"
    },
]'''
result = content.replace(old, new)
open('ai_engine/collectors/rss_collector.py', 'w', encoding='utf-8').write(result)
print('Done - replacements:', content.count(old))
