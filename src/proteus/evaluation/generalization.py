"""Generalization difference between seen and held-out tasks."""
def generalization_gap(train_score: float,heldout_score: float) -> float:
    return train_score-heldout_score
