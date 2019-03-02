from enum import Enum


class ItemType(Enum):
    DIRT = 1
    STONE = 2
    JELTSIUM = 3
    LENINIUM = 4
    MARXINIUM = 5
    NOKIA_PHONIUM = 6
    HALF_LITER_KLOKKIUM = 7


PATHS = {}
PATHS[ItemType.DIRT] = {"location": "assets/graphics/items/dirt_item.png"}
PATHS[ItemType.STONE] = {"location": "assets/graphics/items/stone_item.png"}
PATHS[ItemType.JELTSIUM] = {"location": "assets/graphics/items/jeltsium_item.png"}
PATHS[ItemType.LENINIUM] = {"location": "assets/graphics/items/leninium_item.png"}
PATHS[ItemType.MARXINIUM] = {"location": "assets/graphics/items/marxinium_item.png"}
PATHS[ItemType.NOKIA_PHONIUM] = {"location": "assets/graphics/items/nokia_phonium_item.png"}
PATHS[ItemType.HALF_LITER_KLOKKIUM] = {"location": "assets/graphics/items/half_liter_klokkium_item.png"}




