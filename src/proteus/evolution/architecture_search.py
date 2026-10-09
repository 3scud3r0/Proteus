"""Finite configuration search, not neural architecture invention."""
from itertools import product

def grid(search: dict[str,list]) -> list[dict]:
    keys=list(search)
    return [dict(zip(keys,v)) for v in product(*(search[k] for k in keys))]
