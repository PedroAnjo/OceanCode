from dataclasses import dataclass, field
from .mission import Missao, criar_missoes
from .level import Desafio

@dataclass
class EstadoJogo:
    missoes: tuple[Missao, ...] = field(default_factory=criar_missoes)
    missao_selecionada: Missao | None = None
    desafio_selecionado: Desafio | None = None
    comandos: list[str] = field(default_factory=list)
    xp: int = 0
    nivel: int = 1
    musica_ativada: bool = True
    mensagem: str = 'Adicione comandos para planejar sua rota.'
    posicao_submarino: tuple[int, int] = (0, 2)
    executando: bool = False
    indice_comando: int = 0
    tempo_acumulado: float = 0
    tipo_resultado: str | None = None
    mensagem_resultado: str = ''
    xp_recebido: int = 0
    proximo_disponivel: bool = False

    def reiniciar_desafio(self, preservar_comandos=False):
        if not preservar_comandos:
            self.comandos.clear()
        self.posicao_submarino = self.desafio_selecionado.posicao_inicial
        self.executando = False
        self.indice_comando = 0
        self.tempo_acumulado = 0
        self.tipo_resultado = None
        self.mensagem_resultado = ''
        self.xp_recebido = 0
        self.proximo_disponivel = False
        self.mensagem = 'Adicione comandos para planejar sua rota.'
