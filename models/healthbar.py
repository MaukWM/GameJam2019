import pygame
import math

class HealthBar:

    txt_surface = None

    def __init__(self):
        self.health = 1000
        self.font = pygame.font.SysFont("Arial", 30, True)
        self.txt_surface  =self.font.render("Health: " + str(self.health), True, (0, 255, 0))

    def step(self):
        pass

    def take_damage(self, amount):
        self.health -= math.floor(amount)
        if self.health > 500:
            self.txt_surface = self.font.render("Health: " + str(self.health), True, (0, 255, 0))
        elif self.health > 250:
            self.txt_surface = self.font.render("Health: " + str(self.health), True, (255, 255, 102))
        else:
            self.txt_surface = self.font.render("Health: " + str(self.health), True, (255, 0, 0))

    def draw(self, surface):
        surface.blit(self.txt_surface, (10, 620))