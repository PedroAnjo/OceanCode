"""Verificação de regras sem renderização e do fluxo por cliques, sem janela."""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
from collections import deque
import pygame
from oceancode import config as c
from oceancode.models.game_state import EstadoJogo
from oceancode.models.level import StatusDesafio
from oceancode.controllers.game_controller import ControladorJogo, DIRECOES
from oceancode.controllers.navigation_controller import ControladorNavegacao
from oceancode.controllers.app_controller import ControladorAplicacao


def encontrar_rota(desafio):
    fila = deque([(desafio.posicao_inicial, [])])
    visitados = {desafio.posicao_inicial}
    while fila:
        posicao, rota = fila.popleft()
        if posicao == desafio.posicao_objetivo:
            return rota
        for direcao, (dx, dy) in DIRECOES.items():
            seguinte = (posicao[0]+dx, posicao[1]+dy)
            if (0 <= seguinte[0] < c.COLUNAS and 0 <= seguinte[1] < c.LINHAS
                    and seguinte not in desafio.obstaculos and seguinte not in visitados):
                visitados.add(seguinte)
                fila.append((seguinte, rota+[direcao]))
    raise AssertionError('Mapa sem rota válida')


def verificar_logica():
    estado = EstadoJogo()
    navegacao = ControladorNavegacao(estado)
    jogo = ControladorJogo(estado)
    navegacao.selecionar_missao(1)
    rotas = []
    for numero, xp_esperado in [(1,20),(2,50),(3,100)]:
        navegacao.selecionar_desafio(numero)
        desafio = estado.desafio_selecionado
        rota = encontrar_rota(desafio)
        rotas.append(rota)
        assert len(rota) <= desafio.limite_comandos
        for direcao in rota:
            jogo.tratar_acao(('comando',direcao))
        jogo.tratar_acao(('executar',))
        posicao = estado.posicao_submarino
        jogo.atualizar(c.INTERVALO_COMANDOS/2)
        assert estado.posicao_submarino == posicao
        jogo.tratar_acao(('limpar',))
        jogo.tratar_acao(('remover',0))
        jogo.tratar_acao(('comando','baixo'))
        assert estado.comandos == rota
        jogo.atualizar(c.INTERVALO_COMANDOS*(len(rota)+1))
        assert estado.tipo_resultado == 'sucesso' and estado.xp == xp_esperado
        assert desafio.status == StatusDesafio.CONCLUIDO
        navegacao.selecionar_desafio(numero)
        estado.comandos.extend(rota)
        jogo.tratar_acao(('executar',))
        jogo.atualizar(10)
        assert estado.xp == xp_esperado and estado.xp_recebido == 0
    assert len(rotas[2]) > len(rotas[1]) > len(rotas[0])
    assert all(desafio.status == StatusDesafio.BLOQUEADO for desafio in estado.missoes[0].desafios[3:])
    assert estado.missoes[0].concluidos == 3
    for numero, comandos, trecho in [(1,['esquerda'],'sair'),(2,['direita'],'barreira'),(1,['cima'],'terminou')]:
        navegacao.selecionar_desafio(numero)
        estado.comandos.extend(comandos)
        jogo.tratar_acao(('executar',))
        jogo.atualizar(10)
        assert estado.tipo_resultado == 'erro' and trecho in estado.mensagem_resultado
    print('PASS: mapas, temporização, colisões, progressão, repetição e XP (100)')


def verificar_interface():
    aplicacao = ControladorAplicacao()
    def clicar(acao):
        aplicacao.desenhar()
        botao = next(botao for botao in aplicacao.telas[aplicacao.navegacao.ativa].botoes if botao.acao == acao)
        aplicacao.tratar_evento(pygame.event.Event(pygame.MOUSEBUTTONDOWN,button=1,pos=botao.retangulo.center))
    try:
        assert aplicacao.navegacao.ativa == 'inicio'
        assert aplicacao.estado.xp == 0 and aplicacao.estado.nivel == 1
        if c.MUSICA_FUNDO.is_file():
            assert aplicacao.audio.musica_carregada and pygame.mixer.music.get_busy()
        if c.SOM_CLIQUE.is_file():
            assert aplicacao.audio.som_clique is not None
            aplicacao.audio.tocar_clique()
            assert aplicacao.audio.som_clique.get_num_channels() > 0
        clicar(('musica',))
        assert not aplicacao.estado.musica_ativada
        assert not pygame.mixer.music.get_busy()
        if aplicacao.audio.som_clique is not None:
            assert aplicacao.audio.som_clique.get_num_channels() == 0
        clicar(('musica',))
        if aplicacao.audio.musica_carregada:
            assert pygame.mixer.music.get_busy()
        clicar(('musica',))
        assert aplicacao.telas['inicio'].botoes[-1].icone == 'som_desligado'
        clicar(('jogar',))
        assert aplicacao.navegacao.ativa == 'missoes'
        for numero in (2,3,4):
            clicar(('missao',numero))
            assert aplicacao.navegacao.ativa == 'missoes'
        clicar(('missao',1))
        assert aplicacao.navegacao.ativa == 'desafios'
        for numero in range(2,11):
            clicar(('desafio',numero))
            assert aplicacao.navegacao.ativa == 'desafios'
        clicar(('desafio',1))
        assert aplicacao.navegacao.ativa == 'jogo'
        for direcao in DIRECOES:
            clicar(('comando',direcao))
        clicar(('remover',1))
        assert aplicacao.estado.comandos == ['cima','esquerda','direita']
        clicar(('limpar',))
        clicar(('executar',))
        assert not aplicacao.estado.executando and 'Adicione' in aplicacao.estado.mensagem
        for _ in range(8):
            clicar(('comando','direita'))
        assert len(aplicacao.estado.comandos) == 5
        clicar(('limpar',))
        for _ in range(3):
            clicar(('comando','direita'))
        clicar(('executar',))
        clicar(('limpar',))
        assert len(aplicacao.estado.comandos) == 3
        aplicacao.atualizar(2)
        assert aplicacao.navegacao.ativa == 'retorno'
        assert aplicacao.estado.xp == 20 and aplicacao.estado.missoes[0].desafios[1].jogavel
        clicar(('proximo',))
        assert aplicacao.estado.desafio_selecionado.numero == 2
        clicar(('comando','direita'))
        clicar(('executar',))
        aplicacao.atualizar(1)
        assert aplicacao.estado.tipo_resultado == 'erro'
        clicar(('tentar_novamente',))
        assert aplicacao.estado.posicao_submarino == (0,4) and aplicacao.estado.comandos == ['direita']
        clicar(('limpar',))
        for direcao in encontrar_rota(aplicacao.estado.desafio_selecionado):
            clicar(('comando',direcao))
        clicar(('executar',))
        aplicacao.atualizar(5)
        clicar(('proximo',))
        for direcao in encontrar_rota(aplicacao.estado.desafio_selecionado):
            clicar(('comando',direcao))
        clicar(('executar',))
        aplicacao.atualizar(5)
        aplicacao.desenhar()
        assert aplicacao.estado.xp == 100
        assert not any(botao.acao == ('proximo',) for botao in aplicacao.telas['retorno'].botoes)
        clicar(('menu_desafios',))
        clicar(('desafio',4))
        assert aplicacao.navegacao.ativa == 'desafios'
        clicar(('desafio',1))
        clicar(('comando','direita'))
        clicar(('executar',))
        clicar(('voltar',))
        assert not aplicacao.estado.executando
        clicar(('voltar',)); clicar(('voltar',))
        assert aplicacao.navegacao.ativa == 'inicio'
        clicar(('sair',))
        assert not aplicacao.em_execucao
    finally:
        pygame.quit()
    aplicacao = ControladorAplicacao()
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    aplicacao.executar()
    assert not pygame.display.get_init()
    print('PASS: cinco telas, cliques, bloqueios, execução, retorno, som e encerramento')

if __name__ == '__main__':
    verificar_logica()
    verificar_interface()
