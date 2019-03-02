from models.player import Player
from models.world import World
from constants import TILE_SIZE_IN_PIXELS, SCREEN_HEIGHT


class Game(object):
    def __init__(self, width, height):
        self.world = World(width, height)

        # Iets wat niet een blokje of player is is een entity:
        self.entities = []
        self.player = Player(self.world, 10, 20)

    def draw(self, surface):

        # The camera follows the player:

        # Uncomment this if you want the camera to move on the grid
        # camera_y = int((self.player.y + -SCREEN_HEIGHT//2)/TILE_SIZE_IN_PIXELS)*TILE_SIZE_IN_PIXELS

        # Uncomment this if you want the camera to follow the player without regard for the grid
        camera_y = int(self.player.y + -SCREEN_HEIGHT // 2)

        self.world.draw(surface, camera_y)
        self.player.draw(surface, camera_y)
        for entity in self.entities:
            entity.draw(surface, camera_y)

    def step(self):
        # Do game logic n stuff
        self.player.step()
