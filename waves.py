import random

import pygame
from pytmx.util_pygame import load_pygame

import Map
import Player
import Sinkhole


def main():
    pygame.init()
    tile_size = 32
    scr_width, scr_height = 30 * tile_size, 30 * tile_size
    pygame.key.set_repeat(1, 30)
    screen = pygame.display.set_mode((scr_width, scr_height))
    tiled_map = load_pygame('assets/maps/lvl0.tmx')

    pygame.display.set_caption("Tilemap game")
    pygame.mouse.set_visible(0)

    # clock
    clock = pygame.time.Clock()

    # flow control
    done = False

    player_dx = int(scr_width / 32 / 2) - 1
    player_dy = int(scr_height / 32 / 2) - 1
    camera_x, camera_y = 72 - player_dx, 70 - player_dy

    # Create game objects
    # Create player
    player = Player.Player(player_dx, player_dy, camera_x, camera_y)
    # Create map
    current_map = Map.Map(camera_x, camera_y, tiled_map)
    # FPS
    fps = 30

    sinkhole = Sinkhole.Sinkhole(tiled_map)
    # sinkhole.generateSinkhole(10, 10, 5, 10)
    # sinkhole.generateSinkhole(80, 82, 10, 5)

    count = 0
    sinkhole.generateCanion(80, 80, 5)


    # Start loop
    while not done:
        # Spawn random water sinkholes
        count += 1
        if count is fps / 4:
            count = 0
            # sinkhole.generateSinkhole(random.randint(70, 300), random.randint(70, 300), random.randint(3, 12), random.randint(3,8))
            # sinkhole.generateWave(random.randint(70, 300), random.randint(70, 300), random.randint(10, 30))
            sinkhole.generateCanion(random.randint(70, 300), random.randint(70, 300), random.randint(10, 30))


        clock.tick(fps)
        # fill screen
        screen.fill((198, 209, 255))
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
                if not player.is_colliding(key, tiled_map):
                    current_map.handle_input(key)

        current_map.render(screen)
        player.render(screen)
        # flip screen
        pygame.display.flip()


if __name__ == '__main__':
    # Call main
    main()