"""Machine-readable metric summary."""
def scorecard(scores: dict) -> dict:
    return {"metrics":scores,"passed":all(isinstance(v,(float,int)) for v in scores.values())}
