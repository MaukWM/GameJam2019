import pygame
import sys
import time
from controllers import game_controller
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE, DEV_MODE


class MenuController(object):

    meme_mode = False
    title_1_surface = None
    title_2_surface = None
    meme_mode_text = None
    start_text = None
    meme_mode_checkbox = pygame.image.load('assets/graphics/menu/unchecked.png')

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
            # draws the title
            self.title_1_surface = self.title_font.render("METEOR DISASTER", False, (255, 255, 255))
            self.title_2_surface = self.title_font.render("MINER DELUXE!", False, (255, 255, 255))

            # meme mode checkbox
            self.meme_mode_text = self.title_font.render("meme mode", False, (255, 255, 255))

            # start
            self.start_text = self.title_font.render("START!", False, (0, 255, 0))
        else:
            game_controller.GameController(self.window, self.meme_mode).run()


    # handle a pressed key event in the context of the game root
    def handle_key_press(self, event_key):
        if event_key == pygame.K_ESCAPE:
            # end the program, close the window
            pygame.quit()
            sys.exit()

    def toggle_meme_mode(self):
        self.meme_mode = not self.meme_mode
        if self.meme_mode:
            self.meme_mode_checkbox = pygame.image.load('assets/graphics/menu/checked.png')

        else:
            self.meme_mode_checkbox = pygame.image.load('assets/graphics/menu/unchecked.png')
            self.window.blit(self.meme_mode_checkbox, (420, 180))

    def handle_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        x, y = int(mouse_pos[0]), int(mouse_pos[1])
        if 420 <= x <= 420+109:
            if 180 <= y <= 180+109:
                self.toggle_meme_mode()
        # 520, 480, 210, 70
        if 520 <= x <= 520+210:
            if 480 <= y <= 480+70:
                game_controller.GameController(self.window, self.meme_mode).run()

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
        self.window.fill((133, 133, 133))

        self.window.blit(self.title_1_surface, (330, 10))
        self.window.blit(self.title_2_surface, (380, 70))

        self.window.blit(self.meme_mode_checkbox, (420, 180))
        self.window.blit(self.meme_mode_text, (550, 200))

        self.window.blit(self.meme_mode_checkbox, (420, 180))

        pygame.draw.rect(self.window, (0, 0, 0), (520, 480, 210, 70))
        self.window.blit(self.start_text, (520, 480))


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
