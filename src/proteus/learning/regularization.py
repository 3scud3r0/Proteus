"""Quadratic parameter drift penalty, usable for small models."""
def l2_anchor(current: list[float],anchor: list[float],strength: float = 1.0) -> float:
    if len(current)!=len(anchor): raise ValueError("Mismatched vector sizes")
    return strength*sum((x-y)**2 for x,y in zip(current,anchor))
