from models.tiles.dirt_tile import Dirt
from models.tiles.half_liter_klokkium_tile import HalfLiterKlokkium
from models.tiles.tile import Tile
from constants import TILE_SIZE_IN_PIXELS
import pygame
from models.items.item_types import ItemType

WHEAT_SPRITES = [
    pygame.transform.scale(pygame.image.load('assets/graphics/wheat/wheat_0.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS)),
    pygame.transform.scale(pygame.image.load('assets/graphics/wheat/wheat_1.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS)),
    pygame.transform.scale(pygame.image.load('assets/graphics/wheat/wheat_2.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS)),
    pygame.transform.scale(pygame.image.load('assets/graphics/wheat/wheat_3.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS)),
    pygame.transform.scale(pygame.image.load('assets/graphics/wheat/wheat_4.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS)),
    pygame.transform.scale(pygame.image.load('assets/graphics/wheat/wheat_5.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS)),
    pygame.transform.scale(pygame.image.load('assets/graphics/wheat/wheat_6.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS)),

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
        self.wrong_ground_type = False
        # Goes to 1 over the course of growing
        self.growth_level = 0

        # Coole shit
        tile_below = self.world.get_tile_at_indices(self.x, self.y+1)
        self.growing_speed = 1
        if isinstance(tile_below, Dirt):
            self.growing_speed *= 0.001
        elif isinstance(tile_below, HalfLiterKlokkium):
            self.growing_speed *= 0.1
        else:
            self.growing_speed = 0
            self.wrong_ground_type = True

        depth = self.y - 20
        if depth > 100:
            self.growing_speed *= 0.01
        else:
            self.growing_speed *= (1-(depth / 100)) * (1 - 0.01) + 0.01

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

        if self.wrong_ground_type:
            self.world.destroy_tile(self)

        # If the wheat is ready: change the drop type
        if not self.ready and self.growth_level * len(WHEAT_SPRITES) > len(WHEAT_SPRITES) - 1:
            self.item_type = {
                ItemType.WHEAT: 1,
                ItemType.SEEDS: 2,
            }
            self.ready = True

