"""Conteúdo da missão de sequência; cada criação inicia um novo progresso."""
from ..models.level import Desafio, StatusDesafio
from ..models.mission import Missao


def criar_desafios_sequencia():
    return (
        Desafio(1, StatusDesafio.DISPONIVEL, 'Primeiros Movimentos',
                posicao_inicial=(0, 2), posicao_objetivo=(3, 2),
                limite_comandos=5, recompensa_xp=20, implementado=True),

        Desafio(2, nome='Contornando Obstáculos',
                objetivo='Contorne a rocha e alcance a amostra.',
                posicao_inicial=(0, 4), posicao_objetivo=(3, 2),
                obstaculos=((1, 4),),
                limite_comandos=7, recompensa_xp=30, implementado=True),

        Desafio(3, nome='Rota de Exploração',
                posicao_inicial=(0, 5), posicao_objetivo=(4, 1),
                obstaculos=((0, 4), (2, 4), (2, 2), (4, 3)),
                limite_comandos=10, recompensa_xp=50, implementado=True),

        Desafio(4, nome='Passagem Estreita',
                objetivo='Encontre uma passagem entre as rochas.',
                posicao_inicial=(0, 1), posicao_objetivo=(4, 1),
                obstaculos=((1, 1), (1, 2), (1, 3),
                            (3, 0), (3, 2), (3, 3)),
                limite_comandos=12, recompensa_xp=60, implementado=True),

        Desafio(5, nome='Corredor Submarino',
                objetivo='Atravesse o corredor de obstáculos.',
                posicao_inicial=(0, 0), posicao_objetivo=(5, 4),
                obstaculos=((1, 0), (1, 1), (1, 2), (1, 4), (1, 5),
                            (2, 5), (3, 1), (3, 2), (3, 3), (3, 5),
                            (4, 5)),
                limite_comandos=16, recompensa_xp=70, implementado=True),

        Desafio(6, nome='Campo de Rochas',
                objetivo='Desvie das rochas e alcance a amostra.',
                posicao_inicial=(0, 3), posicao_objetivo=(5, 4),
                obstaculos=((1, 2), (1, 3), (1, 4),
                            (2, 1), (2, 5), (3, 1),
                            (3, 3), (3, 5), (4, 3)),
                limite_comandos=16, recompensa_xp=80, implementado=True),

        Desafio(7, nome='Travessia Profunda',
                objetivo='Encontre uma rota segura até o outro lado.',
                posicao_inicial=(0, 0), posicao_objetivo=(5, 4),
                obstaculos=((0, 2), (1, 2), (2, 2), (3, 2),
                            (4, 2), (2, 4), (2, 5), (2, 6),
                            (4, 4), (4, 5), (4, 6)),
                limite_comandos=18, recompensa_xp=90, implementado=True),

        Desafio(8, nome='Labirinto de Corais',
                objetivo='Navegue pelo labirinto sem tocar nos corais.',
                posicao_inicial=(0, 0), posicao_objetivo=(5, 4),
                obstaculos=((0, 3), (1, 1), (1, 3), (1, 5),
                            (2, 1), (2, 5), (3, 1), (3, 2),
                            (3, 3), (3, 5), (4, 5), (4, 6)),
                limite_comandos=20, recompensa_xp=100, implementado=True),

        Desafio(9, nome='Rota de Alta Precisão',
                objetivo='Planeje uma rota eficiente até o objetivo.',
                posicao_inicial=(0, 6), posicao_objetivo=(5, 0),
                obstaculos=((0, 4), (1, 2), (1, 4), (2, 2),
                            (2, 4), (2, 6), (3, 1), (3, 4),
                            (4, 1), (4, 3), (4, 5), (5, 3)),
                limite_comandos=20, recompensa_xp=110, implementado=True),

        Desafio(10, nome='Expedição Final',
                objetivo='Supere os obstáculos e conclua a exploração.',
                posicao_inicial=(0, 0), posicao_objetivo=(5, 5),
                obstaculos=((0, 2), (0, 5), (1, 2), (1, 5),
                            (2, 0), (2, 1), (2, 3), (2, 5), (2, 6),
                            (3, 3), (3, 4), (3, 6),
                            (4, 1), (4, 4), (4, 6)),
                limite_comandos=22, recompensa_xp=150, implementado=True),
    )


def criar_missao_sequencia():
    return Missao(1, 'Primeiras Expediçôes', 'Sequências', 100, True,
                  criar_desafios_sequencia())
