"""Estrutura da missão de condicionais; desafios ainda não implementados."""
from ..models.level import Desafio, TipoDesafio
from ..models.mission import Missao


def criar_desafios_condicionais():
    return tuple(Desafio(numero, tipo=TipoDesafio.CONDICIONAIS)
                 for numero in range(1, 11))


def criar_missao_condicionais():
    return Missao(3, 'Decisões no Abismo', 'Condicionais', 200,
                  disponivel=False, desafios=criar_desafios_condicionais())
