from .button import Button, text
from ... import config as c
from ...models.level import LevelStatus

class LevelButton(Button):
    def __init__(self, rect, level):
        super().__init__(rect, str(level.number), ("level", level.number), level.playable)
        self.level = level

    def draw(self, surface, mouse):
        super().draw(surface, mouse)
        if self.level.status == LevelStatus.COMPLETED:
            text(surface, "OK", (self.rect.right - 30, self.rect.y + 8), 16, c.WHITE)
        text(surface, self.level.status.value, (self.rect.centerx, self.rect.bottom + 20), 17, c.MUTED, True)
