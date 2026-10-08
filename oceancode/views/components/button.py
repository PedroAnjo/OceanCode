from functools import lru_cache
import pygame
from ... import config as c

@lru_cache(maxsize=16)
def font(size):
    return pygame.font.SysFont(c.FONT_NAME, size)

def text(surface, label, position, size=c.FONT_BODY, color=c.NAVY, center=False):
    rendered = font(size).render(str(label), True, color)
    rect = rendered.get_rect(center=position) if center else rendered.get_rect(topleft=position)
    surface.blit(rendered, rect)

def panel(surface, rect, color=c.PALE):
    pygame.draw.rect(surface, color, rect, border_radius=c.RADIUS)

def arrow(surface, direction, center, color=c.WHITE):
    x, y = center
    points = [(0, -15), (-11, -3), (-4, -3), (-4, 14), (4, 14), (4, -3), (11, -3)]
    rotations = {"up": 0, "right": 1, "down": 2, "left": 3}
    for _ in range(rotations[direction]):
        points = [(-py, px) for px, py in points]
    pygame.draw.polygon(surface, color, [(x + px, y + py) for px, py in points])

class Button:
    def __init__(self, rect, label, action, enabled=True, direction=None):
        self.rect = pygame.Rect(rect)
        self.label, self.action, self.enabled, self.direction = label, action, enabled, direction

    def draw(self, surface, mouse):
        color = c.BLUE if self.enabled else c.GRAY
        if self.enabled and self.rect.collidepoint(mouse):
            color = (18, 82, 173)
        panel(surface, self.rect, color)
        if self.direction:
            arrow(surface, self.direction, self.rect.center)
        else:
            text(surface, self.label, self.rect.center, color=c.WHITE, center=True)

    def hit(self, position):
        return self.enabled and self.rect.collidepoint(position)
