"""Observe, update, optionally replay previous experiences."""
from proteus.core.protocols import Transition
from proteus.learning.online_learner import OnlineQLearner
from proteus.learning.replay_buffer import ReplayBuffer

class ContinualLearner:
    def __init__(self,learner: OnlineQLearner,replay: ReplayBuffer, replay_per_step: int = 2, replay_scale: float = 0.25):
        self.learner=learner; self.replay=replay
        self.replay_per_step=replay_per_step; self.replay_scale=replay_scale
    def observe(self,transition: Transition) -> float:
        error=self.learner.learn(transition)
        self.replay.add(transition)
        for prior in self.replay.sample(self.replay_per_step):
            self.learner.learn(prior,self.replay_scale)
        return error
