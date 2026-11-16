import pygame
from .button import Botao, painel, texto
from ... import config as c


class MenuOpcoes:
    def __init__(self):
        self.retangulo = pygame.Rect(c.RETANGULO_MENU_OPCOES)
        self.botoes = []
        self.sombra = pygame.Surface((c.LARGURA, c.ALTURA), pygame.SRCALPHA)
        self.sombra.fill((*c.AZUL_ESCURO, 140))

    def desenhar(self, superficie, estado, posicao_mouse, tela_inicial):
        superficie.blit(self.sombra, (0, 0))
        painel(superficie, self.retangulo, c.BRANCO)
        x, y = self.retangulo.topleft
        texto(superficie, 'Opções', (x + 24, y + 20), 30, peso='bold')
        opcoes = [
            ('Voltar ao início', ('voltar_inicio',), not tela_inicial),
            (f'Música: {"ligada" if estado.musica_ativada else "desligada"}', ('musica',), True),
            (f'Efeitos sonoros: {"ligados" if estado.efeitos_ativados else "desligados"}', ('efeitos',), True),
            ('Tutorial', ('abrir_tutorial',), True),
            ('Fechar', ('fechar_menu',), True)]
        self.botoes = [Botao((x + 24, y + 76 + indice * 64, self.retangulo.width - 48, 52),
                             rotulo, acao, habilitado)
                       for indice, (rotulo, acao, habilitado) in enumerate(opcoes)]
        for botao in self.botoes:
            botao.desenhar(superficie, posicao_mouse)
