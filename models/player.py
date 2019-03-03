import math
import pygame

from models.items.inventory import Inventory
from constants import TILE_SIZE_IN_PIXELS, FRAME_RATE, SCREEN_HEIGHT
from models.items.dropped_item import DroppedItem
from models.items.dropped_item import DROPPED_ITEM_HEIGHT, DROPPED_ITEM_WIDTH
from models.meteor import Meteor
from models.explosion import Explosion
from models.healthbar import HealthBar
from models.tiles.air_tile import Air
from models.tiles.dirt_tile import Dirt
from models.tiles.half_liter_klokkium_tile import HalfLiterKlokkium
from models.tiles.jeltisium_tile import Jeltisnium
from models.tiles.leninium_tile import Leninium
from models.tiles.marxinium_tile import Marxinium
from models.tiles.nokia_phonium_tile import NokiaPhonium
from models.tiles.stone_tile import Stone
from models.world import DIRT_START
from models.pickaxe import Pickaxe
from models.items.item_types import PATHS, ItemType  # TODO: Add meme path

PLAYER_WIDTH, PLAYER_HEIGHT = 28, 60
PLAYER_SPRITE = pygame.transform.scale(pygame.image.load('assets/graphics/player.png'),
                                       (PLAYER_WIDTH, PLAYER_HEIGHT))

DIFFERENT_ITEM_NUMBER = 7


class Player(object):

    def __init__(self, game, x, y, memes_enabled):
        self.game = game
        self.world = game.world
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0
        self.highest_reached_y = DIRT_START - 2  # -2 because then it works properly
        self.can_jump = True
        self.selected_tile = None
        self.inventory = Inventory(memes_enabled)
        self.health_bar = HealthBar()
        self.selected_inventory_item = 0
        self.pickaxe = Pickaxe(self)
        self.font = pygame.font.SysFont("Arial", 30, True)
        self.shifts = False

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
            can_move_right = self.can_move_to_relative_tile_x(0, x=new_x + PLAYER_WIDTH, y=self.y)

            # Compute the tile index of the tile containing the right side of the player
            x_tile_right = ((new_x + PLAYER_WIDTH) // TILE_SIZE_IN_PIXELS)*TILE_SIZE_IN_PIXELS
            if not can_move_right:
                # If we can't, keep the player at the edge of the tile we're in at the new timestep
                new_x = x_tile_right - PLAYER_WIDTH
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
            can_move_down = self.can_move_to_relative_tile_y(0, x=new_x, y=new_y + PLAYER_HEIGHT)

            # Compute the tile index of the tile containing the bottom side of the player
            y_tile_bottom = ((new_y + PLAYER_HEIGHT) // TILE_SIZE_IN_PIXELS)*TILE_SIZE_IN_PIXELS
            if not can_move_down:
                # Reset jump
                self.can_jump = True
                new_y = y_tile_bottom - PLAYER_HEIGHT
                if self.y_speed < 1:
                    self.y_speed = 0
                else:
                    self.y_speed = -self.y_speed * 0.15
        elif self.y_speed < 0:
            # Moving up, same logic as moving left
            can_move_up = self.can_move_to_relative_tile_y(0, x=new_x, y=new_y)
            if not can_move_up:
                new_y = y_tile + TILE_SIZE_IN_PIXELS
                self.y_speed = 0
        self.x, self.y = new_x, new_y

        if new_tile_y > self.highest_reached_y:
            difference = new_tile_y - self.highest_reached_y
            self.highest_reached_y = new_tile_y
            self.game.add_depth_score(difference)

        # Check for collisions with items and meteorites
        self.check_entity_collisions()

        # Realistic friction ;P
        self.x_speed *= 0.8

    def check_entity_collisions(self):
        for entity in self.game.entities:
            if (self.x - entity.x) < 4 and (self.y - entity.y) < 4:
                if isinstance(entity, DroppedItem) or isinstance(entity, Meteor):
                    self.check_entity_collision(entity)

    def check_entity_collision(self, entity):
        player_box = (self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)
        if isinstance(entity, DroppedItem):
            entity_box = (entity.x, entity.y, DROPPED_ITEM_WIDTH, DROPPED_ITEM_HEIGHT)
            if self.check_overlap(player_box, entity_box):
                self.consume_item(entity)
                return True
            return False
        elif isinstance(entity, Meteor):
            entity_box = (entity.x, entity.y, entity.width, entity.height)
            if self.check_overlap(player_box, entity_box):

                # handle impact from meteor with player
                self.game.entities.append(Explosion(entity.x, entity.y, entity.width))
                self.health_bar.take_damage(entity.size * 30)
                self.game.entities.remove(entity)
                if self.health_bar.health <= 0:
                    self.game.game_over = True
                return True
            return False

    @staticmethod
    def check_overlap(box1, box2):
        if box1[0] > (box2[0] + box2[2]) or (box1[0] + box1[2]) < box2[0]:
            return False
        if box1[1] > (box2[1] + box2[3]) or (box1[1] + box1[3]) < box2[1]:
            return False
        return True

    def consume_item(self, entity: DroppedItem):
        self.game.player.inventory.increment_item_amount(entity.item_type)
        self.game.add_resource_score(entity.item_type)
        self.game.entities.remove(entity)

    def draw(self, surface, camera_y):
        surface.blit(PLAYER_SPRITE, (self.x, self.y - camera_y))
        self.inventory.draw(surface, self.selected_inventory_item)
        self.health_bar.draw(surface)
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

        # Compute the number of tiles that the player spans over the x-axis
        # The small offset is added to avoid one-off errors. I'm vewy sowwy UwU - Gewwyfwap
        y_range = int((y + PLAYER_HEIGHT - 1e-5)//TILE_SIZE_IN_PIXELS - tile_y)
        y_range += 1


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

        # Compute the number of tiles that the player spans over the x-axis
        # The small offset is added to avoid one-off errors. I'm vewy sowwy UwU - Gewwyfwap
        x_range = int((x + PLAYER_WIDTH - 1e-5)//TILE_SIZE_IN_PIXELS - tile_x)
        x_range += 1

        for dx in range(x_range):
            tile = self.world.get_tile_at_indices(int(tile_x + dx), int(tile_y + dy))
            if tile is None or tile.is_solid():
                return False
        return True

    def jump(self):
        if self.can_jump:
            self.can_jump = False
            self.y_speed -= 6.0

    def find_selected_tile(self, mouse_x, mouse_y):
        """
        Finds the selected tile (with the mouse) and returns it if it's close enough
        :param mouse_x: The x-position of the mouse on the screen
        :param mouse_y: The y-position of the mouse on the screen
        :return: A tile if there's a close enough tile there, otherwise None
        """
        camera_y = int(self.y - SCREEN_HEIGHT // 2)
        x, y = mouse_x, mouse_y + camera_y
        tile_x, tile_y = x//TILE_SIZE_IN_PIXELS, y//TILE_SIZE_IN_PIXELS

        ptile_x_left, ptile_y_top = self.x//TILE_SIZE_IN_PIXELS, self.y//TILE_SIZE_IN_PIXELS
        ptile_x_right, ptile_y_bot = (self.x + PLAYER_WIDTH-0.01)//TILE_SIZE_IN_PIXELS, (self.y + PLAYER_HEIGHT - 0.01)//TILE_SIZE_IN_PIXELS

        dist_x_1 = abs(ptile_x_left - tile_x)
        dist_x_2 = abs(ptile_x_right - tile_x)
        dist_y_1 = abs(ptile_y_bot - tile_y)
        dist_y_2 = abs(ptile_y_top - tile_y)

        if (min(dist_x_1, dist_x_2) == 1 and max(dist_y_1, dist_y_2) <= 2) or \
                (min(dist_y_1, dist_y_2) == 1 and max(dist_x_1, dist_x_2) <= 1):
            return self.world.get_tile_at_indices(tile_x, tile_y)
        else:
            return None

    def set_selected_tile(self, tile):
        self.selected_tile = tile

    def update_selected_tile(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        self.set_selected_tile(self.find_selected_tile(mouse_x, mouse_y))

    def mine(self):
        if self.selected_tile is not None and self.selected_tile.is_solid():
            destroyed = self.selected_tile.damage(self.pickaxe.strength)
            if destroyed:
                self.drop_item(self.selected_tile)
                self.world.destroy_tile(self.selected_tile)

    def drop_item(self, tile):
        x_tile, y_tile = tile.x * TILE_SIZE_IN_PIXELS, tile.y * TILE_SIZE_IN_PIXELS
        self.game.entities.append(DroppedItem(self.game, tile.item_type, x_tile, y_tile, meme_mode=self.game.memes_enabled))

    #kan gebruikt worden als je een scrollwheel gebruikt
    def increment_item_selected(self, bool):
        if bool:
            self.change_item_selected(self.selected_inventory_item + 1)
        else:
            self.change_item_selected(self.selected_inventory_item + 1)

    def change_item_selected(self, number):
        self.selected_inventory_item = number % DIFFERENT_ITEM_NUMBER

    map_inventory_to_placeable = {0:True,
                                 1:True,
                                 2:True,
                                 3:True,
                                 4:True,
                                 5:True,
                                 6:True,
                                 }

    map_inventory_to_consturcter = {0:lambda x,y,world,solid : Dirt(world,x,y,False, solid),
                                    1:lambda x,y,world,solid : Stone(world,x,y, solid),
                                    2:lambda x,y,world,solid : Jeltisnium(world,x,y, False, solid),
                                    3:lambda x,y,world,solid : Leninium(world,x,y, False, solid),
                                    4:lambda x,y,world,solid : Marxinium(world,x,y, False, solid),
                                    5:lambda x,y,world,solid : NokiaPhonium(world,x,y, False, solid),
                                    6:lambda x,y,world,solid : HalfLiterKlokkium(world,x,y, False, solid),
                                  }

    def use_inventory_item(self):
        if self.map_inventory_to_placeable[self.selected_inventory_item]:
            if isinstance(self.selected_tile, Air):
                if self.inventory.inventory[ItemType(self.selected_inventory_item + 1)].amount > 0:
                    self.inventory.inventory[ItemType(self.selected_inventory_item + 1)].amount -= 1
                    x = self.selected_tile.x
                    y = self.selected_tile.y
                    block = self.map_inventory_to_consturcter[self.selected_inventory_item](x, y, self.world, not self.shifts)
                    if block is not None:
                        self.world.tile_matrix[x][y] = block
