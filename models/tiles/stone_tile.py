import pygame

from constants import TILE_SIZE_IN_PIXELS
from models.tiles.tile import Tile
from models.items.item_types import ItemType

STONE_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/stone.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))


class Stone(Tile):
    def get_initial_strength(self):
        return 0.7

    def get_resistance(self):
        return 10

    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.item_type = ItemType.STONE

    def get_strength(self):
        return 10.0

    def is_solid(self):
        return True

    def draw(self, surface, camera_y):
        x, y = self.x * TILE_SIZE_IN_PIXELS, self.y * TILE_SIZE_IN_PIXELS - camera_y
        surface.blit(STONE_SPRITE, (x, y))
