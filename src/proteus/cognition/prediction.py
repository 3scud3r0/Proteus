"""One-step prediction with reliability exposed."""
from proteus.cognition.world_model import WorldModel

def predict(model: WorldModel,state: tuple,action: int) -> dict:
    outcome=model.predict(state,action)
    return {"known":outcome is not None,"state":outcome[0] if outcome else None,"confidence":outcome[1] if outcome else 0.0}
