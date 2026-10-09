"""Difficulty estimate is heuristic, not ground truth."""
def estimate(size: int, wall_count: int) -> float:
    return float(size + 3*wall_count/max(1,size*size))
