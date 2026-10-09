import pytest
from proteus.core.event_bus import EventBus
from proteus.core.scheduler import Scheduler
from proteus.core.state import StateStore
from proteus.core.lifecycle import Lifecycle,Phase
from proteus.core.resource_manager import Budget,ResourceManager
from proteus.core.goals import Goal

def test_events_and_scheduler():
    events=[];bus=EventBus();bus.subscribe("x",lambda e: events.append(e.data["n"]))
    bus.emit("x",n=9)
    assert events==[9]
    scheduler=Scheduler();scheduler.add("low",lambda:1,priority=0);scheduler.add("high",lambda:2,priority=4)
    assert scheduler.step()==("high",2)
    assert scheduler.step()==("low",1)
    assert scheduler.step() is None

def test_state_is_atomic_and_json(tmp_path):
    store=StateStore(tmp_path/"deep"/"test.json")
    assert store.load()=={}
    store.save({"x":42})
    assert store.load()=={"x":42}

def test_lifecycle_and_budget():
    cycle=Lifecycle();cycle.start();cycle.pause();cycle.stop()
    assert cycle.phase==Phase.STOPPED
    budget=ResourceManager(Budget(max_seconds=30,max_episodes=1))
    assert budget.allowed()
    budget.record_episode()
    assert not budget.allowed()
    assert Goal("accuracy","success",0.5).achieved({"success":0.6})
