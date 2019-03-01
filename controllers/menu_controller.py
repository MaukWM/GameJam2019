import pygame
import sys
import time
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE


class MenuController(object):

    def __init__(self):
        # setup stuff
        pygame.init()
        window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 20)


    # Do all necessary setup
    def setup(self):
        pass



    # handle a pressed key event in the context of the game root
    def handle_key_press(self, event_key):
        if event_key == pygame.K_ESCAPE:
            # end the program, close the window
            pygame.quit()
            sys.exit()


    # Handle all pygame events
    def handle_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.handle_key_press(event.key)


    # Do all updates to the game state in this function
    def update_state(self):
        pass


    def run(self):
        self.setup()
        while True:
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
