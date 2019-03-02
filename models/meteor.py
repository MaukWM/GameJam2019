from constants import FRAME_RATE
import math
import pygame
import models.tiles.air_tile
import random


class Meteor(object):

    sprites = [
        pygame.image.load('assets/graphics/meteors/basestation.png'),
        pygame.image.load('assets/graphics/meteors/stone1.png')
    ]


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
        self.SPRITE = self.sprites[random.randint(0, len(self.sprites) - 1)]

        # used for step calculations
        self.delta_x = math.sin(self.angle) * self.speed
        self.delta_y = math.cos(self.angle) * self.speed

    # update the internal state to the next state
    def step(self):
       self.x += self.delta_x
       self.y += self.delta_y

    # draw this meteor at the position in the next frame
    def draw(self, surface, camera_y):
        to_draw_y = self.y - camera_y
        to_draw_x= self.x
        surface.blit(self.SPRITE, (to_draw_x, to_draw_y))

    def is_colliding(self, TILE_SIZE, game_tiles):
        try:
            return game_tiles[math.floor(self.x / TILE_SIZE)][math.floor(self.y / TILE_SIZE)].is_solid() or \
                   game_tiles[math.floor(self.x / TILE_SIZE)][math.ceil(self.y / TILE_SIZE)].is_solid() or \
                   game_tiles[math.ceil(self.x / TILE_SIZE)][math.floor(self.y / TILE_SIZE)].is_solid() or \
                   game_tiles[math.ceil(self.x / TILE_SIZE)][math.ceil(self.y / TILE_SIZE)].is_solid()
        except IndexError:
            raise NotOnScreenError()


class NotOnScreenError(Exception):
    pass
