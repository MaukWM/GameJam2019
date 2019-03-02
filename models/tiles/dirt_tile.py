from models.tiles.tile import Tile
from constants import TILE_SIZE_IN_PIXELS
import pygame

DIRT_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/dirt.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
DIRT_SPRITE_WITH_GRASS = pygame.transform.scale(pygame.image.load('assets/graphics/dirt_with_grass.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))


class Dirt(Tile):
    strength = 0.1
    stability = 1
    should_fall = False

    def __init__(self, world, x, y, is_grass: bool=False):
        super().__init__(world, x, y)
        self.is_grass = is_grass

    def is_solid(self):
        return True

    def draw(self, surface, camera_y):
        x, y = self.x*TILE_SIZE_IN_PIXELS, self.y*TILE_SIZE_IN_PIXELS - camera_y
        if self.is_grass:
            surface.blit(DIRT_SPRITE_WITH_GRASS, (x, y))
        else:
            surface.blit(DIRT_SPRITE, (x, y))

    def is_grass(self):
        return self.is_grass

    def damage(self, amount):
        self.stability -= amount
        if self.stability <= 0:
            return True             #it breaks
        else:
            return False            #it doesn't break
