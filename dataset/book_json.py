"""(module) book_json."""

from dataclasses import dataclass


@dataclass
class Book:
    """Data class for request deserialization."""

    kind: str
    full_sort_key: str
    title: str
    url: str
    cover_color: str
    author: str
    cover: str
    epoch: str
    href: str
    has_audio: bool
    genre: str
    simple_thumb: str
    slug: str
    cover_thumb: str
    liked: None
