"""Persistent bounded agent: online learning, observations, replay, auditability."""
import json
import time
from pathlib import Path
from typing import Callable
from proteus.core.event_bus import EventBus
from proteus.core.protocols import Transition
from proteus.core.resource_manager import ResourceManager, Budget
from proteus.core.state import StateStore
from proteus.cognition.world_model import WorldModel
from proteus.cognition.curiosity import Curiosity
from proteus.environments.gridworld.environment import GridWorld
from proteus.evaluation.evaluator import evaluate
from proteus.infrastructure.database import Database
from proteus.learning.online_learner import OnlineQLearner, QSettings
from proteus.learning.continual_learner import ContinualLearner
from proteus.learning.replay_buffer import ReplayBuffer
from proteus.learning.checkpoint import save as save_checkpoint, load as load_checkpoint
from proteus.memory.episodic import EpisodicMemory
from proteus.memory.forgetting import prune_experiences
from proteus.learning.curriculum import Curriculum
from proteus.safety.emergency_stop import StopSignal

class ProteusAgent:
    """Learning agents operate only in simulator; tools require separate explicit invocation."""
    def __init__(self,home: Path,config: dict | None = None,seed: int = 7, replay_enabled: bool = True):
        self.home=Path(home).resolve()
        self.home.mkdir(parents=True,exist_ok=True)
        self.config=config or {}
        self.seed=seed
        self.db=Database(self.home/"proteus.sqlite3")
        self.memory=EpisodicMemory(self.db)
        learning=self.config.get("learning",{})
        settings=QSettings(
            alpha=float(learning.get("alpha",0.24)),gamma=float(learning.get("gamma",0.94)),
            epsilon=float(learning.get("epsilon_start",0.35)),
            epsilon_final=float(learning.get("epsilon_final",0.06)),
            epsilon_decay=float(learning.get("epsilon_decay",0.985)))
        self.learner=OnlineQLearner(settings=settings,seed=seed)
        self.replay=ReplayBuffer(capacity=int(learning.get("replay_capacity",1500)),seed=seed+1)
        self.trainer=ContinualLearner(self.learner,self.replay,
             replay_per_step=(int(learning.get("replay_per_step",2)) if replay_enabled else 0),
             replay_scale=float(learning.get("replay_alpha_scale",0.25)))
        self.world=WorldModel()
        self.curiosity=Curiosity(float(learning.get("curiosity_bonus",0.0)))
        self.bus=EventBus()
        self.checkpoint=self.home/"agent-checkpoint.json"
        self.state_file=StateStore(self.home/"agent-state.json")
        self.completed=0
        self.curriculum=Curriculum()
        self.stop=StopSignal(self.home/"STOP")
        self.load()

    def load(self) -> None:
        if self.checkpoint.exists(): load_checkpoint(self.learner,self.checkpoint)
        state=self.state_file.load()
        self.completed=int(state.get("completed",0))
        self.curriculum.level=int(state.get("curriculum_level",1))
        if "world" in state:self.world.restore(state["world"])
        # Replay and RNG sequences restart, and are not claimed to be bit-for-bit reproducible after resume.
        for t in reversed(self.memory.recent(self.replay.values.maxlen or 1500)):
            self.replay.add(t)

    def save(self) -> None:
        save_checkpoint(self.learner,self.checkpoint)
        self.state_file.save({"completed":self.completed,"world":self.world.snapshot(),"seed":self.seed,"curriculum_level":self.curriculum.level})

    def train(self,episodes: int, size: int = 6, wall_probability: float = 0.,max_steps: int = 64,
              max_seconds: float = 30.0, callback: Callable[[dict],None] | None = None) -> dict:
        if episodes<0: raise ValueError("episodes cannot be negative")
        budget=ResourceManager(Budget(max_seconds=max_seconds,max_episodes=episodes))
        successes=0; return_sum=0.; steps_sum=0
        stopped=False
        try:
            while budget.allowed():
                if self.stop.requested():
                    stopped=True;break
                ep=self.completed
                env=GridWorld(size=size,wall_probability=wall_probability,max_steps=max_steps,seed=self.seed+ep*131)
                state=env.reset(seed=self.seed+ep*131)
                total=0.; info={"success":False}
                for step in range(max_steps):
                    action=self.learner.select_action(state,training=True)
                    next_state,reward,done,info=env.step(action)
                    reward_shaped=reward+self.curiosity.bonus(state,action)
                    transition=Transition(state,action,reward_shaped,next_state,done,ep,{"extrinsic":reward})
                    self.trainer.observe(transition)
                    self.world.observe(transition)
                    self.memory.add(transition)
                    self.bus.emit("transition",episode=ep,action=action,reward=reward)
                    state=next_state;total+=reward
                    if done:break
                self.learner.end_episode()
                self.completed+=1; budget.record_episode()
                successes+=int(info["success"]);return_sum+=total;steps_sum+=step+1
                self.db.save_metric("episode_return",total,{"episode":ep,"success":info["success"]})
                self.bus.emit("episode_completed",episode=ep,success=info["success"],reward=total)
                if callback:callback({"episode":ep,"success":bool(info["success"]),"return":round(total,4)})
                if self.completed % 10 == 0:
                    limit=int(self.config.get("hardware",{}).get("max_memory_records",200000))
                    prune_experiences(self.db,max(0,limit))
                    self.save()
        finally:
            self.save()
        n=budget.completed
        return {"episodes":n,"total_episodes":self.completed,"success_rate":successes/n if n else 0.,
                "mean_return":return_sum/n if n else 0.,"mean_steps":steps_sum/n if n else 0.,
                "model_observations":self.world.total_observations,"q_states":len(self.learner.q),
                "stopped":stopped,"time_budget_exhausted":not stopped and n<episodes}

    def explore(self,cycles: int = 3,episodes_per_cycle: int = 60,max_seconds: float = 45.) -> list[dict]:
        """Curriculum-driven procedural exploration; complexity adapts to measured success."""
        from proteus.environments.procedural.task_generator import generate_task
        if cycles < 1 or episodes_per_cycle < 1:
            raise ValueError("Positive cycles and episodes required")
        records=[]
        for i in range(cycles):
            if self.stop.requested():break
            level=self.curriculum.level
            example=generate_task(self.seed+i,level)
            training=self.train(episodes_per_cycle,size=example.size,wall_probability=example.wall_probability,
                                max_steps=example.max_steps,max_seconds=max_seconds)
            evaluation=self.evaluate(20,seed=8100+i*100,size=example.size,
                                     wall_probability=example.wall_probability,max_steps=example.max_steps)
            self.curriculum.update(evaluation["success_rate"])
            records.append({"cycle":i,"level":level,"training":training,"heldout":evaluation,
                            "next_level":self.curriculum.level})
            self.save()
        return records

    def evaluate(self,episodes: int = 20,seed: int = 8100,size: int = 6,wall_probability: float = 0.,max_steps: int = 64) -> dict:
        return evaluate(self.learner,episodes,seed,size,wall_probability,max_steps).to_dict()

    def status(self) -> dict:
        return {"episodes":self.completed,"experiences":len(self.memory),"model_observations":self.world.total_observations,
                "q_states":len(self.learner.q),"updates":self.learner.updates,"epsilon":self.learner.settings.epsilon,
                "facts":self.db.count("facts"),"skills":self.db.count("skills"),"curriculum_level":self.curriculum.level,"stop_requested":self.stop.requested()}

    def close(self) -> None:
        self.db.close()

    def __enter__(self): return self
    def __exit__(self,*_):self.close()
