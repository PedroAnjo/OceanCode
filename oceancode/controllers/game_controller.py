from .. import config as c
from ..models.level import StatusDesafio

DIRECOES = {'cima': (0, -1), 'baixo': (0, 1), 'esquerda': (-1, 0), 'direita': (1, 0)}

class ControladorJogo:
    def __init__(self, estado):
        self.estado = estado

    def tratar_acao(self, acao):
        estado = self.estado
        if estado.executando or not estado.desafio_selecionado or estado.tipo_resultado:
            return
        tipo, *argumentos = acao
        if tipo == 'comando' and argumentos[0] in DIRECOES:
            if len(estado.comandos) < estado.desafio_selecionado.limite_comandos:
                estado.comandos.append(argumentos[0])
                estado.mensagem = 'Clique em um comando da sequência para removê-lo.'
            else:
                estado.mensagem = 'Limite de comandos atingido.'
        elif tipo == 'remover' and 0 <= argumentos[0] < len(estado.comandos):
            estado.comandos.pop(argumentos[0])
        elif tipo == 'limpar':
            estado.comandos.clear()
            estado.mensagem = 'Sequência limpa. Planeje uma nova rota.'
        elif tipo == 'executar':
            if not estado.comandos:
                estado.mensagem = 'Adicione ao menos um comando antes de executar.'
                return
            estado.reiniciar_desafio(preservar_comandos=True)
            estado.executando = True
            estado.mensagem = 'Executando sua sequência…'

    def atualizar(self, tempo_decorrido):
        estado = self.estado
        if not estado.executando:
            return
        estado.tempo_acumulado += tempo_decorrido
        while estado.executando and estado.tempo_acumulado >= c.INTERVALO_COMANDOS:
            estado.tempo_acumulado -= c.INTERVALO_COMANDOS
            self.mover()

    def mover(self):
        estado = self.estado
        desafio = estado.desafio_selecionado
        deslocamento = DIRECOES[estado.comandos[estado.indice_comando]]
        coluna, linha = (estado.posicao_submarino[0] + deslocamento[0],
                         estado.posicao_submarino[1] + deslocamento[1])
        if not (0 <= coluna < c.COLUNAS and 0 <= linha < c.LINHAS):
            self.finalizar('erro', 'O submarino tentou sair da área de exploração.')
            return
        if (coluna, linha) in desafio.obstaculos:
            self.finalizar('erro', 'O submarino encontrou uma barreira.')
            return
        estado.posicao_submarino = (coluna, linha)
        estado.indice_comando += 1
        if estado.posicao_submarino == desafio.posicao_objetivo:
            self.finalizar('sucesso', 'Você encontrou a amostra.')
        elif estado.indice_comando == len(estado.comandos):
            self.finalizar('erro', 'A sequência terminou antes de alcançar o objetivo.')

    def finalizar(self, tipo, mensagem):
        estado = self.estado
        estado.executando = False
        estado.tipo_resultado = tipo
        estado.mensagem_resultado = mensagem
        desafio = estado.desafio_selecionado
        if tipo == 'sucesso':
            if desafio.status != StatusDesafio.CONCLUIDO:
                estado.xp_recebido = desafio.recompensa_xp
                estado.xp += estado.xp_recebido
                desafio.status = StatusDesafio.CONCLUIDO
            proximo = self.proximo_desafio()
            if proximo and proximo.status == StatusDesafio.BLOQUEADO:
                proximo.status = StatusDesafio.DISPONIVEL
            estado.proximo_disponivel = bool(proximo and proximo.jogavel)

    def proximo_desafio(self):
        estado = self.estado
        if not estado.missao_selecionada or not estado.desafio_selecionado:
            return None
        return next((desafio for desafio in estado.missao_selecionada.desafios
                     if desafio.numero == estado.desafio_selecionado.numero + 1
                     and desafio.implementado), None)
