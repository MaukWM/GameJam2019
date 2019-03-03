from models.tiles.tile import Tile
from constants import TILE_SIZE_IN_PIXELS
import pygame
from models.items.item_types import ItemType

JELTISIUM_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/jeltsinium.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
STONE_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/stone.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
JELTISIUM_BLOCK_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/jeltsinium_block.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
JELTISIUM_BEAM_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/support_beams/jeltsinium_block.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
AIR_UNDERGROUND_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/background.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))


class Jeltisnium(Tile):

    def get_initial_strength(self):
        return 0.45

    def get_resistance(self):
        return 5.0

    def __init__(self, world, x, y, ore_bool=True, solid: bool=True):
        super().__init__(world, x, y)
        self.item_type = ItemType.JELTSIUM
        self.ore_bool = ore_bool
        self.solid = solid

    def is_solid(self):
        return self.solid

    def draw(self, surface, camera_y):
        x, y = self.x * TILE_SIZE_IN_PIXELS, self.y * TILE_SIZE_IN_PIXELS - camera_y
        if self.ore_bool:
            surface.blit(STONE_SPRITE, (x, y))
            surface.blit(JELTISIUM_SPRITE, (x, y))
        else:
            if self.solid:
                surface.blit(JELTISIUM_BLOCK_SPRITE, (x, y))
            else:
                if self.y >= 20:
                    surface.blit(AIR_UNDERGROUND_SPRITE, (x, y))
                surface.blit(JELTISIUM_BEAM_SPRITE, (x, y))
