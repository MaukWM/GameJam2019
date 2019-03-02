import pygame
import sys
import time
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE, DEV_MODE


class MenuController(object):

    meme_mode = False

    def __init__(self):
        # setup stuff
        pygame.init()
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 60)

    # Do all necessary setup
    def setup(self):
        if not DEV_MODE:
            self.window.fill((133, 133, 133))

            # draws the title
            title_1_surface = self.title_font.render("METEOR DISASTER", False, (255, 255, 255))
            title_2_surface = self.title_font.render("MINER DELUXE!", False, (255, 255, 255))
            self.window.blit(title_1_surface, (330, 10))
            self.window.blit(title_2_surface, (380, 70))

            # meme mode checkbox
            meme_mode_checkbox = pygame.image.load('assets/graphics/menu/unchecked.png')
            meme_mode_text = self.title_font.render("meme mode", False, (255, 255, 255))
            self.window.blit(meme_mode_checkbox, (420, 180))
            self.window.blit(meme_mode_text, (550, 200))

    # handle a pressed key event in the context of the game root
    def handle_key_press(self, event_key):
        if event_key == pygame.K_ESCAPE:
            # end the program, close the window
            pygame.quit()
            sys.exit()

    def toggle_meme_mode(self):


    def handle_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        x, y = int(mouse_pos[0]), int(mouse_pos[1])
        if 420 <= x <= 420+109:
            if 180 <= y <= 180+109:
                self.toggle_meme_mode()

    # Handle all pygame events
    def handle_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.handle_key_press(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse()


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
