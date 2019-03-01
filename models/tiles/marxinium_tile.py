from models.tiles.tile import Tile


class Marxinium(Tile):

    def is_solid(self):
        return True

    def draw(self, surface, camera_y):
        pass
