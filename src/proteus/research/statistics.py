"""Sample statistics and approximate 95% uncertainty interval."""
import math
import statistics

def mean_ci(values: list[float]) -> dict:
    if not values: raise ValueError("Empty samples")
    avg=statistics.mean(values)
    if len(values)<2:return {"mean":avg,"ci95_half_width":None,"n":len(values)}
    stderr=statistics.stdev(values)/math.sqrt(len(values))
    return {"mean":avg,"ci95_half_width":1.96*stderr,"n":len(values)}
