import random

from models.tiles.dirt_tile import Dirt
from models.tiles.stone_tile import Stone


class World(object):
    def __init__(self, width, height):
        self.tile_matrix = self.gen_world(width, height)
        self.width = width
        self.height = height

    def gen_world(self, width, height):
        world_matrix = []
        for x in range(width):
            column = []
            for y in range(height):
                if random.random() > 0.9:
                    column.append(Stone(self, x, y))
                else:
                    column.append(Dirt(self, x, y))
            world_matrix.append(column)
        return world_matrix

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
    world = World(64, 4096)
    print(world)
