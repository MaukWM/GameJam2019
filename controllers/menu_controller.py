import pygame
import sys
import time
from controllers import game_controller
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE, DEV_MODE


class MenuController(object):

    meme_mode = False
    rows_updated_per_frame = 2
    meteor_spawn_rate = 10

    title_1_surface = None
    title_2_surface = None
    meme_mode_text = None
    speed_setting_text = None
    speed_setting_slow = None
    speed_setting_medium = None
    speed_setting_fast = None
    speed_setting_value = None
    difficulty_text = None
    difficulty_easy = None
    difficulty_medium = None
    difficulty_hard = None
    difficulty_value = None
    start_text = None
    help_text = None
    help_enabled = False
    meme_mode_checkbox = pygame.transform.scale(pygame.image.load('assets/graphics/menu/unchecked.png'), (64, 64))

    MENU_ITEM_X = 520
    MENU_ITEM_WIDTH = 215
    MENU_ITEM_HEIGHT = 70

    MENU_ITEM_MEME_MODE_Y = 140

    MENU_ITEM_SPEED_Y = 220

    MENU_ITEM_DIFFICULTY_Y = 300

    MENU_ITEM_HELP_Y = 500
    MENU_ITEM_START_Y = 600

    def __init__(self):
        # setup stuff
        pygame.init()
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 60)
        if DEV_MODE:
            game_controller.GameController(self.window, self.meme_mode, self.rows_updated_per_frame, self.meteor_spawn_rate).run()
        self.setup()

    # Do all necessary setup
    def setup(self):
        # draws the title
        self.title_1_surface = self.title_font.render("METEOR DISASTER", False, (255, 255, 255))
        self.title_2_surface = self.title_font.render("MINER DELUXE!", False, (255, 255, 255))

        # meme mode checkbox
        self.meme_mode_text = self.title_font.render("meme mode", False, (255, 255, 255))

        # computer speed setting
        self.speed_setting_text = self.title_font.render("my computer is: ", False, (255, 255, 255))
        self.speed_setting_slow = self.title_font.render("slow", False, (0, 0, 255))
        self.speed_setting_medium = self.title_font.render("medium", False, (0, 0, 255))
        self.speed_setting_fast = self.title_font.render("fast", False, (0, 0, 255))
        self.speed_setting_value = self.speed_setting_medium

        # difficulty setting
        self.difficulty_text = self.title_font.render("difficulty: ", False, (255, 255, 255))
        self.difficulty_easy = self.title_font.render("easy peasy", False, (0, 0, 255))
        self.difficulty_medium = self.title_font.render("doable", False, (0, 0, 255))
        self.difficulty_hard = self.title_font.render("OH JEEZ", False, (0, 0, 255))
        self.difficulty_value = self.difficulty_medium


        # help
        self.help_text = self.title_font.render("HELP", False, (0, 255, 0))

        # start
        self.start_text = self.title_font.render("START!", False, (0, 255, 0))

    # handle a pressed key event in the context of the game root
    @staticmethod
    def handle_key_press(event_key):
        if event_key == pygame.K_ESCAPE:
            # end the program, close the window
            pygame.quit()
            sys.exit()

    def toggle_help_screen(self):
        self.help_enabled = not self.help_enabled
        # TODO: display help menu

    def toggle_meme_mode(self):
        self.meme_mode = not self.meme_mode
        if self.meme_mode:
            self.meme_mode_checkbox = pygame.transform.scale(pygame.image.load('assets/graphics/menu/checked.png'), (64, 64))

        else:
            self.meme_mode_checkbox = pygame.transform.scale(pygame.image.load('assets/graphics/menu/unchecked.png'), (64, 64))

    def toggle_speed_setting(self):
        if self.rows_updated_per_frame == 5:
            # toggle to medium
            self.rows_updated_per_frame = 10
            self.speed_setting_value = self.speed_setting_medium
        elif self.rows_updated_per_frame == 10:
            # toggle to fast
            self.rows_updated_per_frame = 20
            self.speed_setting_value = self.speed_setting_fast
        else: # current setting is fast
            # toggle to slow
            self.rows_updated_per_frame = 5
            self.speed_setting_value = self.speed_setting_slow

    def toggle_difficulty(self):
        if self.meteor_spawn_rate == 10:
            # toggle to medium
            self.meteor_spawn_rate = 50
            self.difficulty_value = self.difficulty_medium
        elif self.meteor_spawn_rate == 50:
            # toggle to hard
            self.meteor_spawn_rate = 100
            self.difficulty_value = self.difficulty_hard
        else: # current setting is hard
            # toggle to easy
            self.meteor_spawn_rate = 10
            self.difficulty_value = self.difficulty_easy

    def handle_mouse(self, event):
        if event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            x, y = int(mouse_pos[0]), int(mouse_pos[1])
            if 420 <= x <= 420+109:
                if self.MENU_ITEM_MEME_MODE_Y <= y <= self.MENU_ITEM_MEME_MODE_Y+109:
                    self.toggle_meme_mode()
            if 730 <= x <= 1280:
                if self.MENU_ITEM_SPEED_Y < y < self.MENU_ITEM_SPEED_Y + 100:
                    self.toggle_speed_setting()
            if 680 <= x <= 1280:
                if self.MENU_ITEM_DIFFICULTY_Y < y < self.MENU_ITEM_DIFFICULTY_Y + 100:
                    self.toggle_difficulty()
            # Check menu items
            if self.MENU_ITEM_X <= x <= self.MENU_ITEM_X + self.MENU_ITEM_WIDTH:
                # Start button
                if self.MENU_ITEM_START_Y <= y <= self.MENU_ITEM_START_Y + self.MENU_ITEM_HEIGHT:
                    game_controller.GameController(self.window, self.meme_mode, self.rows_updated_per_frame, self.meteor_spawn_rate).run()
                    self.setup()
                # Help button
                if self.MENU_ITEM_HELP_Y <= y <= self.MENU_ITEM_HELP_Y + self.MENU_ITEM_HEIGHT:
                    self.toggle_help_screen()

    # Handle all pygame events
    def handle_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.handle_key_press(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse(event)

    # Do all updates to the game state in this function
    def update_state(self):
        self.window.fill((133, 133, 133))

        self.window.blit(self.title_1_surface, (330, 10))
        self.window.blit(self.title_2_surface, (380, 70))

        # meme mode
        self.window.blit(self.meme_mode_checkbox, (420, self.MENU_ITEM_MEME_MODE_Y))
        self.window.blit(self.meme_mode_text, (490, self.MENU_ITEM_MEME_MODE_Y - 10))

        # speed setting
        speed_item_x = 300
        self.window.blit(self.speed_setting_text, (speed_item_x, self.MENU_ITEM_SPEED_Y))
        self.window.blit(self.speed_setting_value, (speed_item_x + 430, self.MENU_ITEM_SPEED_Y))

        # difficulty setting
        difficulty_item_x = 440
        self.window.blit(self.difficulty_text, (difficulty_item_x, self.MENU_ITEM_DIFFICULTY_Y))
        self.window.blit(self.difficulty_value, (difficulty_item_x + 240, self.MENU_ITEM_DIFFICULTY_Y))

        pygame.draw.rect(self.window, (0, 0, 0), (self.MENU_ITEM_X, self.MENU_ITEM_HELP_Y, self.MENU_ITEM_WIDTH, self.MENU_ITEM_HEIGHT))
        self.window.blit(self.help_text, (550, self.MENU_ITEM_HELP_Y))

        pygame.draw.rect(self.window, (0, 0, 0), (self.MENU_ITEM_X, self.MENU_ITEM_START_Y, self.MENU_ITEM_WIDTH, self.MENU_ITEM_HEIGHT))
        self.window.blit(self.start_text, (520, self.MENU_ITEM_START_Y))

    def run(self):
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
