"""Conteúdo da missão de repetição; cada criação inicia um novo progresso."""
from ..models.level import Desafio, TipoDesafio
from ..models.mission import Missao


def criar_desafios_repeticao():
    return (
        # Solução esperada: 5[D].
        # Reconheça a distância e substitua movimentos iguais por um laço.
        # 2 blocos escritos; 5 ações. Mínimo sem repetição: 5.
        Desafio(
            1, nome='Trilha da Corrente',
            objetivo='Siga a corrente e alcance a primeira amostra.',
            posicao_inicial=(1, 2),
            posicao_objetivo=(6, 2),
            obstaculos=((3, 1), (3, 3)),
            limite_comandos=2,
            recompensa_xp=20,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),

        # Solução esperada: 5[D], C.
        # Separe o trecho repetido da subida; uma sexta direita atinge o monstro.
        # 3 blocos escritos; 6 ações. Mínimo sem repetição: 6.
        Desafio(
            2, nome='Curva antes do Perigo',
            objetivo='Atravesse o corredor e suba antes da criatura.',
            posicao_inicial=(1, 4),
            posicao_objetivo=(6, 3),
            obstaculos=((3, 3), (4, 3), (5, 3)),
            monstros=((7, 4),),
            limite_comandos=3,
            recompensa_xp=30,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),

        # Solução esperada: 4[C], 4[E].
        # Combine dois laços simples em direções diferentes.
        # A quinta subida encontraria o monstro em (6, 0).
        # 4 blocos escritos; 8 ações. Mínimo sem repetição: 8.
        Desafio(
            3, nome='Rota entre Recifes',
            objetivo='Suba ao lado do recife e explore a passagem à esquerda.',
            posicao_inicial=(6, 5),
            posicao_objetivo=(2, 1),
            obstaculos=(
                (2, 2), (5, 2),
                (5, 3),
                (5, 4),
            ),
            monstros=((6, 0),),
            limite_comandos=4,
            recompensa_xp=50,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),

        # Solução esperada: 3[CD], 3[D].
        # Repita um corpo com duas ações e depois troque para um trecho linear.
        # Um quarto degrau atingiria o monstro em (3, 1).
        # 5 blocos escritos; 9 ações. Mínimo sem repetição: 9.
        Desafio(
            4, nome='Degraus e Travessia',
            objetivo='Suba os degraus e encontre a passagem entre os guardiões.',
            posicao_inicial=(0, 5),
            posicao_objetivo=(6, 2),
            obstaculos=(
                (5, 1),
                (1, 2),
                (0, 3), (5, 3),
                (2, 4),
                (1, 5),
            ),
            monstros=((3, 1), (3, 3)),
            limite_comandos=5,
            recompensa_xp=60,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),

        # Solução esperada: 3[DC], 3[DB].
        # Colete a primeira amostra na subida e a segunda na descida.
        # Alternativa: 3[CD], 3[BD], também com 6 blocos.
        # 6 blocos escritos; 12 ações. Mínimo sem repetição: 12.
        Desafio(
            5, nome='Duas Encostas',
            objetivo='Explore as duas encostas e recolha ambas as amostras.',
            posicao_inicial=(0, 4),
            posicao_objetivo=(6, 4),
            posicoes_objetivos=(
                (3, 1),
                (6, 4),
            ),
            obstaculos=(
                (2, 0),
                (1, 1), (5, 1),
                (0, 2), (6, 2),
                (3, 3),
                (2, 4), (4, 4),
                (2, 5), (3, 5),
            ),
            monstros=((4, 0),),
            limite_comandos=6,
            recompensa_xp=70,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),

        # Solução esperada: 3[MDDB], D, B.
        # Repita disparo, avanço duplo e descida; continue após a primeira coleta.
        # A primeira amostra é coletada ao terminar o segundo ciclo.
        # 7 blocos escritos; 14 ações. Mínimo sem repetição: 14.
        Desafio(
            6, nome='Coleta em Cascata',
            objetivo='Abra as passagens e recolha as amostras entre os recifes.',
            posicao_inicial=(0, 1),
            posicao_objetivo=(7, 5),
            posicoes_objetivos=(
                (4, 3),
                (7, 5),
            ),
            obstaculos=(
                (3, 1),
                (0, 2), (1, 2), (5, 2),
                (2, 3), (3, 3), (7, 3),
                (4, 4),
                (6, 5),
            ),
            monstros=((1, 1), (3, 2), (5, 3)),
            limite_comandos=7,
            recompensa_xp=80,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),

        # Solução esperada: 3[EB], 2[E], 2[BE].
        # Conecte três trechos e inverta a ordem das ações no último padrão.
        # Alternativa: 3[EB], E, 2[EB], E; mesmo percurso, outro agrupamento.
        # Ambas usam 8 blocos e 12 ações. Mínimo sem repetição: 12.
        Desafio(
            7, nome='Correntes Alternadas',
            objetivo='Atravesse os corredores e ajuste o ritmo entre as coletas.',
            posicao_inicial=(7, 0),
            posicao_objetivo=(0, 5),
            posicoes_objetivos=(
                (4, 3),
                (0, 5),
            ),
            obstaculos=(
                (5, 0),
                (4, 1), (7, 1),
                (2, 2), (6, 2),
                (1, 3), (5, 3),
                (0, 4), (4, 4),
                (3, 5),
            ),
            monstros=((3, 2), (3, 4)),
            limite_comandos=8,
            recompensa_xp=90,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),

        # Solução esperada: 2[C], 3[MDD], D, 5[B].
        # Rota superior: coleta (7, 0) antes de (7, 5); 9 blocos e 17 ações.
        # Alternativa: 3[B], 3[MDD], D, 5[C].
        # Rota inferior: inverte a coleta; 9 blocos e 18 ações.
        # Mínimo sem repetição: 17. Rochas e monstros ocupam 18/48 células.
        Desafio(
            8, nome='Ilha de Coleta Dupla',
            objetivo='Escolha um lado da ilha e planeje a ordem das duas coletas.',
            posicao_inicial=(0, 2),
            posicao_objetivo=(7, 5),
            posicoes_objetivos=(
                (7, 0),
                (7, 5),
            ),
            obstaculos=(
                (2, 1), (3, 1), (4, 1),
                (2, 2), (3, 2), (4, 2),
                (2, 3), (3, 3), (4, 3),
                (2, 4), (3, 4), (4, 4),
            ),
            monstros=(
                (1, 0), (3, 0), (5, 0),
                (1, 5), (3, 5), (5, 5),
            ),
            limite_comandos=9,
            recompensa_xp=100,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),

        # Solução esperada: 2[B], C, D, 4[C], 3[MDD].
        # Ordem: (0, 5), (1, 0), (7, 0); 10 blocos e 17 ações.
        # Alternativa: D, 3[C], 3[MDD], 4[B], 6[E], E, B.
        # Ordem: (1, 0), (7, 0), (0, 5); 13 blocos e 25 ações.
        # Planejar a ordem evita uma longa travessia de retorno.
        # Mínimo sem repetição: 17. O limite permite as duas estratégias.
        Desafio(
            9, nome='Triângulo de Exploração',
            objetivo='Planeje uma expedição para recuperar as três amostras.',
            posicao_inicial=(0, 3),
            posicao_objetivo=(7, 0),
            posicoes_objetivos=(
                (0, 5),
                (1, 0),
                (7, 0),
            ),
            obstaculos=(
                (0, 1), (2, 1), (3, 1), (4, 1), (5, 1),
                (3, 2), (4, 2), (5, 2),
                (3, 3), (4, 3), (5, 3),
            ),
            monstros=(
                (2, 0), (4, 0), (6, 0),
                (6, 5),
            ),
            limite_comandos=13,
            recompensa_xp=110,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),

        # Solução esperada:
        # 3[MDD], D, 2[B], 6[E], E, 2[B], D, 2[MDD].
        # Colete no alto, atravesse até a esquerda e entre no setor inferior.
        # O D antes do último laço também orienta os disparos para a direita.
        # Alternativa, descendo pela coluna 6:
        # 3[MDD], D, E, 2[B], 6[E], 2[B], D, 2[MDD].
        # Ambas usam 17 blocos e 28 ações. Mínimo sem repetição: 28.
        # Rochas e monstros ocupam 19/48 células.
        Desafio(
            10, nome='Expedição dos Três Setores',
            objetivo=(
                'Combine os padrões, atravesse os três setores '
                'e recupere todas as amostras.'
            ),
            posicao_inicial=(0, 0),
            posicao_objetivo=(5, 4),
            posicoes_objetivos=(
                (7, 0),
                (0, 2),
                (5, 4),
            ),
            obstaculos=(
                (0, 1), (1, 1), (2, 1),
                (3, 1), (4, 1), (5, 1),
                (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
                (3, 5), (5, 5),
            ),
            monstros=(
                (2, 0), (4, 0), (6, 0),
                (2, 4), (4, 4), (6, 4),
            ),
            limite_comandos=17,
            recompensa_xp=150,
            implementado=True,
            tipo=TipoDesafio.REPETICAO,
        ),
    )

def criar_missao_repeticao():
    return Missao(2, 'Correntes Marinhas', 'Repetição', 250,
                  disponivel=False, desafios=criar_desafios_repeticao(),
                  permite_repeticao=True)
