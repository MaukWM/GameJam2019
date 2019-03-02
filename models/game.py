from models.player import Player
from models.world import World
from constants import TILE_SIZE_IN_PIXELS, SCREEN_WIDTH
from models.meteor import Meteor, NotOnScreenError
import random
import models.world
import models.tiles.air_tile


class Game(object):

    # todo: fix circular dependency and put in constants.py
    METEOR_SPAWN_RATE = 10

    def __init__(self, width, height):
        self.world = World(width, height)

        # Iets wat niet een blokje of player is is een entity:
        self.entities = []
        self.player = Player(10, 20)

    def draw(self, surface):
        camera_y = int(self.player.y/TILE_SIZE_IN_PIXELS)*TILE_SIZE_IN_PIXELS

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
                        if entity.is_colliding(models.world.DIRT_START, TILE_SIZE_IN_PIXELS, self.world.tile_matrix):
                            self.entities.remove(entity)
                    except NotOnScreenError:
                        self.entities.remove(entity)

        # time to maybe spawn a meteor
        if random.randint(0, 1000) > 1000 - self.METEOR_SPAWN_RATE:
            self.entities.append(Meteor(random.randint(0, SCREEN_WIDTH), random.randint(50, 500) / 100))
