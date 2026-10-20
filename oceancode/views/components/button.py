from functools import lru_cache
import pygame
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

class Botao:
    def __init__(self, retangulo, rotulo, acao, habilitado=True, direcao=None, icone=None):
        self.retangulo = pygame.Rect(retangulo)
        self.rotulo, self.acao = rotulo, acao
        self.habilitado, self.direcao, self.icone = habilitado, direcao, icone

    def desenhar(self, superficie, posicao_mouse):
        cor = c.AMARELO if self.habilitado else c.CINZA
        if self.habilitado and self.retangulo.collidepoint(posicao_mouse):
            cor = c.AMARELO_PRESSIONADO if pygame.mouse.get_pressed()[0] else c.AMARELO_HOVER
        if self.icone:
            pygame.draw.circle(superficie, cor, self.retangulo.center, self.retangulo.width // 2)
            x, y = self.retangulo.center
            pygame.draw.polygon(superficie, c.AZUL_ESCURO, [(x-12,y-6),(x-6,y-6),(x+2,y-12),(x+2,y+12),(x-6,y+6),(x-12,y+6)])
            if self.icone == 'som_ligado':
                pygame.draw.arc(superficie, c.AZUL_ESCURO, (x-7,y-13,22,26), -1.1, 1.1, 2)
            else:
                pygame.draw.line(superficie, c.AZUL_ESCURO, (x+6,y-7), (x+15,y+7), 3)
                pygame.draw.line(superficie, c.AZUL_ESCURO, (x+6,y+7), (x+15,y-7), 3)
        else:
            painel(superficie, self.retangulo, cor)
            if self.direcao:
                seta(superficie, self.direcao, self.retangulo.center)
            else:
                texto(superficie, self.rotulo, self.retangulo.center, centralizado=True,
                      peso='semibold', largura_maxima=self.retangulo.width - 24)

    def contem(self, posicao):
        if self.icone:
            return self.habilitado and pygame.Vector2(posicao).distance_to(self.retangulo.center) <= self.retangulo.width / 2
        return self.habilitado and self.retangulo.collidepoint(posicao)
