from models.tiles.tile import Tile
from constants import TILE_SIZE_IN_PIXELS
import pygame

LENINIUM_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/leninium.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS))

class Leninium(Tile):

    def is_solid(self):
        return True

    def draw(self, surface, camera_y):
        x, y = self.x * TILE_SIZE_IN_PIXELS, self.y * TILE_SIZE_IN_PIXELS - camera_y
        surface.blit(LENINIUM_SPRITE, (x, y))
