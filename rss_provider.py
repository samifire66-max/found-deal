import feedparser

from normalizer import normalize
from sources import SOURCES


def get_rss_deals():

    deals = []

    print("\n========== RSS DEBUG ==========\n")

    for source in SOURCES:

        print(f"Reading: {source['name']}")
        print(f"URL: {source['url']}")

        try:
            feed = feedparser.parse(source["url"])

            if getattr(feed, "bozo", False):
                print(f"  ⚠ Feed parsing warning: {feed.bozo_exception}")

            if not feed.entries:
                print("  -> 0 entries\n")
                continue

            print(f"  -> {len(feed.entries)} entries")

            added = 0

            for entry in feed.entries:

                deal = normalize(
                    {
                        "title": entry.get("title", ""),
                        "link": entry.get("link", ""),
                        "source": source["name"],
                        "published": entry.get("published", ""),
                        "summary": entry.get("summary", ""),
                    }
                )

                if deal:
                    deals.append(deal)
                    added += 1

            print(f"  -> Added {added} deals\n")

        except Exception as e:
            print(f"  ERROR: {e}\n")

    print("========== END RSS DEBUG ==========\n")
    print(f"Total deals collected: {len(deals)}\n")

    return deals
