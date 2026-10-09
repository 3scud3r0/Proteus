"""Evaluation never updates learner parameters or memory."""
from proteus.environments.gridworld.environment import GridWorld
from proteus.evaluation.metrics import Scores
from proteus.learning.online_learner import OnlineQLearner

def evaluate(learner: OnlineQLearner, episodes: int = 20, seed: int = 8100, size: int = 6, wall_probability: float = 0., max_steps: int = 64) -> Scores:
    if episodes<=0: raise ValueError("Positive episode count required")
    successes=0; total_reward=0.; total_steps=0
    for i in range(episodes):
        env=GridWorld(size=size,wall_probability=wall_probability,max_steps=max_steps,seed=seed+i)
        state=env.reset(seed+i)
        for step in range(max_steps):
            action=learner.select_action(state,training=False)
            state,reward,done,info=env.step(action)
            total_reward+=reward
            if done:
                successes+=int(info["success"])
                total_steps+=step+1
                break
    return Scores(episodes,successes/episodes,total_reward/episodes,total_steps/episodes)
