import pygame
from .base_view import BaseView
from .components.button import Button, text, panel
from .. import config as c

class GameView(BaseView):
    def __init__(self):
        super().__init__()
        self.background = None
        if c.BACKGROUND_IMAGE.is_file():
            try:
                self.background = pygame.image.load(str(c.BACKGROUND_IMAGE)).convert()
            except pygame.error:
                pass

    def board(self, surface):
        r = pygame.Rect(c.BOARD_RECT)
        if self.background is not None:
            surface.blit(pygame.transform.smoothscale(self.background, r.size), r)
        else:
            for row in range(r.height):
                t = row / r.height
                color = tuple(int(a + (b - a) * t) for a, b in zip(c.OCEAN_TOP, c.OCEAN_BOTTOM))
                pygame.draw.line(surface, color, (r.x, r.y + row), (r.right - 1, r.y + row))
            for x, y in [(90, 180), (560, 230), (760, 410), (370, 445)]:
                pygame.draw.circle(surface, (82, 181, 211), (x, y), 10, 2)
        cw, ch = r.width // c.BOARD_COLS, r.height // c.BOARD_ROWS
        for col in range(c.BOARD_COLS + 1):
            pygame.draw.line(surface, (83, 162, 198), (r.x + col * cw, r.y), (r.x + col * cw, r.bottom))
        for row in range(c.BOARD_ROWS + 1):
            pygame.draw.line(surface, (83, 162, 198), (r.x, r.y + row * ch), (r.right, r.y + row * ch))
        def cell(col, row):
            return r.x + col * cw + cw // 2, r.y + row * ch + ch // 2
        for col, row in [(3, 1), (4, 3), (2, 4), (6, 2)]:
            x, y = cell(col, row)
            pygame.draw.polygon(surface, (70, 94, 114), [(x-32,y+21), (x-23,y-12), (x+5,y-24), (x+30,y+2), (x+34,y+21)])
        x, y = cell(0, 3)
        pygame.draw.polygon(surface, (235, 171, 45), [(x-25,y), (x-43,y-16), (x-43,y+16)])
        pygame.draw.ellipse(surface, (255, 207, 75), (x-33,y-18,72,36))
        pygame.draw.circle(surface, (31, 96, 140), (x+12,y), 10)
        pygame.draw.lines(surface, (255, 207, 75), False, [(x,y-18),(x,y-29),(x+15,y-29)], 6)
        x, y = cell(7, 0)
        pygame.draw.circle(surface, (105, 231, 188), (x,y), 22, 3)
        pygame.draw.polygon(surface, (105, 231, 188), [(x,y-15),(x+12,y),(x,y+15),(x-12,y)])

    def draw(self, surface, state, mouse):
        self.header(surface, f"{state.selected_mission.name}  /  Fase {state.selected_level.number}", "Protótipo visual • Submarino e obstáculos demonstrativos")
        self.board(surface)
        panel(surface, (936, 116, 296, 384))
        text(surface, "COMANDOS", (1084, 145), 24, c.NAVY, True)
        self.buttons = [Button((988, 180 + i * 76, 192, 60), "", ("command", d), direction=d)
                        for i, d in enumerate(("up", "down", "left", "right"))]
        panel(surface, (48, 520, 1184, 188))
        text(surface, "ÁREA DE PROGRAMAÇÃO", (72, 535), 22)
        text(surface, f"{len(state.commands)}/{c.MAX_COMMANDS} • Clique em uma seta para removê-la", (690, 537), 18, c.MUTED)
        for i in range(c.MAX_COMMANDS):
            rect = (72 + i * 67, 575, 56, 50)
            if i < len(state.commands):
                self.buttons.append(Button(rect, "", ("remove", i), direction=state.commands[i]))
            else:
                pygame.draw.rect(surface, c.BORDER, rect, 2, border_radius=10)
        self.buttons += [Button((928, 575, 140, 50), "Executar", ("execute",)),
                         Button((1080, 575, 128, 50), "Limpar", ("clear",)),
                         Button((72, 647, 116, 40), "Voltar", ("back",))]
        text(surface, state.message, (212, 657), 18, c.MUTED)
        self.draw_buttons(surface, mouse)
