"""ASCII representation for the terminal."""
from proteus.environments.gridworld.environment import GridWorld

def render(env: GridWorld) -> str:
    return "\n".join("".join("A" if (x,y)==env.position else "G" if (x,y)==env.goal else "#" if (x,y) in env.walls else "." for x in range(env.size)) for y in range(env.size))
