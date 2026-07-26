HOTEL_WORDS = [
    "hotel",
    "hostel",
    "resort",
    "apartment",
    "apartments",
    "villa",
    "suite",
    "double room",
    "premier inn",
    "intercontinental",
    "leonardo",
    "eurostars",
    # עברית
    "מלון",
    "מלונות",
    "הוטל",
    "סוויטה",
    "חדר במלון",
    "חדרים",
    "וילה",
    "צימר",
    "אכסניה",
]

NOT_FLIGHT_WORDS = [
    "train",
    "rail",
    "railway",
    "express",
    "cruise",
    "ferry",
    # עברית
    "רכבת",
    "שייט",
    "מעבורת",
]

FLIGHT_WORDS = [
    "flight",
    "flights",
    "airfare",
    "fare",
    "round trip",
    "return",
    "non-stop",
    "nonstop",
    "direct flight",
    "ryanair",
    "wizz",
    "wizzair",
    "easyjet",
    "pegasus",
    "el al",
    "aegean",
    "lufthansa",
    "boarding",
    # עברית - מילים ושמות חברות תעופה שמופיעים בערוצי דילים ישראליים
    "טיסה",
    "טיסות",
    "טיסת",
    "כרטיס טיסה",
    "כרטיסי טיסה",
    "הלוך וחזור",
    "ישירות",
    "טיסה ישירה",
    "טיסות ישירות",
    "אל על",
    "ארקיע",
    "ישראייר",
    "וויז אייר",
    "פגסוס",
    "איתיחאד",
    "לופט",
    "לוט",
    "איטה איירווייז",
    "חברת תעופה",
]


def is_flight(text: str) -> bool:
    if not text:
        return False

    text = text.lower()

    for word in HOTEL_WORDS:
        if word in text:
            return False

    for word in NOT_FLIGHT_WORDS:
        if word in text:
            return False

    for word in FLIGHT_WORDS:
        if word in text:
            return True

    return False
