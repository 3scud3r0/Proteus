"""Deterministic grid generation with guaranteed path to target."""
import random
from collections import deque

DIRECTIONS = ((0,-1),(0,1),(-1,0),(1,0))

def reachable(size: int, walls: set[tuple[int,int]], start: tuple[int,int], goal: tuple[int,int]) -> bool:
    pending = deque([start]); visited = {start}
    while pending:
        u = pending.popleft()
        if u == goal:
            return True
        for dx,dy in DIRECTIONS:
            nxt=(u[0]+dx,u[1]+dy)
            if 0 <= nxt[0] < size and 0 <= nxt[1] < size and nxt not in visited and nxt not in walls:
                visited.add(nxt); pending.append(nxt)
    return False

def generate(size: int, probability: float, seed: int, start=(0,0), goal=None) -> set[tuple[int,int]]:
    if size < 2 or not 0 <= probability <= 0.7:
        raise ValueError("Invalid grid parameters")
    goal = goal or (size-1,size-1)
    rng = random.Random(seed)
    for _ in range(60):
        walls={(x,y) for y in range(size) for x in range(size) if (x,y) not in (start,goal) and rng.random()<probability}
        if reachable(size,walls,start,goal):
            return walls
    return set()  # Always viable fallback, reported via environment metadata.
