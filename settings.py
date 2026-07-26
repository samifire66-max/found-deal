"""
טוען את הדרישות מתוך config.json (קובץ יחיד שאפשר לערוך בלי לגעת בקוד
פייתון - ראו README, סעיף "עריכת הדרישות").

אם config.json חסר או פגום, נופלים חזרה לברירות מחדל סבירות כדי
שהריצה לא תיפול.
"""

import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

DEFAULTS = {
    "flights": {
        "max_price_usd": 300,
        "telegram_channels": ["secretflights"],
        "max_results": 10,
    },
    "packages": {
        "max_total_price_ils": 4000,
        "max_exception_price_ils": 4200,
    },
}


def _load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARNING: could not read config.json ({e}), using defaults")
        return {}


_config = _load_config()

_flights = {**DEFAULTS["flights"], **_config.get("flights", {})}
_packages = {**DEFAULTS["packages"], **_config.get("packages", {})}

# נשמר בשם SEARCH (ותומך במפתחות הישנים) כדי שהמודולים הקיימים
# (relevance.py, main.py) ימשיכו לעבוד בלי שינוי מבני
SEARCH = {
    "max_price_usd": _flights["max_price_usd"],
    "telegram_channels": _flights["telegram_channels"],
    "max_results": _flights["max_results"],
    "max_price": _packages["max_total_price_ils"],
    "max_price_exception": _packages["max_exception_price_ils"],
}

# גישה נוחה גם לחלק ה"search" המלא (יעדים, נוסעים, כללי עבודה וכו')
# - עדיין לא כולם בשימוש אוטומטי בקוד, אבל זמינים אם תרצה להרחיב
FULL_CONFIG = _config
