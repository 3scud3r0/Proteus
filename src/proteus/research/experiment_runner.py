"""Paired reproducible replay ablation: two agents, identical seeds and budgets."""
from pathlib import Path
from tempfile import TemporaryDirectory
from proteus.core.agent import ProteusAgent
from proteus.research.statistics import mean_ci
from proteus.research.metrics import paired_effect
from proteus.research.findings import interpret

def compare_replay(seeds: list[int],training_episodes: int = 150,evaluation_episodes: int = 30,
                   size: int = 6, wall_probability: float = 0.0) -> dict:
    if not seeds or training_episodes<1 or evaluation_episodes<1:raise ValueError("Invalid study design")
    observations=[]
    with TemporaryDirectory(prefix="proteus_research_") as tmp:
        for seed in seeds:
            outcomes={}
            for label,enabled in (("control",False),("replay",True)):
                home=Path(tmp)/f"{seed}_{label}"
                with ProteusAgent(home,seed=seed,replay_enabled=enabled) as agent:
                    training=agent.train(training_episodes,size,wall_probability,max_seconds=120)
                    evaluation=agent.evaluate(evaluation_episodes,seed=8100,size=size,wall_probability=wall_probability)
                    outcomes[label]={"train":training,"heldout":evaluation}
            observations.append({"seed":seed,**outcomes})
    delta=paired_effect([o["replay"]["heldout"]["success_rate"] for o in observations],
                        [o["control"]["heldout"]["success_rate"] for o in observations])
    summary=mean_ci(delta)
    conclusion=interpret(summary["mean"])
    if summary["ci95_half_width"] is None or abs(summary["mean"]) <= summary["ci95_half_width"]:
        conclusion="inconclusive"
    return {"question":"Does uniform replay improve held-out success?","observations":observations,
            "paired_success_deltas":delta,"summary":summary,"interpretation":conclusion,
            "limitations":"Small tabular task, unblinded, exploratory; results do not establish general intelligence or new science."}
