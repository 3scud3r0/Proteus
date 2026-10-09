from proteus.infrastructure.database import Database
from proteus.memory.episodic import EpisodicMemory
from proteus.memory.semantic import SemanticMemory
from proteus.memory.procedural import ProceduralMemory
from proteus.memory.vector_index import VectorIndex
from proteus.memory.forgetting import prune_experiences
from proteus.core.protocols import Transition

def test_memories_persist(tmp_path):
    path=tmp_path/"db.sqlite3"
    with Database(path) as db:
        episodic=EpisodicMemory(db)
        t=Transition((0,0,2,2),1,0.5,(0,1,2,2),False)
        episodic.add(t)
        assert episodic.recent()==[t]
        facts=SemanticMemory(db);facts.put("k",{"value":3},"experiment")
        assert facts.get("k")=={"value":3}
        skills=ProceduralMemory(db);skills.save("right",{"action":3},0.9,True)
        assert skills.validated()[0]["name"]=="right"
    with Database(path) as db:
        assert EpisodicMemory(db).recent()==[t]
        assert SemanticMemory(db).get("k")=={"value":3}
        assert prune_experiences(db,0)==1
        assert db.count("experiences")==0

def test_cosine_index():
    v=VectorIndex();v.put("a",[1,0]);v.put("b",[0,1]);v.put("c",[-1,0])
    assert v.search([1,0],1)[0][0]=="a"
