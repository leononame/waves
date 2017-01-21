import random


class Sinkhole:
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

    def generateSinkhole(self, xpos, ypos, width, height):

        # Check pos moves the starting position to water if necessary
        direction = random.randint(0, 3)
        xpos, ypos = self.checkPos(xpos, ypos, direction)

        for i in range(width):
            for j in range(height):
                # Check if on pos is already an asset. If yes, then set a water asset
                # if self.fringe_layer.data[ypos + j][xpos + i] in [self.topl, self.top, self.topr, self.l, self.w, self.r, self.bottom, self.bottomr,self.bottoml]:
                #     self.fringe_layer.data[ypos + j][xpos + i] = self.w
                #     self.collision_layer.data[ypos + j][xpos + i] = self.w
                #     continue

                # Corners
                if i is 0 and j is 0:  # top left corner
                    pos = self.topl
                elif i is width - 1 and j is 0:  # top right corner
                    pos = self.topr
                elif i is 0 and j is height - 1:  # bot left corner
                    pos = self.bottoml
                elif i is width - 1 and j is height - 1:  # bot right corner
                    pos = self.bottomr
                # Borders
                elif i is 0:  # left border
                    if(self.isBorder(xpos, ypos, i, j)): # dont't replace a border with water
                        continue
                    pos = self.l
                elif i is width - 1:  # right border
                    if(self.isBorder(xpos, ypos, i, j)): # dont't replace a border with water
                        continue
                    pos = self.r
                elif j is 0:  # top border
                    if(self.isBorder(xpos, ypos, i, j)): # dont't replace a border with water
                        continue
                    pos = self.top
                elif j is height - 1:  # bot border
                    if(self.isBorder(xpos, ypos, i, j)): # dont't replace a border with water
                        continue
                    pos = self.bottom
                else:
                    pos = self.w

                # If the tile is already occupied with something from asset layer change to water
                if self.isAsset(xpos, ypos, i, j):
                    pos = self.w
                # Change gid
                self.fringe_layer.data[ypos + j][xpos + i] = pos

                # Add collison layer
                if pos is self.w or pos is self.top:
                    self.collision_layer.data[ypos + j][xpos + i] = pos

    # If the starting position of the sinkhole is not in water, search near water and place it there
    def checkPos(self, xpos, ypos, direction):
        if self.ground_layer.data[ypos][xpos] is self.ground_layer.data[0][0]:
            return (xpos, ypos)
        else:
            if direction is 0: # move up
                return self.checkPos(xpos, ypos - 1, direction)
            if direction is 1: # move down
                return self.checkPos(xpos, ypos + 1, direction)
            if direction is 2: # move left
                return self.checkPos(xpos - 1, ypos, direction)
            if direction is 3: # mover right
                return self.checkPos(xpos + 1, ypos, direction)


    def isBorder(self, xpos, ypos, i, j):
            return self.fringe_layer.data[ypos + j][xpos + i] in [self.topl, self.top, self.topr, self.l, self.r, self.bottom, self.bottomr, self.bottoml]


    def isAsset(self, xpos, ypos, i, j):
        return self.fringe_layer.data[ypos + j][xpos + i] in [self.topl, self.top, self.topr, self.l, self.w, self.r, self.bottom, self.bottomr, self.bottoml]