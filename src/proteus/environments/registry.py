"""Namespaced environment factories."""
from collections.abc import Callable

class EnvironmentRegistry:
    def __init__(self):
        self.factories: dict[str, Callable] = {}
    def register(self, name: str, factory: Callable) -> None:
        if name in self.factories:
            raise ValueError("Duplicate environment")
        self.factories[name] = factory
    def create(self, name: str, **kwargs):
        return self.factories[name](**kwargs)
