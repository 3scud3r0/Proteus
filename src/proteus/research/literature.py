"""Locally tracked scientific references; no fabricated citation lookup."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Reference:
    title: str
    authors: str
    url: str
    verified: bool = False
