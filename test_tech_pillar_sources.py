import feedparser

sources = [
    ("Ars Technica",         "https://feeds.arstechnica.com/arstechnica/index"),
    ("TechCrunch",           "https://techcrunch.com/feed/"),
    ("The Register",         "https://www.theregister.com/headlines.atom"),
    ("IEEE Spectrum",        "https://spectrum.ieee.org/feeds/feed.rss"),
    ("Krebs on Security",    "https://krebsonsecurity.com/feed/"),
    ("Dark Reading",         "https://www.darkreading.com/rss.xml"),
    ("EFF Deeplinks",        "https://www.eff.org/rss/updates.xml"),
    ("Rest of World",        "https://restofworld.org/feed/"),
    ("Protocol",             "https://www.protocol.com/feeds/feed.rss"),
    ("Semiconductor Digest", "https://www.semiconductor-digest.com/feed/"),
    ("Tom's Hardware",       "https://www.tomshardware.com/feeds/all"),
    ("Tech Policy Press",    "https://techpolicy.press/feed/"),
    ("Lawfare",              "https://www.lawfaremedia.org/feed"),
    ("War on the Rocks",     "https://warontherocks.com/feed/"),
]

print("Testing 14 tech pillar candidates...\n")
ok = []
empty = []

for name, url in sources:
    try:
        feed = feedparser.parse(url)
        if feed.entries and not feed.bozo:
            title = feed.entries[0].get("title", "")[:55]
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
print(f"WORKING: {len(ok)}")
for name, count, title, url in ok:
    print(f"  {name}: {count} articles")
print(f"\nNOT WORKING: {len(empty)}")
for name, url in empty:
    print(f"  {name}")
