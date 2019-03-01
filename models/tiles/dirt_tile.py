from models.tiles.tile import Tile
from constants import TILE_SIZE_IN_PIXELS
import pygame

DIRT_SPRITE = pygame.image.load('assets/graphics/dirt.png')


class Dirt(Tile):
    def __init__(self, world, x, y, is_grass: bool=False):
        super().__init__(world, x, y)
        self.is_grass = is_grass

    def is_solid(self):
        return True

    def draw(self, surface, camera_y):
        x, y = self.x*TILE_SIZE_IN_PIXELS, self.y*TILE_SIZE_IN_PIXELS - camera_y
        surface.blit(DIRT_SPRITE, (x, y))

    def is_grass(self):
        return self.is_grass
