"""Estrutura da missão de repetição; desafios ainda não implementados."""
from ..models.level import Desafio, TipoDesafio
from ..models.mission import Missao


def criar_desafios_repeticao():
    return tuple(Desafio(numero, tipo=TipoDesafio.REPETICAO)
                 for numero in range(1, 11))


def criar_missao_repeticao():
    return Missao(4, 'Correntes Marinhas', 'Repetição', 250,
                  disponivel=False, desafios=criar_desafios_repeticao())
