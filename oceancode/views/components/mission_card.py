import pygame
from .button import Botao, painel, texto
from ... import config as c

class PastaMissao(Botao):
    def __init__(self, retangulo, missao):
        super().__init__(retangulo, missao.nome, ('missao',missao.numero), missao.disponivel)
        self.missao = missao

    def desenhar(self, superficie, posicao_mouse):
        missao, retangulo = self.missao, self.retangulo
        cor = c.CINZA
        if missao.disponivel:
            cor = c.AMARELO_HOVER if self.contem(posicao_mouse) else c.AMARELO
            if self.contem(posicao_mouse) and pygame.mouse.get_pressed()[0]:
                cor = c.AMARELO_PRESSIONADO
        painel(superficie, (retangulo.x,retangulo.y-16,145,35), cor)
        painel(superficie, retangulo, cor)
        texto(superficie, f'MISSÃO {missao.numero:02}', (retangulo.x+24,retangulo.y+20), 18)
        texto(superficie, missao.nome, (retangulo.x+24,retangulo.y+52), 28)
        texto(superficie, f'Conteúdo: {missao.conteudo}', (retangulo.x+24,retangulo.y+95), 22)
        texto(superficie, f'Desafios: {missao.concluidos}/{len(missao.desafios)}   •   Recompensa: +{missao.recompensa} XP', (retangulo.x+24,retangulo.y+132), 20)
        texto(superficie, 'Disponível / Abrir missão' if missao.disponivel else 'Bloqueada', (retangulo.x+24,retangulo.y+175), 20)
