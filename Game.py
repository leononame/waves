import pygame
from pytmx.util_pygame import load_pygame

import Map
import Player


class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        # Size of tileset: 32x32
        self.tile_size = 32
        # 30x30 tile screen
        self.scr_width = 30 * self.tile_size
        self.scr_height = 30 * self.tile_size
        # Enable repitition of event when key is being pressed continuously
        pygame.key.set_repeat(1, 30)
        # Initialize window
        self.screen = pygame.display.set_mode(self.scr_width, self.scr_height)
        # Load map
        self.tiled_map = load_pygame('assets/maps/lvl0.tmx')
        # Window caption
        pygame.display.set_caption("Tilemap game")
        # Mouse invisible
        pygame.mouse.set_visible(0)
        # clock
        self.clock = pygame.time.Clock()
        # Player position
        self.player_dx = int(self.scr_width / 32 / 2) - 1
        self.player_dy = int(self.scr_height / 32 / 2) - 1
        # Create game objects
        # Create player
        self.player = Player.Player(self.player_dx, self.player_dy, self.camera_x, self.camera_y)
        # Create map
        self.current_map = Map.Map(self.camera_x, self.camera_y, self.tiled_map)
        # FPS
        self.fps = 30