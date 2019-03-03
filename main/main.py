import pygame
from tkinter.simpledialog import askstring
import tkinter

from controllers.menu_controller import MenuController
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


if __name__ == "__main__":

    root = tkinter.Tk()
    name = askstring("Name", "What's your name?")
    root.withdraw()

    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.font.init()

    menu_controller = MenuController(name)
    menu_controller.run()

