from models.tiles.tile import Tile


class Dirt(Tile):
    def __init__(self, world, x, y, is_grass: bool=False):
        super().__init__(world, x, y)
        self.is_grass = is_grass

    def is_solid(self):
        return True

    def draw(self, surface, camera_y):
        pass

    def is_grass(self):
        return self.is_grass
