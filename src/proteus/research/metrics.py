"""Paired effect size for controlled experiments."""
def paired_effect(test: list[float],control: list[float]) -> list[float]:
    if len(test)!=len(control): raise ValueError("Paired experiments require same seed count")
    return [x-y for x,y in zip(test,control)]
