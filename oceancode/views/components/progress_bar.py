"""Indicadores desenhados com Pygame, sem assets ou mudanças no progresso."""
import math
import pygame
from ... import config as c


def barra_progresso(superficie, retangulo, valor, total, cor=c.AZUL,
                    cor_fundo=c.BRANCO):
    retangulo = pygame.Rect(retangulo)
    proporcao = max(0, min(valor / total, 1)) if total > 0 else 0
    raio = retangulo.height // 2
    pygame.draw.rect(superficie, cor_fundo, retangulo, border_radius=raio)
    largura = round(retangulo.width * proporcao)
    if largura:
        preenchimento = pygame.Rect(retangulo.x, retangulo.y, largura, retangulo.height)
        pygame.draw.rect(superficie, cor, preenchimento, border_radius=raio)
    pygame.draw.rect(superficie, c.BORDA, retangulo, 1, border_radius=raio)


def estrela(superficie, centro, raio=12, preenchida=True, cor=c.AMARELO):
    pontos = []
    for indice in range(10):
        angulo = -math.pi / 2 + indice * math.pi / 5
        distancia = raio if indice % 2 == 0 else raio * 0.45
        pontos.append((centro[0] + math.cos(angulo) * distancia,
                       centro[1] + math.sin(angulo) * distancia))
    if preenchida:
        pygame.draw.polygon(superficie, cor, pontos)
    pygame.draw.polygon(superficie, c.AZUL_ESCURO if preenchida else c.BORDA,
                        pontos, 2)


def estrelas_missao(superficie, centro, concluidos, total):
    # Marcos visuais: começou, chegou à metade, concluiu toda a missão.
    quantidade = (int(concluidos > 0) + int(total > 0 and concluidos / total >= 0.5)
                  + int(total > 0 and concluidos >= total))
    for indice in range(3):
        estrela(superficie, (centro[0] + (indice - 1) * 34, centro[1]),
                preenchida=indice < quantidade, cor=c.AZUL)


def cadeado(superficie, centro):
    x, y = centro
    pygame.draw.rect(superficie, c.AZUL_ESCURO, (x-9, y-2, 18, 15), border_radius=4)
    pygame.draw.arc(superficie, c.AZUL_ESCURO, (x-7, y-13, 14, 20), 0, math.pi, 3)
    pygame.draw.circle(superficie, c.SUAVE, (x, y+4), 2)
