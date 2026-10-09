"""Select informative transitions by prediction error magnitude."""
def select_surprising(transitions: list, errors: list[float], count: int):
    return [t for _,t in sorted(zip(errors,transitions),key=lambda e:abs(e[0]),reverse=True)[:max(0,count)]]
