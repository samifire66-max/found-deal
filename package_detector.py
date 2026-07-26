"""
Classifies a deal's text as one of: "flight", "package", or None (irrelevant).

flight_detector.is_flight() rejects any text that mentions hotel/accommodation
words - that's correct for finding pure flight deals, but it also means real
flight+hotel PACKAGE posts (which legitimately mention both) get thrown away
entirely. This module restores those by checking for flight- AND
accommodation-related words together.
"""

from flight_detector import FLIGHT_WORDS, HOTEL_WORDS, NOT_FLIGHT_WORDS


def _contains_any(text, words):
    return any(word in text for word in words)


def classify(text):
    if not text:
        return None

    text = text.lower()

    if _contains_any(text, NOT_FLIGHT_WORDS):
        return None

    has_flight = _contains_any(text, FLIGHT_WORDS)
    has_hotel = _contains_any(text, HOTEL_WORDS)

    if has_flight and has_hotel:
        return "package"

    if has_flight:
        return "flight"

    return None
