"""Empirical Markov transition model updated after every observation."""
from collections import Counter,defaultdict
from proteus.core.protocols import State,Transition

class WorldModel:
    def __init__(self):
        self.counts: dict[tuple[State,int],Counter] = defaultdict(Counter)
        self.total_observations=0
    def observe(self,t: Transition) -> None:
        self.counts[(t.state,t.action)][t.next_state]+=1
        self.total_observations+=1
    def predict(self,state: State,action: int) -> tuple[State,float] | None:
        counter=self.counts.get((state,action))
        if not counter: return None
        next_state,count=counter.most_common(1)[0]
        return next_state,count/sum(counter.values())
    def uncertainty(self,state: State,action: int) -> float:
        counter=self.counts.get((state,action))
        if not counter:return 1.0
        return 1-max(counter.values())/sum(counter.values())
    def snapshot(self) -> list:
        return [[list(s),a,[[list(ns),count] for ns,count in counter.items()]] for (s,a),counter in self.counts.items()]
    def restore(self,data: list) -> None:
        self.counts.clear(); self.total_observations=0
        for state,action,outcomes in data:
            c=Counter({tuple(ns):int(n) for ns,n in outcomes})
            self.counts[(tuple(state),int(action))]=c
            self.total_observations+=sum(c.values())
