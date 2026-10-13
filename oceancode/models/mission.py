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

    @property
    def concluidos(self):
        return sum(desafio.status == StatusDesafio.CONCLUIDO for desafio in self.desafios)

def criar_missoes():
    descricoes = [('Primeira Expedição', 'Sequências', 100),
                  ('Rotas Perigosas', 'Depuração', 150),
                  ('Decisões no Abismo', 'Condicionais', 200),
                  ('Correntes Marinhas', 'Repetição', 250)]
    desafios = (
        Desafio(1, StatusDesafio.DISPONIVEL, 'Primeiros Movimentos',
                posicao_inicial=(0, 2), posicao_objetivo=(3, 2),
                limite_comandos=5, recompensa_xp=20, implementado=True),
        Desafio(2, nome='Contornando Obstáculos', objetivo='Contorne a rocha e alcance a amostra.',
                posicao_inicial=(0, 4), posicao_objetivo=(3, 2), obstaculos=((1, 4),),
                limite_comandos=7, recompensa_xp=30, implementado=True),
        Desafio(3, nome='Rota de Exploração', posicao_inicial=(0, 5), posicao_objetivo=(4, 1),
                obstaculos=((0, 4), (2, 4), (2, 2), (4, 3)),
                limite_comandos=10, recompensa_xp=50, implementado=True),
        *(Desafio(numero) for numero in range(4, 11)))
    return tuple(Missao(numero, nome, conteudo, recompensa, numero == 1,
                        desafios if numero == 1 else tuple(Desafio(n) for n in range(1, 11)))
                 for numero, (nome, conteudo, recompensa) in enumerate(descricoes, 1))
