from models.tiles.tile import Tile
from constants import TILE_SIZE_IN_PIXELS
import pygame

DIRT_SPRITE = pygame.image.load('assets/graphics/dirt.png')


class Dirt(Tile):
    def is_solid(self):
        return True

    def draw(self, surface, camera_y):
        x, y = self.x*TILE_SIZE_IN_PIXELS, self.y*TILE_SIZE_IN_PIXELS - camera_y
        surface.blit(DIRT_SPRITE, (x, y))
