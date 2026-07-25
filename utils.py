from datetime import date, timedelta


def next_weekend_dates():
    today = date.today()

    # Thursday of this or next week
    days_until_thursday = (3 - today.weekday()) % 7
    thursday = today + timedelta(days=days_until_thursday)

    # Sunday after that Thursday
    sunday = thursday + timedelta(days=3)

    return thursday.isoformat(), sunday.isoformat()


def format_price(price):
    return f"₪{price:,.0f}"
