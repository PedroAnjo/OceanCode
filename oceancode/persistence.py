from contextlib import closing, contextmanager
from pathlib import Path
import sqlite3
from . import config as c


class ErroPersistencia(Exception):
    pass


class PersistenciaJogo:
    def __init__(self, caminho=None):
        self.caminho = Path(caminho) if caminho is not None else c.CAMINHO_BANCO

    @contextmanager
    def _conexao(self):
        try:
            with closing(sqlite3.connect(self.caminho, timeout=1)) as conexao:
                with conexao:
                    conexao.execute('BEGIN')
                    yield conexao
        except (sqlite3.Error, OSError) as erro:
            raise ErroPersistencia('Não foi possível acessar os dados locais.') from erro

    def preparar(self):
        try:
            self.caminho.parent.mkdir(parents=True, exist_ok=True)
        except OSError as erro:
            raise ErroPersistencia('Não foi possível criar a pasta de dados.') from erro
        with self._conexao() as conexao:
            conexao.execute('''CREATE TABLE IF NOT EXISTS salvamento (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                xp INTEGER NOT NULL CHECK (xp >= 0),
                nivel INTEGER NOT NULL CHECK (nivel >= 1))''')
            conexao.execute('''CREATE TABLE IF NOT EXISTS desafios_concluidos (
                missao INTEGER NOT NULL CHECK (missao > 0),
                desafio INTEGER NOT NULL CHECK (desafio > 0),
                PRIMARY KEY (missao, desafio))''')
            conexao.execute('''CREATE TABLE IF NOT EXISTS preferencias (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                musica_ativada INTEGER NOT NULL CHECK (musica_ativada IN (0, 1)),
                efeitos_ativados INTEGER NOT NULL CHECK (efeitos_ativados IN (0, 1)))''')
            conexao.execute('INSERT OR IGNORE INTO preferencias VALUES (1, ?, ?)', (1, 1))

    def existe_salvamento(self):
        with self._conexao() as conexao:
            return conexao.execute('SELECT 1 FROM salvamento WHERE id = 1').fetchone() is not None

    def carregar_preferencias(self):
        with self._conexao() as conexao:
            preferencias = conexao.execute(
                'SELECT musica_ativada, efeitos_ativados FROM preferencias WHERE id = 1').fetchone()
            if preferencias is None or any(valor not in (0, 1) for valor in preferencias):
                raise ErroPersistencia('Preferências inválidas.')
            return tuple(bool(valor) for valor in preferencias)

    def salvar_preferencias(self, musica_ativada, efeitos_ativados):
        with self._conexao() as conexao:
            conexao.execute('''INSERT INTO preferencias VALUES (1, ?, ?)
                ON CONFLICT(id) DO UPDATE SET musica_ativada = excluded.musica_ativada,
                efeitos_ativados = excluded.efeitos_ativados''',
                (int(musica_ativada), int(efeitos_ativados)))

    def carregar_progresso(self):
        with self._conexao() as conexao:
            progresso = conexao.execute('SELECT xp, nivel FROM salvamento WHERE id = 1').fetchone()
            if progresso is None:
                return None
            xp, nivel = progresso
            if type(xp) is not int or xp < 0 or type(nivel) is not int or nivel < 1:
                raise ErroPersistencia('Progresso inválido.')
            concluidos = tuple(conexao.execute(
                'SELECT missao, desafio FROM desafios_concluidos ORDER BY missao, desafio'))
            return xp, nivel, concluidos

    def salvar_progresso(self, xp, nivel, concluidos):
        with self._conexao() as conexao:
            conexao.execute('''INSERT INTO salvamento VALUES (1, ?, ?)
                ON CONFLICT(id) DO UPDATE SET xp = excluded.xp, nivel = excluded.nivel''', (xp, nivel))
            conexao.execute('DELETE FROM desafios_concluidos')
            conexao.executemany('INSERT INTO desafios_concluidos VALUES (?, ?)', sorted(set(concluidos)))

    def iniciar_partida(self):
        self.salvar_progresso(0, 1, ())
