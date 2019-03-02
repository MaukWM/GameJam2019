from models.items.item_types import ItemType
from constants import ITEM_SIZE_IN_PIXELS
from models.items.item_types import PATHS, MEME_PATHS

import pygame


class InventoryItem(object):

    def __init__(self, item_type: ItemType, amount: int):
        self.item_type = item_type
        self.amount = amount
        self.font = pygame.font.SysFont("Arial", 18)

    def draw(self, surface, memes_enabled, selected_item):
        if memes_enabled:
            sprite = pygame.transform.scale(pygame.image.load(MEME_PATHS[self.item_type]["location"]),
                                                  (ITEM_SIZE_IN_PIXELS, ITEM_SIZE_IN_PIXELS))
        else:
            sprite = pygame.transform.scale(pygame.image.load(PATHS[self.item_type]["location"]),
                                                  (ITEM_SIZE_IN_PIXELS, ITEM_SIZE_IN_PIXELS))
        x, y = 1 * ITEM_SIZE_IN_PIXELS, self.item_type.value * ITEM_SIZE_IN_PIXELS
        if selected_item + 1 == self.item_type.value: #waarom beginnen mensen met tellen bij 1 ?!?!??!?!?!?!?!??!
            half = ITEM_SIZE_IN_PIXELS//2
            pygame.draw.circle(sprite, (245, 1, 1), (half, half), half, 2)
        msg_surface = self.font.render(str(self.amount), False, (255, 255, 255))
        surface.blit(msg_surface, (x + ITEM_SIZE_IN_PIXELS * 1.25, y + 5))
        surface.blit(sprite, (x, y))

    def __repr__(self):
        return str(self.__class__.__name__)
