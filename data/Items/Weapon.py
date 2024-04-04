from data.Cost import Cost
from data.Dice import Dice
import enum


class WeaponProperty(enum.Enum):
    AMMUNITION_30_120 = 0
    AMMUNITION_80_320 = 1
    AMMUNITION_150_600 = 2
    FINESSE = 3
    HEAVY = 4
    LIGHT = 5
    LOADING = 6
    REACH = 7
    SPECIAL = 8
    THROWN_20_60 = 9
    TWO_HANDED = 10
    VERSATILE = 11


class WeaponType(enum.Enum):
    SIMPLE_MELEE = 0
    SIMPLE_RANGED = 1
    MARTIAL_MELEE = 2
    MARTIAL_RANGED = 3


class Weapon:

    def __init__(self, weaponType: WeaponType, weaponName: str, cost: Cost, damage: Dice, properties: list):
        self.weaponType = weaponType
        self.weaponName = weaponName
        self.cost = cost
        self.damage = damage
        self.properties = properties
