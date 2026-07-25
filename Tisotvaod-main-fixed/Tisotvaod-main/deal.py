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

    # חדש
    summary: str = ""
