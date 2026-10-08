from dataclasses import dataclass
from .level import Level, LevelStatus

@dataclass(frozen=True)
class Mission:
    number: int
    name: str
    content: str
    reward: int
    available: bool
    levels: tuple[Level, ...]

def demo_missions():
    descriptions = [("Primeira Expedição", "Sequências", 100),
                    ("Rotas Perigosas", "Depuração", 150),
                    ("Decisões no Abismo", "Condicionais", 200),
                    ("Correntes Marinhas", "Repetição", 250)]
    levels = tuple(Level(n, LevelStatus.COMPLETED if n <= 2 else
                         LevelStatus.AVAILABLE if n == 3 else LevelStatus.LOCKED)
                   for n in range(1, 11))
    return tuple(Mission(i, name, content, reward, i <= 2, levels)
                 for i, (name, content, reward) in enumerate(descriptions, 1))
