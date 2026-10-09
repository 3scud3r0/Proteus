from proteus.core.agent import ProteusAgent
from proteus.safety.emergency_stop import StopSignal

def test_agent_training_evaluation_resume(tmp_path):
    with ProteusAgent(tmp_path,seed=12) as a:
        result=a.train(130,size=5,max_steps=45,max_seconds=30)
        assert result["episodes"]==130
        assert a.status()["experiences"]>0
        heldout=a.evaluate(25,size=5,max_steps=45)
        assert 0<=heldout["success_rate"]<=1
        before=(len(a.memory),a.learner.updates,a.world.total_observations)
        a.evaluate(20,size=5,max_steps=45)
        assert (len(a.memory),a.learner.updates,a.world.total_observations)==before
    with ProteusAgent(tmp_path,seed=12) as b:
        assert b.completed==130
        assert len(b.learner.q)>0
        assert b.world.total_observations>0
        b.train(3,size=5)
        assert b.completed==133

def test_stop_file_prevents_episode(tmp_path):
    signal=StopSignal(tmp_path/"STOP");signal.request()
    with ProteusAgent(tmp_path) as agent:
        assert agent.train(50)["episodes"]==0
    signal.clear()
    with ProteusAgent(tmp_path) as agent:
        assert agent.train(1)["episodes"]==1

def test_procedural_curriculum_persists(tmp_path):
    with ProteusAgent(tmp_path,seed=9) as agent:
        records=agent.explore(cycles=2,episodes_per_cycle=15,max_seconds=20)
        assert len(records)==2
        level=agent.curriculum.level
    with ProteusAgent(tmp_path,seed=9) as recovered:
        assert recovered.curriculum.level==level
        assert recovered.completed==30
