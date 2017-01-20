import pygame


class Animation(object):
    def __init__(self, image, start_x, start_y, num, width, height, duration):
        # save surface
        self.image = image

        # position, number, height, width of frames
        self.start_x = start_x
        self.start_y = start_y
        self.num = num
        self.height = height
        self.width = width

        # Duration of frame
        self.duration = duration

        # current time and frame
        self.time = 0
        self.current = 0

    def render(self, screen, pos):
        screen.blit(self.image, pos, pygame.Rect(self.start_x + (self.width * self.current), self.start_y, self.width, self.height))

    def update(self, time=1):
        # Add time
        self.time += time

        # If we go past duration
        if self.time > self.duration:
            # Reset time and go to next frame
            self.time = 0
            self.current += 1
            # Make sure that the current frame is available
            if self.current >= self.num:
                self.current = 0