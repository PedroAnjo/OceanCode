from .base_view import BaseView
from .components.button import text
from .components.level_button import LevelButton
from .. import config as c

class LevelView(BaseView):
    def draw(self, surface, state, mouse):
        m = state.selected_mission
        self.header(surface, f"Missão {m.number} — {m.name}", f"Conteúdo: {m.content}  •  Escolha uma fase para explorar.")
        self.buttons = [LevelButton((190 + (i % 5) * 190, 210 + (i // 5) * 180, 140, 110), level)
                        for i, level in enumerate(m.levels)] + [self.back()]
        text(surface, "OK: concluída   •   Azul: disponível   •   Cinza: bloqueada", (640, 570), 20, c.MUTED, True)
        self.draw_buttons(surface, mouse)
