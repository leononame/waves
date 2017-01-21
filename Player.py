import pygame

import Animation
import Utils


class Player(object):
    def __init__(self, x, y, cx, cy):
        num = 8
        duration = 3
        self.anim_image_right = Utils.load_image("assets/LPC Base Assets/sprites/people/princess.png")
        self.anim_right = Animation.Animation(self.anim_image_right, 64, 192, num, 64, 64, duration)
        self.anim_image_left = Utils.load_image("assets/LPC Base Assets/sprites/people/princess.png")
        self.anim_left = Animation.Animation(self.anim_image_left, 64, 64, num, 64, 64, duration)
        self.anim_image_up = Utils.load_image("assets/LPC Base Assets/sprites/people/princess.png")
        self.anim_up = Animation.Animation(self.anim_image_up, 64, 0, num, 64, 64, duration)
        self.anim_image_down = Utils.load_image("assets/LPC Base Assets/sprites/people/princess.png")
        self.anim_down = Animation.Animation(self.anim_image_down, 64, 128, num, 64, 64, duration)
        # position and direction and running
        self.pos_x = x * 32
        self.pos_y = y * 32

        self.walking = False
        self.interval = num * duration
        self.counter = 0

        self.__up = 1
        self.__down = 2
        self.__right = 3
        self.__left = 4
        self.__still = 0
        self.dir = self.__still

        self.map_x = x + cx
        self.map_y = y + 1 + cy

        self.carrying_log = False

    def is_colliding(self, key, map):
        if key == pygame.K_LEFT:
            self.dir = self.__left
            self.walking = True
            if self.is_collision(self.map_x - 1, self.map_y, map):
                return True
            self.map_x -= 1
        if key == pygame.K_RIGHT:
            self.dir = self.__right
            self.walking = True
            if self.is_collision(self.map_x + 1, self.map_y, map) or self.is_collision(self.map_x + 2, self.map_y, map):
                return True
            self.map_x += 1
        if key == pygame.K_DOWN:
            self.dir = self.__down
            self.walking = True
            if self.is_collision(self.map_x, self.map_y + 1, map) or self.is_collision(self.map_x + 1, self.map_y + 1, map):
                return True
            self.map_y += 1
        if key == pygame.K_UP:
            self.dir = self.__up
            self.walking = True
            if self.is_collision(self.map_x, self.map_y - 1, map) or self.is_collision(self.map_x + 1, self.map_y - 1, map):
                return True
            self.map_y -= 1
        return False

    def render(self, screen):
        if self.dir == self.__left:
            if self.walking:
                self.anim_left.update()
            self.anim_left.render(screen, (self.pos_x, self.pos_y))
        elif self.dir == self.__right:
            if self.walking:
                self.anim_right.update()
            self.anim_right.render(screen, (self.pos_x, self.pos_y))
        elif self.dir == self.__up:
            if self.walking:
                self.anim_up.update()
            self.anim_up.render(screen, (self.pos_x, self.pos_y))
        elif self.dir == self.__down:
            if self.walking:
                self.anim_down.update()
            self.anim_down.render(screen, (self.pos_x, self.pos_y))
        else:
            self.anim_down.render(screen, (self.pos_x, self.pos_y))
        # self.counter += 1
        # if self.counter == self.interval:
        #     self.counter = 0
        self.walking = False

    def is_collision(self, x, y, map):
        # Layer 2 is collision layer
        return map.get_tile_image(x, y, 2) is not None

    def __is_trunk(self, x, y, tile_map):
        # Layer 6 is tree trunk layer
        return tile_map.get_tile_image(x, y, 6) is not None

    # Check if player is dead
    def is_dead(self, tile_map):
        # Player is dead if he is on a collision tile (a wave hit him)
        return tile_map.get_tile_image(self.map_x, self.map_y, 2) is not None

    # Checks if player is looking right at a tree in order to fell it
    def is_in_front_of_tree(self, map):
        # Check directions
        if self.dir == self.__down:
            # When looking down, we collide when x,y+1 or x+1,y+1
            return self.__is_trunk(self.map_x, self.map_y + 1, map) or self.__is_trunk(self.map_x + 1, self.map_y + 1, map)
        elif self.dir == self.__right:
            return self.__is_trunk(self.map_x + 1, self.map_y, map) or self.__is_trunk(self.map_x + 2, self.map_y, map)
        elif self.dir == self.__left:
            return self.__is_trunk(self.map_x - 1, self.map_y, map)
        elif self.dir == self.__up:
            return self.__is_trunk(self.map_x, self.map_y - 1, map) or self.__is_trunk(self.map_x + 1, self.map_y - 1, map)
        return False

    # Checks if player can pick up log
    def is_standing_on_log(self, tile_map, offset = True):
        # Layer 7 is log layer
        if offset:
            if self.dir == self.__right:
                 return tile_map.get_tile_image(self.map_x + 2, self.map_y, 7) is not None and tile_map.get_tile_image(self.map_x + 3, self.map_y, 7) is not None
            elif self.dir == self.__left:
                return tile_map.get_tile_image(self.map_x - 1, self.map_y, 7) is not None and tile_map.get_tile_image(self.map_x - 2, self.map_y, 7) is not None
            elif self.dir == self.__down:
                return tile_map.get_tile_image(self.map_x, self.map_y + 1, 7) is not None and tile_map.get_tile_image(self.map_x + 1, self.map_y + 1, 7) is not None
            elif self.dir == self.__up:
                return tile_map.get_tile_image(self.map_x, self.map_y - 1, 7) is not None and tile_map.get_tile_image(self.map_x + 1, self.map_y - 1, 7) is not None
        else:
         return tile_map.get_tile_image(self.map_x, self.map_y, 7) is not None and tile_map.get_tile_image(self.map_x + 1, self.map_y, 7) is not None

    def pick_up_log(self, tile_map, offset = True):
        # If offset is True, we pick up the log in front of us
        # Otherwise, we pick up the log we're standing on
        self.carrying_log = True
        if offset:
            # Remove log from log layer
            if self.dir == self.__right:
                Utils.remove_tile(self.map_x + 2, self.map_y, tile_map, 7)
                Utils.remove_tile(self.map_x + 3, self.map_y, tile_map, 7)
            elif self.dir == self.__left:
                Utils.remove_tile(self.map_x - 1, self.map_y, tile_map, 7)
                Utils.remove_tile(self.map_x - 2, self.map_y, tile_map, 7)
            elif self.dir == self.__down:
                Utils.remove_tile(self.map_x, self.map_y + 1, tile_map, 7)
                Utils.remove_tile(self.map_x + 1, self.map_y + 1, tile_map, 7)
            elif self.dir == self.__up:
                Utils.remove_tile(self.map_x, self.map_y - 1, tile_map, 7)
                Utils.remove_tile(self.map_x + 1, self.map_y - 1, tile_map, 7)
        else:
            # Remove log from log layer
            Utils.remove_tile(self.map_x, self.map_y, tile_map, 7)
            Utils.remove_tile(self.map_x + 1, self.map_y, tile_map, 7)

    def throw_log(self, tile_map, offset=True):
        self.carrying_log = False
        if offset:
            if self.dir == self.__right:
                Utils.add_log(self.map_x + 2, self.map_y, tile_map)
                Utils.add_log(self.map_x + 3, self.map_y, tile_map)
            elif self.dir == self.__left:
                Utils.add_log(self.map_x - 1, self.map_y, tile_map)
                Utils.add_log(self.map_x - 2, self.map_y, tile_map)
            elif self.dir == self.__down:
                Utils.add_log(self.map_x, self.map_y + 1, tile_map)
                Utils.add_log(self.map_x + 1, self.map_y + 1, tile_map)
            elif self.dir == self.__up:
                Utils.add_log(self.map_x, self.map_y - 1, tile_map)
                Utils.add_log(self.map_x + 1, self.map_y - 1, tile_map)
        else:
            Utils.add_log(self.map_x, self.map_y, tile_map)
            Utils.add_log(self.map_x + 1, self.map_y, tile_map)


    def fell_tree(self, tile_map):
        # Check directions
        if self.dir == self.__down:
            # When looking down, we collide when x,y+1 or x+1,y+1
            if self.__is_trunk(self.map_x, self.map_y + 1, tile_map):
                x = self.map_x
                y = self.map_y + 1
            elif self.__is_trunk(self.map_x + 1, self.map_y + 1, tile_map):
                x = self.map_x + 1
                y = self.map_y +1
        elif self.dir == self.__right:
            if self.__is_trunk(self.map_x + 1, self.map_y, tile_map):
                x = self.map_x + 1
                y = self.map_y
            elif self.__is_trunk(self.map_x + 2, self.map_y, tile_map):
                x = self.map_x + 2
                y = self.map_y
        elif self.dir == self.__left:
            if self.__is_trunk(self.map_x - 1, self.map_y, tile_map):
                x = self.map_x - 1
                y = self.map_y
        elif self.dir == self.__up:
            if self.__is_trunk(self.map_x, self.map_y - 1, tile_map):
                x = self.map_x
                y = self.map_y - 1
            elif self.__is_trunk(self.map_x + 1, self.map_y - 1, tile_map):
                x = self.map_x + 1
                y = self.map_y - 1
        if x is not None and y is not None:
            Utils.fell_tree_at(x, y, tile_map)
            Utils.generate_logs(x, y, tile_map)

