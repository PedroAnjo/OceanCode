import pygame
from .button import Botao, painel, texto
from ... import config as c


class ConfirmacaoNovaPartida:
    def __init__(self):
        self.botoes = [Botao((278, 394, 240, 56), 'Cancelar', ('cancelar_nova_partida',)),
                       Botao((544, 394, 458, 56), 'Iniciar nova partida', ('confirmar_nova_partida',))]
        self.sombra = pygame.Surface((c.LARGURA, c.ALTURA), pygame.SRCALPHA)
        self.sombra.fill((*c.AZUL_ESCURO, 140))

    def desenhar(self, superficie, posicao_mouse):
        superficie.blit(self.sombra, (0, 0))
        painel(superficie, (250, 230, 780, 248), c.BRANCO)
        texto(superficie, 'Nova partida', (640, 274), 32, centralizado=True, peso='bold')
        texto(superficie, 'Iniciar uma nova partida apagará o progresso atual.',
              (640, 334), centralizado=True, largura_maxima=724)
        for botao in self.botoes:
            botao.desenhar(superficie, posicao_mouse)
