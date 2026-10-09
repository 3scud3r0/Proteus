"""Portable inference adapter; external LLM connections are deliberately absent."""
from proteus.learning.online_learner import OnlineQLearner

class ModelRuntime:
    def __init__(self,learner: OnlineQLearner):self.learner=learner
    def predict_action(self,state: tuple) -> int:return self.learner.select_action(state,training=False)
