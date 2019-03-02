import pygame

from constants import TILE_SIZE_IN_PIXELS
from models.tiles.tile import Tile

STONE_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/stone.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))

class Stone(Tile):
    strength = 0.5
    stability = 1
    should_fall = False
    def is_solid(self):
        return True

    def draw(self, surface, camera_y):
        x, y = self.x * TILE_SIZE_IN_PIXELS, self.y * TILE_SIZE_IN_PIXELS - camera_y
        surface.blit(STONE_SPRITE, (x, y))
