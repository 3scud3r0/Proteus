"""Diagnostic flags for observable training pathologies."""
def diagnose(recent_rewards: list[float], older_rewards: list[float]) -> dict:
    if not recent_rewards or not older_rewards:return {"enough_data":False}
    new=sum(recent_rewards)/len(recent_rewards)
    old=sum(older_rewards)/len(older_rewards)
    return {"enough_data":True,"recent_mean":new,"previous_mean":old,"regression":new<old-0.05}
