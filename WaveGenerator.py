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

        self.specials = (self.topl, self.top, self.topr, self.l, self.r, self.bottoml, self.bottom, self.bottomr, self.outer_topl, self.outer_topr, self.outer_bottoml, self.outer_bottomr, self.w)
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

        if not self.neighbours_ok(direction, xpos, ypos):
            self.special_case(direction, xpos, ypos)
        else:
            # Generate a water tile
            # Also adds collision and removes from fringe list
            self.generate_water_tile(xpos, ypos)

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
        for i in range(1, len):
            xpos, ypos = self.next_iteration(direction, xpos, ypos)
            # Middle tile is always water tile
            self.generate_water_tile(xpos, ypos)
            # Make borders
            self.generate_borders(direction, xpos, ypos)

        self.generate_finish_borders(direction, xpos, ypos)

    def generate_finish_borders(self, direction, xpos, ypos):
        xpos, ypos = self.next_iteration(direction, xpos, ypos)
        if direction is self.down:
            self.fringe_layer.data[ypos][xpos] = self.bottom
            self.fringe_layer.data[ypos][xpos - 1] = self.bottoml
            self.fringe_layer.data[ypos][xpos + 1] = self.bottomr
            self.extend_to_list(((xpos, ypos), (xpos - 1, ypos), (xpos + 1, ypos)))
        elif direction is self.up:
            self.fringe_layer.data[ypos][xpos] = self.top
            self.fringe_layer.data[ypos][xpos - 1] = self.topl
            self.fringe_layer.data[ypos][xpos + 1] = self.topr
            self.extend_to_list(((xpos, ypos), (xpos - 1, ypos), (xpos + 1, ypos)))
        elif direction is self.right:
            self.fringe_layer.data[ypos - 1][xpos] = self.topr
            self.fringe_layer.data[ypos][xpos] = self.r
            self.fringe_layer.data[ypos + 1][xpos] = self.bottomr
            self.extend_to_list(((xpos, ypos), (xpos, ypos - 1), (xpos, ypos + 1)))
        elif direction is self.left:
            self.fringe_layer.data[ypos - 1][xpos] = self.topl
            self.fringe_layer.data[ypos][xpos] = self.l
            self.fringe_layer.data[ypos + 1][xpos] = self.bottoml
            self.extend_to_list(((xpos, ypos), (xpos, ypos - 1), (xpos, ypos + 1)))

    def generate_borders(self, direction, xpos, ypos):
        # Rules for downward borders
        if direction is self.down:
            # Check if we collide with another fringe object
            if (xpos - 1, ypos) in self.fringe_objects:
                # Save bject for easy access
                left_tile = self.fringe_layer.data[ypos][xpos - 1]
                if left_tile is self.topr or left_tile is self.top:
                    self.fringe_layer.data[ypos][xpos - 1] = self.outer_bottoml
                elif left_tile is self.topl or left_tile is self.bottoml or left_tile is self.l:
                    self.fringe_layer.data[ypos][xpos - 1] = self.l
                elif left_tile is self.r:
                    self.generate_water_tile(xpos - 1, ypos)
                elif left_tile is self.bottomr:
                    self.fringe_layer.data[ypos][xpos - 1] = self.outer_topr
                elif left_tile is self.bottom:
                    self.fringe_layer.data[ypos][xpos - 1] = self.outer_topl
            else:
                self.fringe_layer.data[ypos][xpos - 1] = self.l
                self.add_to_list((xpos - 1, ypos))

            if (xpos + 1, ypos) in self.fringe_objects:
                right_tile = self.fringe_layer.data[ypos][xpos + 1]
                if right_tile is self.topl or right_tile is self.top:
                    self.fringe_layer.data[ypos][xpos + 1] = self.outer_bottomr
                # outer_bottomr has to be replaced by outer_topr
                elif right_tile is self.topr or right_tile is self.bottomr or right_tile is self.r:
                    self.fringe_layer.data[ypos][xpos + 1] = self.r
                elif right_tile is self.l:
                    self.generate_water_tile(xpos + 1, ypos)
                elif right_tile is self.bottoml:
                    self.fringe_layer.data[ypos][xpos + 1] = self.outer_topl
                elif right_tile is self.bottom:
                    self.fringe_layer.data[ypos][xpos + 1] = self.outer_topr

            else:
                self.fringe_layer.data[ypos][xpos + 1] = self.r
                self.add_to_list((xpos + 1, ypos))

        elif direction is self.up:
            self.fringe_layer.data[ypos][xpos - 1] = self.l
            self.add_to_list((xpos - 1, ypos))
            self.fringe_layer.data[ypos][xpos + 1] = self.r
            self.add_to_list((xpos + 1, ypos))

        elif direction is self.left or self.right:
            self.fringe_layer.data[ypos - 1][xpos] = self.top
            self.collision_layer.data[ypos - 1][xpos] = self.top
            self.fringe_layer.data[ypos + 1][xpos] = self.bottom
            self.add_to_list((xpos, ypos - 1))
            self.add_to_list((xpos, ypos + 1))

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

    def neighbours_ok(self, direction, xpos, ypos):
        if direction is self.up or direction is self.down:
            return self.fringe_layer.data[ypos][xpos - 1] in [self.top, self.bottom] and self.fringe_layer.data[ypos][xpos + 1] in [self.top, self.bottom]
        elif direction is self.left or direction is self.right:
            return self.fringe_layer.data[ypos - 1][xpos] in [self.l, self.r] and self.fringe_layer.data[ypos + 1][xpos] in [self.l, self.r]

    def special_case(self, direction, xpos, ypos):
        if direction is self.left:
            self.special_case_left(xpos, ypos)
        elif direction is self.right:
            self.special_case_right(xpos, ypos)
        elif direction is self.up:
            self.special_case_up(xpos, ypos)
        elif direction is self.down:
            self.special_case_down(xpos, ypos)

    def special_case_left(self, xpos, ypos):
        return None

    def special_case_right(self, xpos, ypos):
        return None

    def special_case_up(self, xpos, ypos):
        return None

    def special_case_down(self, xpos, ypos):
        # First row
        if self.fringe_layer.data[ypos][xpos - 1] is self.bottoml:
            self.fringe_layer.data[ypos][xpos - 1] = self.l
        elif self.fringe_layer.data[ypos][xpos - 1] is self.outer_topr:
            self.generate_water_tile(xpos - 1, ypos)
        else:
            self.fringe_layer.data[ypos][xpos - 1] = self.outer_topl

        if self.fringe_layer.data[ypos][xpos + 1] is self.bottomr:
            self.fringe_layer.data[ypos][xpos + 1] = self.r
        elif self.fringe_layer.data[ypos][xpos + 1] is self.outer_topl:
            self.generate_water_tile(xpos + 1, ypos)
        else:
            self.fringe_layer.data[ypos][xpos + 1] = self.outer_topr

        # Make tile water
        self.ground_layer.data[ypos][xpos] = self.w
        self.collision_layer.data[ypos][xpos] = self.w

        return None

    def add_to_list(self, el):
        if el not in self.fringe_objects:
            self.fringe_objects.append(el)

    def extend_to_list(self, el):
        for (x, y) in el:
            if (x, y) not in self.fringe_objects:
                self.fringe_objects.append((x, y))

    def remove_from_list(self, el):
        if el in self.fringe_objects:
            self.fringe_objects.remove(el)

    def generate_water_tile(self, xpos, ypos):
        self.ground_layer.data[ypos][xpos] = self.w
        self.collision_layer.data[ypos][xpos] = self.w
        self.remove_from_list((xpos, ypos))
