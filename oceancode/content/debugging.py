"""Estrutura da missão de depuração; desafios ainda não implementados."""
from ..models.level import Desafio, TipoDesafio
from ..models.mission import Missao


def criar_desafios_depuracao():
    return tuple(Desafio(numero, tipo=TipoDesafio.DEPURACAO)
                 for numero in range(1, 11))


def criar_missao_depuracao():
    return Missao(2, 'Rotas Perigosas', 'Depuração', 150,
                  disponivel=False, desafios=criar_desafios_depuracao())
