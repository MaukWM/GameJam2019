from constants import FRAME_RATE
import math
import pygame
import models.tiles.air_tile


class Meteor(object):

    METEOR_SPRITE = pygame.image.load('assets/graphics/meteor1.png')

    # the angle of the meteor in radians
    angle = 0.1

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
        grid_x = int(self.x / TILE_SIZE)
        grid_y = int(self.y / TILE_SIZE)
        width = len(game_tiles)
        height = len(game_tiles[0])
        if grid_y >= 0 and grid_y < height and grid_x >= 0 and grid_x < width:
            if type(game_tiles[grid_x][grid_y]) != models.tiles.air_tile.Air:
                range_size = math.ceil(self.size)
                # The x,y-position of this meteor contains a non-air tile, collision
                for delta_x in range(-range_size,range_size):
                    for delta_y in range(-range_size,range_size):
                        distance_factor = (delta_x**2 + delta_y**2) / self.size**2
                        if distance_factor < 1:
                            damage = 0.5 - distance_factor/(self.size*0.5)
                            effective_y = grid_y + delta_y
                            effective_x = grid_x + delta_x
                            if effective_y >= 0 and effective_y < height and effective_x >= 0 and effective_x < width:
                                it_breaks = game_tiles[effective_x][effective_y].damage(damage)
                                if it_breaks:
                                    game_tiles[effective_x][effective_y] = models.tiles.air_tile.Air(self, grid_x + delta_x, grid_y + delta_y)
                return True
        return False
