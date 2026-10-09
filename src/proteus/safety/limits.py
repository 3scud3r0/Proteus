"""Guard finite numeric budgets."""
def require_range(name: str,value: float,minimum: float,maximum: float) -> float:
    if not minimum<=value<=maximum:raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return value
