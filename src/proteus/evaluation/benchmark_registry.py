"""Registry of explicit evaluation tasks."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Benchmark:
    name: str
    size: int
    wall_probability: float
    seed: int

DEFAULT_BENCHMARKS=(Benchmark("unobstructed",6,0.,8100),Benchmark("obstacles",6,0.12,9100))
