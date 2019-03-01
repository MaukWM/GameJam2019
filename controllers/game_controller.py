import pygame
import sys
import time
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE, TILE_SIZE_IN_PIXELS
from models.game import Game


class GameController(object):
    def __init__(self, window):
        # setup stuff
        self.game = Game(SCREEN_WIDTH//TILE_SIZE_IN_PIXELS, 128)
        self.window = window
        self.held_keys = set()

    # Do all necessary setup
    def setup(self):
        pass

    # handle a pressed key event in the context of the game root
    def handle_key_press(self, event_key):
        if event_key == pygame.K_ESCAPE:
            # end the program, close the window
            pygame.quit()
            sys.exit()

    def handle_key_held(self, event_key):

        # TODO: REMOVE THESE HACKS
        if event_key == pygame.K_DOWN:
            self.game.player.y += 60

        # TODO: REMOVE THESE HACKS
        if event_key == pygame.K_UP:
            self.game.player.y -= 60

    # Handle all pygame events
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.handle_key_press(event.key)
                self.held_keys.add(event.key)

            if event.type == pygame.KEYUP:
                self.held_keys.remove(event.key)

        for key in self.held_keys:
            self.handle_key_held(key)


    # Do all updates to the game state in this function
    def update_state(self):
        self.game.step()

    def draw(self):
        self.game.draw(self.window)

    def run(self):
        self.setup()
        while True:
            start_time = time.clock()

            # handle pygame events from the queue
            self.handle_events()
            # update the state of the game
            self.update_state()

            self.window.fill((0, 0, 0))

            self.draw()

            # possibly delay program execution to ensure steady frame rate
            running_time = time.clock() - start_time
            if running_time < 1 / FRAME_RATE:
                time.sleep((1 / FRAME_RATE) - running_time)

            pygame.display.update()