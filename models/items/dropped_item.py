import pygame

from constants import TILE_SIZE_IN_PIXELS, FRAME_RATE, DROPPED_ITEM_SIZE
from models.items.item_types import ItemType

DROPPED_ITEM_WIDTH, DROPPED_ITEM_HEIGHT = DROPPED_ITEM_SIZE, DROPPED_ITEM_SIZE
DROPPED_ITEM_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/dropped_items/test_item.png'), (DROPPED_ITEM_SIZE, DROPPED_ITEM_SIZE))


class DroppedItem(object):

    def __init__(self, game, item_type: ItemType, x, y):
        self.item_type = item_type
        self.game = game
        self.world = game.world
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0

    def step(self):

        # Calculate y position
        new_y = self.y + self.y_speed

        # Add gravity to fall speed
        self.y_speed += 9.81 / FRAME_RATE

        # x, y in tile positions
        new_tile_y = new_y // TILE_SIZE_IN_PIXELS

        # Tile corner (top left) Y (real) coordinates
        y_tile = new_tile_y * TILE_SIZE_IN_PIXELS

        if self.y_speed > 0:
            # Falling down, check the tile below the player on the new y
            # I use the new x here because it has already been validated and corrected above
            can_move_down = self.can_move_to_relative_tile_y(0, y=new_y + DROPPED_ITEM_SIZE)
            y_tile_bottom = ((new_y + DROPPED_ITEM_SIZE) // TILE_SIZE_IN_PIXELS) * TILE_SIZE_IN_PIXELS
            if not can_move_down:
                # Bounce back
                new_y = y_tile_bottom - DROPPED_ITEM_SIZE
                if self.y_speed < 1:
                    self.y_speed = 0
                else:
                    self.y_speed = -self.y_speed * 0.42

        elif self.y_speed < 0:
            # Moving up, same logic as moving left
            can_move_up = self.can_move_to_relative_tile_y(0, y=new_y)
            if not can_move_up:
                new_y = y_tile + TILE_SIZE_IN_PIXELS
                self.y_speed = 0

        self.y = new_y

    def draw(self, surface, camera_y):
        surface.blit(DROPPED_ITEM_SPRITE, (self.x, self.y - camera_y))

    def can_move_to_relative_tile_y(self, dy, x=None, y=None):
        """
        Checks whether the player can actually move dy tiles from the given x and y
        :param dy: Delta y. The difference in y position in tile coordinates
        :param x: If filled in this parameter overrides the default x = self.x
        :param y: If filled in this parameter overrides the default y = self.y
        :return: Whether the player can stand at this dy without colliding
        """
        if x is None:
            x = self.x

        if y is None:
            y = self.y

        tile_x, tile_y = x // TILE_SIZE_IN_PIXELS, y // TILE_SIZE_IN_PIXELS

        if x % TILE_SIZE_IN_PIXELS == 0:
            x_range = 1
        else:
            x_range = 2

        for dx in range(x_range):
            tile = self.world.get_tile_at_indices(int(tile_x + dx), int(tile_y + dy))
            if tile is None or tile.is_solid():
                return False
        return True

