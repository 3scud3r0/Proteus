"""Success-based difficulty adjustment, deliberately slow."""
from dataclasses import dataclass

@dataclass
class Curriculum:
    level: int = 1
    maximum: int = 6
    def update(self, recent_success: float) -> int:
        if recent_success >= 0.85: self.level=min(self.maximum,self.level+1)
        elif recent_success < 0.15: self.level=max(1,self.level-1)
        return self.level
