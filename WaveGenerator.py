import random


class WaveGenerator:
    def __init__(self, tiled_map):
        # Layers
        self.tiled_map = tiled_map
        self.ground_layer = self.tiled_map.layers[0]
        self.fringe_layer = self.tiled_map.layers[1]
        self.collision_layer = self.tiled_map.layers[2]
        self.asset_layer = self.tiled_map.layers[3]

        # gid's for Water-Sinkhole asset
        self.topl, self.top, self.topr = self.asset_layer.data[0][0], self.asset_layer.data[0][1], self.asset_layer.data[0][2]
        self.l, self.w, self.r = self.asset_layer.data[1][0], self.asset_layer.data[1][1], self.asset_layer.data[1][2]
        self.bottoml, self.bottom, self.bottomr = self.asset_layer.data[2][0], self.asset_layer.data[2][1], self.asset_layer.data[2][2]
        # gids for outer corners
        self.outer_topr, self.outer_bottomr, self.outer_topl, self.outer_bottoml = self.asset_layer.data[1][3], self.asset_layer.data[2][3], self.asset_layer.data[1][4], self.asset_layer.data[2][4]
        # gid for Grass
        self.grass = self.asset_layer.data[0][3]

        # directions
        self.up = 0
        self.down = 1
        self.left = 2
        self.right = 3

        self.fringe_objects = []
        none_gid = self.fringe_layer.data[0][0]
        for x in range(self.tiled_map.width):
            for y in range(self.tiled_map.height):
                if self.fringe_layer.data[y][x] is not none_gid:
                    self.fringe_objects.append((x, y))

    def generateCanion(self, len, xpos=0, ypos=0):
        # Get position
        if xpos is 0 and ypos is 0:
            xpos, ypos = self.get_starting_position()

        tile = self.fringe_layer.data[ypos][xpos]
        if tile is self.top:
            direction = self.up
        elif tile is self.bottom:
            direction = self.down
        elif tile is self.l:
            direction = self.left
        elif tile is self.r:
            direction = self.right
        else:
            return None

        # Update fringe list
        self.fringe_objects.remove((xpos, ypos))
        # Make tile water
        self.ground_layer.data[ypos][xpos] = self.w
        self.collision_layer.data[ypos][xpos] = self.w

        # Set outer corners
        if direction == self.down:
            self.fringe_layer.data[ypos][xpos - 1] = self.outer_topl
            self.fringe_layer.data[ypos][xpos + 1] = self.outer_topr
        if direction == self.up:
            self.fringe_layer.data[ypos][xpos - 1] = self.outer_bottoml
            self.fringe_layer.data[ypos][xpos + 1] = self.outer_bottomr
        if direction == self.right:
            self.fringe_layer.data[ypos - 1][xpos] = self.outer_bottomr
            self.fringe_layer.data[ypos + 1][xpos] = self.outer_topr
        if direction == self.left:
            self.fringe_layer.data[ypos - 1][xpos] = self.outer_bottoml
            self.fringe_layer.data[ypos + 1][xpos] = self.outer_topl

        # Build middle tunnel
        for i in range(1, len - 2):
            xpos, ypos = self.next_iteration(direction, xpos, ypos)
            # Make tile water
            self.ground_layer.data[ypos][xpos] = self.w
            self.collision_layer.data[ypos][xpos] = self.w
            # Make borders
            self.generate_borders(direction, xpos, ypos)

        self.generate_finish_borders(direction, xpos, ypos)

    def generate_finish_borders(self, direction, xpos, ypos):
        xpos, ypos = self.next_iteration(direction, xpos, ypos)
        if direction is self.down:
            self.fringe_layer.data[ypos][xpos] = self.bottom
            self.fringe_layer.data[ypos][xpos - 1] = self.bottoml
            self.fringe_layer.data[ypos][xpos + 1] = self.bottomr
            self.fringe_objects.extend(((xpos, ypos), (xpos - 1, ypos), (xpos + 1, ypos)))
        elif direction is self.up:
            self.fringe_layer.data[ypos][xpos] = self.top
            self.fringe_layer.data[ypos][xpos - 1] = self.topl
            self.fringe_layer.data[ypos][xpos + 1] = self.topr
            self.fringe_objects.extend(((xpos, ypos), (xpos - 1, ypos), (xpos + 1, ypos)))
        elif direction is self.right:
            self.fringe_layer.data[ypos - 1][xpos] = self.topr
            self.fringe_layer.data[ypos][xpos] = self.r
            self.fringe_layer.data[ypos + 1][xpos] = self.bottomr
            self.fringe_objects.extend(((xpos, ypos), (xpos, ypos - 1), (xpos, ypos + 1)))
        elif direction is self.left:
            self.fringe_layer.data[ypos - 1][xpos ] = self.topl
            self.fringe_layer.data[ypos][xpos] = self.l
            self.fringe_layer.data[ypos + 1][xpos] = self.bottoml
            self.fringe_objects.extend(((xpos, ypos), (xpos, ypos - 1), (xpos, ypos + 1)))

    def generate_borders(self, direction, xpos, ypos):
        if direction is self.up or direction is self.down:
            self.fringe_layer.data[ypos][xpos - 1] = self.l
            self.fringe_layer.data[ypos][xpos + 1] = self.r
            self.fringe_objects.append((xpos - 1, ypos))
            self.fringe_objects.append((xpos + 1, ypos))
        elif direction is self.left or self.right:
            self.fringe_layer.data[ypos - 1][xpos] = self.top
            self.collision_layer.data[ypos - 1][xpos] = self.top
            self.fringe_layer.data[ypos + 1][xpos] = self.bottom
            self.fringe_objects.append((xpos, ypos - 1))
            self.fringe_objects.append((xpos, ypos + 1))

    def next_iteration(self, direction, xpos, ypos):
        if direction is self.up:
            return xpos, ypos - 1
        if direction is self.down:
            return xpos, ypos + 1
        if direction is self.left:
            return xpos - 1, ypos
        if direction is self.right:
            return xpos + 1, ypos

    def get_starting_position(self):
        length = len(self.fringe_objects)
        x = 0
        y = 0
        while self.fringe_layer.data[y][x] not in [self.top, self.bottom, self.l, self.r]:
            r = random.randint(0, length - 1)
            print(r)
            x, y = self.fringe_objects[r]
        return x, y