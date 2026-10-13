import pygame
from .components.button import Botao, texto, painel
from .components.ocean_background import FundoOceanico
from .. import config as c

class ViewBase:
    def __init__(self):
        self.botoes = []
        self.fundo = FundoOceanico(caminho=c.IMAGEM_FUNDO)

    def iniciar(self, superficie):
        self.fundo.desenhar(superficie)
        self.botoes = []

    def cabecalho(self, superficie, titulo, subtitulo):
        texto(superficie, titulo, (122, 24), c.FONTE_CABECALHO)
        texto(superficie, subtitulo, (122, 72), c.FONTE_PEQUENA)

    def hud(self, superficie, estado, posicao=(940, 25)):
        x, y = posicao
        texto(superficie, f'XP: {estado.xp}   •   Nível: {estado.nivel}', (x,y), 20)
        pygame.draw.rect(superficie, c.SUAVE, (x,y+30,270,10), border_radius=5)
        pygame.draw.rect(superficie, c.AMARELO, (x,y+30,int(270*min(estado.xp/c.META_XP,1)),10), border_radius=5)

    def finalizar(self, superficie, estado, posicao_mouse, voltar=True):
        if voltar:
            self.botoes.append(Botao(c.RETANGULO_VOLTAR, '‹', ('voltar',)))
        self.botoes.append(Botao(c.RETANGULO_SOM, '', ('musica',),
                                icone='som_ligado' if estado.musica_ativada else 'som_desligado'))
        for botao in self.botoes:
            botao.desenhar(superficie, posicao_mouse)
