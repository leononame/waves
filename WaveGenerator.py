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
        if xpos is 0 and ypos is 0:
            xpos, ypos = self.get_starting_position()
        print(xpos)
        print(ypos)
        return None
        # (xpos, ypos) = self.get_starting_position()
        # Check pos moves the starting position to water if necessary
        # direction = random.randint(0, 3)
        # direction = self.up
        # xpos, ypos = self.checkPos(xpos, ypos, direction)
        # print("At pos: (" + str(xpos) + ', ' + str(ypos) + ')')
        # neg_dir = self.negateDirection(direction)
        #
        # print("Entering loop")
        # # Todo
        # # self.setCorners_Begin(xpos, ypos, neg_dir)
        # while self.getType(xpos, ypos) is self.w:
        #     xpos, ypos = self.spreadCanion(xpos, ypos, neg_dir)
        #
        # for i in range(len):
        #     print("Changing tile: (" + str(xpos) + ', ' + str(ypos) + ')')
        #
        #     # Change the water tile...
        #     self.changeToWater(xpos, ypos)
        #     #  ... and then the borders at the adjacent tiles
        #     self.changeToBorder(xpos, ypos, neg_dir, False)
        #     # Generate outer borders
        #     if i == 0:
        #         if neg_dir == self.down:
        #             self.fringe_layer.data[ypos][xpos - 1] = self.outer_topl
        #             self.fringe_layer.data[ypos][xpos + 1] = self.outer_topr
        #         if neg_dir == self.up:
        #             self.fringe_layer.data[ypos][xpos - 1] = self.outer_bottoml
        #             self.fringe_layer.data[ypos][xpos + 1] = self.outer_bottomr
        #         if neg_dir == self.right:
        #             self.fringe_layer.data[ypos - 1][xpos] = self.outer_bottomr
        #             self.fringe_layer.data[ypos + 1][xpos] = self.outer_topr
        #         if neg_dir == self.left:
        #             self.fringe_layer.data[ypos - 1][xpos] = self.outer_bottoml
        #             self.fringe_layer.data[ypos + 1][xpos] = self.outer_topl
        #     if i is not len - 1:
        #         xpos, ypos = self.spreadCanion(xpos, ypos, neg_dir)
        #
        # self.changeToBorder(xpos, ypos, neg_dir, True)

    def get_starting_position(self):
        length = len(self.fringe_objects)
        x = 0
        y = 0
        while self.fringe_layer.data[y][x] not in [self.top, self.bottom, self.l, self.r]:
            r = random.randint(0, length - 1)
            x, y = self.fringe_objects[r]
        return x, y