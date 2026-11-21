from dataclasses import dataclass, field
from ..content.catalog import criar_missoes
from .mission import Missao
from .level import Desafio, StatusDesafio
from .monster import Monstro

@dataclass
class Comando:
    tipo: str
    quantidade: int = 2
    corpo: list['Comando'] = field(default_factory=list)


@dataclass
class EstadoJogo:
    missoes: tuple[Missao, ...] = field(default_factory=criar_missoes)
    missao_selecionada: Missao | None = None
    desafio_selecionado: Desafio | None = None
    comandos: list[Comando] = field(default_factory=list)
    destino_laco: int | None = None
    xp: int = 0
    nivel: int = 1
    musica_ativada: bool = True
    efeitos_ativados: bool = True
    audio_ativado: bool = True
    partida_iniciada: bool = False
    mensagem: str = 'Adicione comandos para planejar sua rota.'
    posicao_submarino: tuple[int, int] = (0, 2)
    orientacao_submarino: str = 'direita'
    monstros_restantes: list[Monstro] = field(default_factory=list)
    objetivos_restantes: set[tuple[int, int]] = field(default_factory=set)
    trajeto_missil: tuple[tuple[int, int], tuple[int, int]] | None = None
    impacto_missil: str | None = None
    executando: bool = False
    indice_comando: int = 0
    indice_interno: int = 0
    repeticao_atual: int = 1
    comando_em_execucao: tuple[int, int | None] | None = None
    repeticao_em_execucao: int = 0
    tempo_acumulado: float = 0
    tempo_resultado_ms: float = 0
    tipo_resultado: str | None = None
    mensagem_resultado: str = ''
    xp_recebido: int = 0
    proximo_disponivel: bool = False

    @property
    def total_blocos(self):
        return sum(1 + len(comando.corpo) for comando in self.comandos)

    @property
    def permite_repeticao(self):
        return bool(self.missao_selecionada and self.missao_selecionada.permite_repeticao)

    @property
    def desafios_concluidos(self):
        return tuple((missao.numero, desafio.numero)
                     for missao in self.missoes for desafio in missao.desafios
                     if desafio.status == StatusDesafio.CONCLUIDO)

    def aplicar_progresso(self, xp=0, nivel=1, concluidos=()):
        self.missoes = criar_missoes()
        self.xp, self.nivel = xp, nivel
        self.partida_iniciada = True
        self.missao_selecionada = None
        self.desafio_selecionado = None
        self.reiniciar_desafio()
        concluidos = set(concluidos)
        for missao in self.missoes:
            for desafio in missao.desafios:
                if (missao.numero, desafio.numero) in concluidos:
                    desafio.status = StatusDesafio.CONCLUIDO
        self.atualizar_desbloqueios()

    def atualizar_desbloqueios(self):
        anterior_concluida = True
        for missao in self.missoes:
            missao.disponivel = anterior_concluida
            missao.atualizar_desbloqueios()
            anterior_concluida = missao.disponivel and missao.concluida

    def reiniciar_desafio(self, preservar_comandos=False):
        if not preservar_comandos:
            self.comandos = []
        self.destino_laco = None
        self.posicao_submarino = (self.desafio_selecionado.posicao_inicial
                                  if self.desafio_selecionado else (0, 2))
        self.orientacao_submarino = 'direita'
        self.monstros_restantes = ([Monstro(posicao) for posicao in self.desafio_selecionado.monstros]
                                   if self.desafio_selecionado else [])
        self.objetivos_restantes = (set(self.desafio_selecionado.objetivos)
                                    if self.desafio_selecionado else set())
        self.trajeto_missil = None
        self.impacto_missil = None
        self.executando = False
        self.indice_comando = 0
        self.indice_interno = 0
        self.repeticao_atual = 1
        self.comando_em_execucao = None
        self.repeticao_em_execucao = 0
        self.tempo_acumulado = 0
        self.tempo_resultado_ms = 0
        self.tipo_resultado = None
        self.mensagem_resultado = ''
        self.xp_recebido = 0
        self.proximo_disponivel = False
        self.mensagem = 'Adicione comandos para planejar sua rota.'
