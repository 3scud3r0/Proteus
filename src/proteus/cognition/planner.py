"""Finite-horizon planning using model transitions and a heuristic."""
from proteus.cognition.world_model import WorldModel

def choose_action(model: WorldModel,state: tuple,actions: tuple[int,...]=(0,1,2,3)) -> int:
    x,y,gx,gy=state
    ranking=[]
    for a in actions:
        predicted=model.predict(state,a)
        if predicted is None: continue
        ns,confidence=predicted
        manhattan=abs(gx-ns[0])+abs(gy-ns[1])
        ranking.append((manhattan+(1-confidence)*2,a))
    return min(ranking)[1] if ranking else min(actions)
