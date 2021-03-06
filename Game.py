import random

import pygame
from pytmx.util_pygame import load_pygame

import AudioPlayer
import Map
import Player
import Utils
import WaveGenerator


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag
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

        # Music
        self.music = AudioPlayer.AudioPlayer()

        # Display start screen
        # Fill screen
        self.screen.fill((0, 0, 0))
        # Initialize font
        font = pygame.font.SysFont("monospace", 40)
        # Render text
        label = font.render("Press space to start...", 1, (204, 153, 0))
        self.screen.blit(label, (135, 115))
        # Flip display
        pygame.display.flip()
        start = False
        self.music.startMenuMusic()
        while not start:
            # Check events
            # Get all events
            for event in pygame.event.get():
                # controls
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Display waiting screen
                        # Fill screen
                        self.screen.fill((0, 0, 0))
                        # Initialize font
                        font = pygame.font.SysFont("monospace", 40)
                        # Render text
                        label = font.render("Loading map...", 1, (204, 153, 0))
                        self.screen.blit(label, (135, 115))
                        # Flip display
                        pygame.display.flip()
                        start = True
                    # exit
                    if event.key == pygame.K_ESCAPE:
                        exit(0)



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
        # Create sinkhole generator
        waves = WaveGenerator.WaveGenerator(tiled_map)
        # Flow control
        done = False
        debounced_space = False
        debounced_alt = True

        wave_limit = 3
        random_limit = 3
        wave_counter = 0
        random_counter = 0
        self.music.startGameMusic()
        # waves.generateCanion(10, 80, 70)
        while not done:
            wave_counter += 1
            random_counter += 1
            if wave_counter is wave_limit:
                wave_counter = 0
                waves.generateCanion(random.randint(5, 20))
            if random_counter is random_limit:
                random_counter = 0
                waves.rand_generateWave(random.randint(72, 440), random.randint(70, 438), random.randint(3, 20))
            self.clock.tick(self.fps)
            # Fill screen
            self.screen.fill((198, 209, 255))
            # Check events
            # Get all events
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        debounced_space = True
                    if event.key == pygame.K_RALT or event.key == pygame.K_LALT:
                        debounced_alt = True
                # exit game
                if event.type == pygame.QUIT:
                    done = True
                # controls
                if event.type == pygame.KEYDOWN:
                    # escape exits game
                    if event.key == pygame.K_ESCAPE:
                        done = True
                        # Render
                        current_map.render(self.screen)
                        player.render(self.screen)
                        self.screen_overlay()
                        pygame.display.flip()
                        return None
                    key = event.key
                    # pass keys to map if player is not colliding in order to move camera
                    if not player.is_colliding(key, tiled_map):
                        current_map.handle_input(key)
                    # SPACE is action key
                    if event.key == pygame.K_SPACE:
                        # Fell tree if possible
                        if player.is_in_front_of_tree(tiled_map):
                            debounced_space = False
                            player.fell_tree(tiled_map)
                        # Pick up log if possible
                        elif not player.carrying_log and player.is_standing_on_log(tiled_map) and debounced_space:
                            player.pick_up_log(tiled_map)
                            debounced_space = False
                        # elif player.carrying_log and player.can_throw_log(tiled_map) and debounced_space:
                        elif player.carrying_log and player.can_throw_log(tiled_map) and debounced_space:
                            player.throw_log(tiled_map)
                            debounced_space = False
                    # ALT key for secondary action
                    if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                        # Pick up log if possible
                        # ALT key picks up logs you are standing on
                        if not player.carrying_log and player.is_standing_on_log(tiled_map, False) and debounced_alt:
                            player.pick_up_log(tiled_map, False)
                            debounced_alt = False
                        elif player.carrying_log and player.can_throw_log(tiled_map, False) and debounced_alt:
                            player.throw_log(tiled_map, False)
                            debounced_alt = False


            # Render
            current_map.render(self.screen)
            player.render(self.screen)
            current_map.render_ontop_of_player(self.screen)
            waves.render_animations(self.screen, current_map.camera_x, current_map.camera_y)
            if player.is_dead(tiled_map):
                done = True
                self.display_game_over()

            # flip screen
            pygame.display.flip()

    def screen_overlay(self):
        # new surface
        s = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        # Set transparent
        s.set_alpha(128)
        # Fill black
        s.fill((0, 0, 0))  # this fills the entire surface
        self.screen.blit(s, (0, 0))  # (0,0) are the top-left coordinates

    # Display a game over message
    def display_game_over(self):
        self.screen_overlay()
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
        self.music.startMenuMusic()
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
                        # Display waiting screen
                        # Fill screen
                        self.screen.fill((0, 0, 0))
                        # Initialize font
                        font = pygame.font.SysFont("monospace", 40)
                        # Render text
                        label = font.render("Loading map...", 1, (204, 153, 0))
                        self.screen.blit(label, (135, 115))
                        # Flip display
                        pygame.display.flip()
                        return True
        return False