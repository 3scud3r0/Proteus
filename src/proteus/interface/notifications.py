"""Local, in-process notifications; no unsolicited external messages."""
class Notifications:
    def __init__(self):self.messages=[]
    def publish(self,level: str,message: str) -> None:
        self.messages.append({"level":level,"message":message})
    def recent(self,limit: int = 20) -> list[dict]:
        return self.messages[-limit:]
