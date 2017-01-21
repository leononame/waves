import random

import pygame
from pytmx.util_pygame import load_pygame

import Map
import Player
import Utils


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
        self.screen = pygame.display.set_mode((self.scr_width, self.scr_height))
        # Window caption
        pygame.display.set_caption("Tilemap game")
        # Mouse invisible
        pygame.mouse.set_visible(0)
        # clock
        self.clock = pygame.time.Clock()
        # FPS
        self.fps = 30

    def run(self):
        # Player position
        player_dx = int(self.scr_width / 32 / 2) - 1
        player_dy = int(self.scr_height / 32 / 2) - 1
        # Camera position
        camera_x = 72 - player_dx
        camera_y = 70 - player_dy
        # Load map
        tiled_map = load_pygame('assets/maps/lvl0.tmx')

        # Create game objects
        # Create player
        player = Player.Player(player_dx, player_dy, camera_x, camera_y)
        # Create map
        current_map = Map.Map(camera_x, camera_y, tiled_map)

        # Flow control
        done = False

        while not done:
            # Temporarily generate water here
            for i in range(0, 10):
                self.generateSinkhole(tiled_map, random.randint(80, 400), random.randint(80, 400), random.randint(3, 16), random.randint(3, 12))
            self.clock.tick(self.fps)
            # Fill screen
            self.screen.fill((198, 209, 255))
            # Check events
            # Get all events
            for event in pygame.event.get():
                # exit game
                if event.type == pygame.QUIT:
                    done = True
                # controls
                if event.type == pygame.KEYDOWN:
                    # escape exits game
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                    key = event.key
                    # pass keys to map if player is not colliding in order to move camera
                    if not player.is_colliding(key, tiled_map):
                        current_map.handle_input(key)

            # Render
            current_map.render(self.screen)
            player.render(self.screen)

            if player.is_dead(tiled_map):
                done = True
                self.display_game_over()

            # flip screen
            pygame.display.flip()

    # Display a game over message
    def display_game_over(self):
        # new surface
        s = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        # Set transparent
        s.set_alpha(128)
        # Fill black
        s.fill((0, 0, 0))  # this fills the entire surface
        self.screen.blit(s, (0, 0))  # (0,0) are the top-left coordinates
        # GUI Tile
        gui_tiles = Utils.load_image("assets/RPG GUI/RPG_GUI_v1.png")
        self.screen.blit(gui_tiles, (100, 100), pygame.Rect(15, 115, 300, 80))
        # Initialize font
        font = pygame.font.SysFont("monospace", 40)
        # Render text
        label = font.render("Game Over", 1, (204, 153, 0))
        self.screen.blit(label, (135, 115))
        # Flip display
        pygame.display.flip()

    def wants_repeat(self):
        exit = False
        while not exit:
            self.clock.tick(self.fps)
            # Get all events
            for event in pygame.event.get():
                # exit game
                if event.type == pygame.QUIT:
                    exit = True

                # controls
                if event.type == pygame.KEYDOWN:
                    # escape exits game
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                    if event.key == pygame.K_SPACE:
                        return True
        return False


    #Only a temporary method
    def generateSinkhole(self, tiled_map, xpos, ypos, width, height):
        fringe_layer = tiled_map.layers[1]
        collision_layer = tiled_map.layers[2]
        asset_layer = tiled_map.layers[3]
        topl, top, topr = asset_layer.data[0][0], asset_layer.data[0][1], asset_layer.data[0][2]
        l, w, r = asset_layer.data[1][0], asset_layer.data[1][1], asset_layer.data[1][2]
        bottoml, bottom, bottomr = asset_layer.data[2][0], asset_layer.data[2][1], asset_layer.data[2][2]

        for i in range(width):
            for j in range(height):
                if fringe_layer.data[ypos + j][xpos + i] in [topl, top, topr, l, w, r, bottom, bottomr, bottoml]:
                    fringe_layer.data[ypos + j][xpos + i] = w
                    collision_layer.data[ypos + j][xpos + i] = w
                    continue
                # Corners
                if i is 0 and j is 0:  # top left corner
                    pos = topl
                elif i is width - 1 and j is 0:  # top right corner
                    pos = topr
                elif i is 0 and j is height - 1:  # bot left corner
                    pos = bottoml
                elif i is width - 1 and j is height - 1:  # bot right corner
                    pos = bottomr
                # Borders
                elif i is 0:  # left border
                    pos = l
                elif i is width - 1:  # right border
                    pos = r
                elif j is 0:  # top border
                    pos = top
                elif j is height - 1:  # bot border
                    pos = bottom
                else:
                    pos = w

                fringe_layer.data[ypos + j][xpos + i] = pos
                if pos is w or pos is top:
                    collision_layer.data[ypos + j][xpos + i] = pos