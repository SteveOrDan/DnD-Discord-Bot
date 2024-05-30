import enum

from data.CampaignMember import StatTypeEnum
from data import Dice
from data.Dice import D20


class MonsterState(enum.Enum):
    ALIVE = 0
    DEAD = 1


class Monster:

    def __init__(self, name: str, AC: int, HP: int,
                 STR: int, DEX: int, CON: int, INT: int, WIS: int, CHA: int,
                 attack_bonus: int, dice_num: int, damage_dice: int, damage_bonus: int):
        self.name = name
        self.AC = AC
        self.HP = HP

        self.total_stats: [int] = [0, 0, 0, 0, 0, 0]
        self.stats_modifiers: [int] = [0, 0, 0, 0, 0, 0]

        self.total_stats[StatTypeEnum.STR.value] = STR
        self.total_stats[StatTypeEnum.DEX.value] = DEX
        self.total_stats[StatTypeEnum.CON.value] = CON
        self.total_stats[StatTypeEnum.INT.value] = INT
        self.total_stats[StatTypeEnum.WIS.value] = WIS
        self.total_stats[StatTypeEnum.CHA.value] = CHA

        self.attack_bonus = attack_bonus
        self.dice_num = dice_num
        self.damage_dice = Dice.dice_from_int(damage_dice)
        self.damage_bonus = damage_bonus
        self.calculate_modifiers()

    def calculate_modifiers(self):
        for i in range(6):
            self.stats_modifiers[i] = (self.total_stats[i] - 10) // 2

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

    def ability_check(self, ability: str):
        # Get stat type
        stat = StatTypeEnum.str_to_enum(ability)

        # Roll a D20
        roll = D20().throw() + self.stats_modifiers[stat.value]

        return roll

    def toString(self):
        return f"Name: {self.name}\n" \
               f"AC: {self.AC}\n" \
               f"HP: {self.HP}\n" \
               f"Attack bonus: {self.attack_bonus}\n" \
               f"Damage dice: {self.damage_dice.__str__()}\n" \
               f"Damage bonus: {self.damage_bonus}\n" \
               f"STR: {self.total_stats[StatTypeEnum.STR.value]} ({self.stats_modifiers[StatTypeEnum.STR.value]})\n" \
               f"DEX: {self.total_stats[StatTypeEnum.DEX.value]} ({self.stats_modifiers[StatTypeEnum.DEX.value]})\n" \
               f"CON: {self.total_stats[StatTypeEnum.CON.value]} ({self.stats_modifiers[StatTypeEnum.CON.value]})\n" \
               f"INT: {self.total_stats[StatTypeEnum.INT.value]} ({self.stats_modifiers[StatTypeEnum.INT.value]})\n" \
               f"WIS: {self.total_stats[StatTypeEnum.WIS.value]} ({self.stats_modifiers[StatTypeEnum.WIS.value]})\n" \
               f"CHA: {self.total_stats[StatTypeEnum.CHA.value]} ({self.stats_modifiers[StatTypeEnum.CHA.value]})"


monsters = {
    "scorpion": Monster("scorpion", 11, 1, 2, 11, 8, 1, 8, 2, 2, 1, 8, 1),
    "bandit": Monster("bandit", 12, 11, 11, 12, 12, 10, 10, 10, 3, 1, 6, 1),
    "goblin": Monster("goblin", 15, 7, 8, 14, 10, 10, 8, 8, 4, 1, 6, 2),
    "orc": Monster("orc", 13, 15, 16, 12, 16, 7, 11, 10, 5, 1, 12, 3),
    "ghoul": Monster("ghoul", 12, 22, 13, 15, 10, 7, 10, 6, 2, 2, 6, 2),
    "ogre": Monster("ogre", 11, 59, 19, 8, 16, 5, 7, 7, 6, 2, 8, 4),
    "doppelganger": Monster("doppelganger", 14, 52, 11, 18, 14, 11, 12, 14, 6, 1, 6, 4),
    "young green dragon": Monster("young green dragon", 18, 136, 19, 12, 17, 16, 13, 15, 7, 2, 10, 4),
    "adult red dragon": Monster("adult red dragon", 19, 256, 27, 10, 25, 16, 13, 21, 14, 2, 10, 8),
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
