import pygame
from .. import config as c
from ..views.components.button import fonte
from ..models.game_state import EstadoJogo
from ..views.start_view import ViewInicio
from ..views.mission_view import ViewMissoes
from ..views.level_view import ViewDesafios
from ..views.game_view import ViewJogo
from ..views.result_view import ViewRetorno
from .navigation_controller import ControladorNavegacao
from .game_controller import ControladorJogo
from .audio_controller import ControladorAudio

class ControladorAplicacao:
    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        fonte.cache_clear()
        self.superficie = pygame.display.set_mode((c.LARGURA,c.ALTURA))
        pygame.display.set_caption(c.TITULO)
        self.relogio = pygame.time.Clock()
        self.estado = EstadoJogo()
        self.audio = ControladorAudio(self.estado)
        self.navegacao = ControladorNavegacao(self.estado)
        self.jogo = ControladorJogo(self.estado)
        self.telas = {'inicio':ViewInicio(),'missoes':ViewMissoes(),'desafios':ViewDesafios(),
                      'jogo':ViewJogo(),'retorno':ViewRetorno()}
        self.em_execucao = True
        self.desenhar()

    def tratar_acao(self, acao):
        tipo,*argumentos = acao
        if tipo == 'sair':
            self.em_execucao = False
        elif tipo == 'jogar':
            self.navegacao.ativa = 'missoes'
        elif tipo == 'voltar':
            self.navegacao.voltar()
        elif tipo == 'musica':
            self.estado.musica_ativada = not self.estado.musica_ativada
            self.audio.atualizar_som()
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
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.navegacao.voltar()
            self.desenhar()
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for botao in self.telas[self.navegacao.ativa].botoes:
                if botao.contem(evento.pos):
                    self.tratar_acao(botao.acao)
                    self.audio.tocar_clique()
                    break
            self.desenhar()

    def atualizar(self, tempo_decorrido):
        if self.navegacao.ativa == 'jogo':
            self.jogo.atualizar(tempo_decorrido)
            if self.estado.tipo_resultado:
                self.navegacao.ativa = 'retorno'

    def desenhar(self):
        self.telas[self.navegacao.ativa].desenhar(self.superficie,self.estado,pygame.mouse.get_pos())

    def executar(self):
        try:
            while self.em_execucao:
                tempo_decorrido = self.relogio.tick(c.FPS)/1000
                for evento in pygame.event.get():
                    self.tratar_evento(evento)
                self.atualizar(tempo_decorrido)
                self.desenhar()
                pygame.display.flip()
        finally:
            pygame.quit()
