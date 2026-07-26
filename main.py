from providers import get_all_deals
from telegram import send_message
from relevance import score
from settings import SEARCH
from dedup_store import load_sent, save_sent, filter_unsent, mark_sent


def build_message(deal):

    icon = "📦" if deal.deal_type == "package" else "✈️"

    lines = [
        f"{icon} {deal.title}"
    ]

    if deal.deal_type == "package":
        lines.append("(דיל חבילה משוער - טיסה+לינה. בדוק ידנית דירוג/כוכבים/מיקום המלון)")

    if deal.destination:
        lines.append(f"📍 יעד: {deal.destination}")

    if deal.price is not None:
        currency = deal.currency or ""
        lines.append(f"💰 מחיר: {currency}{deal.price}")

    if deal.source:
        lines.append(f"📰 מקור: {deal.source}")

    lines.append(f"⭐ ציון: {score(deal)}")

    if deal.link:
        lines.append("")
        lines.append(deal.link)

    return "\n".join(lines)


def remove_duplicates(deals):

    seen = set()
    result = []

    for deal in deals:

        key = (
            (deal.link or "").strip().lower(),
            (deal.title or "").strip().lower()
        )

        if key in seen:
            continue

        seen.add(key)
        result.append(deal)

    return result


def main():

    print("========== DEBUG ==========")

    deals = get_all_deals()

    print(f"Deals returned: {len(deals)}")

    if not deals:
        print("No deals found.")
        return

    deals = remove_duplicates(deals)

    print(f"After duplicates: {len(deals)}")

    sent_keys = load_sent()
    deals = filter_unsent(deals, sent_keys)

    print(f"After removing already-sent: {len(deals)}")

    deals.sort(key=score, reverse=True)

    sent = 0
    newly_sent = []

    for deal in deals:

        s = score(deal)

        print(f"[{s}] {deal.title}")

        if s < 60:
            continue

        send_message(build_message(deal))
        newly_sent.append(deal)
        sent += 1

        if sent >= SEARCH["max_results"]:
            break

    if newly_sent:
        sent_keys = mark_sent(newly_sent, sent_keys)
        save_sent(sent_keys)

    print(f"Sent {sent} deals")
    print("========== END ==========")


if __name__ == "__main__":
    main()
