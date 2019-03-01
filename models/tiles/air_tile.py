from models.tiles.tile import Tile


class Air(Tile):
    def draw(self, surface, camera_y):
        pass

    def is_solid(self):
        return False
