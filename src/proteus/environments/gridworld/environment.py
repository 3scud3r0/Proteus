"""Compact task with observable goals and stochastic starts."""
import random
from proteus.environments.gridworld.generator import generate, reachable
from proteus.environments.gridworld.dynamics import move

class GridWorld:
    actions = (0,1,2,3)
    def __init__(self, size: int = 6, wall_probability: float = 0.0, max_steps: int = 64, seed: int = 7, random_starts: bool = True):
        if size < 2 or max_steps <= 0:
            raise ValueError("size must be >= 2 and max_steps > 0")
        self.size = size
        self.wall_probability = wall_probability
        self.max_steps = max_steps
        self.base_seed = seed
        self.random_starts = random_starts
        self.goal = (size-1,size-1)
        self.walls: set[tuple[int,int]] = set()
        self.position = (0,0)
        self.steps = 0
        self._rng = random.Random(seed)
        self.reset(seed)

    def observation(self) -> tuple[int,int,int,int]:
        return (*self.position,*self.goal)

    def reset(self, seed: int | None = None) -> tuple[int,int,int,int]:
        if seed is not None:
            self._rng.seed(seed)
        scene_seed = self._rng.randrange(2**31)
        self.walls = generate(self.size,self.wall_probability,scene_seed)
        candidates = [(x,y) for x in range(self.size) for y in range(self.size)
                      if (x,y)!=self.goal and (x,y) not in self.walls and reachable(self.size,self.walls,(x,y),self.goal)]
        self.position = self._rng.choice(candidates) if self.random_starts else (0,0)
        self.steps = 0
        return self.observation()

    def step(self, action: int) -> tuple[tuple[int,int,int,int],float,bool,dict]:
        previous = self.position
        self.position = move(previous,action,self.size,self.walls)
        self.steps += 1
        won = self.position == self.goal
        terminal = won or self.steps >= self.max_steps
        reward = (1.0 if won else -0.01) + (-0.02 if self.position == previous and not won else 0.0)
        return self.observation(), reward, terminal, {"success":won,"steps":self.steps,"blocked":self.position==previous}
