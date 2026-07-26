import re

PRICE_REGEX = re.compile(
    r"(₪|\$|€|£)\s?(\d+(?:,\d{3})?)|(\d+(?:,\d{3})?)\s?(₪|\$|€|£)",
    re.IGNORECASE,
)

# מחיר בשקלים כתוב במילים ("1,890 ש"ח" / "1890 שח" / "1890 שקל")
# ולא בסימן ₪ - מאוד נפוץ בפוסטים ישראליים
ILS_TEXT_REGEX = re.compile(
    r"(\d+(?:,\d{3})?)\s?ש[\"'׳״]?ח\b|(\d+(?:,\d{3})?)\s?שקל(?:ים)?",
)

DESTINATIONS = {
    "rome": "Rome",
    "milan": "Milan",
    "bergamo": "Milan",
    "athens": "Athens",
    "thessaloniki": "Thessaloniki",
    "larnaca": "Larnaca",
    "paphos": "Paphos",
    "prague": "Prague",
    "budapest": "Budapest",
    "vienna": "Vienna",
    "berlin": "Berlin",
    "munich": "Munich",
    "frankfurt": "Frankfurt",
    "paris": "Paris",
    "nice": "Nice",
    "london": "London",
    "manchester": "Manchester",
    "barcelona": "Barcelona",
    "madrid": "Madrid",
    "lisbon": "Lisbon",
    "porto": "Porto",
    "amsterdam": "Amsterdam",
    "brussels": "Brussels",
    "warsaw": "Warsaw",
    "krakow": "Krakow",
    "bucharest": "Bucharest",
    "sofia": "Sofia",
    "dubrovnik": "Dubrovnik",
    "zagreb": "Zagreb",
    "split": "Split",
    "naples": "Naples",
    "venice": "Venice",
    "dubai": "Dubai",
    "abu dhabi": "Abu Dhabi",
    "madeira": "Madeira",
    "malta": "Malta",
    "crete": "Crete",
    "heraklion": "Heraklion",
    "rhodes": "Rhodes",
    "sicily": "Sicily",
    "catania": "Catania",
    "palermo": "Palermo",
}

HEBREW_DESTINATIONS = {
    "רומא": "Rome",
    "מילאנו": "Milan",
    "ברגמו": "Milan",
    "אתונה": "Athens",
    "סלוניקי": "Thessaloniki",
    "לרנקה": "Larnaca",
    "פאפוס": "Paphos",
    "פראג": "Prague",
    "בודפשט": "Budapest",
    "וינה": "Vienna",
    "ברלין": "Berlin",
    "מינכן": "Munich",
    "פרנקפורט": "Frankfurt",
    "פריז": "Paris",
    "ניס": "Nice",
    "לונדון": "London",
    "מנצ'סטר": "Manchester",
    "ברצלונה": "Barcelona",
    "מדריד": "Madrid",
    "ליסבון": "Lisbon",
    "פורטו": "Porto",
    "אמסטרדם": "Amsterdam",
    "בריסל": "Brussels",
    "ורשה": "Warsaw",
    "קרקוב": "Krakow",
    "בוקרשט": "Bucharest",
    "סופיה": "Sofia",
    "דוברובניק": "Dubrovnik",
    "זאגרב": "Zagreb",
    "ספליט": "Split",
    "נאפולי": "Naples",
    "ונציה": "Venice",
    "דובאי": "Dubai",
    "אבו דאבי": "Abu Dhabi",
    "מדיירה": "Madeira",
    "מלטה": "Malta",
    "כרתים": "Crete",
    "הרקליון": "Heraklion",
    "רודוס": "Rhodes",
    "סיציליה": "Sicily",
    "קטניה": "Catania",
    "פלרמו": "Palermo",
    "טביליסי": "Tbilisi",
    "באטומי": "Batumi",
    "איסלנד": "Iceland",
    "ניו יורק": "New York",
    "מיאמי": "Miami",
    "שיקגו": "Chicago",
    "לוס אנג'לס": "Los Angeles",
    "זנזיבר": "Zanzibar",
    "בנגקוק": "Bangkok",
    "תאילנד": "Thailand",
    "סאו פאולו": "Sao Paulo",
    "טביליסי": "Tbilisi",
}

TLV_PATTERNS = (
    "tlv",
    "tel aviv",
    "ben gurion",
    "ben-gurion",
    "israel",
    "from israel",
    "departing israel",
    "departing tel aviv",
    "from tel aviv",
    # עברית
    "נתב\"ג",
    "נתבג",
    "תל אביב",
    "מישראל",
    "מנתב\"ג",
)


def clean_text(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"<[^>]+>", " ", text).lower()


def extract_price(text):

    text = clean_text(text)

    m = PRICE_REGEX.search(text)

    if m:
        if m.group(1):
            return int(m.group(2).replace(",", "")), m.group(1)
        return int(m.group(3).replace(",", "")), m.group(4)

    m = ILS_TEXT_REGEX.search(text)

    if m:
        amount = m.group(1) or m.group(2)
        return int(amount.replace(",", "")), "₪"

    return None, None


def extract_destination(text):

    text = clean_text(text)

    found = []

    for key, value in {**DESTINATIONS, **HEBREW_DESTINATIONS}.items():
        if key in text:
            found.append((text.index(key), value))

    if not found:
        return None

    found.sort()

    return found[0][1]


def has_tlv(text):

    text = clean_text(text)

    return any(pattern in text for pattern in TLV_PATTERNS)
