"""Valide os mapas de repetição: execute ``python repetition_check.py``.

As soluções usam a legenda de oceancode/content/repetition.py. Um par
(quantidade, corpo) representa um laço; strings representam ações isoladas.
A busca de menor programa sequencial usa movimento e disparo do próprio motor.
"""

from collections import deque
import unittest

from oceancode import config as c
from oceancode.content.repetition import criar_missao_repeticao
from oceancode.controllers.game_controller import ControladorJogo, DIRECOES
from oceancode.models.game_state import Comando, EstadoJogo
from oceancode.models.level import StatusDesafio, TipoDesafio
from oceancode.models.monster import Monstro


ACOES = {
    'D': 'direita', 'E': 'esquerda', 'C': 'cima',
    'B': 'baixo', 'M': 'missil',
}
SOLUCOES = {
    1: ((6, 'D'),),
    2: ((5, 'D'), 'C'),
    3: ((5, 'D'), (4, 'C')),
    4: ((4, 'CD'), (2, 'D')),
    5: ((3, 'DDC'), 'D', 'C'),
    6: ((3, 'MDDB'), 'D', 'B'),
    7: ((3, 'DC'), (2, 'D'), (2, 'CD')),
    8: ((2, 'C'), (3, 'MDD'), 'D', (2, 'B')),
    9: ((2, 'MDDCC'), (3, 'D'), (2, 'B')),
    10: ((3, 'MDD'), (2, 'C'), (3, 'EME'), (3, 'C')),
}
ALTERNATIVAS = {
    8: ((2, 'B'), (3, 'MDD'), 'D', (2, 'C')),
    9: ((2, 'CCMDD'), (3, 'D'), (2, 'B')),
    10: ((3, 'MDD'), 'D', (2, 'C'), (3, 'EME'), 'E', (3, 'C')),
}


def criar_estado(numero):
    missao = criar_missao_repeticao()
    desafio = missao.desafios[numero - 1]
    missao.disponivel = True
    desafio.status = StatusDesafio.DISPONIVEL
    estado = EstadoJogo(
        missoes=(missao,), missao_selecionada=missao,
        desafio_selecionado=desafio,
    )
    estado.reiniciar_desafio()
    return estado


def montar_programa(estado, plano):
    """Monte pelos mesmos eventos da interface, respeitando o limite."""
    jogo = ControladorJogo(estado)
    esperado = []
    for indice, bloco in enumerate(plano):
        if isinstance(bloco, str):
            jogo.tratar_acao(('comando', ACOES[bloco]))
            esperado.append(Comando(ACOES[bloco]))
            continue
        quantidade, corpo = bloco
        assert 1 <= quantidade <= 6
        jogo.tratar_acao(('comando', 'repetir'))
        assert len(estado.comandos) == indice + 1, estado.mensagem
        while estado.comandos[indice].quantidade != quantidade:
            jogo.tratar_acao(('quantidade', indice))
        jogo.tratar_acao(('destino', indice))
        for acao in corpo:
            jogo.tratar_acao(('comando', ACOES[acao]))
        jogo.tratar_acao(('destino', None))
        esperado.append(Comando(
            'repetir', quantidade, [Comando(ACOES[acao]) for acao in corpo],
        ))
    assert estado.comandos == esperado, estado.mensagem
    assert estado.total_blocos <= estado.desafio_selecionado.limite_comandos
    return jogo


def executar(numero, plano):
    estado = criar_estado(numero)
    jogo = montar_programa(estado, plano)
    jogo.tratar_acao(('executar',))
    assert estado.executando, estado.mensagem
    trajeto = [estado.posicao_submarino]
    for _ in range(200):
        jogo.atualizar(c.INTERVALO_COMANDOS)
        trajeto.append(estado.posicao_submarino)
        if not estado.executando:
            return estado, trajeto
    raise AssertionError('A execução não terminou em 200 ações.')


def menor_sequencia(numero):
    """Busque em largura incluindo orientação e monstros ainda vivos.

    Cada aresta custa uma ação simples: movimento ou míssil. Usar o motor
    também considera mudanças de orientação, rochas e alcance do disparo.
    """
    estado = criar_estado(numero)
    jogo = ControladorJogo(estado)
    desafio = estado.desafio_selecionado

    def fotografia():
        return (
            estado.posicao_submarino, estado.orientacao_submarino,
            tuple(monstro.posicao for monstro in estado.monstros_restantes),
        )

    inicial = fotografia()
    fila = deque([(inicial, 0)])
    visitados = {inicial}
    while fila:
        (posicao, orientacao, monstros), custo = fila.popleft()
        if posicao == desafio.posicao_objetivo:
            return custo
        for acao in (*DIRECOES, 'missil'):
            estado.posicao_submarino = posicao
            estado.orientacao_submarino = orientacao
            estado.monstros_restantes = [Monstro(p) for p in monstros]
            estado.tipo_resultado = None
            estado.executando = True
            if acao == 'missil':
                jogo.disparar()
            else:
                jogo.mover(acao)
            if estado.tipo_resultado == 'erro':
                continue
            seguinte = fotografia()
            if seguinte not in visitados:
                visitados.add(seguinte)
                fila.append((seguinte, custo + 1))
    raise AssertionError(f'Desafio {numero}: não existe rota navegável.')


class RepeticaoCheck(unittest.TestCase):
    def test_catalogo_e_coordenadas(self):
        missao = criar_missao_repeticao()
        self.assertEqual((c.COLUNAS, c.LINHAS), (8, 6))
        self.assertEqual(missao.numero, 2)
        self.assertTrue(missao.permite_repeticao)
        self.assertEqual([d.numero for d in missao.desafios], list(SOLUCOES))
        self.assertEqual(
            [d.recompensa_xp for d in missao.desafios],
            [20, 30, 50, 60, 70, 80, 90, 100, 110, 150],
        )
        for desafio in missao.desafios:
            with self.subTest(desafio=desafio.numero):
                self.assertTrue(desafio.implementado)
                self.assertEqual(desafio.tipo, TipoDesafio.REPETICAO)
                self.assertEqual(desafio.status, StatusDesafio.BLOQUEADO)
                self.assertIsInstance(desafio.obstaculos, tuple)
                self.assertIsInstance(desafio.monstros, tuple)
                posicoes = (
                    desafio.posicao_inicial, desafio.posicao_objetivo,
                    *desafio.obstaculos, *desafio.monstros,
                )
                self.assertEqual(len(posicoes), len(set(posicoes)))
                for posicao in posicoes:
                    self.assertIsInstance(posicao, tuple)
                    self.assertEqual(len(posicao), 2)
                    coluna, linha = posicao
                    self.assertIsInstance(coluna, int)
                    self.assertIsInstance(linha, int)
                    self.assertTrue(0 <= coluna < c.COLUNAS)
                    self.assertTrue(0 <= linha < c.LINHAS)

    def test_solucoes_no_motor_e_progressao(self):
        contagens = []
        for numero, plano in SOLUCOES.items():
            with self.subTest(desafio=numero):
                estado, _ = executar(numero, plano)
                self.assertEqual(
                    estado.tipo_resultado, 'sucesso',
                    estado.mensagem_resultado,
                )
                self.assertFalse(estado.objetivos_restantes)
                self.assertEqual(
                    estado.xp, estado.desafio_selecionado.recompensa_xp,
                )
                contagens.append(estado.total_blocos)
        self.assertEqual(contagens, [2, 3, 4, 5, 6, 7, 8, 9, 10, 12])

    def test_repeticao_obrigatoria_em_todas_as_rotas(self):
        for desafio in criar_missao_repeticao().desafios:
            with self.subTest(desafio=desafio.numero):
                minimo = menor_sequencia(desafio.numero)
                self.assertLess(desafio.limite_comandos, minimo)
                print(
                    f'Desafio {desafio.numero:2}: '
                    f'limite={desafio.limite_comandos:2}, '
                    f'mínimo sem laços={minimo:2}',
                )

    def test_rotas_alternativas_e_densidade_final(self):
        for numero, plano in ALTERNATIVAS.items():
            with self.subTest(desafio=numero):
                _, principal = executar(numero, SOLUCOES[numero])
                estado, alternativa = executar(numero, plano)
                self.assertEqual(
                    estado.tipo_resultado, 'sucesso',
                    estado.mensagem_resultado,
                )
                self.assertNotEqual(set(principal), set(alternativa))
                desafio = estado.desafio_selecionado
                ocupadas = len(desafio.obstaculos) + len(desafio.monstros)
                densidade = ocupadas / (c.COLUNAS * c.LINHAS)
                self.assertGreaterEqual(densidade, 0.25)
                self.assertLessEqual(densidade, 0.40)

    def test_monstros_punem_erros_de_uma_repeticao(self):
        for numero, diferenca in (
            (2, 1), (4, -1), (4, 1), (5, -1),
            (6, -1), (7, -1), (7, 1),
        ):
            with self.subTest(desafio=numero, diferenca=diferenca):
                plano = list(SOLUCOES[numero])
                quantidade, corpo = plano[0]
                plano[0] = (quantidade + diferenca, corpo)
                estado, _ = executar(numero, plano)
                self.assertEqual(estado.tipo_resultado, 'erro')
                self.assertIn('monstro', estado.mensagem_resultado)

    def test_disparos_sao_necessarios_nas_rotas_guardadas(self):
        for numero in (6, 8, 9, 10):
            with self.subTest(desafio=numero):
                plano = tuple(
                    (bloco[0], bloco[1].replace('M', ''))
                    if isinstance(bloco, tuple) else bloco
                    for bloco in SOLUCOES[numero]
                )
                estado, _ = executar(numero, plano)
                self.assertEqual(estado.tipo_resultado, 'erro')
                self.assertIn('monstro', estado.mensagem_resultado)


if __name__ == '__main__':
    unittest.main(verbosity=2)
