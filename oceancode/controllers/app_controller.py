import pygame
from .. import config as c
from ..views.components.button import font
from ..models.game_state import GameState
from ..views.start_view import StartView
from ..views.mission_view import MissionView
from ..views.level_view import LevelView
from ..views.game_view import GameView
from .navigation_controller import NavigationController
from .game_controller import GameController

class AppController:
    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        font.cache_clear()
        self.surface = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
        pygame.display.set_caption(c.TITLE)
        self.clock = pygame.time.Clock()
        self.state = GameState()
        self.navigation = NavigationController(self.state)
        self.game = GameController(self.state)
        self.views = {"start": StartView(), "missions": MissionView(), "levels": LevelView(), "game": GameView()}
        self.running = True
        self.draw()

    def dispatch(self, action):
        kind, *args = action
        if kind == "quit":
            self.running = False
        elif kind == "play":
            self.navigation.active = "missions"
        elif kind == "back":
            self.navigation.back()
        elif kind == "music":
            self.state.music_enabled = not self.state.music_enabled
        elif kind == "mission":
            self.navigation.mission(args[0])
        elif kind == "level":
            self.navigation.level(args[0])
        else:
            self.game.handle(action)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.navigation.back()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.views[self.navigation.active].buttons:
                if button.hit(event.pos):
                    self.dispatch(button.action)
                    break
            self.draw()  # Refresh click targets even when several events arrive together.

    def draw(self):
        self.surface.fill(c.WHITE)
        self.views[self.navigation.active].draw(self.surface, self.state, pygame.mouse.get_pos())

    def run(self):
        try:
            while self.running:
                for event in pygame.event.get():
                    self.handle_event(event)
                self.draw()
                pygame.display.flip()
                self.clock.tick(c.FPS)
        finally:
            pygame.quit()
