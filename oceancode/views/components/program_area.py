import pygame
from .button import Botao, texto, painel, seta, foguete, repetir
from ... import config as c


ROTULOS = {'cima': 'Cima', 'baixo': 'Baixo', 'esquerda': 'Esquerda',
           'direita': 'Direita', 'foguete': 'Foguete', 'repetir': 'Repetir'}
ALTURA_BLOCO = 46
PASSO_BLOCO = 54


def desenhar_bloco(superficie, retangulo, tipo, rotulo, habilitado=True, ativo=False, compacto=False):
    r = pygame.Rect(retangulo)
    cor = c.COR_REPETICAO if tipo == 'repetir' else c.AMARELO
    if not habilitado:
        cor = c.CINZA
    pontos = [(r.x, r.y+5), (r.x+18, r.y+5), (r.x+23, r.y+10),
              (r.x+43, r.y+10), (r.x+48, r.y+5), (r.right, r.y+5),
              (r.right, r.bottom-5), (r.x+48, r.bottom-5), (r.x+43, r.bottom),
              (r.x+23, r.bottom), (r.x+18, r.bottom-5), (r.x, r.bottom-5)]
    pygame.draw.polygon(superficie, cor, pontos)
    pygame.draw.polygon(superficie, c.AZUL_ESCURO if ativo else c.BORDA, pontos, 3 if ativo else 2)
    centro = (r.centerx, r.y+27) if compacto else (r.x+26, r.centery)
    if tipo == 'foguete':
        foguete(superficie, centro)
    elif tipo == 'repetir':
        repetir(superficie, centro)
    else:
        seta(superficie, tipo, centro)
    if compacto:
        texto(superficie, rotulo, (r.centerx, r.bottom-16), 16, centralizado=True,
              peso='semibold', largura_maxima=r.width-12)
    else:
        texto(superficie, rotulo, (r.x+49, r.centery-12), 20,
              peso='semibold', largura_maxima=r.width-88)


class AreaClique(Botao):
    def desenhar(self, superficie, posicao_mouse):
        pass


class AreaProgramacao:
    def __init__(self):
        self.regiao = pygame.Rect(c.RETANGULO_CONTEUDO_PROGRAMA)
        self.rolagem = 0
        self.altura_conteudo = 0
        self.programa = None
        self.ultimo_ativo = None
        self.botoes = []

    def rolar(self, quantidade, posicao):
        if self.regiao.collidepoint(posicao):
            limite = max(0, self.altura_conteudo-self.regiao.height)
            self.rolagem = max(0, min(limite, self.rolagem-quantidade*40))

    def area(self, retangulo, acao, habilitado, recortar=True):
        r = pygame.Rect(retangulo)
        if recortar:
            r = r.clip(self.regiao)
        if r.width and r.height:
            self.botoes.append(AreaClique(r, '', acao, habilitado))

    def controle(self, superficie, retangulo, rotulo, acao, habilitado, mouse):
        r = pygame.Rect(retangulo)
        cor = c.BRANCO if habilitado else c.CINZA
        if habilitado and r.collidepoint(mouse):
            cor = c.AMARELO_HOVER
        pygame.draw.rect(superficie, cor, r, border_radius=6)
        pygame.draw.rect(superficie, c.AZUL_ESCURO, r, 1, border_radius=6)
        texto(superficie, rotulo, r.center, 20, centralizado=True, peso='semibold')
        self.area(r, acao, habilitado)

    def insercao(self, superficie, retangulo, rotulo, destino, estado, recortar=True):
        r = pygame.Rect(retangulo)
        selecionado = estado.destino_laco == destino and not estado.executando
        pygame.draw.rect(superficie, c.BRANCO, r, border_radius=8)
        pygame.draw.rect(superficie, c.AZUL_ESCURO if selecionado else c.BORDA, r,
                         3 if selecionado else 1, border_radius=8)
        texto(superficie, rotulo, r.center, 18, centralizado=True, peso='semibold',
              largura_maxima=r.width-16)
        self.area(r, ('destino', destino), not estado.executando, recortar)

    def comando(self, superficie, r, comando, caminho, estado, mouse):
        ativo = estado.executando and estado.comando_em_execucao == caminho
        desenhar_bloco(superficie, r, comando.tipo, ROTULOS[comando.tipo], ativo=ativo)
        self.controle(superficie, (r.right-34, r.y+10, 26, 26), '×',
                      ('remover', *caminho), not estado.executando, mouse)

    def laco(self, superficie, r, comando, indice, estado, mouse):
        selecionado = estado.destino_laco == indice and not estado.executando
        ativo = (estado.executando and estado.comando_em_execucao is not None
                 and estado.comando_em_execucao[0] == indice)
        corpo = pygame.Rect(r.x+20, r.y+52, r.width-20, r.height-72)
        pygame.draw.rect(superficie, c.BRANCO if selecionado else c.SUAVE, corpo)
        pontos = [(r.x, r.y+5), (r.x+18, r.y+5), (r.x+23, r.y+10),
                  (r.x+43, r.y+10), (r.x+48, r.y+5), (r.right, r.y+5),
                  (r.right, corpo.y), (corpo.x, corpo.y), (corpo.x, corpo.bottom),
                  (r.right, corpo.bottom), (r.right, r.bottom-5),
                  (r.x+48, r.bottom-5), (r.x+43, r.bottom),
                  (r.x+23, r.bottom), (r.x+18, r.bottom-5), (r.x, r.bottom-5)]
        pygame.draw.polygon(superficie, c.COR_REPETICAO, pontos)
        pygame.draw.polygon(superficie, c.AZUL_ESCURO if ativo else c.BORDA_REPETICAO,
                            pontos, 3 if ativo else 2)
        repetir(superficie, (r.x+27, r.y+29))
        texto(superficie, f'Repetir {comando.quantidade} vezes', (r.x+50, r.y+17), 20,
              peso='semibold', largura_maxima=r.width-220)
        if ativo:
            texto(superficie, f'{estado.repeticao_em_execucao}/{comando.quantidade}',
                  (r.right-160, r.y+29), 20, centralizado=True, peso='semibold')
        for deslocamento, rotulo, ajuste in [(130, '−', -1), (92, '+', 1)]:
            habilitado = not estado.executando and 1 <= comando.quantidade+ajuste <= 9
            self.controle(superficie, (r.right-deslocamento, r.y+14, 30, 30), rotulo,
                          ('quantidade', indice, ajuste), habilitado, mouse)
        self.controle(superficie, (r.right-34, r.y+16, 26, 26), '×',
                      ('remover', indice, None), not estado.executando, mouse)
        if selecionado:
            pygame.draw.rect(superficie, c.AZUL_ESCURO, corpo, 2)
        for interno, filho in enumerate(comando.corpo):
            filho_rect = pygame.Rect(corpo.x+12, corpo.y+6+interno*PASSO_BLOCO,
                                     corpo.width-24, ALTURA_BLOCO)
            self.comando(superficie, filho_rect, filho, (indice, interno), estado, mouse)
        insercao = pygame.Rect(corpo.x+12, corpo.bottom-42, corpo.width-24, 34)
        rotulo = 'Adicionar neste laço' if comando.corpo else 'Adicionar comandos aqui'
        self.insercao(superficie, insercao, rotulo, indice, estado)
        self.area(corpo, ('destino', indice), not estado.executando)

    def desenhar(self, superficie, estado, mouse):
        self.botoes = []
        if self.programa is not estado.comandos:
            self.programa = estado.comandos
            self.rolagem = 0
        painel(superficie, c.RETANGULO_PROGRAMACAO)
        texto(superficie, 'ÁREA DE PROGRAMAÇÃO', (732, 132), 22, peso='semibold')
        texto(superficie, f'{estado.total_blocos}/{estado.desafio_selecionado.limite_comandos} blocos',
              (1110, 136), 18)
        self.insercao(superficie, (740, 164, 450, 32), 'Adicionar na sequência', None,
                      estado, recortar=False)
        blocos = []
        y = 8
        for indice, comando in enumerate(estado.comandos):
            altura = 122+len(comando.corpo)*PASSO_BLOCO if comando.tipo == 'repetir' else ALTURA_BLOCO
            blocos.append((indice, comando, pygame.Rect(self.regiao.x+8, y, 450, altura)))
            y += altura+8
        self.altura_conteudo = y+50
        limite = max(0, self.altura_conteudo-self.regiao.height)
        self.rolagem = min(self.rolagem, limite)
        atual = estado.comando_em_execucao if estado.executando else None
        if atual is not None and atual != self.ultimo_ativo:
            alvo = blocos[atual[0]][2].copy()
            if atual[1] is not None:
                alvo.y += 58+atual[1]*PASSO_BLOCO
                alvo.height = ALTURA_BLOCO
            if alvo.y < self.rolagem:
                self.rolagem = alvo.y
            elif alvo.bottom > self.rolagem+self.regiao.height:
                self.rolagem = alvo.bottom-self.regiao.height
        self.ultimo_ativo = atual
        recorte = superficie.get_clip()
        superficie.set_clip(self.regiao)
        for indice, comando, r in blocos:
            r.y += self.regiao.y-self.rolagem
            if comando.tipo == 'repetir':
                self.laco(superficie, r, comando, indice, estado, mouse)
            else:
                self.comando(superficie, r, comando, (indice, None), estado, mouse)
        self.insercao(superficie, (740, self.regiao.y+y-self.rolagem, 450, 34),
                      'Adicionar na sequência', None, estado)
        superficie.set_clip(recorte)
        if limite:
            trilho = pygame.Rect(1204, self.regiao.y, 8, self.regiao.height)
            pygame.draw.rect(superficie, c.BORDA, trilho, border_radius=4)
            altura = max(24, self.regiao.height*self.regiao.height//self.altura_conteudo)
            topo = trilho.y+round((trilho.height-altura)*self.rolagem/limite)
            pygame.draw.rect(superficie, c.AZUL_ESCURO, (trilho.x, topo, 8, altura), border_radius=4)
        if estado.executando:
            rotulo = 'Executando • edição bloqueada'
            if atual is not None and atual[1] is not None:
                quantidade = estado.comandos[atual[0]].quantidade
                rotulo = f'Repetição {estado.repeticao_em_execucao}/{quantidade} • edição bloqueada'
        else:
            destino = 'Adicionar na sequência' if estado.destino_laco is None else 'Adicionar neste laço'
            rotulo = f'{destino} • role para ver mais • × remove'
        texto(superficie, rotulo, (740, 561), 16, largura_maxima=470)
