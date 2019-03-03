import pygame
import time

import sys

from constants import DEV_MODE, SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE
from controllers import game_controller


class HelpController(object):
    MENU_ITEM_X = 520
    MENU_ITEM_WIDTH = 215
    MENU_ITEM_HEIGHT = 70

    MENU_ITEM_HELP_Y = 380
    MENU_ITEM_START_Y = 480

    def __init__(self, window):
        # setup stuff
        self.running = True
        self.window = window
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 60)
        self.setup()


    # Handle all pygame events
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse(event)

    def handle_mouse(self, event):
        if event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            x, y = int(mouse_pos[0]), int(mouse_pos[1])
            # Check menu items
            if self.MENU_ITEM_X <= x <= self.MENU_ITEM_X + self.MENU_ITEM_WIDTH:
                # Back button
                if self.MENU_ITEM_START_Y <= y <= self.MENU_ITEM_START_Y + self.MENU_ITEM_HEIGHT:
                    self.running = False


    # Do all updates to the game state in this function
    def update_state(self):
        self.window.fill((133, 133, 133))

        self.window.blit(self.title_1_surface, (250, 10))
        self.window.blit(self.title_2_surface, (250, 70))
        self.window.blit(self.title_3_surface, (250, 130))
        self.window.blit(self.title_4_surface, (250, 190))
        self.window.blit(self.title_5_surface, (250, 250))
        self.window.blit(self.title_6_surface, (250, 310))
        self.window.blit(self.title_7_surface, (250, 370))


        pygame.draw.rect(self.window, (0, 0, 0), (self.MENU_ITEM_X, self.MENU_ITEM_START_Y, self.MENU_ITEM_WIDTH, self.MENU_ITEM_HEIGHT))
        self.window.blit(self.start_text, (520, self.MENU_ITEM_START_Y))

    def setup(self):
        # draws the title
        self.title_1_surface = self.title_font.render("use a,d or ←,→ to move left and right", False, (255, 255, 255))
        self.title_2_surface = self.title_font.render("use w,↑ or space to jump", False, (255, 255, 255))
        self.title_3_surface = self.title_font.render("use left mouse to break blocks", False, (255, 255, 255))
        self.title_4_surface = self.title_font.render("use right mouse to place blocks", False, (255, 255, 255))
        self.title_5_surface = self.title_font.render("    with shift to place support beams", False, (255, 255, 255))
        self.title_6_surface = self.title_font.render("use u to upgrade your pickaxe", False, (255, 255, 255))
        self.title_7_surface = self.title_font.render("use e to eat", False, (255, 255, 255))

        # back
        self.start_text = self.title_font.render("BACK", False, (0, 255, 0))

    def run(self):
        while self.running:
            start_time = time.clock()

            # handle pygame events from the queue
            self.handle_events()
            # update the state of the game
            self.update_state()

            # possibly delay program execution to ensure steady frame rate
            running_time = time.clock() - start_time
            if running_time < 1/FRAME_RATE:
                time.sleep((1/FRAME_RATE) - running_time)

            pygame.display.update()