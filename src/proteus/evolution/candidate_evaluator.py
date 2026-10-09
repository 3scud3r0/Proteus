"""Evaluate bounded learning configurations from identical initial conditions."""
from pathlib import Path
from tempfile import TemporaryDirectory
from proteus.core.agent import ProteusAgent

def evaluate_candidate(settings: dict,training_episodes: int = 100,eval_episodes: int = 20,seed: int = 7) -> dict:
    with TemporaryDirectory(prefix="proteus_candidate_") as tmp:
        with ProteusAgent(Path(tmp),config={"learning":settings},seed=seed) as agent:
            train=agent.train(training_episodes,max_seconds=120)
            score=agent.evaluate(eval_episodes,seed=9999)
    return {"training":train,"heldout":score}
