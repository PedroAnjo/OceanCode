from .base_view import ViewBase
from .components.button import Botao, texto
from .. import config as c

class ViewInicio(ViewBase):
    def desenhar(self, superficie, estado, posicao_mouse):
        self.iniciar(superficie)
        texto(superficie, 'OceanCode', (640,205), c.FONTE_TITULO, centralizado=True)
        texto(superficie, 'Expedição Oceânica', (640,278), 30, centralizado=True)
        self.botoes = [Botao((500,360,280,58), 'JOGAR', ('jogar',)),
                       Botao((500,446,280,58), 'SAIR', ('sair',))]
        self.finalizar(superficie, estado, posicao_mouse, voltar=False)
