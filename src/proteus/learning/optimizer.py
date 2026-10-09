"""Scalar SGD utility independent from Q-learning."""
def sgd_step(value: float, gradient: float, lr: float) -> float:
    if lr < 0: raise ValueError("negative learning rate")
    return value-lr*gradient
