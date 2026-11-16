# OceanCode — Expedição Oceânica

Jogo educacional desktop de sequências e lógica de programação, desenvolvido
com Python e Pygame. Interface em azul e amarelo pastel, com janela fixa de
1280 × 720. O progresso e as preferências de áudio são salvos localmente em SQLite.

## Executar

O ambiente existente utiliza Python 3.13 e Pygame 2.6.1. Na raiz:

```powershell
.\.venv313\Scripts\python.exe main.py
```

Com o ambiente virtual ativado, também é possível executar `python main.py`
ou `python -m oceancode.main`. No editor, selecione
`.venv313\Scripts\python.exe` como interpretador.

Para preparar outro ambiente:

```powershell
py -3.13 -m venv .venv313
.\.venv313\Scripts\python.exe -m pip install -r requirements.txt
```

## Arquitetura MVC

Os arquivos e diretórios originais foram preservados; os identificadores da
aplicação estão em português brasileiro.

- **Model:** `EstadoJogo`, `Missao`, `Desafio`, `StatusDesafio` e `TipoDesafio` guardam mapas,
  sequência, posição lógica, progresso, XP e preferências de música e efeitos. Não desenham
  nem dependem do Pygame ou SQLite.
- **Conteúdo:** `content/catalog.py` cria o catálogo da sessão;
  `content/sequence.py`, `content/debugging.py`, `content/conditionals.py` e
  `content/repetition.py` definem as missões e seus desafios.
- **Controller:** `ControladorAplicacao` mantém o loop, os painéis sobrepostos,
  encaminha eventos e coordena o carregamento e salvamento;
  `ControladorNavegacao` seleciona telas e valida o acesso aos conteúdos;
  `ControladorJogo` edita a sequência, executa movimentos, valida colisões,
  define o retorno e atualiza progresso e XP; `ControladorAudio` controla a
  trilha e os efeitos separadamente.
- **View:** `ViewInicio`, `ViewMissoes`, `ViewDesafios`, `ViewJogo` e
  `ViewRetorno` apresentam o estado. `ViewBase` centraliza fundo, cabeçalho,
  HUD, voltar e botão Menu. `MenuOpcoes`, `Botao`, `PastaMissao`, `BotaoDesafio` e `FundoOceanico`
  são componentes reutilizáveis.
- **Persistência:** `persistence.py` concentra o SQL e as transações de um único
  salvamento, mantendo as preferências separadas do progresso.

`config.py` reúne resolução, FPS, paleta, fontes, dimensões principais,
intervalo de comandos e caminhos dos assets. O ponto de entrada da raiz
chama `principal` no pacote, sem duplicar o loop.

### Organização do conteúdo

`models/mission.py` representa a missão e calcula a quantidade de desafios
concluídos. `models/level.py` representa os dados do desafio, seu status e a
regra de acesso `jogavel`. `EstadoJogo` obtém suas missões pela fábrica
`criar_missoes()` de `content/catalog.py`. Cada chamada cria objetos novos,
evitando compartilhar progresso entre sessões.

Para desenvolver desafios da missão de sequência, edite
`criar_desafios_sequencia()` em `content/sequence.py`. Nesta versão, mantenha
os dez espaços e apenas os desafios 1–3 implementados; os espaços 4–10 são
reservados. O rascunho local do desafio 4 foi preservado, mas está explicitamente
marcado como não implementado. `criar_missao_sequencia()` reúne os metadados
da missão e obtém essa lista de desafios.

As missões 2–4 já possuem módulos próprios: `content/debugging.py`
(depuração), `content/conditionals.py` (condicionais) e `content/repetition.py`
(repetição). Cada módulo contém uma fábrica de desafios e uma fábrica de missão,
seguindo o padrão de sequência. As três missões mantêm `disponivel=False`,
com dez desafios reservados, bloqueados e não implementados. Para desenvolvê-las
futuramente, edite as respectivas fábricas de desafios nesses módulos.

`content/catalog.py` apenas importa e chama as quatro fábricas na ordem das
missões. Para registrar uma missão adicional, crie seu módulo de conteúdo,
importe sua fábrica no catálogo e inclua a chamada no retorno de
`criar_missoes()`, mantendo cada definição em um único módulo.

`TipoDesafio` identifica sequência, condicionais, repetição e depuração.
O campo `Desafio.tipo` foi acrescentado ao final dos argumentos, com sequência
como padrão, preservando a construção dos desafios existentes. Esse campo é
somente metadado; as mecânicas futuras ainda não foram implementadas.
`implementado` é uma propriedade do conteúdo e tem padrão `False`; `status`
representa o progresso e começa bloqueado, exceto no primeiro desafio.

A separação entre arquivos de conteúdo e modelos está feita. A separação
completa entre definição e progresso fica para outra etapa: `Desafio.status`
e `Missao.disponivel` continuam nos objetos da sessão, usados diretamente por
controladores e telas. Extrair esses campos agora exigiria alterar navegação,
progressão e apresentação. XP, comandos e posição continuam em `EstadoJogo`;
somente XP, nível e conclusões são persistidos. Os desbloqueios são reconstruídos
pelo Model com a mesma regra usada ao concluir um desafio.

## Telas e controles

Iniciar ou Continuar → Missões → Missão 1 → Desafios → Jogo → Retorno de sucesso ou erro.
Voltar ou Esc retorna à tela anterior; sair ou fechar a janela encerra.
Voltar durante a execução cancela os movimentos restantes.

**Iniciar** cria uma partida com XP zero, nível 1 e os bloqueios originais,
limpando comandos, seleção e execução, sem redefinir o áudio. Se já houver
salvamento, uma confirmação oferece **Cancelar** e **Iniciar nova partida**;
Esc cancela e os cliques ao fundo são ignorados. **Continuar** permanece
visível e desabilitado até existir uma partida, mesmo que seu XP seja zero.
Ele recupera o progresso e abre o painel de missões, sem retomar uma execução.

O botão **Menu**, no canto superior direito das cinco telas, abre as opções
**Voltar ao início**, **Música**, **Efeitos sonoros** e **Fechar**. Enquanto o
menu estiver aberto, cliques na tela ao fundo são ignorados e Esc apenas fecha
o painel. A sequência fica pausada, preservando posição, comandos, índice e
tempo já acumulado; o tempo passado no menu não entra na execução ao retomar.
Voltar ao início cancela a execução e descarta seu tempo pendente, preservando
XP, desafios concluídos, desbloqueios e preferências de áudio. Essa opção fica
desabilitada na tela inicial.

No jogo, o tabuleiro permanece à esquerda, os comandos à direita e a área
de programação embaixo. Clique nas setas para adicionar comandos e nos
comandos da sequência para removê-los. Limpar apaga a sequência.

Executar reinicia o submarino na posição inicial e move uma célula a cada
380 ms pelo loop normal, sem espera bloqueante. Durante a execução, a edição
fica desabilitada e o comando atual recebe destaque. Colisão e saída do mapa
interrompem a execução com erro. Alcançar a amostra encerra com sucesso,
mesmo se existirem comandos restantes. Terminar sem alcançá-la gera erro.
Tentar novamente mantém a sequência para permitir corrigi-la.

Os controles de áudio do menu são independentes e começam ligados na primeira abertura.
**Música** alterna `musica_ativada`, pausando ou retomando apenas a trilha.
**Efeitos sonoros** alterna `efeitos_ativados`, interrompendo os efeitos em
andamento quando desligado e impedindo novos cliques sonoros, sem alterar a
música. Os rótulos refletem a preferência atual. `ControladorAudio` carrega os arquivos de
`oceancode/assets/audio`: `hard pop.wav` para cliques em botões habilitados
e `turning_pages-bio-luminescence-601591.mp3` para música em loop desde o
início. Os volumes ficam em `config.py`. Arquivos ausentes ou inválidos e
indisponibilidade do dispositivo de áudio não impedem a abertura do jogo.

## Salvamento local

O banco fica em `%LOCALAPPDATA%\OceanCode\progresso.sqlite3` no Windows
(normalmente `C:\Users\<usuário>\AppData\Local\OceanCode\progresso.sqlite3`).
Em outros sistemas, usa `$XDG_DATA_HOME/OceanCode` ou `~/.local/share/OceanCode`.
O caminho está em `config.CAMINHO_BANCO` e independe da pasta de execução;
`PersistenciaJogo(caminho)` e `ControladorAplicacao(caminho_banco=...)` permitem
usar outro arquivo. Pasta e tabelas são criadas automaticamente.

As tabelas são `salvamento` (um registro com XP e nível), `desafios_concluidos`
(chave missão/desafio) e `preferencias` (música e efeitos). Somente a presença
do registro em `salvamento` habilita Continuar; um banco com apenas preferências
não representa uma partida. Os mapas continuam no código e conteúdo não
implementado ou missões indisponíveis não são liberados pelo carregamento.

O jogo salva ao iniciar uma partida, concluir um desafio com sucesso ou alterar
o áudio. XP, nível e conclusões são gravados juntos em uma transação. As
preferências são carregadas antes de inicializar o áudio. Voltar ao início
preserva o salvamento; repetir desafios concluídos não concede XP novamente,
inclusive após reabrir o aplicativo. Comandos, posição, temporizadores,
mensagens de resultado e painéis abertos não são salvos.

Falhas de acesso ou gravação aparecem em um aviso na interface. Uma nova
partida só substitui o progresso em memória após a gravação bem-sucedida;
bancos com erro de leitura não são apagados nem recriados automaticamente.

## Missão 1 — Primeiras Expediçôes

Conteúdo: Sequências. Os mapas ficam em `content/sequence.py`; posições são
pares `(coluna, linha)`, independentes de pixels, no tabuleiro 8 × 6.

| Desafio | Início | Amostra | Rochas | Limite | XP |
| --- | --- | --- | --- | --- | --- |
| 1 — Primeiros Movimentos | (0, 2) | (3, 2) | Nenhuma | 5 | 20 |
| 2 — Contornando Obstáculos | (0, 4) | (3, 2) | (1, 4) | 7 | 30 |
| 3 — Rota de Exploração | (0, 5) | (4, 1) | (0, 4), (2, 4), (2, 2), (4, 3) | 10 | 50 |

Uma solução do terceiro desafio é: direita, cima, cima, cima, cima, direita,
direita, direita. Os testes buscam rotas nos três mapas e validam seus limites.

Uma nova partida começa com XP 0, nível 1 e apenas o Desafio 1 disponível. Sua
conclusão libera o 2; concluir o 2 libera o 3. O 3 não libera o 4. Desafios
concluídos podem ser repetidos sem conceder XP novamente. O total desta
versão é 100 XP; o nível permanece 1. O cartão acompanha o progresso até
3/10. A recompensa futura da missão (+100 XP) não é concedida nesta etapa.

Missões 2–4 e desafios 4–10 permanecem visíveis e bloqueados, inclusive na
validação do Controller.

## Assets opcionais

A tipografia está preparada para Fredoka, com pesos Medium, SemiBold e Bold.
Adicione manualmente os arquivos em `oceancode/assets/fonts`:
`Fredoka-Medium.ttf`, `Fredoka-SemiBold.ttf` e `Fredoka-Bold.ttf`.
Reinicie o jogo após adicioná-los. Fontes ausentes ou inválidas utilizam a
fonte de sistema; os objetos de fonte são mantidos em cache por tamanho e peso.

As pastas de missão apresentam barras proporcionais aos desafios concluídos,
contador e recompensa futura. As três estrelas são indicadores visuais:
primeiro desafio concluído, metade da missão e missão completa. Não concedem
XP adicional. Nesta versão, 3/10 preenche 30% da barra e mostra uma estrela.
O HUD apresenta o XP da partida em relação à meta de 100 XP, mantendo o nível
atual do Model. A logo da tela inicial mantém sua imagem, escala e posição.

A aplicação funciona sem imagens externas. O fundo oceânico é desenhado
pelo Pygame, com gradiente, bolhas, silhuetas e sombras discretas.

Imagens opcionais em `oceancode/assets/images`:

- `tabuleiro_oceano.png`: cenário utilizado pelas telas e pelo tabuleiro.
- `submarino.png`, `barreira.png`, `objetivo.png`: substituem as respectivas
  formas geométricas; preservam proporção e se ajustam às células.

Imagens ausentes ou inválidas mantêm o desenho geométrico. Essas substituições
são responsabilidade da View e não alteram as regras nem as posições lógicas.

## Verificar

```powershell
.\.venv313\Scripts\python.exe smoke_check.py
.\.venv313\Scripts\python.exe -m compileall -q oceancode main.py smoke_check.py
```

O smoke check valida as quatro missões, os dez desafios da primeira missão,
os dados e recompensas dos três implementados, os tipos, o tabuleiro 6 × 8
e o isolamento de progresso entre sessões. Testa regras sem renderização e renderiza as cinco telas com
SDL em modo sem janela. Verifica rotas, temporização, colisões, limites,
edição de comandos, progressão, XP único, bloqueios, retorno, repetição,
navegação, menu nas cinco telas, bloqueio de cliques ao fundo, pausa e retomada,
retorno ao início com progresso preservado, prioridade de Esc, quatro combinações
de música/efeitos, ausência de áudio e encerramento do loop. As verificações de
progressão respeitam os desafios marcados como implementados no catálogo local.
Todas as aplicações dos testes usam bancos temporários. Também são verificados
criação das tabelas, Iniciar/Continuar, confirmação, reabertura, persistência de
XP e áudio, transações e preservação dos dados diante de falhas.
A aparência e os estados
hover/pressionado devem também ser conferidos manualmente em uma janela real.

Validação da refatoração (20/10/2026): `python smoke_check.py` não conseguiu
iniciar o executável Python disponível no PATH. Usando o ambiente existente,
`.\.venv313\Scripts\python.exe smoke_check.py` passou nas verificações de
catálogo, lógica e interface. A compilação sintática com `py_compile` dos
sete arquivos Python criados ou alterados também passou. Não foi feita uma
inspeção visual em janela real.

Após separar também as missões 2–4 em módulos próprios, o smoke check foi
executado novamente com o mesmo ambiente virtual e passou nas três etapas
(catálogo, lógica e interface). A compilação com `py_compile` de `catalog.py`,
`debugging.py`, `conditionals.py` e `repetition.py` também passou, assim como
`git diff --check`. Nenhum erro decorrente dessa separação foi encontrado.

## Evoluções pendentes

Desafios 4–10, missões 2–4, condicionais, repetição, funções, efeitos de movimento e resultado,
sprites definitivos, perfis, conquistas, ranking e editor de
fases ainda não estão implementados. O SQLite usa a biblioteca padrão do Python;
não há login ou novas dependências além do Pygame.
