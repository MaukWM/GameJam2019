from models.tiles.tile import Tile


class Dirt(Tile):
    strength = 0.1
    stability = 1
    should_fall = False
    def is_solid(self):
        return True

    def draw(self, surface, camera_y):
        pass
