from .components.button import Botao, texto, painel
from .components.ocean_background import FundoOceanico
from .components.progress_bar import barra_progresso, estrela
from .. import config as c

class ViewBase:
    def __init__(self):
        self.botoes = []
        self.fundo = FundoOceanico(caminho=c.IMAGEM_FUNDO)

    def iniciar(self, superficie):
        self.fundo.desenhar(superficie)
        self.botoes = []

    def cabecalho(self, superficie, titulo, subtitulo, peso='bold'):
        texto(superficie, titulo, (122, 24), c.FONTE_CABECALHO, peso=peso,
              largura_maxima=c.RETANGULO_HUD[0] - 140)
        texto(superficie, subtitulo, (122, 72), c.FONTE_PEQUENA,
              largura_maxima=c.RETANGULO_HUD[0] - 140)

    def hud(self, superficie, estado):
        x, y = c.RETANGULO_HUD[0] + 14, c.RETANGULO_HUD[1] + 10
        painel(superficie, c.RETANGULO_HUD, c.BRANCO)
        estrela(superficie, (x+10,y+11), 11)
        texto(superficie, f'{estado.xp} XP', (x+30,y-3), 20, peso='semibold')
        texto(superficie, f'Nível {estado.nivel}', (x+175,y-3), 18, peso='semibold')
        barra_progresso(superficie, (x,y+28,270,12), estado.xp,c.META_XP,
                        cor=c.AMARELO,cor_fundo=c.SUAVE)

    def finalizar(self, superficie, estado, posicao_mouse, voltar=True):
        if voltar:
            self.botoes.append(Botao(c.RETANGULO_VOLTAR, '‹', ('voltar',)))
        for botao in self.botoes:
            botao.desenhar(superficie, posicao_mouse)

    def desenhar_aviso(self, superficie, mensagem):
        painel(superficie, (32, 682, 1216, 30), c.AMARELO)
        texto(superficie, mensagem, (640, 697), c.FONTE_PEQUENA,
              centralizado=True, largura_maxima=1184)
