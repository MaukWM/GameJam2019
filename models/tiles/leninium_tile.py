from models.tiles.tile import Tile
from constants import TILE_SIZE_IN_PIXELS
import pygame
from models.items.item_types import ItemType

LENINIUM_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/leninium.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
STONE_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/stone.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
LENINIUM_BLOCK_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/leninium_block.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))


class Leninium(Tile):

    def __init__(self, world, x, y, ore_bool=True):
        super().__init__(world, x, y)
        self.item_type = ItemType.LENINIUM
        self.ore_bool = ore_bool

    def get_strength(self):
        return 1

    def get_resistance(self):
        return 20.0

    def is_solid(self):
        return True

    def draw(self, surface, camera_y):
        x, y = self.x * TILE_SIZE_IN_PIXELS, self.y * TILE_SIZE_IN_PIXELS - camera_y
        if self.ore_bool:
            surface.blit(STONE_SPRITE, (x, y))
            surface.blit(LENINIUM_SPRITE, (x, y))
        else:
            surface.blit(LENINIUM_BLOCK_SPRITE, (x, y))
