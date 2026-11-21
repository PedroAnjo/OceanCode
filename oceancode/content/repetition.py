"""Conteúdo da missão de repetição; cada criação inicia um novo progresso."""
from ..models.level import Desafio, TipoDesafio
from ..models.mission import Missao


def criar_desafios_repeticao():
    return (
        # Solução esperada: 6[D] (2 blocos); reconheça a corrente linear.
        Desafio(
            1, nome='Corrente Constante',
            objetivo='Repita o movimento para atravessar a corrente.',
            posicao_inicial=(0, 4),
            posicao_objetivo=(6, 4),
            obstaculos=((5, 1), (2, 2)),
            limite_comandos=2,
            recompensa_xp=20,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),
        # Solução esperada: 5[D], C (3 blocos); saia antes do monstro.
        Desafio(
            2, nome='Saída na Medida',
            objetivo='Conte as repetições e suba antes do monstro.',
            posicao_inicial=(1, 5),
            posicao_objetivo=(6, 4),
            obstaculos=((6, 2), (4, 3), (2, 4)),
            monstros=((7, 5),),
            limite_comandos=3,
            recompensa_xp=30,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),
        # Solução esperada: 5[D], 4[C] (4 blocos); dois trechos em L.
        Desafio(
            3, nome='Encontro de Correntes',
            objetivo=(
                'Combine dois laços com contagens diferentes até a amostra.'
            ),
            posicao_inicial=(0, 5),
            posicao_objetivo=(5, 1),
            obstaculos=((4, 2), (3, 3), (2, 4)),
            monstros=((6, 5),),
            limite_comandos=4,
            recompensa_xp=50,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),
        # Solução esperada: 4[CD], 2[D] (5 blocos); repita o degrau.
        # Três ou cinco degraus levam aos monstros em (4, 2) ou (4, 0).
        Desafio(
            4, nome='Escada dos Sentinelas',
            objetivo='Repita os degraus e acerte a saída entre os monstros.',
            posicao_inicial=(0, 5),
            posicao_objetivo=(6, 1),
            obstaculos=(
                (3, 0), (2, 1), (1, 2), (5, 2),
                (0, 3), (3, 3), (2, 4), (1, 5),
            ),
            monstros=((4, 0), (4, 2)),
            limite_comandos=5,
            recompensa_xp=60,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),
        # Solução esperada: 3[DDC], D, C (6 blocos); degraus mais largos.
        # Com dois ciclos, o ajuste final colide com o monstro em (5, 2).
        Desafio(
            5, nome='Degraus Largos',
            objetivo='Repita passos duplos e ajuste o último degrau.',
            posicao_inicial=(0, 5),
            posicao_objetivo=(7, 1),
            obstaculos=(
                (6, 1), (4, 2), (2, 3), (3, 3), (7, 3),
                (0, 4), (1, 4), (5, 4), (3, 5),
            ),
            monstros=((5, 2), (5, 5)),
            limite_comandos=6,
            recompensa_xp=70,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),
        # Solução esperada: 3[MDDB], D, B (7 blocos); dispare antes de andar.
        # Dois ciclos deixam o monstro em (5, 2) bloqueando o ajuste final.
        Desafio(
            6, nome='Patrulha em Cascata',
            objetivo='Repita disparos e passos duplos para descer os recifes.',
            posicao_inicial=(0, 0),
            posicao_objetivo=(7, 4),
            obstaculos=(
                (3, 0), (0, 1), (1, 1), (5, 1),
                (2, 2), (3, 2), (7, 2), (4, 3), (6, 4),
            ),
            monstros=((1, 0), (3, 1), (5, 2), (5, 3)),
            limite_comandos=7,
            recompensa_xp=80,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),
        # Solução esperada: 3[DC], 2[D], 2[CD] (8 blocos); troque o ritmo.
        # Dois ou quatro ciclos iniciais atingem (4, 3) ou (4, 1).
        Desafio(
            7, nome='Mudança de Ritmo',
            objetivo='Conecte três laços e inverta a ordem do último padrão.',
            posicao_inicial=(0, 5),
            posicao_objetivo=(7, 0),
            obstaculos=(
                (4, 0), (5, 0), (3, 1), (7, 1),
                (0, 2), (2, 2), (6, 2), (1, 3), (5, 3),
                (0, 4), (4, 4), (2, 5),
            ),
            monstros=((4, 1), (4, 3)),
            limite_comandos=8,
            recompensa_xp=90,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),
        # Solução esperada: 2[C], 3[MDD], D, 2[B] (9 blocos), por cima.
        # Alternativa: 2[B], 3[MDD], D, 2[C] (9 blocos), por baixo da ilha.
        Desafio(
            8, nome='Ilha de Duas Rotas',
            objetivo='Escolha um lado da ilha e repita disparos na travessia.',
            posicao_inicial=(0, 3),
            posicao_objetivo=(7, 3),
            obstaculos=(
                (3, 0), (5, 0),
                (2, 2), (3, 2), (4, 2), (5, 2),
                (2, 3), (3, 3), (4, 3), (5, 3),
                (2, 4), (3, 4), (4, 4), (5, 4),
            ),
            monstros=((3, 1), (5, 1), (3, 5), (5, 5)),
            limite_comandos=9,
            recompensa_xp=100,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),
        # Solução esperada: 2[MDDCC], 3[D], 2[B] (10 blocos), pela base.
        # Alternativa: 2[CCMDD], 3[D], 2[B] (10 blocos), pelo alto dos recifes.
        Desafio(
            9, nome='Arquipélago dos Padrões',
            objetivo='Escolha onde subir e agrupe disparos e passos duplos.',
            posicao_inicial=(0, 5),
            posicao_objetivo=(7, 3),
            obstaculos=(
                (2, 0), (5, 0), (6, 0),
                (0, 2), (3, 2), (5, 2), (5, 3),
                (1, 4), (3, 4), (5, 4), (6, 4), (5, 5), (7, 5),
            ),
            monstros=((3, 1), (1, 3), (3, 3), (1, 5)),
            limite_comandos=10,
            recompensa_xp=110,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),
        # Solução esperada: 3[MDD], 2[C], 3[EME], 3[C] (12 blocos).
        # Alternativa pela coluna 7: 3[MDD], D, 2[C], 3[EME], E, 3[C]
        # (14 blocos). Mover à esquerda antes do disparo orienta o míssil.
        Desafio(
            10, nome='Circuito Abissal',
            objetivo=(
                'Combine laços e inverta os disparos para vencer o circuito.'
            ),
            posicao_inicial=(0, 5),
            posicao_objetivo=(0, 0),
            obstaculos=(
                (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2),
                (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4),
            ),
            monstros=((2, 3), (4, 3), (2, 5), (4, 5), (6, 5)),
            limite_comandos=14,
            recompensa_xp=150,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),
    )


def criar_missao_repeticao():
    return Missao(2, 'Correntes Marinhas', 'Repetição', 250,
                  disponivel=False, desafios=criar_desafios_repeticao(),
                  permite_repeticao=True)
