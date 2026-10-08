# OceanCode — Expedição Oceânica

Projeto da disciplina de IHM focado no ensino de lógica de programação.
Protótipo desktop navegável em Python e Pygame, com janela de 1280 × 720.

## Executar

Requer Python 3.13 e Pygame 2.6.1. Na raiz do repositório:

```powershell
py -3.13 -m venv .venv313
.\.venv313\Scripts\python -m pip install -r requirements.txt
.\.venv313\Scripts\python main.py
```

Se o ambiente já estiver instalado, execute somente o último comando.
Também é possível usar `.\.venv313\Scripts\python -m oceancode.main`.
No editor, selecione `.venv313\Scripts\python.exe` como interpretador.
O ambiente virtual guarda o Python e as dependências locais; ele não contém
o código da aplicação e não deve ser incluído no Git. Basta um ambiente.
O Python 3.14 apresentou falha de instalação do Pygame nesta máquina.

## Organização

```text
OceanCode/                 # raiz do repositório e do workspace
├── .git/                  # histórico Git preservado
├── .venv313/              # único ambiente virtual, ignorado pelo Git
├── main.py                # entrada simples para executar a aplicação
├── requirements.txt
├── smoke_check.py         # verificação automática sem janela
├── README.md
└── oceancode/             # pacote da aplicação
    ├── main.py            # inicialização; também executável como módulo
    ├── config.py          # configurações visuais e caminho do cenário
    ├── models/            # missões, fases e estado em memória
    ├── views/             # telas e componentes de desenho
    ├── controllers/       # eventos, navegação e comandos
    └── assets/            # imagens, áudio e fontes
```

O `main.py` da raiz chama a inicialização do pacote: os dois arquivos têm
responsabilidades pequenas e distintas, sem duplicar a lógica da aplicação.
O loop principal fica no `AppController`. A separação segue MVC adaptado ao
Pygame: Model guarda dados, View desenha e Controller trata eventos.

## Demonstração

Jogar → Missões → Fases → Jogo. Voltar ou Esc retorna à tela anterior.
Sair ou fechar a janela encerra a aplicação. Música alterna o estado visual.
Missões 1 e 2 estão disponíveis; 3 e 4 estão bloqueadas. Fases 1 e 2 estão
concluídas e podem ser revisitadas; fase 3 está disponível e 4–10 bloqueadas.

As quatro setas à direita adicionam comandos à sequência inferior, até 12
comandos. Clique em um comando da sequência para removê-lo. Limpar apaga
a sequência; Executar mostra uma mensagem de prévia, sem movimentação.
Abrir uma fase reinicia a sequência. XP 120 e nível 3 são fictícios.

O tabuleiro 8 × 6 usa formas do Pygame para desenhar submarino, pedras e
objetivo. Um cenário opcional pode ser adicionado em
`oceancode/assets/images/tabuleiro_oceano.png`; sem ele, o fundo é desenhado
pelo Pygame. Não há áudio real, movimento, colisões, vitória, desbloqueio,
persistência, banco de dados ou cálculo real de XP nesta etapa.

## Verificar

```powershell
.\.venv313\Scripts\python smoke_check.py
```

A verificação renderiza as quatro telas sem abrir janela e testa os cliques,
bloqueios, música, edição de comandos e encerramento.
