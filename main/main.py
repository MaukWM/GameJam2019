import pygame

from controllers.game_controller import GameController
from controllers.menu_controller import MenuController
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.font.init()

    # TODO: This should *eventually* be uncommented
    # menu_controller = MenuController()
    game_controller = GameController(window)
    game_controller.run()


