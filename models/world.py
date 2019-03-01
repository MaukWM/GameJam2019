import random

from models.tiles.dirt_tile import Dirt
from models.tiles.air_tile import Air
from models.tiles.stone_tile import Stone
from constants import TILE_SIZE_IN_PIXELS
import random


# These values are from above
DIRT_START = 20
STONE_START = 40


class World(object):

    def __init__(self, width, height):
        """

        :param width: Width in tiles
        :param height: Height in tiles
        """
        self.tile_matrix = self.gen_world(width, height)
        self.width = width
        self.height = height

    def gen_world(self, width, height):
        world_matrix = []
        for x in range(width):
            column = []
            for y in range(height):
                # Are we above where the ground starts?
                if y < DIRT_START:
                    column.append(Air(self, x, y))
                    continue
                # Are we where the ground start?
                elif y == DIRT_START:
                    column.append(Dirt(self, x, y, True))
                    continue
                # Are we below where the ground starts but above where the stone starts?
                elif (y > DIRT_START) and (y <= STONE_START):
                    column.append(Dirt(self, x, y, False))
                    continue
                # Are we below where the stone starts?
                elif y > STONE_START:
                    stone_chance = y/height
                    if random.uniform(0, 1) > stone_chance:
                        column.append(Dirt(self, x, y, False))
                    else:
                        column.append(Stone(self, x, y))
                    continue

            world_matrix.append(column)

        world_matrix[5][20] = Air(self, 5, 20)
        world_matrix[6][20] = Air(self, 6, 20)
        world_matrix[6][21] = Air(self, 6, 21)
        return world_matrix

    def get_tile_at_indices(self, tile_x, tile_y):
        if tile_x < 0 or tile_y < 0:
            return None
        try:
            return self.tile_matrix[tile_x][tile_y]
        except IndexError:
            return None

    def get_tile_at(self, x, y):
        return self.get_tile_at_indices(x//TILE_SIZE_IN_PIXELS, y//TILE_SIZE_IN_PIXELS)

    def draw(self, surface, camera_y):
        for x in range(self.width):
            for y in range(self.height):
                self.tile_matrix[x][y].draw(surface, camera_y)

    def __repr__(self):
        s = ""
        for y in range(self.height):
            s += " | "
            for x in range(self.width):
                s += "%8s | "%str(self.tile_matrix[x][y])
            s += "\n"
        return s


if __name__ == "__main__":
    world = World(64, 1024)
    print(world)
