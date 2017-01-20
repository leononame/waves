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
        #     if self.tile_map.get_tile_image(player.map_x, player.map_y, 2) is None:
        for layer in range(0, 2):
            for x in range(0, screen.get_width() / 32):
                for y in range(0, screen.get_height() / 32):
                    tx = x + self.camera_x
                    ty = y + self.camera_y

                    if tx < 0 or tx >= self.tile_map.width or ty < 0 or ty >= self.tile_map.height:
                        continue
                    image = self.tile_map.get_tile_image(tx, ty, layer)
                    if image is not None:
                        screen.blit(image, (x * 32, y * 32))


