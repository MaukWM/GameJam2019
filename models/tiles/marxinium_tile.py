from models.tiles.tile import Tile
from constants import TILE_SIZE_IN_PIXELS
import pygame

MARXINIUM_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/marxinium.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))


class Marxinium(Tile):

    def is_solid(self):
        return True

    def draw(self, surface, camera_y):
        x, y = self.x * TILE_SIZE_IN_PIXELS, self.y * TILE_SIZE_IN_PIXELS - camera_y
        surface.blit(MARXINIUM_SPRITE, (x, y))
