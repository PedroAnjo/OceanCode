"""Conteúdo da missão de sequência; cada criação inicia um novo progresso."""
from ..models.level import Desafio, StatusDesafio
from ..models.mission import Missao


def criar_desafios_sequencia():
    return (
        Desafio(
            1, StatusDesafio.DISPONIVEL, 'Primeiros Movimentos',
            objetivo='Programe os movimentos para alcançar a amostra.',
            posicao_inicial=(0, 2),
            posicao_objetivo=(3, 2),
            limite_comandos=5,
            recompensa_xp=20,
            implementado=True,
        ),

        Desafio(
            2, nome='Contornando Obstáculos',
            objetivo='Contorne a rocha e alcance a amostra.',
            posicao_inicial=(0, 4),
            posicao_objetivo=(3, 2),
            obstaculos=((1, 4),),
            limite_comandos=7,
            recompensa_xp=30,
            implementado=True,
        ),

        Desafio(
            3, nome='Rota de Exploração',
            objetivo='Planeje uma rota entre as rochas até a amostra.',
            posicao_inicial=(0, 5),
            posicao_objetivo=(4, 1),
            obstaculos=(
                (0, 4), (2, 4), (2, 2), (4, 3),
            ),
            limite_comandos=10,
            recompensa_xp=50,
            implementado=True,
        ),

        Desafio(
            4, nome='Duas Passagens',
            objetivo='Escolha uma passagem para contornar a barreira.',
            posicao_inicial=(0, 2),
            posicao_objetivo=(7, 2),
            obstaculos=(
                (5, 0),
                (3, 1),
                (3, 2),
                (3, 3),
                (3, 4),
                (5, 5),
            ),
            limite_comandos=13,
            recompensa_xp=60,
            implementado=True,
        ),

        Desafio(
            5, nome='Primeiro Contato Abissal',
            objetivo='Elimine o monstro para liberar a passagem até a amostra.',
            posicao_inicial=(0, 2),
            posicao_objetivo=(6, 3),
            obstaculos=(
                (4, 0),
                (4, 1),
                (4, 3),
                (4, 4),
                (4, 5),
            ),
            monstros=((4, 2),),
            limite_comandos=10,
            recompensa_xp=70,
            implementado=True,
            ),

        Desafio(
            6, nome='Encontrando a Linha de Tiro',
            objetivo='Alinhe o submarino com o monstro e libere a passagem.',
            posicao_inicial=(0, 4),
            posicao_objetivo=(6, 2),
            obstaculos=(
                (4, 0),
                (4, 2), (5, 2),
                (1, 3), (2, 3), (4, 3),
                (4, 4),
                (4, 5),
            ),
            monstros=((4, 1),),
            limite_comandos=13,
            recompensa_xp=80,
            implementado=True,
        ),

        Desafio(
            7, nome='Coleta em Duas Regiões',
            objetivo='Planeje a coleta das duas amostras e libere a travessia.',
            posicao_inicial=(0, 3),
            posicoes_objetivos=(
                (1, 0),  # Amostra 1.
                (6, 2),  # Amostra 2.
            ),
            obstaculos=(
                (0, 0), (2, 0), (3, 0),
                (3, 1),
                (1, 2), (5, 2),
                (3, 3),
                (3, 4),
                (3, 5),
            ),
            monstros=((3, 2),),
            limite_comandos=16,
            recompensa_xp=90,
            implementado=True,
        ),

        Desafio(
            8, nome='Duas Linhas de Disparo',
            objetivo='Encontre duas posições de tiro e colete todas as amostras.',
            posicao_inicial=(0, 4),
            posicoes_objetivos=(
                (3, 2),  # Amostra 1.
                (7, 3),  # Amostra 2.
            ),
            obstaculos=(
                (2, 0), (5, 0),
                (5, 1),
                (0, 2), (2, 2), (5, 2),
                (2, 3), (3, 3), (5, 3),
                (2, 4),
                (2, 5), (5, 5),
            ),
            monstros=(
                (2, 1),
                (5, 4),
            ),
            limite_comandos=18,
            recompensa_xp=100,
            implementado=True,
        ),

        Desafio(
            9, nome='Dois Alvos no Mesmo Corredor',
            objetivo='Elimine os dois monstros alinhados e colete as amostras.',
            posicao_inicial=(0, 4),
            posicoes_objetivos=(
                (4, 0),  # Amostra 1.
                (7, 4),  # Amostra 2.
            ),
            obstaculos=(
                (3, 0), (5, 0),
                (3, 1), (5, 1),
                (1, 3), (3, 3), (5, 3), (6, 3),
                (3, 4), (5, 4),
                (3, 5), (5, 5),
            ),
            monstros=(
                (3, 2),
                (5, 2),
            ),
            limite_comandos=19,
            recompensa_xp=110,
            implementado=True,
        ),

        Desafio(
            10, nome='Expedição Integrada',
            objetivo='Escolha a ordem de coleta e reúna as três amostras.',
            posicao_inicial=(1, 1),
            posicoes_objetivos=(
                (5, 0),  # Amostra 1.
                (0, 3),  # Amostra 2.
                (7, 5),  # Amostra 3.
            ),
            obstaculos=(
                (3, 0),
                (5, 1),
                (3, 2),
                (3, 3), (4, 3), (5, 3), (6, 3), (7, 3),
                (4, 5),
            ),
            monstros=((3, 1),
                      (4, 4),              
                ),
            limite_comandos=26,
            recompensa_xp=150,
            implementado=True,
        ),
)



def criar_missao_sequencia():
    return Missao(1, 'Primeiras Expedições', 'Sequência', 100, True,
                  criar_desafios_sequencia())
