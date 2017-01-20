import pygame
from pytmx.util_pygame import load_pygame

class Map(object):
    def __init__(self, cx, cy, tile_map):
        self.camera_x = cx
        self.camera_y = cy
        self.tile_map = tile_map

    def handle_input(self, key):
        if key == pygame.K_LEFT: self.camera_x -= 1
        if key == pygame.K_RIGHT: self.camera_x -= -1
        if key == pygame.K_UP: self.camera_y += -1
        if key == pygame.K_DOWN: self.camera_y += 1

    def render(self, screen):
        # for layer in self.tile_map.visible_layers:
            if self.tile_map.get_tile_image(player.map_x, player.map_y, 2) is None:
                for layer in range(0, 2):
                    for x in range(0, width / 32):
                        for y in range(0, height / 32):
                            tx = x + self.camera_x
                            ty = y + self.camera_y

                            if tx < 0 or tx >= 30 or ty < 0 or ty >= 30:
                                continue
                            image = self.tile_map.get_tile_image(tx, ty, layer)
                            if image is not None:
                                screen.blit(image, (x * 32, y * 32))


# def map_animation():
#     global screen, tiled_map, camera_x_current, camera_y_current
#     # for layer in tiled_map.visible_layers:
#     if tiled_map.get_tile_image(player.map_x, player.map_y, 2) is None:
#         for layer in range(0, 2):
#             for x in range(0, width / 32):
#                 for y in range(0, height / 32):
#                     tx = x + camera_x
#                     ty = y + camera_y
#
#                     if tx < 0 or tx >= 30 or ty < 0 or ty >= 30:
#                         continue
#                     image = tiled_map.get_tile_image(tx, ty, layer)
#                     if image is not None:
#                         screen.blit(image, (x * 32, y * 32))
#
# tiled_map = load_pygame('../tilesets/LPC Base/startmap.tmx')

# if key == pygame.K_LEFT: camera_x -= 1
# if key == pygame.K_RIGHT: camera_x -= -1
# if key == pygame.K_UP: camera_y += -1
# if key == pygame.K_DOWN: camera_y += 1
