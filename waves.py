import random

import pygame
from pytmx.util_pygame import load_pygame

import Map
import Player
import Utils


def generateSinkhole(tiled_map, xpos, ypos, width, height):
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
            elif i is width - 1 and j is 0: # top right corner
                pos = topr
            elif i is 0 and j is height - 1:  # bot left corner
                pos = bottoml
            elif i is width - 1 and j is height - 1: # bot right corner
                pos = bottomr
            # Borders
            elif i is 0: # left border
                pos = l
            elif i is width - 1: # right border
                pos = r
            elif j is 0: # top border
                pos = top
            elif j is height - 1: # bot border
                pos = bottom
            else:
                pos = w

            fringe_layer.data[ypos + j][xpos + i] = pos
            if pos is w or pos is top:
                collision_layer.data[ypos + j][xpos + i] = pos


# Display a game over message
def display_game_over(screen):
    # new surface
    s = pygame.Surface((screen.get_width(), screen.get_height()))
    # Set transparent
    s.set_alpha(128)
    # Fill black
    s.fill((0, 0, 0))  # this fills the entire surface
    screen.blit(s, (0, 0))  # (0,0) are the top-left coordinates
    # GUI Tile
    gui_tiles = Utils.load_image("assets/RPG GUI/RPG_GUI_v1.png")
    screen.blit(gui_tiles, (100, 100), pygame.Rect(15, 115, 300, 80))
    # Initialize font
    font = pygame.font.SysFont("monospace", 40)
    # Render text
    label = font.render("Game Over", 1, (204, 153, 0))
    screen.blit(label, (135, 115))
    # Flip display
    pygame.display.flip()
    return True


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

    generateSinkhole(tiled_map, 80, 80, 5, 7)

    count = 0
    # Start loop
    while not done:
        count += 1
        if count is fps / 2:
            count = 0
        generateSinkhole(tiled_map, random.randint(70, 300), random.randint(70, 300), random.randint(3, 12), random.randint(3, 8))
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

        if player.is_dead(tiled_map):
            done = True
            display_game_over(screen)

        done = True
        display_game_over(screen)
        # flip screen
        pygame.display.flip()

    exit = False
    while not exit:
        clock.tick(fps)
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


if __name__ == '__main__':
    # Call main
    main()