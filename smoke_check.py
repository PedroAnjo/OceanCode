"""Verificação de regras sem renderização e do fluxo por cliques, sem janela."""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
from collections import deque
from contextlib import closing
from copy import deepcopy
from math import isclose
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch
import wave
import sqlite3
import pygame
from oceancode import config as c
from oceancode.content.catalog import criar_missoes
from oceancode.models.game_state import EstadoJogo
from oceancode.models.level import Desafio, StatusDesafio, TipoDesafio
from oceancode.controllers.game_controller import ControladorJogo, DIRECOES
from oceancode.controllers.navigation_controller import ControladorNavegacao
from oceancode.controllers.app_controller import ControladorAplicacao
from oceancode.controllers.audio_controller import ControladorAudio
from oceancode.persistence import PersistenciaJogo, ErroPersistencia


def clicar_botao(aplicacao, acao, ao_fundo=False):
    aplicacao.desenhar()
    if aplicacao.confirmacao_aberta and not ao_fundo:
        botoes = aplicacao.confirmacao.botoes
    elif aplicacao.menu_aberto and not ao_fundo:
        botoes = aplicacao.menu.botoes
    else:
        botoes = aplicacao.telas[aplicacao.navegacao.ativa].botoes
    botao = next(botao for botao in botoes if botao.acao == acao)
    aplicacao.tratar_evento(pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, button=1, pos=botao.retangulo.center))


def pressionar_escape(aplicacao):
    aplicacao.tratar_evento(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))


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


def verificar_catalogo():
    missoes = criar_missoes()
    assert (c.LINHAS, c.COLUNAS) == (6, 8)
    assert [(m.numero, m.nome, m.conteudo, m.recompensa, m.disponivel) for m in missoes] == [
        (1, 'Primeiras Expediçôes', 'Sequências', 100, True),
        (2, 'Rotas Perigosas', 'Depuração', 150, False),
        (3, 'Decisões no Abismo', 'Condicionais', 200, False),
        (4, 'Correntes Marinhas', 'Repetição', 250, False)]
    tipos = (TipoDesafio.SEQUENCIA, TipoDesafio.DEPURACAO,
             TipoDesafio.CONDICIONAIS, TipoDesafio.REPETICAO)
    for missao, tipo in zip(missoes, tipos):
        assert len(missao.desafios) == 10
        assert [d.numero for d in missao.desafios] == list(range(1, 11))
        assert all(d.tipo == tipo for d in missao.desafios)
        assert missao.concluidos == 0
        bloqueados = missao.desafios[1:] if missao.numero == 1 else missao.desafios
        assert all(not d.jogavel and d.status == StatusDesafio.BLOQUEADO for d in bloqueados)
        if missao.numero != 1:
            assert all(not d.implementado for d in missao.desafios)
    assert [(d.numero, d.nome, d.objetivo, d.posicao_inicial, d.posicao_objetivo,
             d.obstaculos, d.limite_comandos, d.recompensa_xp, d.implementado, d.status)
            for d in missoes[0].desafios[:3]] == [
        (1, 'Primeiros Movimentos', 'Leve o submarino até a amostra.',
         (0, 2), (3, 2), (), 5, 20, True, StatusDesafio.DISPONIVEL),
        (2, 'Contornando Obstáculos', 'Contorne a rocha e alcance a amostra.',
         (0, 4), (3, 2), ((1, 4),), 7, 30, True, StatusDesafio.BLOQUEADO),
        (3, 'Rota de Exploração', 'Leve o submarino até a amostra.',
         (0, 5), (4, 1), ((0, 4), (2, 4), (2, 2), (4, 3)),
         10, 50, True, StatusDesafio.BLOQUEADO)]
    # Um status disponível sozinho não pode habilitar conteúdo não implementado.
    assert not Desafio(4, status=StatusDesafio.DISPONIVEL).jogavel
    outra_sessao = EstadoJogo()
    for missao, outra in zip(missoes, outra_sessao.missoes):
        assert missao is not outra
        assert all(d is not outro for d, outro in zip(missao.desafios, outra.desafios))
    missoes[0].desafios[0].status = StatusDesafio.CONCLUIDO
    missoes[0].desafios[1].status = StatusDesafio.DISPONIVEL
    missoes[1].disponivel = True
    assert outra_sessao.missoes[0].desafios[0].status == StatusDesafio.DISPONIVEL
    assert outra_sessao.missoes[0].desafios[1].status == StatusDesafio.BLOQUEADO
    assert not outra_sessao.missoes[1].disponivel and outra_sessao.xp == 0
    print('PASS: catálogo, dados dos desafios, tipos, tabuleiro 6 × 8 e isolamento de sessões')


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
        assert estado.xp_recebido == desafio.recompensa_xp
        assert estado.proximo_disponivel == estado.missoes[0].desafios[numero].implementado
        if estado.proximo_disponivel:
            assert estado.missoes[0].desafios[numero].jogavel
        navegacao.selecionar_desafio(numero)
        estado.comandos.extend(rota)
        jogo.tratar_acao(('executar',))
        jogo.atualizar(10)
        assert estado.xp == xp_esperado and estado.xp_recebido == 0
    assert len(rotas[2]) > len(rotas[1]) > len(rotas[0])
    quarto = estado.missoes[0].desafios[3]
    assert quarto.jogavel == quarto.implementado
    assert jogo.proximo_desafio() is (quarto if quarto.implementado else None)
    assert all(desafio.status == StatusDesafio.BLOQUEADO and not desafio.jogavel
               for desafio in estado.missoes[0].desafios[4:])
    assert estado.missoes[0].concluidos == 3
    for numero, comandos, trecho in [(1,['esquerda'],'sair'),(2,['direita'],'barreira'),(1,['cima'],'terminou')]:
        navegacao.selecionar_desafio(numero)
        estado.comandos.extend(comandos)
        jogo.tratar_acao(('executar',))
        jogo.atualizar(10)
        assert estado.tipo_resultado == 'erro' and trecho in estado.mensagem_resultado
    print('PASS: mapas, temporização, colisões, progressão, repetição e XP (100)')


def verificar_interface(caminho_banco):
    aplicacao = ControladorAplicacao(caminho_banco)
    def clicar(acao, ao_fundo=False):
        clicar_botao(aplicacao, acao, ao_fundo)

    def verificar_menu(tela, acao_ao_fundo):
        assert aplicacao.navegacao.ativa == tela and not aplicacao.menu_aberto
        clicar(('abrir_menu',))
        assert aplicacao.menu_aberto
        assert len(aplicacao.menu.botoes) == 4
        inicio = next(botao for botao in aplicacao.menu.botoes if botao.acao == ('voltar_inicio',))
        assert inicio.habilitado == (tela != 'inicio')
        assert all(aplicacao.menu.retangulo.contains(botao.retangulo) for botao in aplicacao.menu.botoes)
        with patch.object(aplicacao.audio, 'tocar_clique') as som:
            clicar(acao_ao_fundo, ao_fundo=True)
            clicar(('abrir_menu',), ao_fundo=True)
            if tela != 'inicio':
                clicar(('voltar',), ao_fundo=True)
            else:
                clicar(('voltar_inicio',))
            for posicao in [(10, 700), (aplicacao.menu.retangulo.centerx, aplicacao.menu.retangulo.y + 20)]:
                aplicacao.tratar_evento(pygame.event.Event(
                    pygame.MOUSEBUTTONDOWN, button=1, pos=posicao))
            som.assert_not_called()
        assert aplicacao.menu_aberto and aplicacao.navegacao.ativa == tela
        pressionar_escape(aplicacao)
        assert not aplicacao.menu_aberto and aplicacao.navegacao.ativa == tela
        clicar(('abrir_menu',))
        clicar(('fechar_menu',))
        assert not aplicacao.menu_aberto and aplicacao.navegacao.ativa == tela

    try:
        assert aplicacao.navegacao.ativa == 'inicio'
        assert aplicacao.estado.xp == 0 and aplicacao.estado.nivel == 1
        assert aplicacao.estado.musica_ativada and aplicacao.estado.efeitos_ativados
        assert not pygame.Rect(c.RETANGULO_MENU).colliderect(c.RETANGULO_HUD)
        verificar_menu('inicio', ('iniciar',))
        clicar(('abrir_menu',))
        for acao, musica, efeitos in [('musica', False, True), ('efeitos', False, False),
                                      ('musica', True, False), ('efeitos', True, True),
                                      ('musica', False, True), ('efeitos', False, False)]:
            clicar((acao,))
            assert aplicacao.estado.musica_ativada == musica
            assert aplicacao.estado.efeitos_ativados == efeitos
            rotulos = {botao.acao: botao.rotulo for botao in aplicacao.menu.botoes}
            assert rotulos[('musica',)] == f'Música: {"ligada" if musica else "desligada"}'
            assert rotulos[('efeitos',)] == f'Efeitos sonoros: {"ligados" if efeitos else "desligados"}'
        clicar(('fechar_menu',))
        clicar(('iniciar',))
        assert aplicacao.navegacao.ativa == 'missoes'
        verificar_menu('missoes', ('missao', 1))
        for numero in (2,3,4):
            clicar(('missao',numero))
            assert aplicacao.navegacao.ativa == 'missoes'
        clicar(('missao',1))
        assert aplicacao.navegacao.ativa == 'desafios'
        verificar_menu('desafios', ('desafio', 1))
        for numero in range(2,11):
            clicar(('desafio',numero))
            assert aplicacao.navegacao.ativa == 'desafios'
        clicar(('desafio',1))
        assert aplicacao.navegacao.ativa == 'jogo'
        verificar_menu('jogo', ('comando', 'direita'))
        assert aplicacao.estado.comandos == []
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
        aplicacao.atualizar(c.INTERVALO_COMANDOS * 1.25)
        estado = aplicacao.estado
        posicao, indice, tempo = estado.posicao_submarino, estado.indice_comando, estado.tempo_acumulado
        comandos = list(estado.comandos)
        assert indice == 1 and isclose(tempo, c.INTERVALO_COMANDOS / 4)
        clicar(('abrir_menu',))
        for _ in range(3):
            aplicacao.atualizar(30)
            assert estado.executando and aplicacao.navegacao.ativa == 'jogo'
            assert (estado.posicao_submarino, estado.indice_comando, estado.tempo_acumulado) == (posicao, indice, tempo)
            assert estado.comandos == comandos
        clicar(('voltar',), ao_fundo=True)
        assert estado.executando
        pressionar_escape(aplicacao)
        assert not aplicacao.menu_aberto and aplicacao.navegacao.ativa == 'jogo'
        aplicacao.atualizar(c.INTERVALO_COMANDOS / 2)
        assert estado.posicao_submarino == posicao and estado.indice_comando == indice
        aplicacao.atualizar(c.INTERVALO_COMANDOS * 0.3)
        assert estado.indice_comando == indice + 1
        assert isclose(estado.tempo_acumulado, c.INTERVALO_COMANDOS * 0.05)
        aplicacao.atualizar(2)
        assert aplicacao.navegacao.ativa == 'retorno'
        assert aplicacao.estado.xp == 20 and aplicacao.estado.missoes[0].desafios[1].jogavel
        verificar_menu('retorno', ('menu_desafios',))
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
        assert any(botao.acao == ('proximo',) for botao in aplicacao.telas['retorno'].botoes) == bool(aplicacao.jogo.proximo_desafio())
        clicar(('menu_desafios',))
        for desafio in aplicacao.estado.missoes[0].desafios[3:]:
            if not desafio.jogavel:
                clicar(('desafio', desafio.numero))
                assert aplicacao.navegacao.ativa == 'desafios'
        progresso = (estado.xp, estado.nivel,
                     tuple((missao.disponivel, tuple(d.status for d in missao.desafios))
                           for missao in estado.missoes))
        preferencias = (estado.musica_ativada, estado.efeitos_ativados)
        clicar(('desafio',1))
        for _ in range(3):
            clicar(('comando','direita'))
        clicar(('executar',))
        aplicacao.atualizar(c.INTERVALO_COMANDOS * 1.25)
        assert estado.executando and estado.tempo_acumulado > 0
        clicar(('abrir_menu',))
        clicar(('voltar_inicio',))
        assert aplicacao.navegacao.ativa == 'inicio' and not aplicacao.menu_aberto
        assert not estado.executando and estado.tempo_acumulado == 0
        assert (estado.xp, estado.nivel,
                tuple((missao.disponivel, tuple(d.status for d in missao.desafios))
                      for missao in estado.missoes)) == progresso
        assert (estado.musica_ativada, estado.efeitos_ativados) == preferencias
        posicao = estado.posicao_submarino
        aplicacao.atualizar(30)
        assert estado.posicao_submarino == posicao and estado.tempo_acumulado == 0
        clicar(('continuar',))
        clicar(('missao',1))
        clicar(('desafio',1))
        clicar(('comando','direita'))
        clicar(('executar',))
        clicar(('voltar',))
        assert not aplicacao.estado.executando
        pressionar_escape(aplicacao)
        assert aplicacao.navegacao.ativa == 'missoes'
        clicar(('voltar',))
        assert aplicacao.navegacao.ativa == 'inicio'
        clicar(('sair',))
        assert not aplicacao.em_execucao
    finally:
        pygame.quit()
    aplicacao = ControladorAplicacao(caminho_banco)
    clicar_botao(aplicacao, ('abrir_menu',))
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    aplicacao.executar()
    assert not pygame.display.get_init()
    print('PASS: cinco telas, menu, bloqueios, pausa, retorno ao início, preferências, Escape e encerramento')


def verificar_pausa_no_loop(caminho_banco):
    for fechamento in ('escape', 'fechar_menu'):
        aplicacao = ControladorAplicacao(caminho_banco)
        aplicacao.navegacao.selecionar_missao(1)
        aplicacao.navegacao.selecionar_desafio(1)
        aplicacao.estado.comandos.extend(['direita'] * 3)
        aplicacao.tratar_acao(('executar',))
        aplicacao.atualizar(c.INTERVALO_COMANDOS * 1.25)
        clicar_botao(aplicacao, ('abrir_menu',))
        if fechamento == 'escape':
            evento = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
        else:
            botao = next(botao for botao in aplicacao.menu.botoes if botao.acao == ('fechar_menu',))
            evento = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=botao.retangulo.center)
        aplicacao.relogio = Mock()
        aplicacao.relogio.tick.side_effect = [5000, 200, 100, 0]
        with patch('pygame.event.get', side_effect=[[evento], [], [], [pygame.event.Event(pygame.QUIT)]]):
            aplicacao.executar()
        assert not aplicacao.menu_aberto and aplicacao.navegacao.ativa == 'jogo'
        assert aplicacao.estado.executando and aplicacao.estado.indice_comando == 2
        assert aplicacao.estado.posicao_submarino == (2, 2)
        assert isclose(aplicacao.estado.tempo_acumulado, c.INTERVALO_COMANDOS / 4 + 0.3 - c.INTERVALO_COMANDOS)
    print('PASS: loop descarta o tempo do menu ao fechar por clique ou Escape')


def verificar_audio():
    with TemporaryDirectory() as diretorio:
        arquivo = Path(diretorio) / 'audio.wav'
        with wave.open(str(arquivo), 'wb') as gravacao:
            gravacao.setnchannels(1)
            gravacao.setsampwidth(2)
            gravacao.setframerate(22050)
            gravacao.writeframes(bytes(22050 * 2 * 10))
        try:
            with patch.object(c, 'SOM_CLIQUE', arquivo), patch.object(c, 'MUSICA_FUNDO', arquivo):
                audio = ControladorAudio(EstadoJogo())
                assert audio.musica_carregada and audio.musica_iniciada
                assert pygame.mixer.music.get_busy()
                estado = EstadoJogo(musica_ativada=False)
                audio = ControladorAudio(estado)
                assert audio.musica_carregada and not audio.musica_iniciada
                assert not pygame.mixer.music.get_busy()
                audio.tocar_clique()
                assert audio.som_clique.get_num_channels() > 0
                with patch.object(pygame.mixer.music, 'play', wraps=pygame.mixer.music.play) as iniciar:
                    for musica, efeitos in [(True, True), (False, True), (False, False), (True, False), (True, True)]:
                        canais = audio.som_clique.get_num_channels()
                        estado.musica_ativada = musica
                        audio.atualizar_musica()
                        assert audio.som_clique.get_num_channels() == canais
                        estado.efeitos_ativados = efeitos
                        audio.atualizar_efeitos()
                        audio.tocar_clique()
                        assert bool(audio.som_clique.get_num_channels()) == efeitos
                        assert pygame.mixer.music.get_busy() == musica
                    iniciar.assert_called_once_with(loops=-1)
                pygame.mixer.quit()
                audio.tocar_clique()
                audio.atualizar_musica()
                estado.efeitos_ativados = False
                audio.atualizar_efeitos()
        finally:
            pygame.mixer.quit()
    print('PASS: quatro combinações de áudio, pausa/retomada da trilha e interrupção independente dos efeitos')


def verificar_sem_audio(caminho_banco):
    with TemporaryDirectory() as diretorio:
        ausente = Path(diretorio) / 'ausente.wav'
        invalido = Path(diretorio) / 'invalido.wav'
        invalido.write_bytes(b'arquivo sem audio valido')
        for arquivo in (ausente, invalido):
            try:
                with patch.object(c, 'SOM_CLIQUE', arquivo), patch.object(c, 'MUSICA_FUNDO', arquivo):
                    audio = ControladorAudio(EstadoJogo())
                    assert audio.som_clique is None and not audio.musica_carregada
                    for musica, efeitos in [(False, False), (True, False), (False, True), (True, True)]:
                        audio.estado.musica_ativada, audio.estado.efeitos_ativados = musica, efeitos
                        audio.atualizar_musica()
                        audio.atualizar_efeitos()
                        audio.tocar_clique()
            finally:
                pygame.mixer.quit()
    try:
        with patch('pygame.mixer.init', side_effect=pygame.error('Dispositivo indisponível')):
            aplicacao = ControladorAplicacao(caminho_banco)
            assert not pygame.mixer.get_init()
            clicar_botao(aplicacao, ('abrir_menu',))
            for acao in ('musica', 'efeitos', 'musica', 'efeitos'):
                clicar_botao(aplicacao, (acao,))
            assert aplicacao.estado.musica_ativada and aplicacao.estado.efeitos_ativados
            clicar_botao(aplicacao, ('fechar_menu',))
            clicar_botao(aplicacao, ('iniciar',))
            assert aplicacao.navegacao.ativa == 'missoes'
            aplicacao.tratar_evento(pygame.event.Event(pygame.QUIT))
            assert not aplicacao.em_execucao
    finally:
        pygame.quit()
    print('PASS: arquivos de áudio ausentes/inválidos e mixer indisponível')

def concluir_desafio(aplicacao, numero):
    aplicacao.navegacao.selecionar_missao(1)
    aplicacao.navegacao.selecionar_desafio(numero)
    for direcao in encontrar_rota(aplicacao.estado.desafio_selecionado):
        aplicacao.tratar_acao(('comando', direcao))
    aplicacao.tratar_acao(('executar',))
    aplicacao.atualizar(10)
    assert aplicacao.estado.tipo_resultado == 'sucesso'


def voltar_inicio_pelo_menu(aplicacao):
    clicar_botao(aplicacao, ('abrir_menu',))
    clicar_botao(aplicacao, ('voltar_inicio',))
    assert aplicacao.navegacao.ativa == 'inicio' and not aplicacao.menu_aberto


def verificar_banco(caminho):
    persistencia = PersistenciaJogo(caminho)
    assert not caminho.parent.exists()
    persistencia.preparar()
    assert caminho.is_file() and persistencia.carregar_preferencias() == (True, True)
    assert not persistencia.existe_salvamento() and persistencia.carregar_progresso() is None
    with closing(sqlite3.connect(caminho)) as conexao:
        tabelas = {linha[0] for linha in conexao.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
        assert tabelas == {'salvamento', 'desafios_concluidos', 'preferencias'}
    persistencia.salvar_preferencias(False, True)
    persistencia.preparar()
    assert persistencia.carregar_preferencias() == (False, True)
    assert not persistencia.existe_salvamento()
    persistencia.iniciar_partida()
    assert persistencia.existe_salvamento() and persistencia.carregar_progresso() == (0, 1, ())
    persistencia.salvar_progresso(50, 3, ((1, 1), (1, 2)))
    persistencia.preparar()
    assert persistencia.carregar_progresso() == (50, 3, ((1, 1), (1, 2)))
    try:
        persistencia.salvar_progresso(999, 4, ((1, 1), (0, 1)))
        raise AssertionError('A conclusão inválida deveria impedir a gravação.')
    except ErroPersistencia:
        pass
    assert persistencia.carregar_progresso() == (50, 3, ((1, 1), (1, 2)))
    persistencia.iniciar_partida()
    assert persistencia.carregar_progresso() == (0, 1, ())
    assert persistencia.carregar_preferencias() == (False, True)
    caminho_padrao = PersistenciaJogo().caminho
    diretorio_anterior = Path.cwd()
    try:
        os.chdir(caminho.parent)
        assert PersistenciaJogo().caminho == caminho_padrao
    finally:
        os.chdir(diretorio_anterior)
    print('PASS: criação idempotente, preferências separadas, caminho estável e transações do SQLite')


def verificar_restauracao():
    estado = EstadoJogo(musica_ativada=False, efeitos_ativados=False)
    missoes = criar_missoes()
    missoes[0].desafios[2].implementado = False
    missoes[1].desafios[0].implementado = True
    with patch('oceancode.models.game_state.criar_missoes', return_value=missoes):
        estado.aplicar_progresso(50, 3, ((1, 1), (1, 2), (1, 3), (2, 1), (99, 1), (1, 99)))
    assert (estado.xp, estado.nivel) == (50, 3)
    assert estado.desafios_concluidos == ((1, 1), (1, 2))
    assert all(not d.jogavel and d.status == StatusDesafio.BLOQUEADO for d in estado.missoes[0].desafios[2:])
    assert all(not m.disponivel and not any(d.jogavel for d in m.desafios) for m in estado.missoes[1:])
    assert not estado.musica_ativada and not estado.efeitos_ativados
    print('PASS: restauração ignora conteúdo desconhecido, desafios não implementados e missões indisponíveis')


def verificar_salvamento(caminho):
    aplicacao = ControladorAplicacao(caminho)
    try:
        assert aplicacao.navegacao.ativa == 'inicio' and not aplicacao.estado.partida_iniciada
        continuar = next(b for b in aplicacao.telas['inicio'].botoes if b.acao == ('continuar',))
        assert not continuar.habilitado
        clicar_botao(aplicacao, ('continuar',))
        assert aplicacao.navegacao.ativa == 'inicio'
        with patch.object(aplicacao.persistencia, '_conexao', side_effect=AssertionError('Banco acessado por frame.')):
            for _ in range(3):
                aplicacao.desenhar()
                aplicacao.atualizar(1)
        clicar_botao(aplicacao, ('abrir_menu',))
        for acao, preferencias in [('musica', (False, True)), ('efeitos', (False, False)),
                                   ('musica', (True, False)), ('efeitos', (True, True)),
                                   ('musica', (False, True))]:
            clicar_botao(aplicacao, (acao,))
            assert PersistenciaJogo(caminho).carregar_preferencias() == preferencias
        clicar_botao(aplicacao, ('fechar_menu',))
        assert not aplicacao.estado.partida_iniciada and not aplicacao.persistencia.existe_salvamento()
    finally:
        pygame.quit()
    with patch.object(pygame.mixer.music, 'play', wraps=pygame.mixer.music.play) as musica:
        aplicacao = ControladorAplicacao(caminho)
        musica.assert_not_called()
    try:
        assert not aplicacao.estado.musica_ativada and aplicacao.estado.efeitos_ativados
        assert not aplicacao.estado.partida_iniciada
        clicar_botao(aplicacao, ('iniciar',))
        assert aplicacao.navegacao.ativa == 'missoes' and not aplicacao.confirmacao_aberta
        assert aplicacao.persistencia.carregar_progresso() == (0, 1, ())
        voltar_inicio_pelo_menu(aplicacao)
        assert next(b for b in aplicacao.telas['inicio'].botoes if b.acao == ('continuar',)).habilitado
        clicar_botao(aplicacao, ('continuar',))
        concluir_desafio(aplicacao, 1)
        assert PersistenciaJogo(caminho).carregar_progresso() == (20, 1, ((1, 1),))
        aplicacao.persistencia.salvar_progresso(20, 3, ((1, 1),))
    finally:
        pygame.quit()
    aplicacao = ControladorAplicacao(caminho)
    try:
        assert aplicacao.navegacao.ativa == 'inicio' and aplicacao.estado.partida_iniciada
        compartilhado = aplicacao.estado
        clicar_botao(aplicacao, ('continuar',))
        assert aplicacao.estado is compartilhado
        assert (compartilhado.xp, compartilhado.nivel, compartilhado.desafios_concluidos) == (20, 3, ((1, 1),))
        assert compartilhado.missoes[0].desafios[1].jogavel
        assert not compartilhado.executando and not compartilhado.comandos
        assert compartilhado.desafio_selecionado is None and compartilhado.tempo_acumulado == 0
        concluir_desafio(aplicacao, 1)
        assert compartilhado.xp == 20 and compartilhado.xp_recebido == 0
        concluir_desafio(aplicacao, 2)
        salvo = (50, 3, ((1, 1), (1, 2)))
        assert aplicacao.persistencia.carregar_progresso() == salvo
        aplicacao.navegacao.selecionar_desafio(3)
        aplicacao.tratar_acao(('comando', 'direita'))
        aplicacao.tratar_acao(('executar',))
        aplicacao.atualizar(c.INTERVALO_COMANDOS / 2)
        voltar_inicio_pelo_menu(aplicacao)
        assert not compartilhado.executando and compartilhado.tempo_acumulado == 0
        assert compartilhado.partida_iniciada and aplicacao.persistencia.carregar_progresso() == salvo
        clicar_botao(aplicacao, ('continuar',))
        assert compartilhado.xp == 50 and not compartilhado.comandos
        assert compartilhado.missoes[0].desafios[2].jogavel
        assert all(controlador.estado is compartilhado for controlador in
                   (aplicacao.jogo, aplicacao.navegacao, aplicacao.audio))
    finally:
        pygame.quit()
    print('PASS: Iniciar/Continuar, salvamento automático, reabertura, nível, XP único e preferências antes do áudio')


def verificar_confirmacao(caminho):
    persistencia = PersistenciaJogo(caminho)
    persistencia.preparar()
    persistencia.salvar_progresso(50, 3, ((1, 1), (1, 2)))
    persistencia.salvar_preferencias(False, False)
    aplicacao = ControladorAplicacao(caminho)
    try:
        clicar_botao(aplicacao, ('continuar',))
        concluir_desafio(aplicacao, 2)
        voltar_inicio_pelo_menu(aplicacao)
        compartilhado = aplicacao.estado
        anterior = deepcopy(compartilhado)
        salvo = persistencia.carregar_progresso()
        clicar_botao(aplicacao, ('iniciar',))
        assert aplicacao.confirmacao_aberta
        with patch.object(aplicacao.audio, 'tocar_clique') as som:
            for acao in ('continuar', 'iniciar', 'sair', 'abrir_menu'):
                clicar_botao(aplicacao, (acao,), ao_fundo=True)
            aplicacao.tratar_evento(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(10, 700)))
            som.assert_not_called()
        assert aplicacao.confirmacao_aberta and not aplicacao.menu_aberto and aplicacao.em_execucao
        pressionar_escape(aplicacao)
        assert not aplicacao.confirmacao_aberta and aplicacao.navegacao.ativa == 'inicio'
        assert compartilhado == anterior and persistencia.carregar_progresso() == salvo
        clicar_botao(aplicacao, ('iniciar',))
        clicar_botao(aplicacao, ('cancelar_nova_partida',))
        assert compartilhado == anterior and persistencia.carregar_progresso() == salvo
        clicar_botao(aplicacao, ('iniciar',))
        clicar_botao(aplicacao, ('confirmar_nova_partida',))
        assert not aplicacao.confirmacao_aberta and aplicacao.navegacao.ativa == 'missoes'
        assert aplicacao.estado is compartilhado
        assert all(controlador.estado is compartilhado for controlador in
                   (aplicacao.jogo, aplicacao.navegacao, aplicacao.audio))
        assert persistencia.carregar_progresso() == (0, 1, ())
        assert persistencia.carregar_preferencias() == (False, False)
        assert compartilhado.xp == 0 and compartilhado.nivel == 1 and compartilhado.partida_iniciada
        assert compartilhado.missao_selecionada is None and compartilhado.desafio_selecionado is None
        assert not compartilhado.comandos and not compartilhado.executando
        assert compartilhado.indice_comando == 0 and compartilhado.tempo_acumulado == 0
        assert compartilhado.posicao_submarino == (0, 2) and compartilhado.tipo_resultado is None
        assert compartilhado.mensagem_resultado == '' and compartilhado.xp_recebido == 0
        assert not compartilhado.proximo_disponivel
        assert not compartilhado.musica_ativada and not compartilhado.efeitos_ativados
        assert compartilhado.missoes == criar_missoes()
        voltar_inicio_pelo_menu(aplicacao)
        clicar_botao(aplicacao, ('iniciar',))
        assert aplicacao.confirmacao_aberta
        aplicacao.tratar_evento(pygame.event.Event(pygame.QUIT))
        assert not aplicacao.em_execucao
    finally:
        pygame.quit()
    print('PASS: confirmação exclusiva, cancelamento, Escape e nova partida sem trocar o estado compartilhado')


def verificar_falhas_de_gravacao(caminho):
    persistencia = PersistenciaJogo(caminho)
    persistencia.preparar()
    persistencia.salvar_progresso(20, 2, ((1, 1),))
    def executar_sql(instrucao):
        with closing(sqlite3.connect(caminho)) as conexao:
            with conexao:
                conexao.execute(instrucao)
    aplicacao = ControladorAplicacao(caminho)
    try:
        clicar_botao(aplicacao, ('continuar',))
        voltar_inicio_pelo_menu(aplicacao)
        anterior = deepcopy(aplicacao.estado)
        salvo = persistencia.carregar_progresso()
        executar_sql('''CREATE TRIGGER falha_nova_partida BEFORE DELETE ON desafios_concluidos
                        BEGIN SELECT RAISE(ABORT, 'falha de teste'); END''')
        clicar_botao(aplicacao, ('iniciar',))
        clicar_botao(aplicacao, ('confirmar_nova_partida',))
        assert aplicacao.confirmacao_aberta and aplicacao.navegacao.ativa == 'inicio'
        assert aplicacao.estado == anterior and persistencia.carregar_progresso() == salvo
        assert 'Nenhum progresso foi alterado' in aplicacao.mensagem_persistencia
        clicar_botao(aplicacao, ('cancelar_nova_partida',))
        executar_sql('DROP TRIGGER falha_nova_partida')
        executar_sql('''CREATE TRIGGER falha_audio BEFORE UPDATE ON preferencias
                        BEGIN SELECT RAISE(ABORT, 'falha de teste'); END''')
        clicar_botao(aplicacao, ('abrir_menu',))
        with patch.object(aplicacao.audio, 'atualizar_musica') as atualizar:
            clicar_botao(aplicacao, ('musica',))
            atualizar.assert_not_called()
        assert aplicacao.estado.musica_ativada and persistencia.carregar_preferencias() == (True, True)
        assert 'opção anterior' in aplicacao.mensagem_audio
        executar_sql('DROP TRIGGER falha_audio')
        clicar_botao(aplicacao, ('musica',))
        assert not aplicacao.estado.musica_ativada and aplicacao.mensagem_audio == ''
        clicar_botao(aplicacao, ('fechar_menu',))
        clicar_botao(aplicacao, ('continuar',))
        executar_sql('''CREATE TRIGGER falha_conclusao BEFORE INSERT ON desafios_concluidos
                        WHEN NEW.desafio = 2 BEGIN SELECT RAISE(ABORT, 'falha de teste'); END''')
        with patch.object(aplicacao.persistencia, 'salvar_progresso', wraps=aplicacao.persistencia.salvar_progresso) as salvar:
            concluir_desafio(aplicacao, 2)
            for _ in range(3):
                aplicacao.atualizar(1)
                aplicacao.desenhar()
            assert salvar.call_count == 1
        assert aplicacao.estado.xp == 50 and persistencia.carregar_progresso() == salvo
        assert 'apenas nesta sessão' in aplicacao.mensagem_persistencia
        clicar_botao(aplicacao, ('abrir_menu',))
        clicar_botao(aplicacao, ('efeitos',))
        assert 'apenas nesta sessão' in aplicacao.mensagem_persistencia
        clicar_botao(aplicacao, ('fechar_menu',))
        executar_sql('DROP TRIGGER falha_conclusao')
        concluir_desafio(aplicacao, 2)
        assert aplicacao.estado.xp_recebido == 0 and aplicacao.mensagem_persistencia == ''
        assert persistencia.carregar_progresso() == (50, 2, ((1, 1), (1, 2)))
        voltar_inicio_pelo_menu(aplicacao)
        anterior = deepcopy(aplicacao.estado)
        with patch.object(aplicacao.persistencia, 'carregar_progresso', side_effect=ErroPersistencia('falha de leitura')):
            clicar_botao(aplicacao, ('continuar',))
        assert aplicacao.navegacao.ativa == 'inicio' and aplicacao.estado == anterior
        assert 'Seu salvamento foi mantido' in aplicacao.mensagem_persistencia
        assert persistencia.carregar_progresso() == (50, 2, ((1, 1), (1, 2)))
    finally:
        pygame.quit()
    print('PASS: falhas de substituição, conclusão, áudio e leitura preservam os dados e exibem avisos')


def verificar_arquivos_invalidos(pasta):
    corrompido = pasta / 'corrompido.sqlite3'
    corrompido.write_bytes(b'arquivo que nao e um banco SQLite')
    conteudo = corrompido.read_bytes()
    obstaculo = pasta / 'arquivo_no_lugar_da_pasta'
    obstaculo.write_text('preservar', encoding='utf-8')
    for caminho in (corrompido, obstaculo / 'progresso.sqlite3'):
        aplicacao = ControladorAplicacao(caminho)
        try:
            assert aplicacao.mensagem_persistencia and not aplicacao.estado.partida_iniciada
            clicar_botao(aplicacao, ('iniciar',))
            assert aplicacao.navegacao.ativa == 'inicio' and not aplicacao.confirmacao_aberta
            assert aplicacao.mensagem_persistencia
        finally:
            pygame.quit()
    assert corrompido.read_bytes() == conteudo and obstaculo.read_text(encoding='utf-8') == 'preservar'
    print('PASS: banco corrompido e pasta inacessível não são apagados ou recriados')


if __name__ == '__main__':
    verificar_catalogo()
    verificar_logica()
    assert c.CAMINHO_BANCO.is_absolute()
    with TemporaryDirectory(prefix='oceancode-smoke-') as diretorio:
        pasta = Path(diretorio)
        caminho_padrao = pasta / 'padrao_nao_utilizado.sqlite3'
        with patch.object(c, 'CAMINHO_BANCO', caminho_padrao):
            verificar_interface(pasta / 'interface.sqlite3')
            verificar_pausa_no_loop(pasta / 'pausa.sqlite3')
            verificar_audio()
            verificar_sem_audio(pasta / 'sem_audio.sqlite3')
            verificar_banco(pasta / 'banco' / 'progresso.sqlite3')
            verificar_restauracao()
            verificar_salvamento(pasta / 'salvamento.sqlite3')
            verificar_confirmacao(pasta / 'confirmacao.sqlite3')
            verificar_falhas_de_gravacao(pasta / 'falhas.sqlite3')
            verificar_arquivos_invalidos(pasta)
            assert not caminho_padrao.exists(), 'Toda aplicação de teste deve receber um banco temporário explícito.'
