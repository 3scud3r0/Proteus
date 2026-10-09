"""Procedural generation of reproducible gridworld tasks."""
from proteus.environments.gridworld.environment import GridWorld

def generate_task(seed: int, difficulty: int = 1) -> GridWorld:
    size = 4 + max(0, min(6, difficulty))
    walls = min(0.25, max(0,difficulty-1)*0.025)
    return GridWorld(size=size,wall_probability=walls,max_steps=size*size*3,seed=seed)
