"""Synchronous typed-name event dispatch with explicit error propagation."""
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

@dataclass(frozen=True)
class Event:
    name: str
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[[Event], None]]] = defaultdict(list)

    def subscribe(self, name: str, callback: Callable[[Event], None]) -> None:
        self._subscribers[name].append(callback)

    def emit(self, name: str, **data: Any) -> Event:
        event = Event(name=name, data=data)
        for callback in tuple(self._subscribers.get(name, ())):
            callback(event)
        return event
