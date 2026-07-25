from rss_provider import get_rss_deals
from telegram_channel_provider import get_all_telegram_deals
from relevance import is_relevant
from settings import SEARCH


def get_all_deals():

    all_deals = []

    telegram_raw = get_all_telegram_deals(SEARCH.get("telegram_channels", []))
    print(f"Collected from Telegram channels: {len(telegram_raw)}")

    from normalizer import normalize

    for item in telegram_raw:
        deal = normalize(item)
        if deal:
            all_deals.append(deal)

    rss_deals = get_rss_deals()
    print(f"Collected from RSS: {len(rss_deals)}")
    all_deals.extend(rss_deals)

    print(f"Total collected: {len(all_deals)}")

    relevant = []

    for deal in all_deals:

        if is_relevant(deal):
            relevant.append(deal)

    print(f"Relevant deals: {len(relevant)}")

    return relevant
