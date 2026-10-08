from dataclasses import dataclass
from enum import Enum

class LevelStatus(Enum):
    COMPLETED = "Concluída"
    AVAILABLE = "Disponível"
    LOCKED = "Bloqueada"

@dataclass(frozen=True)
class Level:
    number: int
    status: LevelStatus

    @property
    def playable(self):
        return self.status != LevelStatus.LOCKED
