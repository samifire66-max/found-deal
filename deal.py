from dataclasses import dataclass


@dataclass
class Deal:
    title: str
    link: str
    source: str

    destination: str = ""
    price: int | None = None
    currency: str = ""
    published: str = ""

    # "flight" or "package" (flight+hotel) or "" if not yet classified
    deal_type: str = ""

    # חדש
    summary: str = ""
