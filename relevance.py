from flight_detector import is_flight
from settings import SEARCH

EUROPE = {
    "Rome",
    "Milan",
    "Athens",
    "Larnaca",
    "Paphos",
    "Prague",
    "Budapest",
    "Vienna",
    "Berlin",
    "Paris",
    "London",
    "Barcelona",
    "Madrid",
    "Lisbon",
    "Amsterdam",
    "Dubrovnik",
    "Sofia",
    "Bucharest",
    "Warsaw",
    "Krakow",
    "Naples",
    "Venice",
}


def is_israel_departure_source(deal):
    """
    Deals scraped from our curated Israeli Telegram channels (see
    sources.py / TELEGRAM_CHANNELS) are already guaranteed to be
    flights departing from Israel - the channel itself only posts
    those. So we don't need to find "TLV"/"Tel Aviv" text in the
    post itself (which is written in Hebrew and won't contain those
    English strings anyway).
    """
    return (deal.source or "").startswith("Telegram:")


def score(deal):

    title = (deal.title or "") + " " + (deal.summary or "")

    if not is_flight(title):
        return 0

    score = 0

    title_lower = title.lower()

    israel_departure = is_israel_departure_source(deal)

    if israel_departure:
        # הערוץ עצמו כבר מסונן לטיסות מישראל
        score += 60
    else:
        if "tlv" in title_lower:
            score += 60
        if "tel aviv" in title_lower:
            score += 60
        if "ben gurion" in title_lower:
            score += 60

    if deal.destination in EUROPE:
        score += 10

    # ניקוד לפי מחיר לעומת סף התקציב שהוגדר (settings.py -> MAX_PRICE_USD)
    if deal.price is not None:
        max_price = SEARCH.get("max_price_usd", 300)

        if deal.price > max_price:
            # יקר מדי - לא רלוונטי, לא משנה כמה "טוב" הדיל אחרת
            return 0

        if deal.price <= max_price * 0.35:
            score += 40
        elif deal.price <= max_price * 0.65:
            score += 25
        elif deal.price <= max_price:
            score += 10

    usa = [
        "new york",
        "miami",
        "orlando",
        "chicago",
        "las vegas",
        "los angeles",
        "dallas",
        "houston",
        "san francisco",
    ]

    if not israel_departure:
        for city in usa:
            if city in title_lower:
                score -= 100

    return score


def is_relevant(deal):
    return score(deal) >= 60
