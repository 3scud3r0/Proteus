"""Generate arithmetic problems with known answers."""
import random

def make_problem(seed: int, difficulty: int = 1) -> dict:
    rng=random.Random(seed)
    bound=10**max(1,min(4,difficulty))
    a,b=rng.randrange(bound),rng.randrange(bound)
    op=rng.choice(["+","-","*"])
    return {"question":f"{a} {op} {b}","answer":a+b if op=="+" else a-b if op=="-" else a*b}
