"""Compare candidates on frozen held-out scores."""
def select(results: list[dict],metric: str = "success_rate") -> dict:
    if not results:raise ValueError("No candidates")
    return max(results,key=lambda x:(x["heldout"].get(metric,float("-inf")),-x.get("complexity",0)))
