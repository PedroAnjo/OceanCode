import pygame
from .base_view import ViewBase
from .components.button import Botao, texto, painel
from .components.ocean_background import FundoOceanico
from .. import config as c

class ViewJogo(ViewBase):
    def __init__(self):
        super().__init__()
        self.fundo_tabuleiro = FundoOceanico(pygame.Rect(c.RETANGULO_TABULEIRO).size, c.IMAGEM_FUNDO)
        self.imagens = {}
        for tipo in ('submarino','barreira','objetivo'):
            caminho = c.PASTA_IMAGENS / f'{tipo}.png'
            if caminho.is_file():
                try:
                    self.imagens[tipo] = pygame.image.load(str(caminho)).convert_alpha()
                except (pygame.error, OSError):
                    pass

    def desenhar_sprite(self, superficie, tipo, centro, tamanho):
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
        elif tipo == 'submarino':
            pygame.draw.polygon(superficie, c.AMARELO, [(x-25,y),(x-43,y-16),(x-43,y+16)])
            pygame.draw.ellipse(superficie, c.AMARELO, (x-33,y-18,72,36))
            pygame.draw.circle(superficie, c.AZUL_ESCURO, (x+12,y), 10)
            pygame.draw.circle(superficie, c.SUAVE, (x+14,y-3), 4)
            pygame.draw.lines(superficie, c.AMARELO, False, [(x,y-18),(x,y-29),(x+15,y-29)],6)
        else:
            pygame.draw.circle(superficie, c.BRANCO, (x,y),22,3)
            pygame.draw.polygon(superficie, c.AMARELO, [(x,y-15),(x+12,y),(x,y+15),(x-12,y)])

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
        self.desenhar_sprite(superficie,'objetivo',centro(estado.desafio_selecionado.posicao_objetivo),(48,48))
        self.desenhar_sprite(superficie,'submarino',centro(estado.posicao_submarino),(84,58))

    def desenhar(self, superficie, estado, posicao_mouse):
        self.iniciar(superficie)
        desafio = estado.desafio_selecionado
        self.cabecalho(superficie, f'Desafio {desafio.numero} — {desafio.nome}', desafio.objetivo)
        self.hud(superficie,estado)
        self.tabuleiro(superficie,estado)
        painel(superficie,c.RETANGULO_PAINEL_COMANDOS)
        texto(superficie,'COMANDOS',(1084,145),24,centralizado=True)
        self.botoes = [Botao((988,180+indice*76,192,60),'',('comando',direcao),not estado.executando,direcao)
                       for indice,direcao in enumerate(('cima','baixo','esquerda','direita'))]
        painel(superficie,c.RETANGULO_PROGRAMACAO)
        texto(superficie,'ÁREA DE PROGRAMAÇÃO',(72,533),22)
        texto(superficie,f'{len(estado.comandos)}/{desafio.limite_comandos} • Clique para remover',(540,536),18)
        for indice in range(desafio.limite_comandos):
            retangulo = pygame.Rect(c.ORIGEM_SLOTS[0]+indice*c.ESPACAMENTO_SLOTS,
                                    c.ORIGEM_SLOTS[1],*c.TAMANHO_SLOT)
            if indice < len(estado.comandos):
                self.botoes.append(Botao(retangulo,'',('remover',indice),not estado.executando,estado.comandos[indice]))
                if estado.executando and indice == estado.indice_comando:
                    pygame.draw.rect(superficie,c.AZUL_ESCURO,retangulo.inflate(8,8),3,border_radius=12)
            else:
                pygame.draw.rect(superficie,c.BORDA,retangulo,2,border_radius=10)
        self.botoes += [Botao(c.RETANGULO_EXECUTAR,'Executar',('executar',),not estado.executando),
                        Botao(c.RETANGULO_LIMPAR,'Limpar',('limpar',),not estado.executando)]
        texto(superficie,estado.mensagem,(48,662),18)
        self.finalizar(superficie,estado,posicao_mouse)
