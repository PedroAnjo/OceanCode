from dataclasses import dataclass
from enum import Enum

class StatusDesafio(Enum):
    CONCLUIDO = 'Concluído'
    DISPONIVEL = 'Disponível'
    BLOQUEADO = 'Bloqueado'

@dataclass
class Desafio:
    numero: int
    status: StatusDesafio = StatusDesafio.BLOQUEADO
    nome: str = 'Em breve'
    objetivo: str = 'Leve o submarino até a amostra.'
    posicao_inicial: tuple[int, int] = (0, 2)
    posicao_objetivo: tuple[int, int] = (3, 2)
    obstaculos: tuple[tuple[int, int], ...] = ()
    limite_comandos: int = 5
    recompensa_xp: int = 0
    implementado: bool = False

    @property
    def jogavel(self):
        return self.implementado and self.status != StatusDesafio.BLOQUEADO
