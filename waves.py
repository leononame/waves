import random

import pygame
from pytmx.util_pygame import load_pygame

import Game
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
    game = Game.Game()
    game.run()
    game.wait_exit()


if __name__ == '__main__':
    # Call main
    main()