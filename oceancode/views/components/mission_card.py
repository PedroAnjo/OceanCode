import pygame
from .button import Botao, painel, texto
from .progress_bar import barra_progresso, estrelas_missao, estrela, cadeado
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
        x, y = retangulo.topleft
        total = len(missao.desafios)
        texto(superficie, f'MISSÃO {missao.numero:02}', (x+24,y+16), 16, peso='semibold')
        texto(superficie, missao.nome, (x+24,y+43), 28, peso='semibold',
              largura_maxima=retangulo.width-48)
        texto(superficie, missao.conteudo, (x+24,y+82), 20)
        estrelas_missao(superficie, (retangulo.right-78,y+94), missao.concluidos,total)
        texto(superficie, 'PROGRESSO', (x+24,y+117), 14, peso='semibold')
        barra_progresso(superficie, (x+24,y+144,retangulo.width-130,16),
                        missao.concluidos,total, cor=c.AZUL if missao.disponivel else c.BORDA)
        texto(superficie, f'{missao.concluidos}/{total}', (retangulo.right-82,y+137),
              20, peso='semibold')
        estrela(superficie,(x+35,y+184),10,cor=c.AMARELO)
        texto(superficie, f'+{missao.recompensa} XP', (x+55,y+170), 20, peso='semibold')
        if not missao.disponivel:
            cadeado(superficie, (retangulo.right-36,y+27))
