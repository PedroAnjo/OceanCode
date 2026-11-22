import pygame
from .base_view import ViewBase
from .components.button import Botao, texto, painel
from .components.ocean_background import FundoOceanico
from .components.program_area import AreaProgramacao, AreaClique, desenhar_bloco, ROTULOS
from .. import config as c

class ViewJogo(ViewBase):
    def __init__(self):
        super().__init__()
        self.programacao = AreaProgramacao()
        self.fundo_tabuleiro = FundoOceanico(pygame.Rect(c.RETANGULO_TABULEIRO).size, c.IMAGEM_FUNDO)
        self.imagens = {}
        caminhos = {tipo: c.PASTA_IMAGENS / f'{tipo}.png'
                    for tipo in ('submarino', 'barreira', 'objetivo')}
        caminhos['monstro'] = c.IMAGEM_MONSTRO
        for tipo, caminho in caminhos.items():
            if caminho.is_file():
                try:
                    self.imagens[tipo] = pygame.image.load(str(caminho)).convert_alpha()
                except (pygame.error, OSError):
                    pass
        self.preparar_submarinos()

    def preparar_submarinos(self):
        imagem = self.imagens.get('submarino')
        if imagem is None:
            imagem = pygame.Surface((88, 64), pygame.SRCALPHA)
            x, y = 44, 32
            pygame.draw.polygon(imagem, c.AMARELO, [(x-25,y),(x-43,y-16),(x-43,y+16)])
            pygame.draw.ellipse(imagem, c.AMARELO, (x-33,y-18,72,36))
            pygame.draw.circle(imagem, c.AZUL_ESCURO, (x+12,y), 10)
            pygame.draw.circle(imagem, c.SUAVE, (x+14,y-3), 4)
            pygame.draw.lines(imagem, c.AMARELO, False, [(x,y-18),(x,y-29),(x+15,y-29)],6)
        proporcao = min(72 / imagem.get_width(), 54 / imagem.get_height())
        tamanho = (max(1, round(imagem.get_width() * proporcao)),
                   max(1, round(imagem.get_height() * proporcao)))
        direita = pygame.transform.smoothscale(imagem, tamanho)
        self.submarinos = {'direita': direita,
                          'esquerda': pygame.transform.flip(direita, True, False)}

    def desenhar_sprite(self, superficie, tipo, centro, tamanho, orientacao='direita'):
        if tipo == 'submarino':
            imagem = self.submarinos[orientacao]
            superficie.blit(imagem, imagem.get_rect(center=centro))
            return
        if tipo in self.imagens:
            imagem = self.imagens[tipo]
            proporcao = min(tamanho[0]/imagem.get_width(), tamanho[1]/imagem.get_height())
            imagem = pygame.transform.smoothscale(imagem, (max(1,int(imagem.get_width()*proporcao)),max(1,int(imagem.get_height()*proporcao))))
            superficie.blit(imagem, imagem.get_rect(center=centro))
            return
        x,y = centro
        if tipo == 'barreira':
            pygame.draw.polygon(superficie, c.AZUL_ESCURO, [(x-32,y+21),(x-23,y-12),(x+5,y-24),(x+30,y+2),(x+34,y+21)])
            pygame.draw.line(superficie, c.BORDA, (x-20,y-5), (x+3,y-16), 4)
        elif tipo == 'monstro':
            self.desenhar_monstro(superficie, centro)
        else:
            pygame.draw.circle(superficie, c.BRANCO, (x,y),22,3)
            pygame.draw.polygon(superficie, c.AMARELO, [(x,y-15),(x+12,y),(x,y+15),(x-12,y)])

    def desenhar_monstro(self, superficie, centro):
        x, y = centro
        cor = (153, 100, 173)
        for lado in (-1, 1):
            pygame.draw.polygon(superficie, cor,
                                [(x+lado*12, y-10), (x+lado*27, y-25), (x+lado*24, y)])
        for deslocamento in (-18, 0, 18):
            pygame.draw.lines(superficie, cor, False,
                              [(x+deslocamento, y+9), (x+deslocamento, y+23),
                               (x+deslocamento+8, y+19)], 6)
        pygame.draw.ellipse(superficie, cor, (x-28, y-18, 56, 38))
        for deslocamento in (-10, 10):
            pygame.draw.circle(superficie, c.BRANCO, (x+deslocamento, y-4), 8)
            pygame.draw.circle(superficie, c.AZUL_ESCURO, (x+deslocamento, y-4), 4)
        pygame.draw.line(superficie, c.AZUL_ESCURO, (x-10, y+11), (x+10, y+11), 3)

    def tabuleiro(self, superficie, estado):
        retangulo = pygame.Rect(c.RETANGULO_TABULEIRO)
        painel(superficie, retangulo.inflate(8,8), c.BORDA)
        self.fundo_tabuleiro.desenhar(superficie, retangulo.topleft)
        largura_celula, altura_celula = retangulo.width//c.COLUNAS, retangulo.height//c.LINHAS
        for coluna in range(c.COLUNAS+1):
            pygame.draw.line(superficie,c.BORDA,(retangulo.x+coluna*largura_celula,retangulo.y),(retangulo.x+coluna*largura_celula,retangulo.bottom))
        for linha in range(c.LINHAS+1):
            pygame.draw.line(superficie,c.BORDA,(retangulo.x,retangulo.y+linha*altura_celula),(retangulo.right,retangulo.y+linha*altura_celula))
        def centro(posicao):
            coluna,linha = posicao
            return retangulo.x+coluna*largura_celula+largura_celula//2,retangulo.y+linha*altura_celula+altura_celula//2
        for posicao in estado.desafio_selecionado.obstaculos:
            self.desenhar_sprite(superficie,'barreira',centro(posicao),(72,54))
        for monstro in estado.monstros_restantes:
            self.desenhar_sprite(superficie, 'monstro', centro(monstro.posicao), (72,54))
        for posicao in estado.objetivos_restantes:
            self.desenhar_sprite(superficie, 'objetivo', centro(posicao), (48,48))
        if estado.trajeto_missil:
            inicio, fim = (centro(posicao) for posicao in estado.trajeto_missil)
            recorte = superficie.get_clip()
            superficie.set_clip(retangulo)
            pygame.draw.line(superficie, c.BRANCO, inicio, fim, 6)
            pygame.draw.line(superficie, c.AMARELO, inicio, fim, 3)
            if estado.impacto_missil == 'monstro':
                pygame.draw.circle(superficie, c.BRANCO, fim, 18, 3)
                for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    pygame.draw.line(superficie, c.AMARELO, (fim[0] + dx * 12, fim[1] + dy * 12),
                                     (fim[0] + dx * 22, fim[1] + dy * 22), 3)
            elif estado.impacto_missil == 'rocha':
                pygame.draw.circle(superficie, c.CINZA, fim, 12, 3)
            superficie.set_clip(recorte)
        self.desenhar_sprite(superficie,'submarino',centro(estado.posicao_submarino),(84,58),
                             estado.orientacao_submarino)

    def desenhar(self, superficie, estado, posicao_mouse):
        self.iniciar(superficie)
        desafio = estado.desafio_selecionado
        self.cabecalho(superficie, f'Desafio {desafio.numero} — {desafio.nome}', desafio.objetivo,
                       peso='semibold')
        self.hud(superficie,estado)
        self.tabuleiro(superficie,estado)
        painel(superficie,c.RETANGULO_PAINEL_COMANDOS)
        editavel = not estado.executando and not estado.tipo_resultado
        rotulo = 'COMANDOS • clique para adicionar' if editavel else 'COMANDOS • edição bloqueada'
        texto(superficie,rotulo,(64,530),18,peso='semibold')
        for indice, tipo in enumerate(('cima','baixo','esquerda','direita','missil','repetir')):
            retangulo = pygame.Rect(60+indice*104,554,96,74)
            bloqueado = tipo == 'repetir' and not estado.permite_repeticao
            habilitado = (editavel and not bloqueado
                          and (tipo != 'repetir' or estado.destino_laco is None))
            desenhar_bloco(superficie, retangulo, tipo, ROTULOS[tipo], habilitado,
                            ativo=habilitado and retangulo.collidepoint(posicao_mouse),
                            compacto=True, bloqueado=bloqueado)
            self.botoes.append(AreaClique(retangulo, '', ('comando',tipo), habilitado))
        self.programacao.desenhar(superficie, estado, posicao_mouse)
        editavel = not estado.executando and not estado.tipo_resultado
        selecionado = estado.comando_selecionado is not None
        self.botoes += [
            Botao((958, 124, 36, 32), '↑', ('mover_selecionado', -1),
                  editavel and selecionado),
            Botao((998, 124, 36, 32), '↓', ('mover_selecionado', 1),
                  editavel and selecionado),
            Botao((1038, 124, 52, 32), '+', ('inserir',), editavel and selecionado),
        ]
        self.botoes += [Botao(c.RETANGULO_EXECUTAR,'Executar',('executar',),editavel),
                        Botao(c.RETANGULO_LIMPAR,
                              'Restaurar programa' if desafio.tipo.name == 'DEPURACAO' else 'Limpar',
                              ('limpar',), editavel)]
        mensagem = estado.mensagem_resultado if estado.tipo_resultado else estado.mensagem
        texto(superficie,mensagem,(48,662),18,largura_maxima=1184)
        self.finalizar(superficie,estado,posicao_mouse)
