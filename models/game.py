from models.player import Player
from models.world import World
from constants import TILE_SIZE_IN_PIXELS, SCREEN_WIDTH, SCREEN_HEIGHT
from models.meteor import Meteor, NotOnScreenError
from models.explosion import Explosion
import random
import models.world
import models.tiles.air_tile
from models.items.item_types import ItemType
from models.items.item_types import SCORES, NAMES
import pygame


class Game(object):

    # todo: fix circular dependency and put in constants.py
    POINTS_PER_DEPTH = 100
    SCORE_TO_BE_ADDED_INCREMENTS_MINIMUM = 4

    def __init__(self, width, height, memes_enabled, rows_updated_per_frame, meteor_spawn_rate, name):
        self.score: int = 0
        self.meteor_spawn_rate = meteor_spawn_rate
        self.meteor_damage_multiplier = 1
        self.difficulty_factor = 0
        self.determine_score_factor(meteor_spawn_rate)
        self.score_to_be_added: int = 0
        self.world = World(width, height, rows_updated_per_frame)
        self.base_font = pygame.font.SysFont("Arial", 18)
        self.pickaxe_font = pygame.font.SysFont("Arial", 12)
        self.memes_enabled = memes_enabled

        # Iets wat niet een blokje of player is is een entity:
        self.entities = []
        self.player = Player(self, 10, 300, memes_enabled)
        self.game_over = False
        self.name = name

    def determine_score_factor(self, meteor_spawn_rate):
        self.difficulty_factor = (meteor_spawn_rate / 200)

    def draw(self, surface):

        # The camera follows the player:

        # Uncomment this if you want the camera to move on the grid
        # camera_y = int((self.player.y + -SCREEN_HEIGHT//2)/TILE_SIZE_IN_PIXELS)*TILE_SIZE_IN_PIXELS

        # Uncomment this if you want the camera to follow the player without regard for the grid
        camera_y = int(self.player.y - SCREEN_HEIGHT // 2)

        self.world.draw(surface, camera_y)
        self.player.draw(surface, camera_y)
        for entity in self.entities:
            entity.draw(surface, camera_y)

        msg_surface = self.base_font.render("Score: " + str(int(self.score)), True, (255, 255, 255))
        surface.blit(msg_surface, ((SCREEN_WIDTH // 2) - (msg_surface.get_width() // 2), SCREEN_HEIGHT // 50))

        # Check if we can upgrade the players pickaxe, if we can tell the player
        pickaxe_ui_text_base = "Pickaxe: " + str(NAMES[self.player.pickaxe.material]) + ". "
        if self.player.pickaxe.is_upgradeable():
            pickaxe_ui_text_base += " Press U to upgrade pickaxe!"
        pickaxe_ui_surface = self.pickaxe_font.render(pickaxe_ui_text_base, True, (255, 255, 255))
        surface.blit(pickaxe_ui_surface, ((SCREEN_WIDTH // 50), SCREEN_HEIGHT // 70))

    def add_resource_score(self, entity: ItemType):
        self.score_to_be_added += SCORES[entity] * self.difficulty_factor

    def add_depth_score(self, difference):
        """
        Add points for each level the player went deeper
        :param difference: The difference between the previously lowest reached level and the players current level
        :return: Nada
        """
        self.score_to_be_added += self.POINTS_PER_DEPTH * difference * self.difficulty_factor

    def step(self):
        # Increase meteor damage and spawn rate according to difficulty at the start
        self.meteor_spawn_rate += 0.015 * self.difficulty_factor
        self.meteor_damage_multiplier += 0.0005 * self.difficulty_factor
        self.world.step()
        # Dynamically add score
        if self.score_to_be_added > 0:
            score_to_be_added_part = self.score_to_be_added // 100  # Divide amount of points to add by 100 and add that
            if score_to_be_added_part < Game.SCORE_TO_BE_ADDED_INCREMENTS_MINIMUM:
                if self.score_to_be_added < Game.SCORE_TO_BE_ADDED_INCREMENTS_MINIMUM:
                    self.score += self.score_to_be_added
                    self.score_to_be_added = 0
                else:
                    self.score += Game.SCORE_TO_BE_ADDED_INCREMENTS_MINIMUM
                    self.score_to_be_added -= Game.SCORE_TO_BE_ADDED_INCREMENTS_MINIMUM
            else:
                self.score += score_to_be_added_part
                self.score_to_be_added -= score_to_be_added_part
        else:
            self.score += 1 * self.difficulty_factor
        for entity in self.entities:
            entity.step()
            if type(entity) is Meteor:
                if entity.y >= models.world.DIRT_START * TILE_SIZE_IN_PIXELS:
                    # this meteor is below DIRT_START, Check collision
                    try:
                        if entity.is_colliding(TILE_SIZE_IN_PIXELS, self.world.tile_matrix):
                            self.entities.append(Explosion(entity.x + entity.width/2, entity.y + entity.height/4, entity.width * 3))
                            self.entities.remove(entity)
                    except NotOnScreenError:
                        self.entities.remove(entity)
            if type(entity) is Explosion:
                if entity.frame_counter >= 48:
                    self.entities.remove(entity)

        # time to maybe spawn a meteor
        if random.randint(0, 1000) > 1000 - self.meteor_spawn_rate:
            self.entities.append(Meteor(random.randint(0, SCREEN_WIDTH), random.randint(50, 500) / 100, self.world, damage_multiplier=self.meteor_damage_multiplier))

        self.player.step()
