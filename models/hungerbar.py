import pygame
import math

from models.items.item_types import ItemType


class HungerBar:
    txt_surface = None

    def __init__(self, player):
        self.hunger = 1000
        self.font = pygame.font.SysFont("Arial", 30, True)
        self.font_small = pygame.font.SysFont("Arial", 12, True)
        self.txt_surface = self.font.render("Hunger: " + str(int(self.hunger)), True, (0, 255, 0))
        self.txt_2 = self.font_small.render("You're getting hungry, press 'E' to eat 1 wheat.", True, (255, 255, 255))
        self.txt_3 = self.font_small.render("You're getting hungry, try to find something to eat", True, (255, 255, 255))
        self.player = player

    def step(self):
        self.hunger -= 0.1
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
        if self.hunger < 500:
            if self.player.inventory.inventory[ItemType.WHEAT].amount > 0:
                surface.blit(self.txt_2, (10, 700))
            else:
                surface.blit(self.txt_3, (10, 700))

    def eat(self):
        self.hunger += 100
        self.hunger = min(1000, self.hunger)
