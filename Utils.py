import pygame


def load_image(filename, color_key=None):
    image = pygame.image.load(filename)
    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key, pygame.RLEACCEL)

    return image
