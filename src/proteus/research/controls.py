"""Ensure fair benchmark configurations share seeds and budgets."""
def matched(a: dict,b: dict,fields=("episodes","seed","size","max_steps")) -> bool:
    return all(a.get(k)==b.get(k) for k in fields)
