from models.items.item_types import ItemType
from constants import ITEM_SIZE_IN_PIXELS
from models.items.item_types import PATHS

import pygame


class InventoryItem(object):

    def __init__(self, item_type: ItemType, amount: int):
        self.item_type = item_type
        self.amount = amount

    def draw(self, surface):
        sprite = pygame.transform.scale(pygame.image.load(PATHS[self.item_type]["location"]),
                                              (ITEM_SIZE_IN_PIXELS, ITEM_SIZE_IN_PIXELS))
        x, y = 1 * ITEM_SIZE_IN_PIXELS, self.item_type.value * ITEM_SIZE_IN_PIXELS
        font = pygame.font.SysFont("Arial", 18)
        msg_surface = font.render(str(self.amount), False, (255, 255, 255))
        surface.blit(msg_surface, (x + ITEM_SIZE_IN_PIXELS * 1.25, y))
        surface.blit(sprite, (x, y))

    def __repr__(self):
        return str(self.__class__.__name__)
