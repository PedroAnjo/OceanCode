import pygame
from .. import config as c


class ControladorAudio:
    def __init__(self, estado):
        self.estado = estado
        self.som_clique = None
        self.musica_carregada = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except pygame.error:
            return
        if c.SOM_CLIQUE.is_file():
            try:
                self.som_clique = pygame.mixer.Sound(str(c.SOM_CLIQUE))
                self.som_clique.set_volume(c.VOLUME_CLIQUE)
            except (pygame.error, OSError):
                pass
        if c.MUSICA_FUNDO.is_file():
            try:
                pygame.mixer.music.load(str(c.MUSICA_FUNDO))
                pygame.mixer.music.set_volume(c.VOLUME_MUSICA)
                if estado.musica_ativada:
                    pygame.mixer.music.play(loops=-1)
                self.musica_carregada = True
            except (pygame.error, OSError):
                pass

    def tocar_clique(self):
        if self.estado.musica_ativada and self.som_clique is not None:
            self.som_clique.play()

    def atualizar_som(self):
        if not pygame.mixer.get_init():
            return
        if self.estado.musica_ativada:
            if self.musica_carregada:
                pygame.mixer.music.unpause()
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(loops=-1)
        else:
            pygame.mixer.music.pause()
            pygame.mixer.stop()
