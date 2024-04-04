import enum

from data.Cost import Cost


class ArmorType(enum.Enum):
    LIGHT = 0
    MEDIUM = 1
    HEAVY = 2
    SHIELD = 3


class Armor:
    def __init__(self, armor_type: ArmorType, name: str, cost: Cost, armor_class: int):
        self.armor_type = armor_type
        self.name = name
        self.cost = cost
        self.armor_class = armor_class
