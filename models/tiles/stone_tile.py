from models.tiles.tile import Tile


class Stone(Tile):
    strength = 0.5
    stability = 1
    should_fall = False
    def is_solid(self):
        return True

    def draw(self, surface, camera_y):
        pass
