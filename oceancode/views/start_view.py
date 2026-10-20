from .base_view import ViewBase
import pygame
from .components.button import Botao, texto
from .. import config as c

class ViewInicio(ViewBase):
    def __init__(self):
        super().__init__()
        self.logo = None
        if c.IMAGEM_LOGO.is_file():
            try:
                imagem = pygame.image.load(str(c.IMAGEM_LOGO)).convert_alpha()
                proporcao = min(c.TAMANHO_MAXIMO_LOGO[0] / imagem.get_width(),
                                c.TAMANHO_MAXIMO_LOGO[1] / imagem.get_height())
                tamanho = (max(1, int(imagem.get_width() * proporcao)),
                           max(1, int(imagem.get_height() * proporcao)))
                self.logo = pygame.transform.smoothscale(imagem, tamanho)
            except (pygame.error, OSError):
                pass

    def desenhar(self, superficie, estado, posicao_mouse):
        self.iniciar(superficie)
        if self.logo is not None:
            superficie.blit(self.logo, self.logo.get_rect(center=c.CENTRO_LOGO))
        else:
            texto(superficie, 'OceanCode', c.CENTRO_LOGO, c.FONTE_TITULO, centralizado=True)
            texto(superficie, 'Expedição Oceânica', (640,300 if self.logo is not None else 278), 30, centralizado=True)
        self.botoes = [Botao((500,520,280,58), 'JOGAR', ('jogar',)),
                       Botao((500,606,280,58), 'SAIR', ('sair',))]
        self.finalizar(superficie, estado, posicao_mouse, voltar=False)
