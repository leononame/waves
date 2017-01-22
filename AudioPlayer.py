import pygame

class AudioPlayer:
    def __init__(self, game_music_path='assets/music/game_music.mp3', menu_music_path='assets/music/menu_music.mp3'):
        self.game_music_path = game_music_path
        self.menu_music_path = menu_music_path


    def startGameMusic(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.game_music_path)
        pygame.mixer.music.play(-1)


    def startMenuMusic(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.menu_music_path)
        pygame.mixer.music.play(-1)

