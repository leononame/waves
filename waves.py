import pygame
from pytmx.util_pygame import load_pygame

import Map
import Player

def main():
    pygame.init()
    tile_size = 32
    scr_width, scr_height = 30 * tile_size, 30 * tile_size
    camera_x, camera_y = 75, 75
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

    # Create game objects
    # Create player
    player = Player.Player(player_dx, player_dy, camera_x, camera_y)
    # Create map
    current_map = Map.Map(camera_x, camera_y, tiled_map)
    # FPS
    fps = 30

    ####################
    # Map manipulation #
    ####################
    ground_layer = tiled_map.layers[1]
    collision_layer = tiled_map.layers[2]
    # # Water gid
    # water_gid = ground_layer.data[0][0]
    # # Collision gid
    # collision_gid = collision_layer.data[0][0]
    # # Manipulate map
    # ground_layer.data[75][75] = water_gid
    # collision_layer.data[75][75] = collision_gid
    ###########################
    # Better map manipulation #
    ###########################
    asset_layer = tiled_map.layers[3]
    topl, top, topr = asset_layer.data[0][0], asset_layer.data[0][1], asset_layer.data[0][2]
    l, w, r = asset_layer.data[1][0], asset_layer.data[1][1], asset_layer.data[1][2]
    bottoml, bottom, bottomr = asset_layer.data[2][0], asset_layer.data[2][1], asset_layer.data[2][2]

    ground_layer.data[75][75] = topl
    ground_layer.data[75][76] = top
    ground_layer.data[75][77] = topr
    ground_layer.data[76][75] = l
    ground_layer.data[76][76] = w
    ground_layer.data[76][77] = r
    ground_layer.data[77][75] = bottoml
    ground_layer.data[77][76] = bottom
    ground_layer.data[77][77] = bottomr
    # collision_layer.data[75][75] = topl
    collision_layer.data[75][76] = top
    # collision_layer.data[75][77] = topr
    # collision_layer.data[76][75] = l
    collision_layer.data[76][76] = w
    # collision_layer.data[76][77] = r
    # collision_layer.data[77][75] = bottoml
    # collision_layer.data[77][76] = bottom
    # collision_layer.data[77][77] = bottomr

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