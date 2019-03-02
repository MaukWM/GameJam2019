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
        grid_x = int(self.x / TILE_SIZE)
        grid_y = int(self.y / TILE_SIZE)
        width = len(game_tiles)
        height = len(game_tiles[0])
        if grid_y >= 0 and grid_y < height and grid_x >= 0 and grid_x < width:
            if type(game_tiles[grid_x][grid_y]) != models.tiles.air_tile.Air:
                range_size = int(math.ceil(self.size))
                # The x,y-position of this meteor contains a non-air tile, collision
                for delta_x in range(-range_size, range_size):
                    for delta_y in range(-range_size, range_size):
                        distance_factor = (delta_x**2 + delta_y**2) / self.size**2
                        if distance_factor < 1:
                            damage = 0.5 - distance_factor/(self.size*0.5)
                            effective_y = grid_y + delta_y
                            effective_x = grid_x + delta_x
                            if effective_y >= 0 and effective_y < height and effective_x >= 0 and effective_x < width:
                                it_breaks = game_tiles[effective_x][effective_y].damage(damage)
                                if it_breaks:
                                    tile_broken = game_tiles[effective_x][effective_y]
                                    game_tiles[effective_x][effective_y] = models.tiles.air_tile.Air(self, grid_x + delta_x, grid_y + delta_y)
                                    self.drop_item(effective_x, effective_y, tile_broken)
                return True
        return False

    def drop_item(self, x, y, tile_broken):
        pass

class NotOnScreenError(Exception):
    pass
