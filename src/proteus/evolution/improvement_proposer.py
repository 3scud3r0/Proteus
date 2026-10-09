"""Small transparent local hyperparameter candidate set."""
def propose_replay(current: int) -> list[int]:
    return sorted({0,max(1,current//2),current,min(8,current+2)})
