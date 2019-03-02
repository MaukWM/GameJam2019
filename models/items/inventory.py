from models.items.item_types import ItemType
from models.items.inventory_item import InventoryItem
from constants import ITEM_SIZE_IN_PIXELS

import pygame

INVENTORY_X = 20
INVENTORY_Y = 20


class Inventory(object):

    def __init__(self):
        self.inventory = self.init_inventory()

    @staticmethod
    def init_inventory():
        inventory = {}
        for item_type in ItemType:
            inventory[item_type] = InventoryItem(item_type, 0)
        return inventory

    def draw(self, surface):
        # Height of background is all the item * their size + a bit more for a border
        background_height = len(self.inventory) * ITEM_SIZE_IN_PIXELS
        # magic for now
        background_width = ITEM_SIZE_IN_PIXELS * 2
        # draw background of inventory
        pygame.draw.rect(surface, (100, 100, 100), (ITEM_SIZE_IN_PIXELS, ITEM_SIZE_IN_PIXELS, background_width, background_height))
        for inv_item in self.inventory:
            self.inventory[inv_item].draw(surface)
        pygame.draw.rect(surface, (30, 30, 30), (ITEM_SIZE_IN_PIXELS - 1, ITEM_SIZE_IN_PIXELS, background_width + 1, background_height), 1)

    def __repr__(self):
        representation = "Inventory: "
        for inv_item in self.inventory:
            representation += "{" + str(inv_item) + ", " + str(self.inventory[inv_item].amount) + "} "
        return representation

