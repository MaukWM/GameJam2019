from models.tiles.tile import Tile
from constants import TILE_SIZE_IN_PIXELS
import pygame

JELTISIUM_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/jeltsinium.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))

class Jeltisnium(Tile):

    def is_solid(self):
        return True

    def draw(self, surface, camera_y):
        x, y = self.x * TILE_SIZE_IN_PIXELS, self.y * TILE_SIZE_IN_PIXELS - camera_y
        surface.blit(JELTISIUM_SPRITE, (x, y))
