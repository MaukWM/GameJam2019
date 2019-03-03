import pygame

from constants import TILE_SIZE_IN_PIXELS
from models.tiles.tile import Tile
from models.items.item_types import ItemType

STONE_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/stone.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
STONE_BEAM_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/support_beams/stone.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
AIR_UNDERGROUND_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/background.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))


class Stone(Tile):
    def get_initial_strength(self):
        return 0.35

    def get_resistance(self):
        return 10

    def __init__(self, world, x, y, solid: bool=True):
        super().__init__(world, x, y)
        self.item_type = ItemType.STONE
        self.solid = solid


    def is_solid(self):
        return self.solid

    def draw(self, surface, camera_y):
        x, y = self.x * TILE_SIZE_IN_PIXELS, self.y * TILE_SIZE_IN_PIXELS - camera_y
        if self.solid:
            surface.blit(STONE_SPRITE, (x, y))
        else:
            if self.y >= 20:
                surface.blit(AIR_UNDERGROUND_SPRITE, (x, y))
            surface.blit(STONE_BEAM_SPRITE, (x, y))
