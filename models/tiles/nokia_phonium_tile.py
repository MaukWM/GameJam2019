from models.tiles.tile import Tile
from constants import TILE_SIZE_IN_PIXELS
import pygame
from models.items.item_types import ItemType

NOKIA_PHONIUM_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/nokiaphonium.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
STONE_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/stone.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
NOKIA_PHONIUM_BLOCK_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/nokiaphonium_block.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
NOKIA_PHONIUM_BEAM_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/nokiaphonium_beam.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))


class NokiaPhonium(Tile):
    def get_resistance(self):
        return 50.0

    def __init__(self, world, x, y, ore_bool=True, solid: bool=True):
        super().__init__(world, x, y)
        self.item_type = ItemType.NOKIA_PHONIUM
        self.ore_bool = ore_bool
        self.solid = solid

    def get_strength(self):
        return 50.0

    def is_solid(self):
        return self.solid

    def draw(self, surface, camera_y):
        x, y = self.x * TILE_SIZE_IN_PIXELS, self.y * TILE_SIZE_IN_PIXELS - camera_y
        if self.ore_bool:
            surface.blit(STONE_SPRITE, (x, y))
            surface.blit(NOKIA_PHONIUM_SPRITE, (x, y))
        else:
            if self.solid:
                surface.blit(NOKIA_PHONIUM_BLOCK_SPRITE, (x, y))
            else:
                surface.blit(NOKIA_PHONIUM_BEAM_SPRITE, (x, y))
