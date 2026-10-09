import math
import pytest
from proteus.learning.online_learner import OnlineQLearner,QSettings
from proteus.learning.checkpoint import save,load
from proteus.learning.replay_buffer import ReplayBuffer
from proteus.learning.continual_learner import ContinualLearner
from proteus.core.protocols import Transition
from proteus.cognition.world_model import WorldModel
from proteus.cognition.uncertainty import entropy
from proteus.cognition.reasoning import infer
from proteus.cognition.perception import perceive
from proteus.cognition.planner import choose_action

def test_bellman_update_and_checkpoint(tmp_path):
    learner=OnlineQLearner(settings=QSettings(alpha=1,gamma=0.9))
    t=Transition((0,0,2,2),3,1,(1,0,2,2),True)
    assert learner.learn(t)==1.0
    assert learner.values(t.state)[3]==1.0
    path=tmp_path/"c.json";save(learner,path)
    restored=OnlineQLearner();load(restored,path)
    assert restored.values(t.state)[3]==1.0
    text=path.read_text();path.write_text(text.replace('"updates": 1','"updates": 2'))
    with pytest.raises(ValueError):load(OnlineQLearner(),path)

def test_replay_and_world_model():
    learner=OnlineQLearner(seed=1)
    replay=ReplayBuffer(capacity=5,seed=2)
    t=Transition((0,0,2,2),1,0.5,(0,1,2,2),False)
    trainer=ContinualLearner(learner,replay,replay_per_step=2)
    trainer.observe(t)
    assert learner.updates==2 and len(replay)==1
    model=WorldModel();model.observe(t)
    assert model.predict(t.state,1)==(t.next_state,1.0)
    other=WorldModel();other.restore(model.snapshot())
    assert other.predict(t.state,1)==(t.next_state,1.0)
    assert choose_action(other,t.state)==1

def test_math_and_input_validations():
    assert entropy([0.5,0.5])==1
    assert infer({"b":["a"],"c":["b"]},{"a"})=={"a","b","c"}
    assert perceive([1,2,3,4])==(1,2,3,4)
    with pytest.raises(ValueError):perceive("1234")
