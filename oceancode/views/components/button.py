from functools import lru_cache
import pygame
from math import pi
from ... import config as c

@lru_cache(maxsize=96)
def fonte(tamanho, peso='medio'):
    caminhos = {'medio': c.FONTE_MEDIA, 'semibold': c.FONTE_SEMIBOLD, 'bold': c.FONTE_BOLD}
    caminho = caminhos.get(peso, c.FONTE_MEDIA)
    if caminho.is_file():
        try:
            return pygame.font.Font(str(caminho), tamanho)
        except (pygame.error, OSError):
            pass
    return pygame.font.SysFont(c.NOME_FONTE, tamanho, bold=peso in ('semibold', 'bold'))

def texto(superficie, rotulo, posicao, tamanho=c.FONTE_CORPO, cor=c.AZUL_ESCURO,
          centralizado=False, peso='medio', largura_maxima=None):
    rotulo = str(rotulo)
    if largura_maxima is not None:
        while tamanho > 12 and fonte(tamanho, peso).size(rotulo)[0] > largura_maxima:
            tamanho -= 1
    desenho = fonte(tamanho, peso).render(rotulo, True, cor)
    retangulo = desenho.get_rect(center=posicao) if centralizado else desenho.get_rect(topleft=posicao)
    superficie.blit(desenho, retangulo)

def painel(superficie, retangulo, cor=c.SUAVE):
    retangulo = pygame.Rect(retangulo)
    pygame.draw.rect(superficie, c.BORDA, retangulo.move(0, 4), border_radius=c.RAIO)
    pygame.draw.rect(superficie, cor, retangulo, border_radius=c.RAIO)

def seta(superficie, direcao, centro, cor=c.AZUL_ESCURO):
    x, y = centro
    pontos = [(0, -15), (-11, -3), (-4, -3), (-4, 14), (4, 14), (4, -3), (11, -3)]
    for _ in range({'cima': 0, 'direita': 1, 'baixo': 2, 'esquerda': 3}[direcao]):
        pontos = [(-py, px) for px, py in pontos]
    pygame.draw.polygon(superficie, cor, [(x + px, y + py) for px, py in pontos])

@lru_cache(maxsize=1)
def imagem_missil():
    if c.IMAGEM_MISSIL.is_file():
        try:
            imagem = pygame.image.load(str(c.IMAGEM_MISSIL)).convert_alpha()
            proporcao = min(32 / imagem.get_width(), 34 / imagem.get_height())
            return pygame.transform.smoothscale(imagem, (max(1, round(imagem.get_width() * proporcao)),
                                                         max(1, round(imagem.get_height() * proporcao))))
        except (pygame.error, OSError):
            pass
    return None


def missil(superficie, centro):
    imagem = imagem_missil()
    if imagem is not None:
        superficie.blit(imagem, imagem.get_rect(center=centro))
        return
    x, y = centro
    pygame.draw.polygon(superficie, c.BRANCO, [(x-5,y+9),(x,y+17),(x+5,y+9)])
    pygame.draw.polygon(superficie, c.AZUL_ESCURO, [(x,y-16),(x+7,y-7),(x+7,y+9),(x-7,y+9),(x-7,y-7)])
    pygame.draw.polygon(superficie, c.AZUL_ESCURO, [(x-7,y),(x-14,y+12),(x-7,y+9)])
    pygame.draw.polygon(superficie, c.AZUL_ESCURO, [(x+7,y),(x+14,y+12),(x+7,y+9)])
    pygame.draw.circle(superficie, c.SUAVE, (x,y-4), 4)


@lru_cache(maxsize=1)
def imagem_repetir():
    if c.IMAGEM_REPETIR.is_file():
        try:
            imagem = pygame.image.load(str(c.IMAGEM_REPETIR)).convert_alpha()
            proporcao = min(32 / imagem.get_width(), 32 / imagem.get_height())
            return pygame.transform.smoothscale(imagem, (max(1, round(imagem.get_width() * proporcao)),
                                                         max(1, round(imagem.get_height() * proporcao))))
        except (pygame.error, OSError):
            pass
    return None


def repetir(superficie, centro):
    imagem = imagem_repetir()
    if imagem is not None:
        superficie.blit(imagem, imagem.get_rect(center=centro))
        return
    x, y = centro
    pygame.draw.arc(superficie, c.AZUL_ESCURO, (x-13, y-13, 26, 26), pi / 4, 2 * pi, 3)
    pygame.draw.polygon(superficie, c.AZUL_ESCURO, [(x+13,y-7), (x+7,y+2), (x+18,y+2)])


class Botao:
    def __init__(self, retangulo, rotulo, acao, habilitado=True, direcao=None, icone=None):
        self.retangulo = pygame.Rect(retangulo)
        self.rotulo, self.acao = rotulo, acao
        self.habilitado, self.direcao = habilitado, direcao
        self.icone = icone

    def desenhar(self, superficie, posicao_mouse):
        cor = c.AMARELO if self.habilitado else c.CINZA
        if self.habilitado and self.retangulo.collidepoint(posicao_mouse):
            cor = c.AMARELO_PRESSIONADO if pygame.mouse.get_pressed()[0] else c.AMARELO_HOVER
        painel(superficie, self.retangulo, cor)
        if self.icone == 'missil':
            centro = (self.retangulo.x + 28, self.retangulo.centery) if self.rotulo else self.retangulo.center
            missil(superficie, centro)
            if self.rotulo:
                texto(superficie, self.rotulo, (self.retangulo.centerx + 20, self.retangulo.centery),
                      centralizado=True, peso='semibold', largura_maxima=self.retangulo.width - 72)
        elif self.direcao:
            seta(superficie, self.direcao, self.retangulo.center)
        else:
            texto(superficie, self.rotulo, self.retangulo.center, centralizado=True,
                  peso='semibold', largura_maxima=self.retangulo.width - 24)

    def contem(self, posicao):
        return self.habilitado and self.retangulo.collidepoint(posicao)
