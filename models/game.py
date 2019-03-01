from models.player import Player
from models.world import World
from constants import TILE_SIZE_IN_PIXELS, SCREEN_WIDTH
from models.meteor import Meteor
import random


class Game(object):
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
                # todo: collision detection
                if entity.y > 1000:
                    self.entities.remove(entity)

        # time to maybe spawn a meteor
        if random.randint(0, 1000) > 990:
            self.entities.append(Meteor(random.randint(0, SCREEN_WIDTH), random.randint(50, 500) / 100))