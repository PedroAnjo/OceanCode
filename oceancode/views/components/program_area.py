import pygame
from .button import Botao, fonte, texto, painel, seta, missil, repetir
from .progress_bar import cadeado
from ... import config as c


ROTULOS = {'cima': 'Cima', 'baixo': 'Baixo', 'esquerda': 'Esquerda',
           'direita': 'Direita', 'missil': 'Míssil', 'repetir': 'Repetir'}
ALTURA_BLOCO = 46
PASSO_BLOCO = 54
INTERVALO_DUPLO_CLIQUE = 350


def desenhar_bloco(superficie, retangulo, tipo, rotulo, habilitado=True, ativo=False,
                   compacto=False, bloqueado=False):
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
    if bloqueado:
        cadeado(superficie, centro)
    elif tipo == 'missil':
        missil(superficie, centro)
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
        self.desafio = None
        self.ultimo_ativo = None
        self.alvos = []
        self.ultimo_clique = None
        self.com_foco = True

    def cancelar_interacao(self):
        self.ultimo_clique = None

    def rolar(self, quantidade, posicao):
        self.cancelar_interacao()
        if self.regiao.collidepoint(posicao):
            limite = max(0, self.altura_conteudo-self.regiao.height)
            self.rolagem = max(0, min(limite, self.rolagem-quantidade*40))

    def registrar_alvo(self, retangulo, tipo, caminho=None, comando=None):
        r = pygame.Rect(retangulo).clip(self.regiao)
        if r.width and r.height:
            self.alvos.append({'retangulo': r, 'tipo': tipo, 'caminho': caminho, 'comando': comando})

    def alvo_em(self, posicao):
        return next((alvo for alvo in self.alvos if alvo['retangulo'].collidepoint(posicao)), None)

    def alvo_valido(self, alvo, estado):
        if self.programa is not estado.comandos or self.desafio is not estado.desafio_selecionado:
            return False
        if alvo['tipo'] == 'fundo':
            return True
        indice, interno = alvo['caminho']
        if not 0 <= indice < len(estado.comandos):
            return False
        comando = estado.comandos[indice]
        if interno is not None:
            if not 0 <= interno < len(comando.corpo):
                return False
            comando = comando.corpo[interno]
        return comando is alvo['comando']

    def tratar_evento(self, evento, estado, ativa):
        if evento.type == pygame.WINDOWFOCUSLOST:
            self.com_foco = False
            self.cancelar_interacao()
        elif evento.type == pygame.WINDOWFOCUSGAINED:
            self.com_foco = True
        elif evento.type == pygame.WINDOWLEAVE:
            self.cancelar_interacao()

        editavel = ativa and self.com_foco and not estado.executando and not estado.tipo_resultado
        if not editavel:
            self.cancelar_interacao()
        if evento.type == pygame.MOUSEWHEEL and ativa and self.com_foco:
            posicao = pygame.mouse.get_pos()
            self.rolar(evento.y, posicao)
            return self.regiao.collidepoint(posicao), None
        if not editavel or evento.type != pygame.MOUSEBUTTONDOWN:
            return False, None

        anterior = self.ultimo_clique
        self.cancelar_interacao()
        if evento.button != 1:
            return False, None
        alvo = self.alvo_em(evento.pos)
        if alvo is None:
            return False, None
        if not self.alvo_valido(alvo, estado):
            return True, None
        if alvo['tipo'] == 'numero':
            return True, ('quantidade', alvo['caminho'][0])
        if alvo['tipo'] in ('comando', 'laco'):
            agora = pygame.time.get_ticks()
            if (anterior is not None and anterior[0] is alvo['comando']
                    and 0 <= agora - anterior[1] <= INTERVALO_DUPLO_CLIQUE):
                return True, ('remover', *alvo['caminho'])
            self.ultimo_clique = (alvo['comando'], agora)
        if alvo['tipo'] in ('laco', 'corpo'):
            return True, ('destino', alvo['caminho'][0])
        if alvo['tipo'] == 'fundo':
            return True, ('destino', None)
        return True, None

    def comando(self, superficie, r, comando, caminho, estado):
        ativo = estado.comando_em_execucao == caminho
        desenhar_bloco(superficie, r, comando.tipo, ROTULOS[comando.tipo], ativo=ativo)
        self.registrar_alvo(r, 'comando', caminho, comando)

    def laco(self, superficie, r, comando, indice, estado, mouse):
        editavel = not estado.executando and not estado.tipo_resultado
        selecionado = estado.destino_laco == indice and editavel
        cor = c.COR_REPETICAO_SELECIONADA if selecionado else c.COR_REPETICAO
        ativo = (estado.comando_em_execucao is not None
                 and estado.comando_em_execucao[0] == indice)
        corpo = pygame.Rect(r.x+20, r.y+52, r.width-20, r.height-72)
        pygame.draw.rect(superficie, c.SUAVE, corpo)
        pontos = [(r.x, r.y+5), (r.x+18, r.y+5), (r.x+23, r.y+10),
                  (r.x+43, r.y+10), (r.x+48, r.y+5), (r.right, r.y+5),
                  (r.right, corpo.y), (corpo.x, corpo.y), (corpo.x, corpo.bottom),
                  (r.right, corpo.bottom), (r.right, r.bottom-5),
                  (r.x+48, r.bottom-5), (r.x+43, r.bottom),
                  (r.x+23, r.bottom), (r.x+18, r.bottom-5), (r.x, r.bottom-5)]
        pygame.draw.polygon(superficie, cor, pontos)
        pygame.draw.polygon(superficie, c.AZUL_ESCURO if ativo else c.BORDA_REPETICAO,
                            pontos, 3 if ativo else 2)
        repetir(superficie, (r.x+27, r.y+29))
        texto(superficie, 'Repetir', (r.x+50, r.y+17), 20, peso='semibold')
        numero = pygame.Rect(r.x+50+fonte(20, 'semibold').size('Repetir ')[0], r.y+14, 30, 30)
        pygame.draw.rect(superficie, cor, numero, border_radius=6)
        borda = c.AZUL_ESCURO if editavel and numero.collidepoint(mouse) else c.BORDA_REPETICAO
        pygame.draw.rect(superficie, borda, numero, 1, border_radius=6)
        texto(superficie, comando.quantidade, numero.center, 20, centralizado=True, peso='semibold')
        texto(superficie, 'vezes', (numero.right+6, r.y+17), 20, peso='semibold')
        self.registrar_alvo(numero, 'numero', (indice, None), comando)
        if ativo:
            texto(superficie, f'{estado.repeticao_em_execucao}/{comando.quantidade}',
                  (r.right-52, r.y+29), 20, centralizado=True, peso='semibold')
        for interno, filho in enumerate(comando.corpo):
            filho_rect = pygame.Rect(corpo.x+12, corpo.y+6+interno*PASSO_BLOCO,
                                     corpo.width-24, ALTURA_BLOCO)
            self.comando(superficie, filho_rect, filho, (indice, interno), estado)
        for parte in ((r.x, r.y, r.width, 52), (r.x, corpo.y, 20, corpo.height),
                      (r.x, corpo.bottom, r.width, 20)):
            self.registrar_alvo(parte, 'laco', (indice, None), comando)
        self.registrar_alvo(corpo, 'corpo', (indice, None), comando)

    def desenhar(self, superficie, estado, mouse):
        self.alvos = []
        if self.programa is not estado.comandos or self.desafio is not estado.desafio_selecionado:
            self.cancelar_interacao()
            self.programa = estado.comandos
            self.desafio = estado.desafio_selecionado
            self.rolagem = 0
            self.ultimo_ativo = None
        painel(superficie, c.RETANGULO_PROGRAMACAO)
        texto(superficie, 'ÁREA DE PROGRAMAÇÃO', (732, 132), 22, peso='semibold')
        texto(superficie, f'{estado.total_blocos}/{estado.desafio_selecionado.limite_comandos} blocos',
              (1110, 136), 18)
        blocos = []
        y = 8
        for indice, comando in enumerate(estado.comandos):
            altura = (72+max(32, len(comando.corpo)*PASSO_BLOCO+4)
                      if comando.tipo == 'repetir' else ALTURA_BLOCO)
            blocos.append((indice, comando, pygame.Rect(self.regiao.x+24, y, self.regiao.width-56, altura)))
            y += altura+8
        self.altura_conteudo = y+8
        limite = max(0, self.altura_conteudo-self.regiao.height)
        self.rolagem = min(self.rolagem, limite)
        atual = estado.comando_em_execucao
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
                self.comando(superficie, r, comando, (indice, None), estado)
        self.registrar_alvo(self.regiao, 'fundo')
        superficie.set_clip(recorte)
        if limite:
            trilho = pygame.Rect(1204, self.regiao.y, 8, self.regiao.height)
            pygame.draw.rect(superficie, c.BORDA, trilho, border_radius=4)
            altura = max(24, self.regiao.height*self.regiao.height//self.altura_conteudo)
            topo = trilho.y+round((trilho.height-altura)*self.rolagem/limite)
            pygame.draw.rect(superficie, c.AZUL_ESCURO, (trilho.x, topo, 8, altura), border_radius=4)
