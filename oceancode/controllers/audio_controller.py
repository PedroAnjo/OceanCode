import pygame
from .. import config as c


class ControladorAudio:
    def __init__(self, estado):
        self.estado = estado
        self.som_clique = None
        self.musica_carregada = False
        self.musica_iniciada = False
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
                self.musica_carregada = True
            except (pygame.error, OSError):
                pass
        self.atualizar_musica()

    def tocar_clique(self):
        if (self.estado.audio_ativado and self.estado.efeitos_ativados
                and self.som_clique is not None and pygame.mixer.get_init()):
            try:
                self.som_clique.play()
            except (pygame.error, OSError):
                pass

    def atualizar_musica(self):
        if not self.musica_carregada or not pygame.mixer.get_init():
            return
        try:
            if self.estado.audio_ativado and self.estado.musica_ativada:
                if self.musica_iniciada:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.play(loops=-1)
                    self.musica_iniciada = True
            else:
                pygame.mixer.music.pause()
        except (pygame.error, OSError):
            pass

