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
        if event_key == pygame.K_e:
            self.game.player.eat()

        if event_key == pygame.K_ESCAPE:
            # end the program, close the window
            pygame.quit()
            sys.exit()
        if event_key == pygame.K_u:
            if self.game.player.pickaxe.is_upgradeable():
                self.game.player.pickaxe.upgrade()

    def handle_key_held(self, event_key):

        if event_key == pygame.K_UP or event_key == pygame.K_w or event_key == pygame.K_SPACE:
            self.game.player.jump()

        elif event_key == pygame.K_LEFT or event_key == pygame.K_a:
            self.game.player.x_speed = -2

        elif event_key == pygame.K_RIGHT or event_key == pygame.K_d:
            self.game.player.x_speed = 2

        # Gravitate downwards if the players want to
        elif event_key == pygame.K_DOWN or event_key == pygame.K_s:
            if self.game.player.y_speed != 0:
                self.game.player.y_speed += 1

        elif event_key == pygame.K_1:
            self.game.player.change_item_selected(0)
        elif event_key == pygame.K_2:
            self.game.player.change_item_selected(1)
        elif event_key == pygame.K_3:
            self.game.player.change_item_selected(2)
        elif event_key == pygame.K_4:
            self.game.player.change_item_selected(3)
        elif event_key == pygame.K_5:
            self.game.player.change_item_selected(4)
        elif event_key == pygame.K_6:
            self.game.player.change_item_selected(5)
        elif event_key == pygame.K_7:
            self.game.player.change_item_selected(6)
        elif event_key == pygame.K_8:
            self.game.player.change_item_selected(7)
        elif event_key == pygame.K_9:
            self.game.player.change_item_selected(8)

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
                if event.button == 4 or event.button == 5:
                    self.handle_scroll(event.button)
                else:
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
            self.game.player.use_inventory_item()

    def handle_scroll(self, button):
        if button == 4:
            self.game.player.decrement_item_selected()
        elif button == 5:
            self.game.player.increment_item_selected()
