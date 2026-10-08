from .base_view import BaseView
from .components.button import Button, text
from .. import config as c

class StartView(BaseView):
    def draw(self, surface, state, mouse):
        text(surface, "OceanCode", (640, 205), c.FONT_TITLE, c.BLUE, True)
        text(surface, "Expedição Oceânica", (640, 278), 30, c.MUTED, True)
        self.buttons = [Button((500, 360, 280, 58), "Jogar", ("play",)),
                        Button((500, 446, 280, 58), "Sair", ("quit",)),
                        Button((1030, 636, 202, 48), "Música: " + ("ligada" if state.music_enabled else "desligada"), ("music",))]
        self.draw_buttons(surface, mouse)
