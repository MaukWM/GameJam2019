import math

import pygame

from constants import TILE_SIZE_IN_PIXELS, FRAME_RATE, SCREEN_HEIGHT

PLAYER_WIDTH, PLAYER_HEIGHT = TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS*2
PLAYER_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/player.png'), (TILE_SIZE_IN_PIXELS, TILE_SIZE_IN_PIXELS*2))


class Player(object):
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0
        self.can_jump = True
        self.selected_tile = None

    def step(self):

        # Calculate new x an y positions
        new_x, new_y = self.x + self.x_speed, self.y + self.y_speed

        # Add gravity to fall speed
        self.y_speed += 9.81 / FRAME_RATE

        # x, y in tile positions
        new_tile_x, new_tile_y = new_x // TILE_SIZE_IN_PIXELS, new_y // TILE_SIZE_IN_PIXELS

        # Tile corner (top left) X/Y (real) coordinates
        x_tile, y_tile = new_tile_x * TILE_SIZE_IN_PIXELS, new_tile_y * TILE_SIZE_IN_PIXELS

        if self.x_speed > 0:
            # We're moving right
            # Check if we can move further right in the tile we're in at the new timestep
            # The y-position is kept at the old value for now, since it has not been validated yet
            can_move_right = self.can_move_to_relative_tile_x(1, x=new_x, y=self.y)
            if not can_move_right:
                # If we can't, keep the player at the edge of the tile we're in at the new timestep
                new_x = x_tile
                self.x_speed = 0

        elif self.x_speed < 0:
            # Do the same if we're moving left.
            # Due to the fact that player x/y is in the top left,
            #   we check the new block we're entering instead of the one left of it
            can_move_left = self.can_move_to_relative_tile_x(0, x=new_x, y=self.y)
            if not can_move_left:
                # If the new x is in a tile, move us back to the tile to the right
                new_x = x_tile + TILE_SIZE_IN_PIXELS
                self.x_speed = 0

        if self.y_speed > 0:
            # Falling down, check the tile below the player on the new x and y
            # I use the new x here because it has already been validated and corrected above
            can_move_down = self.can_move_to_relative_tile_y(2, x=new_x, y=new_y)
            if not can_move_down:
                # Reset jump
                self.can_jump = True
                new_y = y_tile
                self.y_speed = 0
        elif self.y_speed < 0:
            # Moving up, same logic as moving left
            can_move_up = self.can_move_to_relative_tile_y(0, x=new_x, y=new_y)
            if not can_move_up:
                new_y = y_tile + TILE_SIZE_IN_PIXELS
                self.y_speed = 0
        self.x, self.y = new_x, new_y

        # Realistic friction ;P
        self.x_speed *= 0.8

    def draw(self, surface, camera_y):
        surface.blit(PLAYER_SPRITE, (self.x, self.y - camera_y))
        if self.selected_tile is not None:
            rect = (
                self.selected_tile.x * TILE_SIZE_IN_PIXELS,
                self.selected_tile.y * TILE_SIZE_IN_PIXELS - camera_y,
                TILE_SIZE_IN_PIXELS,
                TILE_SIZE_IN_PIXELS,
            )
            pygame.draw.rect(surface, (255, 0, 0), rect, 3)

    def can_move_to_relative_tile_x(self, dx, x=None, y=None):
        """
        Checks whether the player can actually move dx tiles from the given x and y
        :param dx: Delta x. The difference in x position in tile coordinates
        :param x: If filled in this parameter overrides the default x = self.x
        :param y: If filled in this parameter overrides the default y = self.y
        :return: Whether the player can stand at this dx without colliding
        """
        if x is None:
            x = self.x

        if y is None:
            y = self.y

        tile_x, tile_y = x // TILE_SIZE_IN_PIXELS, y // TILE_SIZE_IN_PIXELS

        # If we're exactly on a tile border, check 2 neighbouring tiles, else check 3
        if y % TILE_SIZE_IN_PIXELS == 0:
            y_range = 2
        else:
            y_range = 3

        # Check the tiles on all checked delta y
        for dy in range(y_range):
            tile = self.world.get_tile_at_indices(int(tile_x + dx), int(tile_y + dy))
            if tile is None or tile.is_solid():
                # We cannot pass through the map borders or solid blocks
                return False
        # If we didn't encounter anything holding us back, we can move to this dx
        return True

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

    def jump(self):
        if self.can_jump:
            self.can_jump = False
            self.y_speed -= 6.0

    def find_selected_tile(self, mouse_x, mouse_y, select_solids=True):
        dx = mouse_x - self.x
        dy = mouse_y - SCREEN_HEIGHT//2

        distance_to_mouse = (dx**2 + dy**2)**0.5

        dx_norm = dx/distance_to_mouse
        dy_norm = dy/distance_to_mouse

        dx_sign = 1 if dx_norm >= 0 else -1
        dy_sign = 1 if dy_norm >= 0 else -1

        dx_abs, dy_abs = dx_norm/dx_sign, dy_norm/dy_sign
        angle_top_right = math.atan2(dx_abs, dy_abs)

        # The next code will determine what block we aim at, with angles normalized to top-right.
        # This can be rotated later if we're not looking to the top-left in mathematical x/y space

        looking_at_top = False
        looking_at_right = False
        looking_at_diagonal = False

        if angle_top_right < math.pi/4:
            looking_at_top = True
        else:
            looking_at_right = True

        if math.pi * 2/6 > dx_abs > math.pi/6:
            looking_at_diagonal = True

        print(looking_at_top, looking_at_diagonal, looking_at_right)

        tile_x, tile_y = self.x // TILE_SIZE_IN_PIXELS, self.y // TILE_SIZE_IN_PIXELS
        if self.x % TILE_SIZE_IN_PIXELS != 0 and dx_sign == 1:
            tile_x += 1

        if dy_sign == 1:
            tile_y += 1

        if looking_at_top:
            tile_y += dy_sign
        else:
            tile_x += dx_sign

        tile = self.world.get_tile_at_indices(tile_x, tile_y)
        if tile is None:
            return None

        if (tile.is_solid() and select_solids) or (not tile.is_solid() and not select_solids):
            return tile

        if looking_at_diagonal:
            if looking_at_top:
                tile_x += dx_sign
            else:
                tile_y += dy_sign

            tile = self.world.get_tile_at_indices(tile_x, tile_y)
            if tile is None:
                return None

            if (tile.is_solid() and select_solids) or (not tile.is_solid() and not select_solids):
                return tile
            else:
                return None
        return None

    def set_selected_tile(self, tile):
        self.selected_tile = tile

    def update_selected_tile(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        self.set_selected_tile(self.find_selected_tile(mouse_x, mouse_y))