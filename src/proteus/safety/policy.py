"""Deny-by-default capability policy."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Policy:
    allow_network: bool = False
    allow_shell: bool = False
    allow_arbitrary_python: bool = False
    allow_self_modify: bool = False
    require_approval_for_promotion: bool = True

    def permit(self,capability: str) -> bool:
        return {"network":self.allow_network,"shell":self.allow_shell,
                "arbitrary_python":self.allow_arbitrary_python,"self_modify":self.allow_self_modify}.get(capability,False)
