from models.tiles.tile import Tile
from constants import TILE_SIZE_IN_PIXELS
import pygame

MARXINIUM_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/marxinium.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
STONE_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/stone.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))


class Marxinium(Tile):
    def get_resistance(self):
        return 10.0

    def is_solid(self):
        return True

    def draw(self, surface, camera_y):
        x, y = self.x * TILE_SIZE_IN_PIXELS, self.y * TILE_SIZE_IN_PIXELS - camera_y
        surface.blit(STONE_SPRITE, (x, y))
        surface.blit(MARXINIUM_SPRITE, (x, y))
