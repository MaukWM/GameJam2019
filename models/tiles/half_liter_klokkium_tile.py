from models.tiles.tile import Tile
from constants import TILE_SIZE_IN_PIXELS
import pygame
from models.items.item_types import ItemType

HALF_LITER_KLOKKIUM_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/halfliterklokkium.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
STONE_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/stone.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
HALF_LITER_KLOKKIUM_BLOCK_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/halfliterklokkium_block.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
HALF_LITER_KLOKKIUM_BEAM_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/halfliterklokkium_beam.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))


class HalfLiterKlokkium(Tile):

    def get_resistance(self):
        return 100

    def __init__(self, world, x, y, ore_bool=True, solid: bool=True):
        super().__init__(world, x, y)
        self.item_type = ItemType.HALF_LITER_KLOKKIUM
        self.ore_bool = ore_bool
        self.solid = solid

    def get_strength(self):
        return 1

    def is_solid(self):
        return self.solid

    def draw(self, surface, camera_y):
        x, y = self.x * TILE_SIZE_IN_PIXELS, self.y * TILE_SIZE_IN_PIXELS - camera_y
        if self.ore_bool:
            surface.blit(STONE_SPRITE, (x, y))
            surface.blit(HALF_LITER_KLOKKIUM_SPRITE, (x, y))
        else:
            if self.solid:
                surface.blit(HALF_LITER_KLOKKIUM_BLOCK_SPRITE, (x, y))
            else:
                surface.blit(HALF_LITER_KLOKKIUM_BEAM_SPRITE, (x, y))
