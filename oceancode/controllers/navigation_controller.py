class ControladorNavegacao:
    def __init__(self, estado):
        self.estado = estado
        self.ativa = 'inicio'

    def voltar(self):
        self.estado.executando = False
        self.ativa = {'missoes': 'inicio', 'desafios': 'missoes',
                      'jogo': 'desafios', 'retorno': 'desafios'}.get(self.ativa, 'inicio')

    def selecionar_missao(self, numero):
        missao = next((missao for missao in self.estado.missoes if missao.numero == numero), None)
        if missao and missao.disponivel:
            self.estado.missao_selecionada = missao
            self.estado.desafio_selecionado = None
            self.ativa = 'desafios'

    def selecionar_desafio(self, numero):
        missao = self.estado.missao_selecionada
        desafio = next((desafio for desafio in missao.desafios if desafio.numero == numero), None) if missao else None
        if desafio and desafio.jogavel:
            self.estado.desafio_selecionado = desafio
            self.estado.reiniciar_desafio()
            self.ativa = 'jogo'

    def tentar_novamente(self):
        self.estado.reiniciar_desafio(preservar_comandos=True)
        self.ativa = 'jogo'
