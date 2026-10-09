import pytest
from proteus.environments.gridworld.environment import GridWorld
from proteus.environments.gridworld.generator import reachable,generate
from proteus.environments.gridworld.dynamics import move
from proteus.environments.gridworld.renderer import render
from proteus.environments.physics.environment import PointMass
from proteus.environments.puzzles.generator import make_problem
from proteus.environments.puzzles.verifier import verify
from proteus.environments.multiagent.environment import MultiAgentWorld
from proteus.environments.procedural.task_generator import generate_task

def test_gridworld_seed_determinism_and_reachability():
    a=GridWorld(6,0.2,seed=8)
    b=GridWorld(6,0.2,seed=8)
    assert a.walls==b.walls and a.position==b.position
    assert reachable(a.size,a.walls,a.position,a.goal)
    assert "G" in render(a)
    assert move((0,0),2,6,set())==(0,0)
    with pytest.raises(ValueError):move((0,0),99,6,set())

def test_gridworld_reaches_goal():
    env=GridWorld(size=3,seed=2,random_starts=False)
    env.reset(seed=1)
    for action in (3,3,1,1):state,r,done,info=env.step(action)
    assert done and info["success"] and r==1.0

def test_misc_environments():
    p=PointMass();assert len(p.reset())==3
    assert len(p.step(1))==4
    problem=make_problem(3,2)
    assert verify(problem,problem["answer"])
    assert not verify(problem,"10")
    world=MultiAgentWorld(["a","b"])
    world.broadcast("a",{"x":1})
    assert world.messages.receive("b")==[{"sender":"a","payload":{"x":1}}]
    assert generate_task(1).size==5
