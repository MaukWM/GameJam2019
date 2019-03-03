from constants import TILE_SIZE_IN_PIXELS
from models.tiles.tile import Tile
import pygame

AIR_UNDERGROUND_SPRITE = DIRT_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/background.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))

class Air(Tile):
    def can_support(self):
        return False

    def get_resistance(self):
        return 0

    def draw(self, surface, camera_y):
        if self.y >= 20:
            x, y = self.x*TILE_SIZE_IN_PIXELS, self.y*TILE_SIZE_IN_PIXELS - camera_y
            surface.blit(AIR_UNDERGROUND_SPRITE, (x, y))
        pass

    def is_solid(self):
        return False

    def check_stability(self):
        return False

    def is_mineable(self):
        return False
