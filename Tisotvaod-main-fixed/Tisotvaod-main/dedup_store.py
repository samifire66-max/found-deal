"""
Keeps track of which deals were already sent to Telegram, so the bot
doesn't spam the same deal again on every run (it runs every few hours,
and the same cheap flight often stays posted/relevant for days).

Persisted to a local JSON file. In GitHub Actions this file is kept
between runs via actions/cache (see .github/workflows/search.yml).
"""

import json
import os

STORE_PATH = os.path.join(os.path.dirname(__file__), "sent_deals.json")

# כמה קישורים אחרונים לזכור (כדי שהקובץ לא יגדל לנצח)
MAX_ENTRIES = 500


def _deal_key(deal):
    return (deal.link or "").strip().lower() or (deal.title or "").strip().lower()


def load_sent():
    if not os.path.exists(STORE_PATH):
        return set()

    try:
        with open(STORE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("sent", []))
    except (json.JSONDecodeError, OSError):
        return set()


def save_sent(sent_keys):
    trimmed = list(sent_keys)[-MAX_ENTRIES:]

    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump({"sent": trimmed}, f, ensure_ascii=False, indent=2)


def filter_unsent(deals, sent_keys):
    return [d for d in deals if _deal_key(d) not in sent_keys]


def mark_sent(deals, sent_keys):
    for d in deals:
        sent_keys.add(_deal_key(d))
    return sent_keys
