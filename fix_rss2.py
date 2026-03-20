content = open('ai_engine/collectors/rss_collector.py', encoding='utf-8').read()
old = '''    {
        "name": "Reuters",
        "url": "https://feeds.reuters.com/reuters/worldNews",
        "bias": "Western Liberal"
    },
    {
        "name": "AP News",
        "url": "https://feeds.apnews.com/rss/apf-topnews",
        "bias": "Western Liberal"
    },'''
new = '''    {
        "name": "Middle East Eye",
        "url": "https://www.middleeasteye.net/rss",
        "bias": "Non-Western"
    },
    {
        "name": "USNI News",
        "url": "https://news.usni.org/feed",
        "bias": "Western Liberal"
    },
    {
        "name": "Straits Times",
        "url": "https://www.straitstimes.com/news/world/rss.xml",
        "bias": "Asian Perspective"
    },
    {
        "name": "Eye on the Arctic",
        "url": "https://www.rcinet.ca/eye-on-the-arctic/feed/",
        "bias": "Western Liberal"
    },'''
result = content.replace(old, new)
open('ai_engine/collectors/rss_collector.py', 'w', encoding='utf-8').write(result)
print('Done - replacements:', content.count(old))
