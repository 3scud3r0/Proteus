"""Fraction of previously unseen discrete outcomes."""
def distinct_fraction(current: set,previous: set) -> float:
    return len(current-previous)/max(1,len(current))
