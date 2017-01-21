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


def rotate(l, n):
    return l[-n:] + l[:-n]


def remove_tile(x, y, tile_map, layer):
    # This is an empty tile
    # Get gid to non-existent tile
    invisible_gid = tile_map.layers[3].data[3][0]
    tile_map.layers[layer].data[y][x] = invisible_gid


def fell_tree_at(xpos, ypos, tile_map):
    # Remove collision layer
    remove_tile(xpos, ypos, tile_map, 2)
    # Remove tree trunk layer
    remove_tile(xpos, ypos, tile_map, 6)
    # Remove all tree tiles in tree layer
    for x in range(xpos - 1, xpos + 2):
        for y in range(ypos - 3, ypos + 1):
            # Remove tiles from layer 5 (tree layer)
            remove_tile(x, y, tile_map, 5)


# If a plyer fells a tree, logs should be generated
def generate_logs(xpos, ypos, tile_map):
    # This is the log tile
    log_gid = tile_map.layers[3].data[3][1]
    # Add logs to log layer
    for i in range (-1, 2):
        tile_map.layers[7].data[ypos][xpos + i] = log_gid


def add_log(xpos, ypos, tile_map):
    # This is the log tile
    log_gid = tile_map.layers[3].data[3][1]
    # Add logs to log layer
    tile_map.layers[7].data[ypos][xpos] = log_gid
    # Remove collision from collison layer
    if tile_map.get_tile_image(xpos, ypos, 2) is not None:
        remove_tile(xpos, ypos, tile_map, 2)
