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
