"""Estruturas editáveis que representam um programa do submarino."""
from dataclasses import dataclass, field


@dataclass
class Comando:
    tipo: str
    quantidade: int = 2
    corpo: list['Comando'] = field(default_factory=list)


def copiar_comando(comando: Comando) -> Comando:
    """Cria uma cópia independente de um comando e de seu corpo."""
    return Comando(comando.tipo, comando.quantidade,
                   [copiar_comando(filho) for filho in comando.corpo])


def copiar_programa(programa):
    """Copia todos os blocos de um programa sem compartilhar estado."""
    return [copiar_comando(comando) for comando in programa]
