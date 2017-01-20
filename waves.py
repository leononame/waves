import pygame
from pytmx.util_pygame import load_pygame

import Map
import Player

def main():
    pygame.init()
    tile_size = 32
    scr_width, scr_height = 30 * tile_size, 30 * tile_size
    camera_x, camera_y = 0, 0
    pygame.key.set_repeat(1, 30)
    screen = pygame.display.set_mode((800, 600))
    tiled_map = load_pygame('lvl0.tmx')

    a = tiled_map.height
    pygame.display.set_caption("Tilemap game")
    pygame.mouse.set_visible(0)

    # clock
    clock = pygame.time.Clock()

    # flow control
    done = False

    player_dx = int(scr_width / 32 / 2) - 1
    player_dy = int(scr_height / 32 / 2) - 1

    # Create game objects
    # Create player
    player = Player.Player(player_dx, player_dy, camera_x, camera_y)
    # Create map
    current_map = Map.Map(camera_x, camera_y, tiled_map)
    # FPS
    fps = 30

    # Start loop
    while not done:
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
                if not player.is_colliding(key, tiled_map):
                    # TODO map key handling
                    b = 0

        # TODO render map
        player.render(screen)
        # flip screen
        pygame.display.flip()



if __name__ == '__main__':
    # Call main
    main()