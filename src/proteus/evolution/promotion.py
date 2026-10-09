"""Promotion requires explicit matching human approval."""
from pathlib import Path
from proteus.safety.approval import Approval
from proteus.core.state import StateStore

def promote(candidate_id: str,settings: dict,approval: Approval,destination: Path) -> None:
    approval.require(candidate_id)
    if not {"alpha","gamma","replay_per_step","epsilon_start"}.issuperset(settings):
        raise PermissionError("Candidate changes disallowed settings")
    StateStore(destination).save({"candidate_id":candidate_id,"settings":settings,"reviewer":approval.reviewer})
