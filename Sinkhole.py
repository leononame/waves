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
        # gid for Grass
        self.grass = self.asset_layer.data[0][3]

        # directions
        self.up = 0
        self.down = 1
        self.left = 2
        self.right = 3

    def negateDirection(self, d):
        if d is self.up:
            return self.down
        if d is self.down:
            return self.up
        if d is self.left:
            return self.right
        if d is self.right:
            return self.left

    def changeToWater(self, xpos, ypos):
        # Change gid in fringe and ground layers
        self.fringe_layer.data[ypos][xpos] = self.w
        self.ground_layer.data[ypos][xpos] = self.w
        # Change collison layer
        self.collision_layer.data[ypos][xpos] = self.w

    def changeToBorder(self, xpos, ypos, d):
        # Canion spreads vertical (up or down) -> change LEFT and RIGHT adjacent tiles
        if d is self.up or d is self.down:

            # assets -> water
            if self.isAsset(xpos - 1, ypos, 0, 0): self.changeToWater(xpos - 1, ypos)
            if self.isAsset(xpos + 1, ypos, 0, 0): self.changeToWater(xpos + 1, ypos)

            # water -> stay water
            if self.getType(xpos - 1, ypos) is self.w: self.changeToWater(xpos - 1, ypos)
            if self.getType(xpos + 1, ypos) is self.w: self.changeToWater(xpos + 1, ypos)

            # grass -> l, r border
            if self.getType(xpos - 1, ypos) is self.grass:
                self.fringe_layer.data[ypos][xpos - 1] = self.l
            if self.getType(xpos + 1, ypos) is self.grass:
                self.fringe_layer.data[ypos][xpos + 1] = self.r


        # Canion spreads horizontal (left or right) -> change TOP and BOTTOM adjacent tiles
        if d is self.left or d is self.right:

            # assets -> water
            if(self.isAsset(xpos, ypos + 1, 0, 0)): self.changeToWater(xpos, ypos + 1)
            if(self.isAsset(xpos, ypos - 1, 0, 0)): self.changeToWater(xpos, ypos - 1)

            # water -> stay water
            if self.getType(xpos, ypos + 1) is self.w: self.changeToWater(xpos, ypos + 1)
            if self.getType(xpos, ypos - 1) is self.w: self.changeToWater(xpos, ypos - 1)

            # grass -> t, b border
            if self.getType(xpos, ypos + 1) is self.grass:
                self.fringe_layer.data[ypos + 1][xpos] = self.bottom
            if self.getType(xpos, ypos - 1) is self.grass:
                self.fringe_layer.data[ypos - 1][xpos] = self.top
                self.collision_layer.data[ypos - 1][xpos] = self.top  # top borders are on collision layer







    # CANIONS
    # Canions can spread only straight on
    # Canions affect 3 tile (borders and corners)
    def spreadCanion(self, xpos, ypos, d):
        if d is self.up:
            dy = -1
            dx = 0
        if d is self.down:
            dy = 1
            dx = 0
        if d is self.left:
            dx = -1
            dy = 0
        if d is self.right:
            dx = 1
            dy = 0
        return (xpos + dx, ypos + dy)

    def generateCanion(self, xpos, ypos, len):
        # Check pos moves the starting position to water if necessary
        direction = random.randint(0, 3)
        xpos, ypos = self.checkPos(xpos, ypos, direction)
        print("At pos: (" + str(xpos) + ', ' + str(ypos) + ')')
        neg_dir = self.negateDirection(direction)

        print("Entering loop")
        for i in range(len):
            xpos, ypos = self.spreadCanion(xpos, ypos, neg_dir)
            print("Changing tile: (" + str(xpos) + ', ' + str(ypos) + ')')

            self.changeToWater(xpos, ypos)
            self.changeToBorder(xpos, ypos, neg_dir)


    # WAVES
    # Waves can spread in diagonal neighbour tiles
    # Temp decission: Waves affect 1-2 tiles (neighbour to avoid gaps). No borders and corners.
    def spreadWave(self, xpos, ypos, d):
        if d is self.up:
            dy = -1
            dx = random.randint(-1, 1)
        if d is self.down:
            dy = 1
            dx = random.randint(-1, 1)
        if d is self.left:
            dx = -1
            dy = random.randint(-1, 1)
        if d is self.right:
            dx = 1
            dy = random.randint(-1, 1)
        return (xpos + dx, ypos + dy)

    def generateWave(self, xpos, ypos, N):
        # Check pos moves the starting position to water if necessary
        direction = random.randint(0, 3)
        xpos, ypos = self.checkPos(xpos, ypos, direction)

        # waves spread in negative direction of water search direction
        neg_dir = self.negateDirection(direction)
        for i in range(N):
            xpos_old, ypos_old = xpos, ypos
            xpos, ypos = self.spreadWave(xpos, ypos, neg_dir)

            self.changeToWater(xpos, ypos)
            # Change neighbour tile from original tile too
            self.fillNeighbour(xpos, ypos, xpos_old, ypos_old, neg_dir)


    def fillNeighbour(self, xpos, ypos, xpos_old, ypos_old, d):
        if d is self.up or d is self.down:
            y = ypos_old
            x = xpos
        if d is self.left or d is self.right:
            x = xpos_old
            y = ypos
        # Change gid in fringe and ground layers
        self.fringe_layer.data[y][x] = self.w
        self.ground_layer.data[y][x] = self.w
        # Change collison layer
        self.collision_layer.data[y][x] = self.w
    ## Waves






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
                # Change gid in fringe layer and for water change ground layer too
                self.fringe_layer.data[ypos + j][xpos + i] = pos
                if pos is self.w:
                    self.ground_layer.data[ypos + j][xpos + i] = pos

                # Add collison layer
                if pos is self.w or pos is self.top:
                    self.collision_layer.data[ypos + j][xpos + i] = pos

    # If the starting position of the sinkhole is not in water, search near water and place it there
    def checkPos(self, xpos, ypos, direction):
        if self.ground_layer.data[ypos][xpos] is self.ground_layer.data[0][0]:
            return (xpos, ypos)
        else:
            if direction is 0: # move up
                print("Going to: (" + str(xpos) + ', ' + str(ypos) + ')')
                return self.checkPos(xpos, ypos - 1, direction)
            if direction is 1: # move down
                print("Going to: (" + str(xpos) + ', ' + str(ypos) + ')')
                return self.checkPos(xpos, ypos + 1, direction)
            if direction is 2: # move left
                print("Going to: (" + str(xpos) + ', ' + str(ypos) + ')')
                return self.checkPos(xpos - 1, ypos, direction)
            if direction is 3: # mover right
                print("Going to: (" + str(xpos) + ', ' + str(ypos) + ')')
                return self.checkPos(xpos + 1, ypos, direction)


    def isBorder(self, xpos, ypos, i, j):
            return self.fringe_layer.data[ypos + j][xpos + i] in [self.topl, self.top, self.topr, self.l, self.r, self.bottom, self.bottomr, self.bottoml]


    def isAsset(self, xpos, ypos, i, j):
        return self.fringe_layer.data[ypos + j][xpos + i] in [self.topl, self.top, self.topr, self.l, self.w, self.r, self.bottom, self.bottomr, self.bottoml]

    def getType(self, xpos, ypos):
        return self.ground_layer.data[ypos][xpos]