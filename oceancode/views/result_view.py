from .base_view import ViewBase
from .components.button import Botao, texto, painel

class ViewRetorno(ViewBase):
    def desenhar(self, superficie, estado, posicao_mouse):
        self.iniciar(superficie)
        self.hud(superficie,estado)
        painel(superficie,(220,150,840,440))
        sucesso = estado.tipo_resultado == 'sucesso'
        texto(superficie,'Expedição concluída!' if sucesso else 'Quase lá!',(640,225),42,centralizado=True)
        texto(superficie,estado.mensagem_resultado,(640,295),24,centralizado=True)
        if sucesso:
            texto(superficie,f'+{estado.xp_recebido} XP' if estado.xp_recebido else 'Desafio já concluído • XP já recebido',(640,345),24,centralizado=True)
        self.botoes = []
        if sucesso:
            if estado.proximo_disponivel:
                self.botoes.append(Botao((425,395,430,58),'PRÓXIMO DESAFIO',('proximo',)))
            else:
                self.botoes.append(Botao((425,395,430,58),'JOGAR NOVAMENTE',('tentar_novamente',)))
        else:
            self.botoes.append(Botao((425,395,430,58),'TENTAR NOVAMENTE',('tentar_novamente',)))
        self.botoes.append(Botao((425,475,430,58),'MENU DE DESAFIOS',('menu_desafios',)))
        self.finalizar(superficie,estado,posicao_mouse)
