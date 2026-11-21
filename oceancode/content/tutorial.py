TOPICOS_TUTORIAL = (
    ('Objetivo',
     'Programe o submarino para coletar todas as amostras do desafio, evitando colisões e os limites '
     'do tabuleiro. Cada amostra é coletada quando o submarino chega à sua casa.'),
    ('Movimentação',
     'Clique nas setas do painel para adicionar movimentos à área de programação. Cada movimento '
     'leva o submarino uma casa na direção indicada. O submarino permanece na horizontal: subir e '
     'descer mantêm o lado para o qual ele aponta; apenas esquerda e direita mudam sua orientação. '
     'Os comandos são executados na ordem em que aparecem.'),
    ('Executar e corrigir',
     'Clique em Executar para iniciar o percurso. Respeite o limite de blocos indicado no desafio: '
     'o bloco Repetir e cada comando dentro dele também contam. A quantidade de repetições não '
     'multiplica essa contagem. A edição fica bloqueada durante a execução. Ao concluir ou falhar, '
     'o tabuleiro permanece visível por um segundo, com a última ação destacada, antes da tela de '
     'resultado. Durante essa pausa, não é possível editar nem executar novamente.\n\n'
     'Para remover um comando, dê dois cliques com o botão esquerdo no mesmo bloco, com intervalo '
     'de até 350 ms. Um clique simples não remove nada. Use Limpar para montar outra sequência. '
     'Se colidir com uma rocha ou monstro, '
     'sair do tabuleiro ou terminar sem coletar todas as amostras, clique em Tentar novamente para corrigir '
     'o programa. A sequência é mantida. Executar de novo, tentar novamente ou selecionar o desafio '
     'restaura o submarino, os monstros e as amostras às condições iniciais.'),
    ('Míssil',
     'Rochas e monstros bloqueiam o movimento. As rochas são indestrutíveis; somente os monstros podem '
     'ser destruídos. Adicione o comando Míssil para lançar um míssil na direção em que o submarino '
     'está apontando. O míssil para no primeiro bloqueio: destrói apenas o monstro atingido ou para '
     'na rocha, sem destruí-la nem atingir o que estiver atrás. Se chegar à borda, termina sem efeito.\n\n'
     'O disparo não movimenta nem gira o submarino. Inicialmente, ele aponta para a direita; '
     'apenas os movimentos para esquerda e direita mudam a direção do disparo, que é sempre horizontal.'),
    ('Repetição',
     'Na missão Sequência, Repetir aparece com um cadeado e fica desabilitado. O comando pode ser usado '
     'nos desafios implementados da missão Repetição e das seguintes.\n\n'
     'Use Repetir para executar um grupo de comandos várias vezes. Cada clique no número em '
     'Repetir X vezes avança a quantidade no ciclo 1 → 2 → 3 → 4 → 5 → 6 → 1. Dois cliques '
     'rápidos no número avançam duas vezes, sem selecionar ou remover o laço. '
     'Um clique simples no cabeçalho, lateral, base ou espaço interno vazio do laço seleciona seu corpo. '
     'O laço selecionado fica mais escuro, e os novos comandos são adicionados ao final dele. '
     'O laço precisa conter ao menos um comando para executar.\n\n'
     'Os blocos dentro do contorno pertencem à repetição; os blocos fora dele são executados normalmente '
     'na sequência. Clique em um espaço vazio fora dos laços, inclusive na margem da área de programação, '
     'para voltar a adicionar ao final da sequência principal. Um clique simples em um comando comum '
     'não muda o destino. É possível usar vários laços na sequência principal, mas não adicionar '
     'um laço dentro de outro.\n\n'
     'Dê um duplo clique no cabeçalho, na lateral ou na base para remover o laço e seus comandos. '
     'Um duplo clique em um comando interno remove somente esse comando. O número de repetições '
     'e os espaços vazios não são alvos de exclusão. Remover o laço selecionado '
     'volta o destino para a sequência principal.'),
    ('Desafios e missões',
     'A ordem das missões é: 1. Sequência; 2. Repetição (Loop); 3. Depuração (Debug); 4. Condicionais. '
     'Conclua um desafio para liberar o próximo da mesma missão. Concluir todos os desafios de uma '
     'missão libera a próxima. Desafios marcados como Em breve ainda não podem ser jogados, mesmo '
     'quando a missão já foi liberada. Sequência e Repetição têm dez desafios implementados cada. '
     'Depuração e Condicionais continuam com desafios em breve.'),
    ('Progresso',
     'As conquistas e o XP são salvos automaticamente ao concluir desafios. Use Continuar para recuperar '
     'esse progresso; a sequência de comandos, os monstros destruídos e as coletas da tentativa não '
     'são salvos. Iniciar começa '
     'uma nova partida e, se já houver progresso salvo, pede confirmação antes de substituí-lo.'),
    ('Navegação e tutorial',
     'Use os botões de navegação das telas ou Escape para voltar. O Tutorial está disponível na tela '
     'inicial. Use Fechar ou Escape para fechá-lo. O tutorial e a confirmação de nova partida pausam '
     'a execução e a espera pelo resultado, além de bloquear cliques na tela ao fundo. '
     'Escape cancela a confirmação de nova partida. '
     'As preferências salvas de música e efeitos sonoros continuam sendo respeitadas de forma independente.'),
)
