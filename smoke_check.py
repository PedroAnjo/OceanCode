import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
import pygame
from oceancode.controllers.app_controller import AppController
app = AppController()
def click(action):
    b = next(b for b in app.views[app.navigation.active].buttons if b.action == action)
    app.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=b.rect.center))
click(('music',)); assert not app.state.music_enabled
click(('play',)); assert app.navigation.active == 'missions'
click(('mission',3)); assert app.navigation.active == 'missions'
click(('mission',1)); assert app.navigation.active == 'levels'
click(('level',4)); assert app.navigation.active == 'levels'
click(('level',3)); assert app.navigation.active == 'game'
for d in ['up','down','left','right']: click(('command',d))
assert app.state.commands == ['up','down','left','right']
click(('remove',1)); assert app.state.commands == ['up','left','right']
for _ in range(20): click(('command','up'))
assert len(app.state.commands) == 12
click(('execute',)); assert len(app.state.commands) == 12
click(('clear',)); assert not app.state.commands
click(('execute',)); assert 'Adicione' in app.state.message
click(('back',)); click(('level',1)); assert app.navigation.active == 'game'
click(('back',)); click(('back',)); click(('mission',2)); click(('level',2))
assert app.state.selected_mission.number == 2
click(('back',)); click(('back',)); click(('back',)); assert app.navigation.active == 'start'
click(('quit',)); assert not app.running
pygame.quit()
app = AppController()
pygame.event.post(pygame.event.Event(pygame.QUIT))
app.run(); assert not pygame.display.get_init()
print('PASS: rendering, click navigation, locks, commands, music, exits')
