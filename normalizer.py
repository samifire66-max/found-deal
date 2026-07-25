from deal import Deal

from extractor import extract_price
from extractor import extract_destination


def normalize(data):

    title = data.get("title", "")
    summary = data.get("summary", "")

    text = f"{title}\n{summary}"

    price, currency = extract_price(text)
    destination = extract_destination(text)

    return Deal(
        title=title,
        link=data.get("link", ""),
        source=data.get("source", ""),
        destination=destination or "",
        price=price,
        currency=currency or "",
        published=data.get("published", ""),
        summary=summary,
    )
