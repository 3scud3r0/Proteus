"""Evaluate model on multiple reproducible task families."""
from proteus.evaluation.evaluator import evaluate
from proteus.evaluation.benchmark_registry import DEFAULT_BENCHMARKS

def run_suite(learner,episodes: int = 20) -> dict:
    return {b.name:evaluate(learner,episodes,seed=b.seed,size=b.size,wall_probability=b.wall_probability).to_dict() for b in DEFAULT_BENCHMARKS}
