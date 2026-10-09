from proteus.research.experiment_runner import compare_replay
from proteus.research.statistics import mean_ci
from proteus.evolution.architecture_search import grid
from proteus.evolution.code_mutation import vary
from proteus.evaluation.regression import acceptable

def test_research_runs_both_conditions():
    result=compare_replay(seeds=[5,9],training_episodes=30,evaluation_episodes=8,size=5)
    assert len(result["observations"])==2
    assert len(result["paired_success_deltas"])==2
    assert result["summary"]["n"]==2

def test_candidates_and_statistics():
    assert len(grid({"a":[1,2],"b":[3,4]}))==4
    assert len(vary({"alpha":0.1},"alpha",[0.1,0.2]))==2
    assert acceptable({"a":0.9},{"a":0.91})
    assert mean_ci([1,2,3])["mean"]==2
