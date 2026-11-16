"""Catálogo central. Retorna objetos novos para cada sessão do jogo."""
from .conditionals import criar_missao_condicionais
from .debugging import criar_missao_depuracao
from .repetition import criar_missao_repeticao
from .sequence import criar_missao_sequencia


def criar_missoes():
    return (
        criar_missao_sequencia(),
        criar_missao_depuracao(),
        criar_missao_condicionais(),
        criar_missao_repeticao())
