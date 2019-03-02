import pygame
import sys


class Explosion:

    frames = list(map(lambda x: pygame.image.load('assets/graphics/explosions/frame_' + str(x) + '_delay-0.08s.png'), range(0, 12)))

    def __init__(self, x, y):
        self.frame_counter = -1
        self.x = x - 40
        self.y = y - 75

    def step(self):
        self.frame_counter += 1

    def draw(self, surface, camera_y):
        try:
            to_draw_y = self.y - camera_y
            to_draw_x= self.x
            surface.blit(self.frames[self.frame_counter // 4], (to_draw_x, to_draw_y))
        except IndexError:
            print("IndexError happened: y, x, frame_counter:")
            print(self.y - camera_y)
            print(self.x)
            print(self.frame_counter)
            sys.exit(1)