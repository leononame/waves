import random

import pygame
from pytmx.util_pygame import load_pygame

import Utils


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
        # iterate over the tile properties
        for gid, props in self.tile_map.tile_properties.items():

            # iterate over the frames of the animation
            # if there is no animation, this list will be empty
            for animation_frame in props['frames']:
                # do something with the gid and duration of the frame
                # this may change in the future, as it is a little awkward now
                image = self.tile_map.get_tile_image_by_gid(gid)
                duration = animation_frame.duration
            # my_anim = props['frames']
            props['frames'] = Utils.rotate(props['frames'], 1)

        for layer in range(0, 2):
            for x in range(0, screen.get_width() / 32):
                for y in range(0, screen.get_height() / 32):
                    tx = x + self.camera_x
                    ty = y + self.camera_y

                    if tx < 0 or tx >= self.tile_map.width or ty < 0 or ty >= self.tile_map.height:
                        continue
                    if self.animate_water(tx, ty, layer):
                        image = self.tile_map.get_tile_image_by_gid(image_gid)
                    props = self.tile_map.get_tile_properties(tx, ty, layer)
                    if props is not None and len(props['frames']) > 1:
                        image_gid = props['frames'][random.randint(0, len(props['frames'])) - 1].gid
                        image = self.tile_map.get_tile_image_by_gid(image_gid)
                    else:
                        image = self.tile_map.get_tile_image(tx, ty, layer)
                    if image is not None:
                        screen.blit(image, (x * 32, y * 32))

    def animate_water(self, x, y, layer):
        props = self.tile_map.get_tile_properties(x, y, layer)
        if props is not None and props['animated_water']:
            image_gid = props['frames'][random.randint(0, 3)].gid
            return image_gid
        return False



