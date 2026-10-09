"""Independent exact arithmetic answer check."""
def verify(problem: dict, answer: int) -> bool:
    return type(answer) is int and answer == problem["answer"]
