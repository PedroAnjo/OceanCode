"""Desafios da missão Depuração, com programas iniciais quase corretos."""
from ..models.command import Comando
from ..models.level import Desafio, TipoDesafio
from ..models.mission import Missao


def _comando(tipo, quantidade=2, corpo=()):
    filhos = [_comando(*filho) if isinstance(filho, tuple) else _comando(filho)
              for filho in corpo]
    return Comando(tipo, quantidade, filhos)


def _programa(*comandos):
    return tuple(_comando(*comando) if isinstance(comando, tuple) else _comando(comando)
                 for comando in comandos)


def criar_desafios_depuracao():
    return (
        Desafio(1, nome='Direção Incorreta', objetivo='Observe o desvio e corrija o movimento que aponta para o lado errado.', posicao_inicial=(0, 0), posicao_objetivo=(2, 0), limite_comandos=3, recompensa_xp=20, implementado=True, tipo=TipoDesafio.DEPURACAO, programa_inicial=_programa('baixo', 'direita', 'direita')),
        Desafio(2, nome='Comando Ausente', objetivo='Encontre a etapa que falta para alcançar a amostra.', posicao_inicial=(0, 2), posicao_objetivo=(3, 2), limite_comandos=5, recompensa_xp=30, implementado=True, tipo=TipoDesafio.DEPURACAO, programa_inicial=_programa('direita', 'cima', 'direita', 'direita')),
        Desafio(3, nome='Comando Excedente', objetivo='Remova o movimento que desvia a rota antes da coleta.', posicao_inicial=(0, 0), posicao_objetivo=(3, 0), limite_comandos=4, recompensa_xp=40, implementado=True, tipo=TipoDesafio.DEPURACAO, programa_inicial=_programa('direita', 'direita', 'baixo', 'direita')),
        Desafio(4, nome='Ordem Incorreta', objetivo='Os comandos estão corretos, mas a ordem cria uma colisão.', posicao_inicial=(0, 1), posicao_objetivo=(2, 0), obstaculos=((1, 1),), limite_comandos=4, recompensa_xp=50, implementado=True, tipo=TipoDesafio.DEPURACAO, programa_inicial=_programa('direita', 'cima', 'direita')),
        Desafio(5, nome='Repetição Insuficiente', objetivo='Ajuste o laço para que o corredor seja percorrido por completo.', posicao_inicial=(0, 0), posicao_objetivo=(3, 0), limite_comandos=3, recompensa_xp=60, implementado=True, tipo=TipoDesafio.DEPURACAO, programa_inicial=_programa(('repetir', 2, ('direita',)))),
        Desafio(6, nome='Repetição Excessiva', objetivo='O laço avança além do ponto necessário. Corrija sua quantidade.', posicao_inicial=(0, 1), posicao_objetivo=(3, 2), limite_comandos=3, recompensa_xp=70, implementado=True, tipo=TipoDesafio.DEPURACAO, programa_inicial=_programa(('repetir', 4, ('direita',)))),
        Desafio(7, nome='Dentro ou Fora do Laço', objetivo='Decida quais ações devem se repetir e quais acontecem uma só vez.', posicao_inicial=(0, 0), posicoes_objetivos=((2, 0), (2, 1)), limite_comandos=5, recompensa_xp=80, implementado=True, tipo=TipoDesafio.DEPURACAO, programa_inicial=_programa(('repetir', 2, ('direita', 'baixo')))),
        Desafio(8, nome='Disparo Desalinhado', objetivo='Alinhe o submarino antes de disparar e recolha as duas amostras.', posicao_inicial=(0, 1), posicoes_objetivos=((4, 1), (4, 2)), monstros=((2, 1),), limite_comandos=9, recompensa_xp=90, implementado=True, tipo=TipoDesafio.DEPURACAO, programa_inicial=_programa('cima', 'missil', 'baixo', 'direita', 'direita', 'direita', 'direita', 'baixo')),
        Desafio(9, nome='Coleta Incompleta', objetivo='Revise o percurso inteiro: uma das três amostras ficou para trás.', posicao_inicial=(0, 0), posicoes_objetivos=((2, 0), (2, 2), (4, 2)), limite_comandos=8, recompensa_xp=100, implementado=True, tipo=TipoDesafio.DEPURACAO, programa_inicial=_programa('direita', 'direita', 'baixo', 'baixo')),
        Desafio(10, nome='Diagnóstico Integrado', objetivo='Corrija os trechos e complete a expedição pelos três setores.', posicao_inicial=(0, 0), posicoes_objetivos=((3, 0), (3, 2), (6, 2)), limite_comandos=8, recompensa_xp=120, implementado=True, tipo=TipoDesafio.DEPURACAO, programa_inicial=_programa(('repetir', 2, ('direita',)), 'baixo', ('repetir', 2, ('direita',)), 'direita')),
    )


def criar_missao_depuracao():
    return Missao(3, 'Rotas Perigosas', 'Depuração', 150,
                  disponivel=False, desafios=criar_desafios_depuracao(),
                  permite_repeticao=True)
