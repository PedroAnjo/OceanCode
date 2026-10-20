from .base_view import ViewBase
from .components.button import texto
from .components.level_button import BotaoDesafio

class ViewDesafios(ViewBase):
    def desenhar(self, superficie, estado, posicao_mouse):
        self.iniciar(superficie)
        missao = estado.missao_selecionada
        self.cabecalho(superficie, f'Missão {missao.numero} — {missao.nome}',
                       f'Conteúdo: {missao.conteudo}', peso='semibold')
        self.botoes = [BotaoDesafio((190+(indice%5)*190,210+(indice//5)*180,140,110),desafio)
                       for indice,desafio in enumerate(missao.desafios)]
        texto(superficie, '✓ Concluído   •   Amarelo: disponível   •   Cinza: bloqueado', (640,570),20,centralizado=True)
        texto(superficie, 'Nesta expedição, os desafios 1 a 3 podem ser desbloqueados.', (640,610),18,centralizado=True)
        self.finalizar(superficie, estado, posicao_mouse)
