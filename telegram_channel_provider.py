"""
Scrapes the public web preview of a Telegram channel (t.me/s/<channel>).
This works for any public channel with no login/API token required -
it's the same page you'd see in a browser without being signed in.

Used to pull real flight-deal posts from Israeli deal channels such as
@secretflights, which publish daily flights departing from Israel
(unlike the generic English-language blogs in sources.py, which mostly
cover flights INTO Tel Aviv rather than out of it).
"""

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def get_telegram_channel_deals(channel):
    """Fetch and parse recent posts from a public Telegram channel."""

    url = f"https://t.me/s/{channel}"
    deals = []

    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"  ERROR fetching {url}: {e}")
        return deals

    soup = BeautifulSoup(response.text, "html.parser")
    messages = soup.select("div.tgme_widget_message_wrap")

    for msg in messages:
        text_div = msg.select_one(".tgme_widget_message_text")
        if not text_div:
            continue

        text = text_div.get_text("\n", strip=True)
        if not text:
            continue

        post_wrap = msg.select_one(".tgme_widget_message")
        data_post = post_wrap.get("data-post") if post_wrap else None
        link = f"https://t.me/{data_post}" if data_post else url

        date_tag = msg.select_one("time")
        published = date_tag.get("datetime", "") if date_tag else ""

        lines = [line for line in text.split("\n") if line.strip()]
        title = lines[0] if lines else text[:80]

        deals.append(
            {
                "title": title,
                "link": link,
                "source": f"Telegram: {channel}",
                "published": published,
                "summary": text,
            }
        )

    return deals


def get_all_telegram_deals(channels):
    """Fetch deals from multiple channels."""

    all_deals = []

    for channel in channels:
        print(f"Reading Telegram channel: {channel}")
        channel_deals = get_telegram_channel_deals(channel)
        print(f"  -> {len(channel_deals)} posts")
        all_deals.extend(channel_deals)

    return all_deals
