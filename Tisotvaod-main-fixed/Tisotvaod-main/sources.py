# מקורות RSS כלליים (אנגלית) - לרוב מסקרים טיסות *אל* יעדים מארה"ב/אירופה,
# ולכן רלוונטיים רק אם הם במפורש מזכירים TLV/Tel Aviv/Ben Gurion.
# נשארים כמקור משני בלבד.
SOURCES = [
    {
        "name": "The Flight Deal",
        "url": "https://www.theflightdeal.com/feed/",
        "weight": 10,
    },
    {
        "name": "Travel-Dealz",
        "url": "https://travel-dealz.com/feed/",
        "weight": 10,
    },
    {
        "name": "Secret Flying",
        "url": "https://www.secretflying.com/feed/",
        "weight": 9,
    },
    {
        "name": "Fly4Free",
        "url": "https://www.fly4free.com/feed/",
        "weight": 9,
    },
    {
        "name": "Holiday Pirates",
        "url": "https://www.holidaypirates.com/feed",
        "weight": 8,
    },
]

# ערוצי טלגרם ישראליים ציבוריים - המקור העיקרי בפועל, כי הם מפרסמים
# דילי טיסות אמיתיים שיוצאים מישראל על בסיס יומי.
# הרשימה גם מוגדרת ב-settings.py (SEARCH["telegram_channels"]); זה כאן
# בשביל תיעוד/שימוש עתידי נוח מתוך sources.py בלבד אם ירצו.
TELEGRAM_CHANNELS = [
    "secretflights",
]
