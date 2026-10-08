from .. import config as c

class GameController:
    def __init__(self, state):
        self.state = state

    def handle(self, action):
        kind, *args = action
        if kind == "command" and args[0] in ("up", "down", "left", "right"):
            if len(self.state.commands) < c.MAX_COMMANDS:
                self.state.commands.append(args[0])
                self.state.message = "Comando adicionado. Clique na sequência para remover."
            else:
                self.state.message = f"Limite de {c.MAX_COMMANDS} comandos atingido."
        elif kind == "remove" and 0 <= args[0] < len(self.state.commands):
            self.state.commands.pop(args[0])
            self.state.message = "Comando removido."
        elif kind == "clear":
            self.state.commands.clear()
            self.state.message = "Sequência limpa. Planeje uma nova rota."
        elif kind == "execute":
            self.state.message = (f"Prévia: {len(self.state.commands)} comandos. Execução ainda não implementada."
                                  if self.state.commands else "Adicione ao menos um comando antes de executar.")
