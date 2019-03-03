from models.tiles.dirt_tile import Dirt
from models.tiles.half_liter_klokkium_tile import HalfLiterKlokkium
from models.tiles.tile import Tile
from constants import TILE_SIZE_IN_PIXELS
import pygame
from models.items.item_types import ItemType

WHEAT_SPRITES = [
    pygame.transform.scale(pygame.image.load('assets/graphics/wheat_0.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS)),
    pygame.transform.scale(pygame.image.load('assets/graphics/wheat_1.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS)),
    pygame.transform.scale(pygame.image.load('assets/graphics/wheat_2.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS)),
    pygame.transform.scale(pygame.image.load('assets/graphics/wheat_3.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS)),
    pygame.transform.scale(pygame.image.load('assets/graphics/wheat_4.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS)),
    pygame.transform.scale(pygame.image.load('assets/graphics/wheat_5.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS)),
    pygame.transform.scale(pygame.image.load('assets/graphics/wheat_6.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS)),

]


class Wheat(Tile):

    def get_resistance(self):
        return 0.01

    def __init__(self, world, x, y):
        super().__init__(world, x, y)

        self.world.register_wheat(self)

        # Multi-spawning
        self.item_type = {
            ItemType.WHEAT: 0,
            ItemType.SEEDS: 1,
        }

        self.ready = False

        # Goes to 1 over the course of growing
        self.growth_level = 0

        # Coole shit
        tile_below = self.world.get_tile_at_indices(self.x, self.y+1)
        self.growing_speed = 1
        if isinstance(tile_below, Dirt):
            self.growing_speed *= 0.001
        elif isinstance(tile_below, HalfLiterKlokkium):
            self.growing_speed *= 0.01
        else:
            self.damage(1000000000)

    def get_strength(self):
        return 0.0

    def is_solid(self):
        return False

    def draw(self, surface, camera_y):
        drawn_sprite = min(int(self.growth_level*len(WHEAT_SPRITES)), len(WHEAT_SPRITES)-1)
        x, y = self.x * TILE_SIZE_IN_PIXELS, self.y * TILE_SIZE_IN_PIXELS - camera_y
        surface.blit(WHEAT_SPRITES[drawn_sprite], (x, y))

    def grow_step(self):
        self.growth_level += self.growing_speed
        self.growth_level = min(1.0, self.growth_level)

        # If the wheat is ready: change the drop type
        if not self.ready and self.growth_level * len(WHEAT_SPRITES) > len(WHEAT_SPRITES) - 1:
            self.item_type = {
                ItemType.WHEAT: 1,
                ItemType.SEEDS: 2,
            }
            self.ready = True

