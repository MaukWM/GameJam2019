from enum import Enum


class ItemType(Enum):
    DIRT = 1
    STONE = 2
    JELTSIUM = 3
    LENINIUM = 4
    MARXINIUM = 5
    NOKIA_PHONIUM = 6
    HALF_LITER_KLOKKIUM = 7

NAMES = dict()
NAMES[ItemType.DIRT] = "Dirt"
NAMES[ItemType.STONE] = "Stone"
NAMES[ItemType.JELTSIUM] = "Jeltisium"
NAMES[ItemType.MARXINIUM] = "Marxinium"
NAMES[ItemType.LENINIUM] = "Leninium"
NAMES[ItemType.NOKIA_PHONIUM] = "Nokia Phonium"
NAMES[ItemType.HALF_LITER_KLOKKIUM] = "Half Liter Klokkium"

SCORES = dict()
SCORES[ItemType.DIRT] = 0
SCORES[ItemType.STONE] = 0
SCORES[ItemType.JELTSIUM] = 250
SCORES[ItemType.MARXINIUM] = 750
SCORES[ItemType.LENINIUM] = 2500
SCORES[ItemType.NOKIA_PHONIUM] = 10000
SCORES[ItemType.HALF_LITER_KLOKKIUM] = 50000

PATHS = dict()
PATHS[ItemType.DIRT] = {"location": "assets/graphics/items/dirt_item.png"}
PATHS[ItemType.STONE] = {"location": "assets/graphics/items/stone_item.png"}
PATHS[ItemType.JELTSIUM] = {"location": "assets/graphics/items/jeltsium_item.png"}
PATHS[ItemType.LENINIUM] = {"location": "assets/graphics/items/leninium_item.png"}
PATHS[ItemType.MARXINIUM] = {"location": "assets/graphics/items/marxinium_item.png"}
PATHS[ItemType.NOKIA_PHONIUM] = {"location": "assets/graphics/items/nokia_phonium_item.png"}
PATHS[ItemType.HALF_LITER_KLOKKIUM] = {"location": "assets/graphics/items/half_liter_klokkium_item.png"}

MEME_PATHS = dict()
MEME_PATHS[ItemType.DIRT] = {"location": "assets/graphics/items/dirt_item.png"}
MEME_PATHS[ItemType.STONE] = {"location": "assets/graphics/items/stone_item.png"}
MEME_PATHS[ItemType.JELTSIUM] = {"location": "assets/graphics/items/meme_jeltsium_item.png"}
MEME_PATHS[ItemType.LENINIUM] = {"location": "assets/graphics/items/meme_leninium_item.png"}
MEME_PATHS[ItemType.MARXINIUM] = {"location": "assets/graphics/items/meme_marxinium_item.png"}
MEME_PATHS[ItemType.NOKIA_PHONIUM] = {"location": "assets/graphics/items/meme_nokia_phonium_item.png"}
MEME_PATHS[ItemType.HALF_LITER_KLOKKIUM] = {"location": "assets/graphics/items/meme_half_liter_klokkium_item.png"}





