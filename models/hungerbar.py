import pygame
import math

class HungerBar:
    txt_surface = None

    def __init__(self, player):
        self.hunger = 1000
        self.font = pygame.font.SysFont("Arial", 30, True)
        self.txt_surface = self.font.render("Hunger: " + str(int(self.hunger)), True, (0, 255, 0))
        self.player = player

    def step(self):
        self.hunger -= 0.05
        if self.hunger > 500:
            self.txt_surface = self.font.render("Hunger: " + str(int(self.hunger)), True, (0, 255, 0))
        elif self.hunger > 250:
            self.txt_surface = self.font.render("Hunger: " + str(int(self.hunger)), True, (255, 255, 102))
        else:
            self.txt_surface = self.font.render("Hunger: " + str(int(self.hunger)), True, (255, 0, 0))

        if self.hunger < 0:
            self.hunger = 0
            self.player.health_bar.take_damage(1)

    def draw(self, surface):
        surface.blit(self.txt_surface, (10, 660))