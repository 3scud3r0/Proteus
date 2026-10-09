"""Evaluate an already trusted local callable; does not execute LLM code."""
from proteus.environments.programming.environment import ProgrammingTask

def assess(fn, task: ProgrammingTask) -> dict:
    results=[]
    for args,expected in task.tests:
        try: results.append(fn(*args)==expected)
        except Exception: results.append(False)
    return {"passed":sum(results),"total":len(results),"success":all(results)}
