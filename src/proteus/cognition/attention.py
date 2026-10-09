"""Top-k salience selection."""
def prioritize(items: list, scores: list[float], budget: int) -> list:
    if len(items)!=len(scores): raise ValueError("Length mismatch")
    return [items[i] for i in sorted(range(len(items)),key=lambda i:scores[i],reverse=True)[:max(0,budget)]]
