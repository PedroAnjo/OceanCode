from dataclasses import dataclass
from .level import Desafio, StatusDesafio

@dataclass
class Missao:
    numero: int
    nome: str
    conteudo: str
    recompensa: int
    disponivel: bool
    desafios: tuple[Desafio, ...]
    permite_repeticao: bool = False

    @property
    def concluidos(self):
        return sum(desafio.status == StatusDesafio.CONCLUIDO for desafio in self.desafios)

    @property
    def concluida(self):
        return bool(self.desafios) and all(
            desafio.implementado and desafio.status == StatusDesafio.CONCLUIDO
            for desafio in self.desafios)

    def atualizar_desbloqueios(self):
        if not self.disponivel:
            return
        concluidos = {desafio.numero for desafio in self.desafios
                      if desafio.implementado and desafio.status == StatusDesafio.CONCLUIDO}
        for desafio in self.desafios:
            if (desafio.implementado and desafio.status == StatusDesafio.BLOQUEADO
                    and (desafio.numero == 1 or desafio.numero - 1 in concluidos)):
                desafio.status = StatusDesafio.DISPONIVEL
