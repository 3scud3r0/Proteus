"""Pure Python cosine nearest-neighbour index, intended for tiny datasets."""
import math

class VectorIndex:
    def __init__(self):
        self.vectors: dict[str, tuple[float, ...]] = {}
    def put(self, key: str, vector) -> None:
        self.vectors[key] = tuple(float(v) for v in vector)
    def search(self, query, k: int = 5) -> list[tuple[str,float]]:
        q = tuple(float(v) for v in query)
        def cosine(v):
            if len(v) != len(q):
                return float("-inf")
            denom = math.sqrt(sum(x*x for x in v)*sum(x*x for x in q))
            return sum(x*y for x,y in zip(v,q))/denom if denom else 0.0
        return sorted(((key,cosine(v)) for key,v in self.vectors.items()),key=lambda t:t[1],reverse=True)[:max(0,k)]
