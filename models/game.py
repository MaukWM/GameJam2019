from models.player import Player
from models.world import World
from constants import TILE_SIZE_IN_PIXELS


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
        # Do game logic n stuff
        pass
