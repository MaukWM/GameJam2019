import pygame
import sys
import random

from constants import SCREEN_HEIGHT


class Explosion:

    frames = list(map(lambda x: pygame.image.load('assets/graphics/explosions/frame_' + str(x) + '_delay-0.08s.png'), range(0, 12)))

    def __init__(self, x, y, impact_radius):
        self.frame_counter = -1
        self.x = x
        self.y = y
        self.damage = self.impact_radius = impact_radius

    def step(self):
        self.frame_counter += 1

    def draw(self, surface, camera_y):
        min_y = camera_y - 108
        max_y = (camera_y + SCREEN_HEIGHT) + 108
        if not min_y < self.y < max_y:
            return
        try:
            to_draw_y = self.y - camera_y - (self.impact_radius // 2)
            to_draw_x = self.x - (self.impact_radius // 2)
            to_blit = self.frames[self.frame_counter // 4]
            to_blit = pygame.transform.scale(to_blit, (self.impact_radius, self.impact_radius))
            surface.blit(to_blit, (to_draw_x, to_draw_y))
        except IndexError:
            print("IndexError happened: y, x, frame_counter:")
            print(self.y - camera_y)
            print(self.x)
            print(self.frame_counter)
            sys.exit(1)