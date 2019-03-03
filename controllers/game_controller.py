import pygame
import sys
import time
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE, TILE_SIZE_IN_PIXELS
from models.game import Game


class GameController(object):

    def __init__(self, window, memes_enabled):
        # setup stuff
        self.game = Game(SCREEN_WIDTH//TILE_SIZE_IN_PIXELS, 512, memes_enabled)
        self.window = window
        self.held_keys = set()
        self.held_mouse_buttons = set()

    # Do all necessary setup
    def setup(self):
        pass

    # handle a pressed key event in the context of the game root
    def handle_key_press(self, event_key):
        if event_key == pygame.K_ESCAPE:
            # end the program, close the window
            pygame.quit()
            sys.exit()
        if event_key == pygame.K_u:
            if self.game.player.pickaxe.is_upgradeable():
                self.game.player.pickaxe.upgrade()

    def handle_key_held(self, event_key):

        # TODO: REMOVE THESE HACKS
        if event_key == pygame.K_UP:
            self.game.player.jump()

        # TODO: REMOVE THESE HACKS
        if event_key == pygame.K_LEFT:
            self.game.player.x_speed = -2

        # TODO: REMOVE THESE HACKS
        if event_key == pygame.K_RIGHT:
            self.game.player.x_speed = 2

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.held_mouse_buttons.add(event.button)

            if event.type == pygame.MOUSEBUTTONUP and event.button in self.held_mouse_buttons:
                self.held_mouse_buttons.remove(event.button)

        for key in self.held_keys:
            self.handle_key_held(key)

        for button in self.held_mouse_buttons:
            self.handle_button_held(button)


    # Do all updates to the game state in this function
    def update_state(self):
        self.game.step()
        self.game.player.update_selected_tile(pygame.mouse.get_pos())

    def draw(self):
        self.game.draw(self.window)

    def run(self):
        self.setup()
        while not self.game.game_over:
            start_time = time.clock()

            # handle pygame events from the queue
            self.handle_events()
            # update the state of the game
            self.update_state()

            self.window.fill((70, 70, 150))

            self.draw()

            # possibly delay program execution to ensure steady frame rate
            running_time = time.clock() - start_time
            if running_time < 1 / FRAME_RATE:
                time.sleep((1 / FRAME_RATE) - running_time)

            pygame.display.update()

    def handle_button_held(self, button):

        if button == 1:
            # LMB
            self.game.player.mine()

        if button == 3:
            # RMB
            pass
