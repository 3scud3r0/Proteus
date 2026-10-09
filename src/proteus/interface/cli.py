"""Single transparent entrypoint; no hidden background tasks or network calls."""
import argparse
import json
import time
from pathlib import Path
from proteus.core.agent import ProteusAgent
from proteus.core.state import StateStore
from proteus.research.experiment_runner import compare_replay
from proteus.research.report import write_report
from proteus.evolution.improvement_proposer import propose_replay
from proteus.evolution.candidate_evaluator import evaluate_candidate
from proteus.tools.python_runner import arithmetic
from proteus.tools.filesystem import FileTools
from proteus.safety.sandbox import Workspace
from proteus.interface.api import serve

PROJECT=Path(__file__).resolve().parents[3]

def config(root: Path = PROJECT) -> dict:
    result={}
    for section in ("default","hardware","safety","learning","evaluation"):
        result[section]=json.loads((root/"configs"/f"{section}.yaml").read_text(encoding="utf-8"))
    return result

def parser() -> argparse.ArgumentParser:
    p=argparse.ArgumentParser(prog="proteus",description="PROTEUS research prototype — CPU first")
    p.add_argument("--home",type=Path,default=PROJECT/"data",help="Persistent agent data directory")
    commands=p.add_subparsers(dest="command",required=True)
    commands.add_parser("init",help="Create local state database")
    train=commands.add_parser("train",help="Incremental tabular Q-learning")
    train.add_argument("--episodes",type=int,default=200)
    train.add_argument("--size",type=int,default=6)
    train.add_argument("--walls",type=float,default=0.)
    train.add_argument("--seconds",type=float,default=60.)
    ev=commands.add_parser("evaluate",help="Evaluate without training")
    ev.add_argument("--episodes",type=int,default=30)
    ev.add_argument("--size",type=int,default=6)
    ev.add_argument("--walls",type=float,default=0.)
    commands.add_parser("status",help="Read persisted state and counts")
    explore=commands.add_parser("explore",help="Self-generated procedural task curriculum")
    explore.add_argument("--cycles",type=int,default=3)
    explore.add_argument("--episodes",type=int,default=60)
    research=commands.add_parser("research",help="Paired experiment replay on/off")
    research.add_argument("--seeds",type=int,default=3)
    research.add_argument("--episodes",type=int,default=100)
    evolve=commands.add_parser("evolve",help="Bounded hyperparameter experiments; no automatic promotion")
    evolve.add_argument("--episodes",type=int,default=80)
    run=commands.add_parser("run",help="Run bounded learning cycles")
    run.add_argument("--episodes-per-cycle",type=int,default=50)
    run.add_argument("--cycles",type=int,default=1,help="Use 0 for continuous mode until Ctrl+C/STOP file")
    commands.add_parser("stop",help="Create STOP sentinel")
    commands.add_parser("resume",help="Clear STOP sentinel")
    server=commands.add_parser("serve",help="Serve loopback read-only dashboard")
    server.add_argument("--port",type=int,default=8765)
    tool=commands.add_parser("tool",help="Manually call tiny safe tools")
    tool.add_argument("operation",choices=("arithmetic","write","read","list"))
    tool.add_argument("value",nargs="?",default="")
    tool.add_argument("--text",default="")
    return p

def main(argv: list[str] | None = None) -> int:
    args=parser().parse_args(argv)
    home=args.home.resolve()
    cfg=config()
    if args.command=="stop":
        from proteus.safety.emergency_stop import StopSignal
        StopSignal(home/"STOP").request();print("STOP requested");return 0
    if args.command=="resume":
        from proteus.safety.emergency_stop import StopSignal
        StopSignal(home/"STOP").clear();print("STOP cleared");return 0
    if args.command=="serve":
        serve(home,args.port);return 0
    if args.command=="tool":
        if args.operation=="arithmetic":output=arithmetic(args.value)
        else:
            safe=FileTools(Workspace(home/"workspace"))
            if args.operation=="write":output=safe.write(args.value,args.text)
            elif args.operation=="read":output=safe.read(args.value)
            else:output=safe.list()
        print(json.dumps(output,ensure_ascii=False,indent=2));return 0
    if args.command=="research":
        if not 1<=args.seeds<=12 or not 1<=args.episodes<=1000:raise ValueError("Research budget outside supported bounds")
        findings=compare_replay(list(range(7,7+args.seeds)),args.episodes)
        path=home/"reports"/f"replay_{args.seeds}seeds_{args.episodes}episodes.md"
        write_report(path,"Replay Ablation",findings)
        print(json.dumps({"report":str(path),"summary":findings["summary"],"interpretation":findings["interpretation"]},indent=2))
        return 0
    if args.command=="evolve":
        candidates=[]
        for replay in propose_replay(2):
            settings={**cfg["learning"],"replay_per_step":replay}
            result=evaluate_candidate(settings,training_episodes=args.episodes,eval_episodes=20)
            candidates.append({"replay_per_step":replay,"heldout":result["heldout"]})
        print(json.dumps({"candidates":candidates,"note":"Exploratory only; no automatic promotion"},indent=2));return 0
    with ProteusAgent(home,config=cfg,seed=int(cfg["default"]["seed"])) as agent:
        if args.command=="init":result={"home":str(home),"status":agent.status()}
        elif args.command=="status":result=agent.status()
        elif args.command=="train":
            if not 0<=args.episodes<=100000:raise ValueError("Invalid episodes")
            result=agent.train(args.episodes,args.size,args.walls,max_seconds=args.seconds)
        elif args.command=="evaluate":result=agent.evaluate(args.episodes,size=args.size,wall_probability=args.walls)
        elif args.command=="explore":result=agent.explore(cycles=args.cycles,episodes_per_cycle=args.episodes)
        elif args.command=="run":
            if args.episodes_per_cycle<1 or args.cycles<0:raise ValueError("Invalid cycle parameters")
            counter=0; history=[]
            try:
                while (args.cycles==0 or counter<args.cycles) and not agent.stop.requested():
                    history.append(agent.train(args.episodes_per_cycle,max_seconds=60))
                    counter+=1
                    if args.cycles==0:time.sleep(0.2)
            except KeyboardInterrupt:pass
            result={"cycles":counter,"last":history[-1] if history else None}
        else:raise AssertionError(args.command)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":raise SystemExit(main())
