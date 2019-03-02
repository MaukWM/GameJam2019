from models.items.item_types import ItemType
from models.items.inventory_item import InventoryItem
from constants import ITEM_SIZE_IN_PIXELS

import pygame

INVENTORY_X = 20
INVENTORY_Y = 20


class Inventory(object):

    def __init__(self, memes_enabled=False):
        self.inventory = self.init_inventory()
        self.memes_enabled = memes_enabled

    @staticmethod
    def init_inventory():
        inventory = {}
        for item_type in ItemType:
            inventory[item_type] = InventoryItem(item_type, 0)
        return inventory

    def increment_item_amount(self, item_type: ItemType):
        self.inventory[item_type].amount = self.inventory[item_type].amount + 1

    def decrement_item_amount(self, item_type: ItemType):
        self.inventory[item_type].amount = self.inventory[item_type].amount - 1

    def draw(self, surface):
        # Height of background is all the item * their size + a bit more for a border
        background_height = len(self.inventory) * ITEM_SIZE_IN_PIXELS
        # magic for now
        highest_digit_count = 0
        for inv_item in self.inventory:
            len_inv_item = len(str(self.inventory[inv_item].amount))
            if len_inv_item > highest_digit_count:
                highest_digit_count = len_inv_item
        background_width = ITEM_SIZE_IN_PIXELS * 2 + ((highest_digit_count - 1) * 10)
        # draw background of inventory
        pygame.draw.rect(surface, (100, 100, 100), (ITEM_SIZE_IN_PIXELS, ITEM_SIZE_IN_PIXELS, background_width, background_height))
        # draw every inventory item
        for inv_item in self.inventory:
            self.inventory[inv_item].draw(surface, self.memes_enabled)
        # draw the border of the inventory
        pygame.draw.rect(surface, (30, 30, 30), (ITEM_SIZE_IN_PIXELS - 1, ITEM_SIZE_IN_PIXELS, background_width + 1, background_height), 1)

    def __repr__(self):
        representation = "Inventory: "
        for inv_item in self.inventory:
            representation += "{" + str(inv_item) + ", " + str(self.inventory[inv_item].amount) + "} "
        return representation

