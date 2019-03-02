from constants import FRAME_RATE
import math
import pygame
import models.tiles.air_tile
import random


class Meteor(object):

    METEOR_SPRITE = pygame.image.load('assets/graphics/meteor1.png')

    # the angle of the meteor in radians
    angle = 0.7

    # the speed of the meteor, in pixels/second
    speed = 320 / FRAME_RATE

    def __init__(self, spawn_x, size):
        """
        :param spawn_x: spawn at this x position, in pixels
        :param size: an integer that describes the radius of the meteor in pixels
        """
        self.x = spawn_x
        self.y = 0
        self.size = size
        self.angle = (random.randint(0, 14) - 7) / 10

    # update the internal state to the next state
    def step(self):
       self.x += math.asin(self.angle) * self.speed
       self.y += math.acos(self.angle) * self.speed

    # draw this meteor at the position in the next frame
    def draw(self, surface, cameray_y):
        to_draw_y = self.y - cameray_y
        to_draw_x= self.x
        surface.blit(self.METEOR_SPRITE, (to_draw_x, to_draw_y))

    def is_colliding(self, DIRT_START, TILE_SIZE, game_tiles):
        try:
            if type(game_tiles[int(self.y / TILE_SIZE)][int(self.x / TILE_SIZE)]) != models.tiles.air_tile.Air:
                # The x,y-position of this meteor contains a non-air tile, collision
                return True
            return False
        except IndexError:
            raise NotOnScreenError()


class NotOnScreenError(Exception):
    pass
