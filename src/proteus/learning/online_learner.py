"""Correct tabular off-policy Q-learning baseline."""
import random
from dataclasses import dataclass
from proteus.core.protocols import State, Transition

@dataclass
class QSettings:
    alpha: float = 0.24
    gamma: float = 0.94
    epsilon: float = 0.35
    epsilon_final: float = 0.06
    epsilon_decay: float = 0.985

class OnlineQLearner:
    def __init__(self, actions: tuple[int,...] = (0,1,2,3), settings: QSettings | None = None, seed: int = 7):
        self.actions = actions
        self.settings = settings or QSettings()
        self.q: dict[State, dict[int,float]] = {}
        self.rng = random.Random(seed)
        self.updates = 0
    def values(self, state: State) -> dict[int,float]:
        return self.q.setdefault(state,{a:0.0 for a in self.actions})
    def select_action(self,state: State,training: bool = True) -> int:
        if training and self.rng.random()<self.settings.epsilon:
            return self.rng.choice(self.actions)
        vals = self.values(state)
        best=max(vals.values())
        candidates=[a for a in self.actions if abs(vals[a]-best)<1e-12]
        return self.rng.choice(candidates) if training else min(candidates)
    def learn(self,transition: Transition, alpha_scale: float = 1.0) -> float:
        current=self.values(transition.state)
        future=0.0 if transition.done else max(self.values(transition.next_state).values())
        error=transition.reward + self.settings.gamma*future-current[transition.action]
        current[transition.action]+=self.settings.alpha*alpha_scale*error
        self.updates+=1
        return error
    def end_episode(self) -> None:
        self.settings.epsilon=max(self.settings.epsilon_final,self.settings.epsilon*self.settings.epsilon_decay)
    def snapshot(self) -> dict:
        return {"settings": vars(self.settings),"q": [[list(k),list(v.items())] for k,v in self.q.items()],"updates":self.updates}
    def restore(self,data: dict) -> None:
        self.settings=QSettings(**data["settings"])
        self.q={tuple(int(x) for x in state):{int(a):float(v) for a,v in pairs} for state,pairs in data["q"]}
        self.updates=int(data.get("updates",0))
