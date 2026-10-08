from .base_view import BaseView
from .components.button import text
from .components.mission_card import MissionCard
from .. import config as c

class MissionView(BaseView):
    def draw(self, surface, state, mouse):
        self.header(surface, "Escolha uma missão para iniciar sua expedição.", "Aprenda lógica de programação explorando cada missão.")
        text(surface, f"XP: {state.xp}   •   Nível: {state.player_level}", (935, 88), 20, c.BLUE)
        self.buttons = [MissionCard((48 + (i % 2) * 604, 160 + (i // 2) * 240, 580, 215), m)
                        for i, m in enumerate(state.missions)] + [self.back()]
        self.draw_buttons(surface, mouse)
