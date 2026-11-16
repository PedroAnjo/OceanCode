import pygame
from .button import Botao, fonte, painel, texto
from ... import config as c
from ...content.tutorial import TOPICOS_TUTORIAL


class PainelTutorial:
    def __init__(self):
        self.retangulo = pygame.Rect(120, 32, 1040, 640)
        self.regiao = pygame.Rect(self.retangulo.x + 32, self.retangulo.y + 80,
                                  self.retangulo.width - 64, self.retangulo.height - 172)
        self.botoes = [Botao((self.retangulo.right - 272, self.retangulo.bottom - 72, 240, 48),
                             'Fechar', ('fechar_tutorial',))]
        self.sombra = pygame.Surface((c.LARGURA, c.ALTURA), pygame.SRCALPHA)
        self.sombra.fill((*c.AZUL_ESCURO, 140))
        self.rolagem = 0
        self.conteudo = self.preparar_conteudo()
        self.limite_rolagem = max(0, self.conteudo.get_height() - self.regiao.height)

    def preparar_conteudo(self):
        largura = self.regiao.width - 24
        fonte_corpo = fonte(22)
        passo = fonte_corpo.get_linesize() + 4
        linhas = []
        y = 0
        for titulo, corpo in TOPICOS_TUTORIAL:
            linhas.append((titulo, y, 24, 'semibold'))
            y += fonte(24, 'semibold').get_linesize() + 8
            for paragrafo in corpo.split('\n\n'):
                linha = ''
                for palavra in paragrafo.split():
                    tentativa = f'{linha} {palavra}' if linha else palavra
                    if linha and fonte_corpo.size(tentativa)[0] > largura:
                        linhas.append((linha, y, 22, 'medio'))
                        y += passo
                        linha = palavra
                    else:
                        linha = tentativa
                if linha:
                    linhas.append((linha, y, 22, 'medio'))
                    y += passo
                y += 8
            y += 16
        conteudo = pygame.Surface((largura, y))
        conteudo.fill(c.BRANCO)
        for rotulo, topo, tamanho, peso in linhas:
            texto(conteudo, rotulo, (0, topo), tamanho, peso=peso)
        return conteudo

    def rolar(self, deslocamento):
        self.rolagem = max(0, min(self.limite_rolagem, self.rolagem + deslocamento))

    def desenhar(self, superficie, posicao_mouse):
        superficie.blit(self.sombra, (0, 0))
        painel(superficie, self.retangulo, c.BRANCO)
        texto(superficie, 'Como jogar', (self.retangulo.centerx, self.retangulo.y + 38),
              34, centralizado=True, peso='bold')
        superficie.blit(self.conteudo, self.regiao.topleft,
                         (0, self.rolagem, self.conteudo.get_width(), self.regiao.height))
        if self.limite_rolagem:
            trilho = pygame.Rect(self.regiao.right - 8, self.regiao.y, 8, self.regiao.height)
            pygame.draw.rect(superficie, c.BORDA, trilho, border_radius=4)
            altura = max(24, trilho.height * trilho.height // self.conteudo.get_height())
            topo = trilho.y + round((trilho.height - altura) * self.rolagem / self.limite_rolagem)
            pygame.draw.rect(superficie, c.AZUL_ESCURO, (trilho.x, topo, 8, altura), border_radius=4)
            texto(superficie, 'Role para ler ou use Page Up / Page Down.',
                  (self.regiao.x, self.retangulo.bottom - 56), c.FONTE_PEQUENA)
        for botao in self.botoes:
            botao.desenhar(superficie, posicao_mouse)
