from models.player import Player
from models.world import World
from constants import TILE_SIZE_IN_PIXELS, SCREEN_WIDTH, SCREEN_HEIGHT
from models.meteor import Meteor, NotOnScreenError
from models.explosion import Explosion
import random
import models.world
import models.tiles.air_tile
from models.items.dropped_item import DroppedItem
from models.items.item_types import ItemType


class Game(object):

    # todo: fix circular dependency and put in constants.py
    METEOR_SPAWN_RATE = 10

    def __init__(self, width, height):
        self.world = World(width, height)

        # Iets wat niet een blokje of player is is een entity:
        self.entities = []
        self.player = Player(self, 10, 20)
        # Uncomment to test item drops :D
        # self.entities.append(DroppedItem(self, ItemType.JELTSIUM, 400, 20))

    def draw(self, surface):

        # The camera follows the player:

        # Uncomment this if you want the camera to move on the grid
        # camera_y = int((self.player.y + -SCREEN_HEIGHT//2)/TILE_SIZE_IN_PIXELS)*TILE_SIZE_IN_PIXELS

        # Uncomment this if you want the camera to follow the player without regard for the grid
        camera_y = int(self.player.y - SCREEN_HEIGHT // 2)

        self.world.draw(surface, camera_y)
        self.player.draw(surface, camera_y)
        for entity in self.entities:
            entity.draw(surface, camera_y)

    def step(self):
        for entity in self.entities:
            entity.step()
            if type(entity) is Meteor:
                if entity.y >= models.world.DIRT_START * TILE_SIZE_IN_PIXELS:
                    # this meteor is below DIRT_START, Check collision
                    try:
                        if entity.is_colliding(TILE_SIZE_IN_PIXELS, self.world.tile_matrix):
                            self.entities.append(Explosion(entity.x, entity.y))
                            self.entities.remove(entity)
                    except NotOnScreenError:
                        self.entities.remove(entity)
            if type(entity) is Explosion:
                if entity.frame_counter >= 48:
                    self.entities.remove(entity)

        # time to maybe spawn a meteor
        if random.randint(0, 1000) > 1000 - self.METEOR_SPAWN_RATE:
            self.entities.append(Meteor(random.randint(0, SCREEN_WIDTH), random.randint(50, 500) / 100))

        self.player.step()
