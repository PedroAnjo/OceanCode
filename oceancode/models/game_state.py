from dataclasses import dataclass, field
from .mission import Mission, demo_missions
from .level import Level

@dataclass
class GameState:
    missions: tuple[Mission, ...] = field(default_factory=demo_missions)
    selected_mission: Mission | None = None
    selected_level: Level | None = None
    commands: list[str] = field(default_factory=list)
    xp: int = 120
    player_level: int = 3
    music_enabled: bool = True
    message: str = "Adicione comandos para planejar sua rota."
