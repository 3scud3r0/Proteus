"""Count-based exploration bonus (not general intrinsic motivation)."""
from collections import Counter
import math

class Curiosity:
    def __init__(self,coefficient: float = 0.0):
        self.coefficient=coefficient
        self.visits=Counter()
    def bonus(self,state: tuple,action: int) -> float:
        self.visits[(state,action)]+=1
        return self.coefficient/math.sqrt(self.visits[(state,action)])
