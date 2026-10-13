import math
import pygame
from ... import config as c

class FundoOceanico:
    def __init__(self, tamanho=(c.LARGURA, c.ALTURA), caminho=None):
        self.base = pygame.Surface(tamanho)
        largura, altura = tamanho
        for linha in range(altura):
            proporcao = linha / altura
            cor = tuple(int(a + (b-a)*proporcao) for a,b in zip(c.SUAVE, c.AZUL))
            pygame.draw.line(self.base, cor, (0, linha), (largura, linha))
        sombras = pygame.Surface(tamanho, pygame.SRCALPHA)
        for x, y, escala in [(0.12,0.3,1), (0.82,0.46,0.7), (0.42,0.83,1.3)]:
            centro = (int(x*largura), int(y*altura))
            pygame.draw.ellipse(sombras, (*c.BORDA, 35), (centro[0],centro[1],int(90*escala),int(30*escala)))
            pygame.draw.polygon(sombras, (*c.BORDA, 35), [(centro[0],centro[1]+15),(centro[0]-20,centro[1]),(centro[0]-20,centro[1]+30)])
        for indice in range(7):
            x = int(largura*(indice+0.5)/7)
            pygame.draw.ellipse(sombras, (*c.BORDA, 28), (x,altura-55,120,90))
        self.base.blit(sombras, (0,0))
        if caminho and caminho.is_file():
            try:
                self.base = pygame.transform.smoothscale(pygame.image.load(str(caminho)).convert(), tamanho)
            except (pygame.error, OSError):
                pass

    def desenhar(self, superficie, posicao=(0,0), animado=True):
        superficie.blit(self.base, posicao)
        largura, altura = self.base.get_size()
        tempo = pygame.time.get_ticks()/1000 if animado else 0
        for indice in range(12):
            x = int((indice*137+47) % largura + math.sin(tempo+indice)*5)
            y = int((indice*83-tempo*(12+indice%3*3)) % altura)
            pygame.draw.circle(superficie, c.SUAVE, (posicao[0]+x,posicao[1]+y), 4+indice%5, 1)
