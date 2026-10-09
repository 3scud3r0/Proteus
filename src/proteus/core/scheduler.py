"""Simple fair priority scheduler for bounded units of work."""
from dataclasses import dataclass, field
import heapq
from typing import Callable

@dataclass(order=True)
class Job:
    sort_priority: tuple[int, int]
    name: str = field(compare=False)
    run: Callable[[], object] = field(compare=False)

class Scheduler:
    def __init__(self):
        self._queue: list[Job] = []
        self._counter = 0
    def add(self, name: str, run: Callable[[], object], priority: int = 0) -> None:
        self._counter += 1
        heapq.heappush(self._queue, Job((-priority, self._counter), name, run))
    def step(self) -> tuple[str, object] | None:
        if not self._queue:
            return None
        job = heapq.heappop(self._queue)
        return job.name, job.run()
    def __len__(self) -> int:
        return len(self._queue)
