import pygame

from constants import TILE_SIZE_IN_PIXELS, FRAME_RATE

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
            # Moving up
            can_move_up = self.can_move_to_relative_tile_y(0, x=new_x, y=new_y)
            if not can_move_up:
                new_y = y_tile + TILE_SIZE_IN_PIXELS
                self.y_speed = 0
        self.x, self.y = new_x, new_y

        # Realistic friction ;P
        self.x_speed = 0

    def draw(self, surface, camera_y):
        surface.blit(PLAYER_SPRITE, (self.x, self.y - camera_y))

    def can_move_to_relative_tile_x(self, dx, x=None, y=None):
        if x is None:
            x = self.x

        if y is None:
            y = self.y

        tile_x, tile_y = x // TILE_SIZE_IN_PIXELS, y // TILE_SIZE_IN_PIXELS

        if y % TILE_SIZE_IN_PIXELS == 0:
            y_range = 2
        else:
            y_range = 3

        print(y_range, )

        for dy in range(y_range):
            tile = self.world.get_tile_at_indices(int(tile_x + dx), int(tile_y + dy))
            print(tile)
            if tile is None or tile.is_solid():
                return False
        return True

    def can_move_to_relative_tile_y(self, dy, x=None, y=None):
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
