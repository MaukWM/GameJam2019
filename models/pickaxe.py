from models.items.item_types import ItemType


class Pickaxe():

    material_list = [ItemType.STONE,
                     ItemType.JELTSIUM,
                     ItemType.MARXINIUM,
                     ItemType.LENINIUM,
                     ItemType.NOKIA_PHONIUM,
                     ItemType.HALF_LITER_KLOKKIUM
                     ]

    item_to_strength = dict()
    item_to_strength[ItemType.STONE] = 0.05
    item_to_strength[ItemType.JELTSIUM] = 0.10
    item_to_strength[ItemType.MARXINIUM] = 0.20
    item_to_strength[ItemType.LENINIUM] = 0.40
    item_to_strength[ItemType.NOKIA_PHONIUM] = 0.80
    item_to_strength[ItemType.HALF_LITER_KLOKKIUM] = 1.60

    cost_to_upgrade_from = dict()
    cost_to_upgrade_from[ItemType.STONE] = {ItemType.JELTSIUM: 10}
    cost_to_upgrade_from[ItemType.JELTSIUM] = {ItemType.MARXINIUM: 10}
    cost_to_upgrade_from[ItemType.MARXINIUM] = {ItemType.LENINIUM: 10}
    cost_to_upgrade_from[ItemType.LENINIUM] = {ItemType.NOKIA_PHONIUM: 10}
    cost_to_upgrade_from[ItemType.NOKIA_PHONIUM] = {ItemType.HALF_LITER_KLOKKIUM: 10}

    def __init__(self, player):
        self.material = ItemType.STONE
        self.strength = 0.05
        self.player = player

    def is_max_level(self):
        return self.material == ItemType.HALF_LITER_KLOKKIUM

    def is_upgradeable(self):
        return (not self.is_max_level()) and self.has_enough_material()

    def has_enough_material(self):
        player_inventory = self.player.inventory.inventory
        for cost_item in self.cost_to_upgrade_from[self.material]:
            if player_inventory[cost_item].amount < self.cost_to_upgrade_from[self.material][cost_item]:
                return False
        return True

    def next_material_level(self):
        for i in range(0, len(self.material_list) - 1):
            if self.material == ItemType.HALF_LITER_KLOKKIUM:
                return None
            if self.material_list[i] == self.material:
                return self.material_list[i + 1]

    def upgrade(self):
        if self.material == ItemType.HALF_LITER_KLOKKIUM:
            return False
        for i in range(0, len(self.material_list) - 1):
            if self.material_list[i] == self.material:
                self.material = self.material_list[i + 1]
                self.strength = self.item_to_strength[self.material]
                return True
        return False

