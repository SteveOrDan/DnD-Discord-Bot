import enum

from data import Dice
from data.Dice import D20


class MonsterState(enum.Enum):
    ALIVE = 0
    DEAD = 1


class Monster:
    def __init__(self, name: str, AC: int, HP: int, attack_bonus: int, dice_num: int, damage_dice: int, damage_bonus: int):
        self.name = name
        self.AC = AC
        self.HP = HP
        self.attack_bonus = attack_bonus
        self.dice_num = dice_num
        self.damage_dice = Dice.dice_from_int(damage_dice)
        self.damage_bonus = damage_bonus

    def take_damage(self, damage: int) -> int:
        self.HP -= damage

        if self.HP <= 0:
            return 0
        else:
            return self.HP

    def attack(self, player_AC: int) -> int:
        if D20().throw() + self.attack_bonus >= player_AC:
            return self.damage_dice.throw_n(self.dice_num) + self.damage_bonus
        else:
            return 0

    def toString(self):
        return f"{self.name}:\nHP: {self.HP}\nAC: {self.AC}\nAttack: Hit + {self.attack_bonus}\nDamage: {self.dice_num}d{self.damage_dice} + {self.damage_bonus}"


monsters = {
    "scorpion": Monster("scorpion", 11, 1, 2, 1, 8, 1),
    "bandit": Monster("bandit", 12, 11, 3, 1, 6, 1),
    "goblin": Monster("goblin", 15, 7, 4, 1, 6, 2),
    "orc": Monster("orc", 13, 15, 5, 1, 12, 3),
    "ghoul": Monster("ghoul", 12, 22, 2, 2, 6, 2),
    "ogre": Monster("ogre", 11, 59, 6, 2, 8, 4),
    "doppelganger": Monster("doppelganger", 14, 52, 6, 1, 6, 4),
    "young green dragon": Monster("young green dragon", 18, 136, 7, 2, 10, 4),
    "adult red dragon": Monster("adult red dragon", 19, 256, 14, 2, 10, 8),
}


def get_monster(monster_name: str) -> Monster | None:
    monster = monsters.get(monster_name.lower())
    if monster is None:
        return None
    return monster


def monster_info(monster_name: str) -> str:
    monster = get_monster(monster_name)
    if monster is None:
        return "Monster not found"
    return monster.toString()


def get_all_monsters():
    res = "Monsters:\n"

    for monster in monsters.keys():
        res += monsters.get(monster).toString() + "\n\n"

    return res
