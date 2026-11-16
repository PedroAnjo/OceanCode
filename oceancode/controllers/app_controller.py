import pygame
from .. import config as c
from ..views.components.button import fonte
from ..views.components.options_menu import MenuOpcoes
from ..views.components.new_game_confirmation import ConfirmacaoNovaPartida
from ..views.components.tutorial_panel import PainelTutorial
from ..models.game_state import EstadoJogo
from ..persistence import PersistenciaJogo, ErroPersistencia
from ..views.start_view import ViewInicio
from ..views.mission_view import ViewMissoes
from ..views.level_view import ViewDesafios
from ..views.game_view import ViewJogo
from ..views.result_view import ViewRetorno
from .navigation_controller import ControladorNavegacao
from .game_controller import ControladorJogo
from .audio_controller import ControladorAudio

class ControladorAplicacao:
    def __init__(self, caminho_banco=None):
        pygame.display.init()
        pygame.font.init()
        fonte.cache_clear()
        self.superficie = pygame.display.set_mode((c.LARGURA,c.ALTURA))
        pygame.display.set_caption(c.TITULO)
        self.relogio = pygame.time.Clock()
        self.estado = EstadoJogo()
        self.persistencia = PersistenciaJogo(caminho_banco)
        self.mensagem_persistencia = ''
        self.mensagem_audio = ''
        self.carregar_dados_iniciais()
        self.audio = ControladorAudio(self.estado)
        self.navegacao = ControladorNavegacao(self.estado)
        self.jogo = ControladorJogo(self.estado)
        self.telas = {'inicio':ViewInicio(),'missoes':ViewMissoes(),'desafios':ViewDesafios(),
                      'jogo':ViewJogo(),'retorno':ViewRetorno()}
        self.menu = MenuOpcoes()
        self.menu_aberto = False
        self.confirmacao = ConfirmacaoNovaPartida()
        self.confirmacao_aberta = False
        self.tutorial = PainelTutorial()
        self.tutorial_aberto = False
        self.em_execucao = True
        self.desenhar()

    @property
    def sobreposicao_aberta(self):
        return self.menu_aberto or self.confirmacao_aberta or self.tutorial_aberto

    def carregar_dados_iniciais(self):
        try:
            self.persistencia.preparar()
            self.estado.musica_ativada, self.estado.efeitos_ativados = self.persistencia.carregar_preferencias()
            self.estado.partida_iniciada = self.persistencia.existe_salvamento()
        except ErroPersistencia:
            self.mensagem_persistencia = 'Não foi possível acessar os dados salvos.'

    def atualizar_disponibilidade(self):
        try:
            self.estado.partida_iniciada = self.persistencia.existe_salvamento()
        except ErroPersistencia:
            self.mensagem_persistencia = 'Não foi possível verificar o salvamento.'
            return False
        return True

    def solicitar_nova_partida(self):
        if not self.atualizar_disponibilidade():
            return
        if self.estado.partida_iniciada:
            self.confirmacao_aberta = True
        else:
            self.iniciar_nova_partida()

    def iniciar_nova_partida(self):
        try:
            self.persistencia.iniciar_partida()
        except ErroPersistencia:
            self.mensagem_persistencia = 'Não foi possível salvar a nova partida. Nenhum progresso foi alterado.'
            return
        self.estado.aplicar_progresso()
        self.confirmacao_aberta = False
        self.menu_aberto = False
        self.mensagem_persistencia = ''
        self.navegacao.ativa = 'missoes'

    def continuar_partida(self):
        try:
            progresso = self.persistencia.carregar_progresso()
        except ErroPersistencia:
            self.mensagem_persistencia = 'Não foi possível carregar a partida. Seu salvamento foi mantido.'
            return
        if progresso is None:
            self.estado.partida_iniciada = False
            self.mensagem_persistencia = 'Nenhuma partida salva. Use Iniciar para começar.'
            return
        self.estado.aplicar_progresso(*progresso)
        self.mensagem_persistencia = ''
        self.navegacao.ativa = 'missoes'

    def salvar_progresso(self):
        try:
            self.persistencia.salvar_progresso(self.estado.xp, self.estado.nivel, self.estado.desafios_concluidos)
        except ErroPersistencia:
            self.mensagem_persistencia = 'Não foi possível salvar o progresso. As novas conquistas estão apenas nesta sessão.'
            return
        self.estado.partida_iniciada = True
        self.mensagem_persistencia = ''

    def alterar_preferencia(self, tipo):
        musica = not self.estado.musica_ativada if tipo == 'musica' else self.estado.musica_ativada
        efeitos = not self.estado.efeitos_ativados if tipo == 'efeitos' else self.estado.efeitos_ativados
        try:
            self.persistencia.salvar_preferencias(musica, efeitos)
        except ErroPersistencia:
            self.mensagem_audio = 'Não foi possível salvar o áudio. A opção anterior foi mantida.'
            return
        self.mensagem_audio = ''
        self.estado.musica_ativada, self.estado.efeitos_ativados = musica, efeitos
        if tipo == 'musica':
            self.audio.atualizar_musica()
        else:
            self.audio.atualizar_efeitos()

    def tratar_acao(self, acao):
        tipo,*argumentos = acao
        if tipo == 'sair':
            self.em_execucao = False
        elif tipo == 'iniciar' and self.navegacao.ativa == 'inicio':
            self.solicitar_nova_partida()
        elif tipo == 'continuar' and self.navegacao.ativa == 'inicio':
            self.continuar_partida()
        elif tipo == 'confirmar_nova_partida' and self.confirmacao_aberta:
            self.iniciar_nova_partida()
        elif tipo == 'cancelar_nova_partida':
            self.confirmacao_aberta = False
        elif tipo == 'voltar':
            self.navegacao.voltar()
            if self.navegacao.ativa == 'inicio':
                self.atualizar_disponibilidade()
        elif tipo == 'abrir_menu':
            self.menu_aberto = True
        elif tipo == 'fechar_menu':
            self.menu_aberto = False
        elif tipo == 'abrir_tutorial':
            self.menu_aberto = False
            self.tutorial.rolagem = 0
            self.tutorial_aberto = True
        elif tipo == 'fechar_tutorial':
            self.tutorial_aberto = False
            self.menu_aberto = False
        elif tipo == 'voltar_inicio':
            self.menu_aberto = False
            self.navegacao.voltar_inicio()
            self.atualizar_disponibilidade()
        elif tipo in ('musica', 'efeitos'):
            self.alterar_preferencia(tipo)
        elif tipo == 'missao':
            self.navegacao.selecionar_missao(argumentos[0])
        elif tipo == 'desafio':
            self.navegacao.selecionar_desafio(argumentos[0])
        elif tipo == 'tentar_novamente' and self.navegacao.ativa == 'retorno':
            self.navegacao.tentar_novamente()
        elif tipo == 'menu_desafios':
            self.estado.executando = False
            self.navegacao.ativa = 'desafios'
        elif tipo == 'proximo' and self.navegacao.ativa == 'retorno':
            proximo = self.jogo.proximo_desafio()
            if proximo:
                self.navegacao.selecionar_desafio(proximo.numero)
        elif self.navegacao.ativa == 'jogo':
            self.jogo.tratar_acao(acao)

    def tratar_evento(self, evento):
        if evento.type == pygame.QUIT:
            self.em_execucao = False
        elif self.tutorial_aberto:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.tratar_acao(('fechar_tutorial',))
                else:
                    deslocamentos = {pygame.K_UP: -40, pygame.K_DOWN: 40,
                                     pygame.K_PAGEUP: -self.tutorial.regiao.height,
                                     pygame.K_PAGEDOWN: self.tutorial.regiao.height,
                                     pygame.K_HOME: -self.tutorial.limite_rolagem,
                                     pygame.K_END: self.tutorial.limite_rolagem}
                    self.tutorial.rolar(deslocamentos.get(evento.key, 0))
            elif evento.type == pygame.MOUSEWHEEL:
                if self.tutorial.regiao.collidepoint(pygame.mouse.get_pos()):
                    self.tutorial.rolar(-evento.y * 40)
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for botao in self.tutorial.botoes:
                    if botao.contem(evento.pos):
                        self.tratar_acao(botao.acao)
                        self.audio.tocar_clique()
                        break
            self.desenhar()
        elif (evento.type == pygame.MOUSEWHEEL and self.navegacao.ativa == 'jogo'
              and not self.sobreposicao_aberta):
            self.telas['jogo'].programacao.rolar(evento.y, pygame.mouse.get_pos())
            self.desenhar()
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            if self.confirmacao_aberta:
                self.confirmacao_aberta = False
            elif self.menu_aberto:
                self.menu_aberto = False
            else:
                self.tratar_acao(('voltar',))
            self.desenhar()
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.confirmacao_aberta:
                botoes = self.confirmacao.botoes
            elif self.menu_aberto:
                botoes = self.menu.botoes
            else:
                botoes = self.telas[self.navegacao.ativa].botoes
            for botao in botoes:
                if botao.contem(evento.pos):
                    self.tratar_acao(botao.acao)
                    self.audio.tocar_clique()
                    break
            self.desenhar()

    def atualizar(self, tempo_decorrido):
        if self.sobreposicao_aberta:
            return
        if self.navegacao.ativa == 'jogo':
            self.jogo.atualizar(tempo_decorrido)
            if self.estado.tipo_resultado:
                if self.estado.tipo_resultado == 'sucesso':
                    self.salvar_progresso()
                self.navegacao.ativa = 'retorno'

    def desenhar(self):
        posicao_mouse = pygame.mouse.get_pos()
        self.telas[self.navegacao.ativa].desenhar(
            self.superficie, self.estado,
            (-1, -1) if self.sobreposicao_aberta else posicao_mouse)
        if self.tutorial_aberto:
            self.tutorial.desenhar(self.superficie, posicao_mouse)
        elif self.confirmacao_aberta:
            self.confirmacao.desenhar(self.superficie, posicao_mouse)
        elif self.menu_aberto:
            self.menu.desenhar(self.superficie, self.estado, posicao_mouse,
                               tela_inicial=self.navegacao.ativa == 'inicio')
        aviso = self.mensagem_audio or self.mensagem_persistencia
        if aviso:
            self.telas[self.navegacao.ativa].desenhar_aviso(self.superficie, aviso)

    def executar(self):
        try:
            while self.em_execucao:
                tempo_decorrido = self.relogio.tick(c.FPS)/1000
                sobreposicao_aberta = self.sobreposicao_aberta
                for evento in pygame.event.get():
                    self.tratar_evento(evento)
                    sobreposicao_aberta = sobreposicao_aberta or self.sobreposicao_aberta
                # O tempo do quadro ainda pertence à pausa se um evento fechar um painel.
                self.atualizar(0 if sobreposicao_aberta else tempo_decorrido)
                self.desenhar()
                pygame.display.flip()
        finally:
            pygame.quit()
