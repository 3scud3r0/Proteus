"""Cardinal deterministic motion."""
MOVES = ((0,-1),(0,1),(-1,0),(1,0))

def move(position: tuple[int,int], action: int, size: int, walls: set[tuple[int,int]]) -> tuple[int,int]:
    if not 0 <= action < len(MOVES):
        raise ValueError("Unknown action")
    dx,dy = MOVES[action]
    candidate = (position[0]+dx, position[1]+dy)
    if not (0 <= candidate[0] < size and 0 <= candidate[1] < size) or candidate in walls:
        return position
    return candidate
