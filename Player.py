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
            if self.is_collision(self.map_x + 2, self.map_y, map):
                return True
            self.map_x += 1
        if key == pygame.K_DOWN:
            self.dir = self.__down
            self.walking = True
            if self.is_collision(self.map_x, self.map_y + 1, map):
                return True
            self.map_y += 1
        if key == pygame.K_UP:
            self.dir = self.__up
            self.walking = True
            if self.is_collision(self.map_x, self.map_y - 1, map):
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
        return map.get_tile_image(x, y, 2) is not None
