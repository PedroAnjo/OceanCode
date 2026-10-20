# OceanCode — Expedição Oceânica

Jogo educacional desktop de sequências e lógica de programação, desenvolvido
com Python e Pygame. Interface em azul e amarelo pastel, com janela fixa de
1280 × 720. O progresso existe somente durante a sessão.

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

- **Model:** `EstadoJogo`, `Missao`, `Desafio` e `StatusDesafio` guardam mapas,
  sequência, posição lógica, progresso, XP e configuração de som. Não desenham
  nem dependem do Pygame.
- **Controller:** `ControladorAplicacao` mantém o loop e encaminha eventos;
  `ControladorNavegacao` seleciona telas e valida o acesso aos conteúdos;
  `ControladorJogo` edita a sequência, executa movimentos, valida colisões,
  define o retorno e atualiza progresso e XP.
- **View:** `ViewInicio`, `ViewMissoes`, `ViewDesafios`, `ViewJogo` e
  `ViewRetorno` apresentam o estado. `ViewBase` centraliza fundo, cabeçalho,
  HUD, voltar e som. `Botao`, `PastaMissao`, `BotaoDesafio` e `FundoOceanico`
  são componentes reutilizáveis.

`config.py` reúne resolução, FPS, paleta, fontes, dimensões principais,
intervalo de comandos e caminhos dos assets. O ponto de entrada da raiz
chama `principal` no pacote, sem duplicar o loop.

## Telas e controles

Jogar → Missões → Missão 1 → Desafios → Jogo → Retorno de sucesso ou erro.
Voltar ou Esc retorna à tela anterior; sair ou fechar a janela encerra.
Voltar durante a execução cancela os movimentos restantes.

No jogo, o tabuleiro permanece à esquerda, os comandos à direita e a área
de programação embaixo. Clique nas setas para adicionar comandos e nos
comandos da sequência para removê-los. Limpar apaga a sequência.

Executar reinicia o submarino na posição inicial e move uma célula a cada
380 ms pelo loop normal, sem espera bloqueante. Durante a execução, a edição
fica desabilitada e o comando atual recebe destaque. Colisão e saída do mapa
interrompem a execução com erro. Alcançar a amostra encerra com sucesso,
mesmo se existirem comandos restantes. Terminar sem alcançá-la gera erro.
Tentar novamente mantém a sequência para permitir corrigi-la.

O botão circular de som alterna `musica_ativada`, pausa ou retoma a música
e silencia os efeitos. `ControladorAudio` carrega os arquivos de
`oceancode/assets/audio`: `hard pop.wav` para cliques em botões habilitados
e `turning_pages-bio-luminescence-601591.mp3` para música em loop desde o
início. Os volumes ficam em `config.py`. Arquivos ausentes ou inválidos e
indisponibilidade do dispositivo de áudio não impedem a abertura do jogo.

## Missão 1 — Primeira Expedição

Conteúdo: Sequências. Os mapas ficam em `models/mission.py`; posições são
pares `(coluna, linha)`, independentes de pixels, no tabuleiro 8 × 6.

| Desafio | Início | Amostra | Rochas | Limite | XP |
| --- | --- | --- | --- | --- | --- |
| 1 — Primeiros Movimentos | (0, 2) | (3, 2) | Nenhuma | 5 | 20 |
| 2 — Contornando Obstáculos | (0, 4) | (3, 2) | (1, 4) | 7 | 30 |
| 3 — Rota de Exploração | (0, 5) | (4, 1) | (0, 4), (2, 4), (2, 2), (4, 3) | 10 | 50 |

Uma solução do terceiro desafio é: direita, cima, cima, cima, cima, direita,
direita, direita. Os testes buscam rotas nos três mapas e validam seus limites.

A sessão começa com XP 0, nível 1 e apenas o Desafio 1 disponível. Sua
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
O HUD apresenta o XP da sessão em relação à meta de 100 XP, mantendo o nível
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

O smoke check testa regras sem renderização e renderiza as cinco telas com
SDL em modo sem janela. Verifica rotas, temporização, colisões, limites,
edição de comandos, progressão, XP único, bloqueios, retorno, repetição,
navegação, ícone de som e encerramento do loop. A aparência e os estados
hover/pressionado devem também ser conferidos manualmente em uma janela real.

## Evoluções pendentes

Desafios 4–10, missões 2–4, condicionais, repetição, funções, efeitos de movimento e resultado,
sprites definitivos, persistência, perfis, conquistas, ranking e editor de
fases ainda não estão implementados. Não há banco de dados, login ou novas
dependências além do Pygame.
