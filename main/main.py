import pygame

from controllers.menu_controller import MenuController
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.font.init()

    menu_controller = MenuController()
    menu_controller.run()

