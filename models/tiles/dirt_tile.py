from models.tiles.tile import Tile
from constants import TILE_SIZE_IN_PIXELS
import pygame
from models.items.item_types import ItemType

DIRT_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/dirt.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
DIRT_BEAM_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/dirt_beam.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
DIRT_SPRITE_WITH_GRASS = pygame.transform.scale(pygame.image.load('assets/graphics/dirt_with_grass.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))


class Dirt(Tile):
    def __init__(self, world, x, y, is_grass: bool=False, solid=True):
        super().__init__(world, x, y)
        self.is_grass = is_grass
        self.item_type = ItemType.DIRT
        self.solid = solid

    def is_solid(self):
        return self.solid

    def draw(self, surface, camera_y):
        x, y = self.x*TILE_SIZE_IN_PIXELS, self.y*TILE_SIZE_IN_PIXELS - camera_y
        if self.is_grass:
            surface.blit(DIRT_SPRITE_WITH_GRASS, (x, y))
        else:
            if self.solid:
                surface.blit(DIRT_SPRITE, (x, y))
            else:
                surface.blit(DIRT_BEAM_SPRITE, (x, y))


    def is_grass(self):
        return self.is_grass

    def get_initial_strength(self):
        return 0.25

    def get_resistance(self):
        return 0.4
