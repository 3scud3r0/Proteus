"""Explicit human approval token for bounded candidate promotion."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Approval:
    candidate_id: str
    reviewer: str
    approved: bool
    def require(self,candidate_id: str) -> None:
        if self.candidate_id!=candidate_id or not self.approved or not self.reviewer:
            raise PermissionError("Explicit matching approval is required")
