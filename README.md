# OceanCode

OceanCode é um jogo educacional desktop sobre sequências e lógica de programação. O jogador programa um submarino para coletar amostras, evitar rochas e lidar com monstros, usando Python e Pygame em uma janela fixa de 1280 × 720.

## Requisitos e execução

- Python 3.13 (o ambiente verificado é `.venv313`).
- Pygame 2.6.1 ou versão compatível com `requirements.txt`.

Na raiz do projeto:

```powershell
py -3.13 -m venv .venv313
.\.venv313\Scripts\python.exe -m pip install -r requirements.txt
.\.venv313\Scripts\python.exe main.py
```

Também é possível executar `python -m oceancode.main` com o ambiente virtual ativo.

## Conteúdo e controles

O catálogo contém quatro missões, nesta ordem: Sequência, Repetição, Depuração e Condicionais. Os dez desafios de Sequência, Repetição e Depuração estão definidos no código; Condicionais permanece reservada para desenvolvimento. A progressão libera desafios e missões conforme as conclusões, sem conceder XP novamente por um desafio já concluído.

No jogo, as setas, Míssil e Repetir adicionam blocos à área de programação. Clique em um bloco para selecioná-lo e use os controles de mover ou inserir; duplo clique remove o bloco. O laço permite de 1 a 6 repetições, não pode conter outro laço e conta junto com os comandos internos para o limite do desafio. Executar move o submarino no intervalo definido em `config.py`; rochas bloqueiam o caminho, monstros podem ser destruídos por disparos horizontais e todos os objetivos precisam ser coletados.

O tutorial explica a movimentação, edição, repetição, disparos, progressão e navegação. Esc retorna à tela anterior ou fecha um painel aberto. O menu permite pausar a execução e alternar música e efeitos sonoros separadamente.

## Salvamento

O progresso e as preferências de áudio são gravados em SQLite:

- Windows: `%LOCALAPPDATA%\OceanCode\progresso.sqlite3`;
- outros sistemas: `$XDG_DATA_HOME/OceanCode` ou `~/.local/share/OceanCode`.

O caminho pode ser substituído ao criar `PersistenciaJogo(caminho)` ou `ControladorAplicacao(caminho_banco=...)`. O banco guarda XP, nível, desafios concluídos e preferências de áudio; comandos, posição e estado de uma tentativa não são persistidos.

## Organização

- `oceancode/models`: estado da partida, missões, desafios, monstros e comandos.
- `oceancode/content`: catálogo e definições dos desafios.
- `oceancode/controllers`: loop da aplicação, navegação, regras do jogo, áudio e persistência.
- `oceancode/views`: telas e componentes Pygame.
- `oceancode/config.py`: dimensões, tempos, cores e caminhos dos recursos.
- `oceancode/assets`: fontes, imagens e áudio opcionais ou distribuídos com o jogo.

A aplicação segue MVC: Models não dependem de Pygame nem de SQLite; Controllers coordenam regras e fluxo; Views desenham e tratam áreas de interação.

## Recursos opcionais

Fontes Fredoka, imagens de fundo, submarino, obstáculos, objetivos, míssil, repetição e cadeado são carregadas pelos caminhos em `oceancode/assets` e `config.py`. Quando uma imagem ou fonte opcional está ausente ou inválida, a aplicação usa o desenho geométrico ou a fonte do sistema. Os arquivos de áudio distribuídos ficam em `oceancode/assets/audio`.

## Verificação

```powershell
.\.venv313\Scripts\python.exe -m unittest repetition_check.py debugging_check.py
.\.venv313\Scripts\python.exe smoke_check.py
.\.venv313\Scripts\python.exe -m compileall -q oceancode main.py smoke_check.py repetition_check.py debugging_check.py
```

Os scripts usam dados temporários quando exercitam persistência. `smoke_check.py` cobre catálogo, lógica, navegação, interface sem janela, áudio e SQLite; os demais verificam especificamente Repetição e Depuração.

## Executáveis

O workflow manual [`oceancode/.github/workflows/build.yml`](oceancode/.github/workflows/build.yml) instala PyInstaller e gera executáveis `OceanCode` para Windows e Linux, incluindo `oceancode/assets`.

## Licença e créditos

Não há um arquivo de licença ou declaração adicional no repositório. Os nomes e créditos dos arquivos de áudio distribuídos são preservados nos próprios nomes dos recursos.
