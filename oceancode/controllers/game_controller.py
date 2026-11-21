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
        if tipo == 'comando' and argumentos[0] in (*DIRECOES, 'missil', 'repetir'):
            comando = argumentos[0]
            if (comando == 'repetir' or estado.destino_laco is not None) and not estado.permite_repeticao:
                estado.mensagem = 'Repetir fica disponível a partir da missão de Repetição.'
                return
            if comando == 'repetir' and estado.destino_laco is not None:
                estado.mensagem = 'Adicione laços na sequência principal.'
                return
            if estado.total_blocos >= estado.desafio_selecionado.limite_comandos:
                estado.mensagem = 'Limite de comandos atingido.'
                return
            destino = (estado.comandos if estado.destino_laco is None
                       else estado.comandos[estado.destino_laco].corpo)
            destino.append(Comando(comando))
            estado.mensagem = ''
        elif tipo == 'destino':
            indice = argumentos[0]
            if indice is None or (estado.permite_repeticao and 0 <= indice < len(estado.comandos)
                                  and estado.comandos[indice].tipo == 'repetir'):
                estado.destino_laco = indice
        elif tipo == 'quantidade' and estado.permite_repeticao:
            indice = argumentos[0]
            if 0 <= indice < len(estado.comandos):
                comando = estado.comandos[indice]
                if comando.tipo == 'repetir':
                    comando.quantidade = comando.quantidade % 6 + 1
        elif tipo == 'remover':
            indice, interno = argumentos
            if 0 <= indice < len(estado.comandos):
                comando = estado.comandos[indice]
                if interno is not None:
                    if 0 <= interno < len(comando.corpo):
                        comando.corpo.pop(interno)
                else:
                    estado.comandos.pop(indice)
                    if estado.destino_laco == indice:
                        estado.destino_laco = None
                    elif estado.destino_laco is not None and indice < estado.destino_laco:
                        estado.destino_laco -= 1
        elif tipo == 'limpar':
            estado.comandos = []
            estado.destino_laco = None
            estado.mensagem = 'Sequência limpa. Planeje uma nova rota.'
        elif tipo == 'executar':
            if not self.validar_programa():
                return
            estado.reiniciar_desafio(preservar_comandos=True)
            estado.executando = True
            estado.mensagem = 'Executando sua sequência…'

    def validar_programa(self):
        estado = self.estado
        if not estado.comandos:
            estado.mensagem = 'Adicione ao menos um comando antes de executar.'
            return False
        for comando in estado.comandos:
            if comando.tipo != 'repetir':
                continue
            if not estado.permite_repeticao:
                estado.mensagem = 'Esta missão ainda não permite laços. Remova o bloco Repetir.'
                return False
            if not comando.corpo:
                estado.mensagem = 'Adicione comandos aos laços vazios.'
                return False
            if not 1 <= comando.quantidade <= 6:
                estado.mensagem = 'Escolha uma quantidade de repetições entre 1 e 6.'
                return False
        return True

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
        estado.trajeto_missil = None
        estado.impacto_missil = None
        estado.mensagem = 'Executando sua sequência…'
        bloco = estado.comandos[estado.indice_comando]
        em_laco = bloco.tipo == 'repetir'
        if em_laco and not estado.permite_repeticao:
            self.finalizar('erro', 'Esta missão ainda não permite laços.')
            return
        comando = bloco.corpo[estado.indice_interno] if em_laco else bloco
        estado.comando_em_execucao = (estado.indice_comando, estado.indice_interno if em_laco else None)
        estado.repeticao_em_execucao = estado.repeticao_atual if em_laco else 0
        if comando.tipo == 'missil':
            self.disparar()
        else:
            self.mover(comando.tipo)
        if not estado.executando:
            return
        estado.objetivos_restantes.discard(estado.posicao_submarino)
        if not estado.objetivos_restantes:
            mensagem = ('Você encontrou a amostra.' if len(estado.desafio_selecionado.objetivos) == 1
                        else 'Você encontrou todas as amostras.')
            self.finalizar('sucesso', mensagem)
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
            self.finalizar('erro', 'A sequência terminou antes de coletar todas as amostras.')

    def mover(self, direcao):
        estado = self.estado
        if direcao in ('esquerda', 'direita'):
            estado.orientacao_submarino = direcao
        deslocamento = DIRECOES[direcao]
        coluna, linha = (estado.posicao_submarino[0] + deslocamento[0],
                         estado.posicao_submarino[1] + deslocamento[1])
        if not (0 <= coluna < c.COLUNAS and 0 <= linha < c.LINHAS):
            self.finalizar('erro', 'O submarino tentou sair da área de exploração.')
            return
        if (coluna, linha) in estado.desafio_selecionado.obstaculos:
            self.finalizar('erro', 'O submarino encontrou uma rocha indestrutível.')
            return
        if any(monstro.posicao == (coluna, linha) for monstro in estado.monstros_restantes):
            self.finalizar('erro', 'Um monstro bloqueia o caminho. Destrua-o com o míssil.')
            return
        estado.posicao_submarino = (coluna, linha)

    def disparar(self):
        estado = self.estado
        estado.impacto_missil = None
        dx, dy = DIRECOES[estado.orientacao_submarino]
        coluna, linha = estado.posicao_submarino
        coluna, linha = coluna + dx, linha + dy
        while 0 <= coluna < c.COLUNAS and 0 <= linha < c.LINHAS:
            if (coluna, linha) in estado.desafio_selecionado.obstaculos:
                estado.impacto_missil = 'rocha'
                break
            monstro = next((monstro for monstro in estado.monstros_restantes
                            if monstro.posicao == (coluna, linha)), None)
            if monstro is not None:
                estado.monstros_restantes.remove(monstro)
                estado.impacto_missil = 'monstro'
                break
            coluna, linha = coluna + dx, linha + dy
        estado.trajeto_missil = (estado.posicao_submarino, (coluna, linha))
        mensagens = {'monstro': 'Míssil: monstro destruído.',
                     'rocha': 'Míssil bloqueado por uma rocha indestrutível.',
                     None: 'Míssil chegou à borda sem atingir um obstáculo.'}
        estado.mensagem = mensagens[estado.impacto_missil]

    def finalizar(self, tipo, mensagem):
        estado = self.estado
        if estado.tipo_resultado is not None:
            return
        estado.executando = False
        estado.tempo_resultado_ms = 0
        estado.tipo_resultado = tipo
        estado.mensagem_resultado = mensagem
        desafio = estado.desafio_selecionado
        if tipo == 'sucesso':
            if desafio.status != StatusDesafio.CONCLUIDO:
                estado.xp_recebido = desafio.recompensa_xp
                estado.xp += estado.xp_recebido
                desafio.status = StatusDesafio.CONCLUIDO
            estado.atualizar_desbloqueios()
            proximo = self.proximo_desafio()
            estado.proximo_disponivel = bool(proximo and proximo.jogavel)

    def proximo_desafio(self):
        estado = self.estado
        if not estado.missao_selecionada or not estado.desafio_selecionado:
            return None
        return next((desafio for desafio in estado.missao_selecionada.desafios
                     if desafio.numero == estado.desafio_selecionado.numero + 1
                     and desafio.implementado), None)
