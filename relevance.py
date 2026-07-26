from package_detector import classify
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

# המרה גסה מאוד דולר->שקל, לצורך השוואה בלבד כשדיל חבילה מתומחר
# בדולרים ולא בשקלים (אין לנו מקור שער חליפין חי כרגע)
USD_TO_ILS = 3.7


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


def _score_flight(deal, title_lower):

    score = 0
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


def _score_package(deal, title_lower):
    """
    ניקוד לדילי חבילה (טיסה+מלון). חשוב: אין לנו כרגע מקור נתונים
    אמיתי שמאמת דירוג מלון/כוכבים/מיקום - זה best-effort, מבוסס רק
    על מה שכתוב בטקסט הפוסט. ראו README לגבי המגבלה הזו.
    """

    israel_departure = is_israel_departure_source(deal)

    if israel_departure:
        base_score = 70
    else:
        # מקור חיצוני (RSS) - כמו בדילי טיסה, חייבים אזכור מפורש
        # של ישראל/תל אביב/נתב"ג, אחרת זו סתם חבילה זרה (לדוגמה
        # "טיסות מוינה" שאין לה שום קשר אלינו)
        if not (
            "tlv" in title_lower
            or "tel aviv" in title_lower
            or "ben gurion" in title_lower
        ):
            return 0
        base_score = 40

    if deal.price is None:
        # אין מחיר בטקסט - עדיין נציג את הדיל (עדיף להתריע ולתת
        # לך לבדוק ידנית, מאשר להחמיץ חבילה טובה), אך בניקוד נמוך יותר
        return base_score - 10

    price_ils = deal.price
    if (deal.currency or "").strip() in ("$", "usd", "USD"):
        price_ils = deal.price * USD_TO_ILS

    max_price = SEARCH.get("max_price", 4000)
    max_price_exception = SEARCH.get("max_price_exception", 4200)

    if price_ils <= max_price:
        return base_score + 30

    if price_ils <= max_price_exception:
        return base_score + 10

    # מעל התקציב, כולל החריגה - לא רלוונטי
    return 0


def score(deal):

    title = (deal.title or "") + " " + (deal.summary or "")
    title_lower = title.lower()

    deal_type = deal.deal_type or classify(title_lower)

    if deal_type == "package":
        return _score_package(deal, title_lower)

    if deal_type == "flight":
        return _score_flight(deal, title_lower)

    return 0


def is_relevant(deal):
    return score(deal) >= 60
