import feedparser

sources = [
    ("Asia Times",        "https://asiatimes.com/feed/"),
    ("Channel News Asia", "https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml&category=6511"),
    ("The Conversation",  "https://theconversation.com/global/articles.atom"),
    ("Business Standard", "https://www.business-standard.com/rss/home_page_top_stories.rss"),
    ("The Diplomat",      "https://thediplomat.com/feed/"),
]

for name, url in sources:
    try:
        feed = feedparser.parse(url)
        if feed.entries:
            title = feed.entries[0].get("title", "(no title)")[:55]
            bias_field = feed.entries[0].get("link", "")[:40]
            print(f"  OK    {name}: {len(feed.entries)} articles")
            print(f"        Sample: {title}")
        else:
            print(f"  EMPTY {name}: 0 articles (bozo={feed.bozo})")
            print(f"        URL: {url}")
    except Exception as e:
        print(f"  ERR   {name}: {e}")
