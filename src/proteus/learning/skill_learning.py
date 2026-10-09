"""Extract common action sequences; no claim of semantic comprehension."""
from collections import Counter

def frequent_sequences(actions: list[int], length: int = 3, top: int = 3):
    if length <= 0: raise ValueError("length must be positive")
    return Counter(tuple(actions[i:i+length]) for i in range(len(actions)-length+1)).most_common(top)
