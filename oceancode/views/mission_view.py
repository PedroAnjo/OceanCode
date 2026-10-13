from .base_view import ViewBase
from .components.button import painel, texto
from .components.mission_card import PastaMissao

class ViewMissoes(ViewBase):
    def desenhar(self, superficie, estado, posicao_mouse):
        self.iniciar(superficie)
        painel(superficie, (24,108,1232,522))
        self.cabecalho(superficie, 'Painel de expedições', 'Escolha uma missão para explorar e aprender.')
        self.hud(superficie, estado)
        self.botoes = [PastaMissao((48+(indice%2)*604,160+(indice//2)*240,580,205),missao)
                       for indice,missao in enumerate(estado.missoes)]
        texto(superficie, 'OCEANCODE  /  CONTROLE DE MISSÕES', (48,651), 18)
        self.finalizar(superficie, estado, posicao_mouse)
