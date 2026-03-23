import feedparser

sources = [
    ("Chatham House",      "https://www.chathamhouse.org/rss.xml"),
    ("Radio Free Asia",    "https://www.rfa.org/english/RSS"),
    ("Human Rights Watch", "https://www.hrw.org/rss.xml"),
    ("Freedom House",      "https://freedomhouse.org/rss.xml"),
    ("Reuters World",      "https://feeds.reuters.com/reuters/worldNews"),
    ("AP News",            "https://rsshub.app/apnews/topics/apf-intlnews"),
    ("AP News alt",        "https://feeds.apnews.com/rss/apf-intlnews"),
    ("VOA News",           "https://www.voanews.com/api/zmpqoemee$"),
    ("VOA alt",            "https://www.voanews.com/rss/world"),
    ("Reporters w/o Borders","https://rsf.org/en/rss.xml"),
    ("The Guardian World", "https://www.theguardian.com/world/rss"),
    ("Independent",        "https://www.independent.co.uk/news/world/rss"),
    ("Amnesty Intl",       "https://www.amnesty.org/en/feed/"),
    ("Open Democracy",     "https://www.opendemocracy.net/en/rss.xml"),
    ("Global Voices",      "https://globalvoices.org/feed/"),
]

print("Testing 15 candidates for RSS availability...\n")
ok = []
empty = []

for name, url in sources:
    try:
        feed = feedparser.parse(url)
        if feed.entries:
            title = feed.entries[0].get("title", "(no title)")[:55]
            count = len(feed.entries)
            ok.append((name, count, title, url))
            print(f"  OK    {name}: {count} articles")
            print(f"        Sample: {title}")
        else:
            empty.append((name, url))
            print(f"  EMPTY {name}: 0 articles (bozo={feed.bozo})")
    except Exception as e:
        empty.append((name, url))
        print(f"  ERR   {name}: {str(e)[:60]}")

print(f"\n{'='*50}")
print(f"WORKING: {len(ok)} sources")
for name, count, title, url in ok:
    print(f"  {name}: {count} articles")
print(f"\nNOT WORKING: {len(empty)} sources")
for name, url in empty:
    print(f"  {name}")
