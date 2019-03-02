from models.tiles.tile import Tile
from constants import TILE_SIZE_IN_PIXELS
import pygame
from models.items.item_types import ItemType

HALF_LITER_KLOKKIUM_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/halfliterklokkium.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))
STONE_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/stone.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))


class HalfLiterKlokkium(Tile):

    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.item_type = ItemType.HALF_LITER_KLOKKIUM

    def get_strength(self):
        return 100.0

    def is_solid(self):
        return True

    def draw(self, surface, camera_y):
        x, y = self.x * TILE_SIZE_IN_PIXELS, self.y * TILE_SIZE_IN_PIXELS - camera_y
        surface.blit(STONE_SPRITE, (x, y))
        surface.blit(HALF_LITER_KLOKKIUM_SPRITE, (x, y))
