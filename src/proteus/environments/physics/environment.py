"""One-dimensional point mass environment, not a realistic simulator."""
from proteus.environments.physics.dynamics import integrate

class PointMass:
    actions=(-1,0,1)
    def __init__(self, target: float = 1.0, max_steps: int = 100):
        self.target=target; self.max_steps=max_steps; self.reset()
    def reset(self, seed=None):
        self.x=0.; self.v=0.; self.steps=0
        return (self.x,self.v,self.target)
    def step(self, action: int):
        if action not in self.actions: raise ValueError("Invalid action")
        self.x,self.v=integrate(self.x,self.v,float(action),0.1)
        self.steps+=1
        success=abs(self.x-self.target)<0.05 and abs(self.v)<0.25
        return (self.x,self.v,self.target), (1.0 if success else -abs(self.x-self.target)/100),success or self.steps>=self.max_steps,{"success":success}
