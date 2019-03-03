from models.tiles.tile import Tile
from constants import TILE_SIZE_IN_PIXELS
import pygame
from models.items.item_types import ItemType

WHEAT_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/wheat.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))


class Wheat(Tile):

    def get_resistance(self):
        return 0.01

    def __init__(self, world, x, y):
        super().__init__(world, x, y)

        # Multi-spawning
        self.item_type = {
            ItemType.WHEAT: 1,
            ItemType.SEEDS: 2,
        }

    def get_strength(self):
        return 1

    def is_solid(self):
        return False

    def draw(self, surface, camera_y):
        x, y = self.x * TILE_SIZE_IN_PIXELS, self.y * TILE_SIZE_IN_PIXELS - camera_y
        surface.blit(WHEAT_SPRITE, (x, y))

    def is_mineable(self):
        return True
