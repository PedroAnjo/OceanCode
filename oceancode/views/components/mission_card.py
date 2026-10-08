import pygame
from .button import Button, panel, text
from ... import config as c

class MissionCard(Button):
    def __init__(self, rect, mission):
        super().__init__(rect, mission.name, ("mission", mission.number), mission.available)
        self.mission = mission

    def draw(self, surface, mouse):
        m, r = self.mission, self.rect
        color = c.PALE if m.available else (242, 243, 245)
        panel(surface, (r.x, r.y - 16, 145, 35), c.BLUE if m.available else c.GRAY)
        panel(surface, r, color)
        pygame.draw.rect(surface, c.BLUE if self.hit(mouse) else c.BORDER, r, 2, border_radius=c.RADIUS)
        ink = c.NAVY if m.available else c.MUTED
        text(surface, f"MISSÃO {m.number:02}", (r.x + 24, r.y + 22), c.FONT_SMALL, c.BLUE if m.available else c.MUTED)
        text(surface, m.name, (r.x + 24, r.y + 55), 28, ink)
        text(surface, f"Conteúdo: {m.content}", (r.x + 24, r.y + 103), 22, ink)
        text(surface, f"{len(m.levels)} fases  •  +{m.reward} XP", (r.x + 24, r.y + 139), 22, ink)
        text(surface, "Disponível  /  Abrir missão" if m.available else "Bloqueada", (r.x + 24, r.y + 184), 20, c.BLUE if m.available else c.MUTED)
