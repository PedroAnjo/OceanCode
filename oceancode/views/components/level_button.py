import pygame
from .button import Botao, texto
from ... import config as c
from ...models.level import StatusDesafio

class BotaoDesafio(Botao):
    def __init__(self, retangulo, desafio):
        super().__init__(retangulo, str(desafio.numero), ('desafio',desafio.numero), desafio.jogavel)
        self.desafio = desafio

    def desenhar(self, superficie, posicao_mouse):
        super().desenhar(superficie, posicao_mouse)
        if self.desafio.status == StatusDesafio.CONCLUIDO:
            x,y = self.retangulo.right-28, self.retangulo.y+18
            pygame.draw.lines(superficie, c.AZUL_ESCURO, False, [(x-8,y),(x-2,y+6),(x+9,y-7)], 3)
        texto(superficie, self.desafio.status.value, (self.retangulo.centerx,self.retangulo.bottom+20), 17, centralizado=True)
