from .. import config as c
from ..models.level import StatusDesafio
from ..models.game_state import Comando

DIRECOES = {'cima': (0, -1), 'baixo': (0, 1), 'esquerda': (-1, 0), 'direita': (1, 0)}

class ControladorJogo:
    def __init__(self, estado):
        self.estado = estado

    def tratar_acao(self, acao):
        estado = self.estado
        if estado.executando or not estado.desafio_selecionado or estado.tipo_resultado:
            return
        tipo, *argumentos = acao
        if tipo == 'comando' and argumentos[0] in (*DIRECOES, 'foguete', 'repetir'):
            comando = argumentos[0]
            if comando == 'repetir' and estado.destino_laco is not None:
                estado.mensagem = 'Adicione laços na sequência principal.'
                return
            if estado.total_blocos >= estado.desafio_selecionado.limite_comandos:
                estado.mensagem = 'Limite de comandos atingido.'
                return
            destino = (estado.comandos if estado.destino_laco is None
                       else estado.comandos[estado.destino_laco].corpo)
            destino.append(Comando(comando))
            estado.mensagem = 'Clique no interior de um laço ou em Adicionar na sequência.'
        elif tipo == 'destino':
            indice = argumentos[0]
            if indice is None or (0 <= indice < len(estado.comandos)
                                  and estado.comandos[indice].tipo == 'repetir'):
                estado.destino_laco = indice
                estado.mensagem = ('Adicionar na sequência' if indice is None
                                   else 'Adicionar neste laço')
        elif tipo == 'quantidade':
            indice, ajuste = argumentos
            if 0 <= indice < len(estado.comandos):
                comando = estado.comandos[indice]
                if comando.tipo == 'repetir':
                    comando.quantidade = max(1, min(9, comando.quantidade + ajuste))
        elif tipo == 'remover':
            indice, interno = argumentos
            if 0 <= indice < len(estado.comandos):
                comando = estado.comandos[indice]
                if interno is not None:
                    if 0 <= interno < len(comando.corpo):
                        comando.corpo.pop(interno)
                else:
                    estado.comandos.pop(indice)
                    if comando.tipo == 'repetir':
                        estado.destino_laco = None
                    elif estado.destino_laco is not None and indice < estado.destino_laco:
                        estado.destino_laco -= 1
        elif tipo == 'limpar':
            estado.comandos = []
            estado.destino_laco = None
            estado.mensagem = 'Sequência limpa. Planeje uma nova rota.'
        elif tipo == 'executar':
            if not estado.comandos:
                estado.mensagem = 'Adicione ao menos um comando antes de executar.'
                return
            if any(comando.tipo == 'repetir' and not comando.corpo for comando in estado.comandos):
                estado.mensagem = 'Adicione comandos aos laços vazios.'
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
            self.executar_comando()

    def executar_comando(self):
        estado = self.estado
        if not estado.executando:
            return
        estado.trajeto_foguete = None
        estado.impacto_foguete = False
        estado.mensagem = 'Executando sua sequência…'
        bloco = estado.comandos[estado.indice_comando]
        em_laco = bloco.tipo == 'repetir'
        comando = bloco.corpo[estado.indice_interno] if em_laco else bloco
        estado.comando_em_execucao = (estado.indice_comando, estado.indice_interno if em_laco else None)
        estado.repeticao_em_execucao = estado.repeticao_atual if em_laco else 0
        if comando.tipo == 'foguete':
            self.disparar()
        else:
            self.mover(comando.tipo)
        if not estado.executando:
            return
        if estado.posicao_submarino == estado.desafio_selecionado.posicao_objetivo:
            self.finalizar('sucesso', 'Você encontrou a amostra.')
            return
        if em_laco:
            estado.mensagem += f' Repetição {estado.repeticao_em_execucao}/{bloco.quantidade}.'
            estado.indice_interno += 1
            if estado.indice_interno == len(bloco.corpo):
                estado.indice_interno = 0
                estado.repeticao_atual += 1
                if estado.repeticao_atual > bloco.quantidade:
                    estado.repeticao_atual = 1
                    estado.indice_comando += 1
        else:
            estado.indice_comando += 1
        if estado.indice_comando == len(estado.comandos):
            self.finalizar('erro', 'A sequência terminou antes de alcançar o objetivo.')

    def mover(self, direcao):
        estado = self.estado
        estado.orientacao_submarino = direcao
        deslocamento = DIRECOES[estado.orientacao_submarino]
        coluna, linha = (estado.posicao_submarino[0] + deslocamento[0],
                         estado.posicao_submarino[1] + deslocamento[1])
        if not (0 <= coluna < c.COLUNAS and 0 <= linha < c.LINHAS):
            self.finalizar('erro', 'O submarino tentou sair da área de exploração.')
            return
        if (coluna, linha) in estado.obstaculos_restantes:
            self.finalizar('erro', 'O submarino encontrou uma barreira.')
            return
        estado.posicao_submarino = (coluna, linha)

    def disparar(self):
        estado = self.estado
        dx, dy = DIRECOES[estado.orientacao_submarino]
        coluna, linha = estado.posicao_submarino
        coluna, linha = coluna + dx, linha + dy
        while 0 <= coluna < c.COLUNAS and 0 <= linha < c.LINHAS:
            if (coluna, linha) in estado.obstaculos_restantes:
                estado.obstaculos_restantes.remove((coluna, linha))
                estado.impacto_foguete = True
                break
            coluna, linha = coluna + dx, linha + dy
        estado.trajeto_foguete = (estado.posicao_submarino, (coluna, linha))
        estado.mensagem = ('Foguete: obstáculo destruído.' if estado.impacto_foguete
                           else 'Foguete disparado: nenhum obstáculo na direção.')

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
            estado.missao_selecionada.atualizar_desbloqueios()
            proximo = self.proximo_desafio()
            estado.proximo_disponivel = bool(proximo and proximo.jogavel)

    def proximo_desafio(self):
        estado = self.estado
        if not estado.missao_selecionada or not estado.desafio_selecionado:
            return None
        return next((desafio for desafio in estado.missao_selecionada.desafios
                     if desafio.numero == estado.desafio_selecionado.numero + 1
                     and desafio.implementado), None)
