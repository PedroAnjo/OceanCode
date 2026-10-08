from .components.button import Button, text
from .. import config as c

class BaseView:
    def __init__(self):
        self.buttons = []

    def header(self, surface, title, subtitle):
        text(surface, title, (48, 30), c.FONT_HEADING)
        text(surface, subtitle, (48, 77), c.FONT_SMALL, c.MUTED)

    def back(self):
        return Button((48, 636, 150, 48), "Voltar", ("back",))

    def draw_buttons(self, surface, mouse):
        for button in self.buttons:
            button.draw(surface, mouse)
