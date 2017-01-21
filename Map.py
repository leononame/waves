import random

import pygame
from pytmx.util_pygame import load_pygame

import Utils


class Map(object):
    def __init__(self, cx, cy, tile_map):
        self.camera_x = cx
        self.camera_y = cy
        self.tile_map = tile_map
        self.animation_duration = 5
        self.counter = 0

    def handle_input(self, key):
        if key == pygame.K_LEFT: self.camera_x -= 1
        if key == pygame.K_RIGHT: self.camera_x -= -1
        if key == pygame.K_UP: self.camera_y += -1
        if key == pygame.K_DOWN: self.camera_y += 1

    def render_ontop_of_player(self, screen):
        layer = 5
        for x in range(0, screen.get_width() / 32):
            for y in range(0, screen.get_height() / 32):
                tx = x + self.camera_x
                ty = y + self.camera_y

                if tx < 0 or tx >= self.tile_map.width or ty < 0 or ty >= self.tile_map.height:
                    continue

                props = self.tile_map.get_tile_properties(tx, ty, layer)
                if props is not None and props['render_last']:
                    image = self.tile_map.get_tile_image(tx, ty, layer)

                    if image is not None:
                        screen.blit(image, (x * 32, y * 32))


    def render(self, screen):
        self.counter += 1
        if self.counter == self.animation_duration:
            self.counter = 0

        for layer in [0, 1, 4, 5]: # ground, fringe, water, trees
            for x in range(0, screen.get_width() / 32):
                for y in range(0, screen.get_height() / 32):
                    tx = x + self.camera_x
                    ty = y + self.camera_y

                    if tx < 0 or tx >= self.tile_map.width or ty < 0 or ty >= self.tile_map.height:
                        continue

                    self.animate_water(tx, ty, layer)
                    image = self.tile_map.get_tile_image(tx, ty, layer)

                    if image is not None:
                        screen.blit(image, (x * 32, y * 32))

    def animate_water(self, x, y, layer):
        props = self.tile_map.get_tile_properties(x, y, layer)
        if self.counter == 0 and props is not None and props.get('animated_water', False):
            image_gid = props['frames'][random.randint(0, 6)].gid
            # Post it on fringe layer because ground layer is buggy
            self.tile_map.layers[4].data[y][x] = image_gid
