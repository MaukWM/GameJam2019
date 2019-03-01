from models.tiles.tile import Tile


class Air(Tile):
    strength = 0
    should_fall = False
    stability = 0
    def draw(self, surface, camera_y):
        pass

    def is_solid(self):
        return False
