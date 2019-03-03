from models.tiles.tile import Tile


class Air(Tile):
    solid = False

    def can_support(self):
        return False

    def get_resistance(self):
        return 0

    def draw(self, surface, camera_y):
        pass

    def is_solid(self):
        return self.solid

    def check_stability(self):
        return False
