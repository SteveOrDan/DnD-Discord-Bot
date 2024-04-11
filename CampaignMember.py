import discord
import enum

import costants
from data.Dice import D8, D10, D6
from data.Items.Items import Weapon, Armor, ArmorType, WeaponType
from data.Purse import Purse


class StatTypeEnum(enum.Enum):

    NONE = -1, "NONE"
    STR = 0, "STR"
    DEX = 1, "DEX"
    CON = 2, "CON"
    INT = 3, "INT"
    WIS = 4, "WIS"
    CHA = 5, "CHA"

    def __new__(cls, value, name):
        member = object.__new__(cls)
        member._value_ = value
        member.fullname = name
        return member

    def __int__(self):
        return self.value

    @staticmethod
    def str_to_enum(stat_name: str):
        stat_name = stat_name.upper()

        stats = {
            "STR": StatTypeEnum.STR,
            "DEX": StatTypeEnum.DEX,
            "CON": StatTypeEnum.CON,
            "INT": StatTypeEnum.INT,
            "WIS": StatTypeEnum.WIS,
            "CHA": StatTypeEnum.CHA
        }

        return stats.get(stat_name)


class AdvClass(enum.Enum):
    CLERIC = "cleric", costants.CLERIC_ROLE_ID, D8(), ["WIS", "CHA"], [ArmorType.LIGHT, ArmorType.MEDIUM, ArmorType.SHIELD], [WeaponType.SIMPLE_MELEE, WeaponType.SIMPLE_RANGED], [],
    FIGHTER = "fighter", costants.FIGHTER_ROLE_ID, D10(), ["STR", "CON"], [ArmorType.LIGHT, ArmorType.MEDIUM, ArmorType.HEAVY, ArmorType.SHIELD], [WeaponType.SIMPLE_MELEE, WeaponType.SIMPLE_RANGED, WeaponType.MARTIAL_MELEE, WeaponType.MARTIAL_RANGED], [],
    ROGUE = "rogue", costants.ROGUE_ROLE_ID, D8(), ["DEX", "INT"], [ArmorType.LIGHT], [WeaponType.SIMPLE_MELEE, WeaponType.SIMPLE_RANGED], ["crossbow hand", "longsword", "rapier", "shortsword"],
    WIZARD = "wizard", costants.WIZARD_ROLE_ID, D6(), ["INT", "WIS"], [], [], ["dagger", "dart", "sling", "quarterstaff", "crossbow light"]

    def get_name(self):
        return self.value[0]

    def get_role_id(self):
        return self.value[1]

    def get_hit_dice(self):
        return self.value[2]

    def get_saving_throws(self):
        return self.value[3]

    def get_armor_proficiencies(self):
        return self.value[4]

    def get_weapon_proficiencies(self):
        return self.value[5]

    def get_class_proficiencies(self):
        return self.value[6]

    @staticmethod
    def enum_from_str(class_name: str):
        class_name = class_name.lower()

        classes = {
            "cleric": AdvClass.CLERIC,
            "fighter": AdvClass.FIGHTER,
            "rogue": AdvClass.ROGUE,
            "wizard": AdvClass.WIZARD
        }

        return classes.get(class_name)


class RaceTypeEnum(enum.Enum):
    DWARF = "dwarf", 0, 0, 2, 0, 0, 0, costants.DWARF_ROLE_ID, ["battleaxe", "handaxe", "light hammer", "warhammer"], 25
    HILL_DWARF = "hill dwarf", 0, 0, 2, 1, 0, 0, costants.HILL_DWARF_ROLE_ID, ["battleaxe", "handaxe", "light hammer", "warhammer"], 25
    MOUNTAIN_DWARF = "mountain dwarf", 2, 0, 2, 0, 0, 0, costants.MOUNTAIN_DWARF_ROLE_ID, ["battleaxe", "handaxe", "light hammer", "warhammer"], 25
    ELF = "elf", 0, 2, 0, 0, 0, 0, costants.ELF_ROLE_ID, ["shortsword", "longsword", "shortbow", "longbow"], 30
    HIGH_ELF = "high elf", 0, 2, 0, 1, 0, 0, costants.HIGH_ELF_ROLE_ID, ["shortsword", "longsword", "shortbow", "longbow"], 30
    WOOD_ELF = "wood elf", 0, 2, 0, 0, 1, 0, costants.WOOD_ELF_ROLE_ID, ["shortsword", "longsword", "shortbow", "longbow"], 30
    HALFLING = "halfling", 0, 2, 0, 0, 0, 0, costants.HALFLING_ROLE_ID, [], 25
    STOUT = "stout", 0, 2, 1, 0, 0, 0, costants.STOUT_ROLE_ID, [], 25
    LIGHTFOOT = "lightfoot", 0, 2, 0, 0, 0, 1, costants.LIGHTFOOT_ROLE_ID, [], 25
    HUMAN = "human", 1, 1, 1, 1, 1, 1, costants.HUMAN_ROLE_ID, [], 30

    def get_name(self):
        return self.value[0]

    def get_str(self):
        return self.value[1]

    def get_dex(self):
        return self.value[2]

    def get_con(self):
        return self.value[3]

    def get_int(self):
        return self.value[4]

    def get_wis(self):
        return self.value[5]

    def get_cha(self):
        return self.value[6]

    def get_role_id(self):
        return self.value[7]

    def get_race_proficiencies(self):
        return self.value[8]

    def get_speed(self):
        return self.value[9]

    @staticmethod
    def enum_from_str(race_name: str):
        race_name = race_name.lower()

        races = {
            "dwarf": RaceTypeEnum.DWARF,
            "hill dwarf": RaceTypeEnum.HILL_DWARF,
            "mountain dwarf": RaceTypeEnum.MOUNTAIN_DWARF,
            "elf": RaceTypeEnum.ELF,
            "high elf": RaceTypeEnum.HIGH_ELF,
            "wood elf": RaceTypeEnum.WOOD_ELF,
            "halfling": RaceTypeEnum.HALFLING,
            "stout": RaceTypeEnum.STOUT,
            "lightfoot": RaceTypeEnum.LIGHTFOOT,
            "human": RaceTypeEnum.HUMAN
        }

        return races.get(race_name)


class CampaignMember:
    member: discord.Member

    max_inventory_weight: int = 0
    curr_inventory_weight: int = 0
    inventory: {str: int} = {}
    equipped_weapon: Weapon = None
    equipped_armor: Armor = None
    has_shield: bool = False

    isAdventurer: bool = False
    isDM: bool = False

    player_num: int = 0

    race: RaceTypeEnum
    adv_class: AdvClass
    alignment: str = "None"
    background: str = "None"
    traits: str = "None"
    ideals: str = "None"
    bonds: str = "None"
    flaws: str = "None"

    level: int = 1
    xp: int = 0

    total_speed: int = 0
    race_speed: int = 0
    speed_debuff: int = 0

    hitPoints: int = 0

    weapon_proficiencies: [WeaponType] = []
    armor_proficiencies: [ArmorType] = []
    saving_throw_proficiencies: [str] = []
    race_proficiencies: [str] = []
    class_proficiencies: [str] = []

    proficiency_bonus: int = 2

    # Display only stats channels
    STR_ch: discord.VoiceChannel = None
    DEX_ch: discord.VoiceChannel = None
    CON_ch: discord.VoiceChannel = None
    INT_ch: discord.VoiceChannel = None
    WIS_ch: discord.VoiceChannel = None
    CHA_ch: discord.VoiceChannel = None

    # Stats
    armor_class: int = 0

    stats_modifiers: [int] = [0, 0, 0, 0, 0, 0]

    total_stats: [int] = [0, 0, 0, 0, 0, 0]

    rolled_stats: [int] = [0, 0, 0, 0, 0, 0]

    race_stats: [int] = [0, 0, 0, 0, 0, 0]

    equip_stats: [int] = [0, 0, 0, 0, 0, 0]

    stats_set_num: int = -1
    stats_set_bools = [False, False, False, False, False, False]

    roll_list: [int] = []

    purse: Purse = None

    def update_total_stat(self, stat_index: int):
        self.total_stats[stat_index] = self.rolled_stats[stat_index] + self.race_stats[stat_index] + self.equip_stats[stat_index]

        if stat_index == 0:
            self.update_max_inventory_weight()

    def update_all_total_stat(self):
        for stat_index in range(len(self.total_stats)):
            self.total_stats[stat_index] = self.rolled_stats[stat_index] + self.race_stats[stat_index] + self.equip_stats[stat_index]

        self.update_max_inventory_weight()

    async def update_stat_ch(self, stat_index: int):
        stat_channels = {
            0: (self.STR_ch, 'STR'),
            1: (self.DEX_ch, 'DEX'),
            2: (self.CON_ch, 'CON'),
            3: (self.INT_ch, 'INT'),
            4: (self.WIS_ch, 'WIS'),
            5: (self.CHA_ch, 'CHA')
        }

        channel, stat_name = stat_channels.get(stat_index)
        if channel:
            await channel.edit(name=f'{stat_name} = {self.total_stats[stat_index]}')

    async def update_all_stat_ch(self):
        for i in range(6):
            await self.update_stat_ch(i)

    def update_stats_modifiers(self):
        for i in range(len(self.stats_modifiers)):
            self.stats_modifiers[i] = (self.total_stats[i] - 10) // 2

    def update_armor_class(self):
        self.armor_class = self.equipped_armor.armor_class

        if self.equipped_armor.armor_type == ArmorType.LIGHT:
            self.armor_class += self.stats_modifiers[1]
        elif self.equipped_armor.armor_type == ArmorType.MEDIUM:
            self.armor_class += min(self.stats_modifiers[1], 2)

        if self.has_shield:
            self.armor_class += 2

    def get_info(self) -> str:
        res = f"{self.member.mention} - {self.member.display_name}\n"

        res += f"Is adventurer: {self.isAdventurer}\n"
        res += f"Is DM: {self.isDM}\n"

        if self.isAdventurer:
            res += "Inventory: "

            for item in self.inventory:
                res += f"{item}; "

            res += "\n"

            res += f"Equipped weapon: {self.equipped_weapon.name}\n"
            res += f"Equipped armor: {self.equipped_armor.name}\n"
            res += f"Has shield: {self.has_shield}\n"

            res += f"Player number: {self.player_num}\n"

            res += f"Character: {self.race.get_name()} {self.adv_class.get_name()} - {self.alignment}\n"

            res += f"Background: {self.background}\n"
            res += f"Traits: {self.traits}\n"
            res += f"Ideals: {self.ideals}\n"
            res += f"Bonds: {self.bonds}\n"
            res += f"Flaws: {self.flaws}\n"

            res += f"Level: {self.level}\n"

            res += f"Hit points: {self.hitPoints}\n"

            res += "Weapon proficiencies: "
            for weapon_prof in self.weapon_proficiencies:
                res += f"{weapon_prof}; "

            res += "\n"

            res += "Armor proficiencies: "
            for armor_prof in self.armor_proficiencies:
                res += f"{armor_prof}; "

            res += "\n"

            res += "Saving throw proficiencies: "
            for saving_throw_prof in self.saving_throw_proficiencies:
                res += f"{saving_throw_prof}; "

            res += "\n"

            res += "Race proficiencies:"
            for race_prof in self.race_proficiencies:
                res += f"{race_prof}; "

            res += "\n"

            res += "Class proficiencies:"
            for class_prof in self.class_proficiencies:
                res += f"{class_prof}; "

            res += "\n"

            res += f"Proficiency bonus: {self.proficiency_bonus}\n"

            res += f"Armor class: {self.armor_class}\n"

            res += f"Stats modifiers: "
            for stat_mod in self.stats_modifiers:
                res += f"{stat_mod}; "

            res += "\n"

            res += f"Total stats: "
            for stat in self.total_stats:
                res += f"{stat}; "

            res += "\n"

            res += f"Rolled stats: "
            for stat in self.rolled_stats:
                res += f"{stat}; "

            res += "\n"

            res += f"Race stats: "
            for stat in self.race_stats:
                res += f"{stat}; "

            res += "\n"

            res += f"Equip stats: "
            for stat in self.equip_stats:
                res += f"{stat}; "

            res += "\n"

            res += f"Stats set num: {self.stats_set_num}\n"

            res += f"Purse: {self.purse.toString()}"

        return res

    def add_xp(self, xp: int):
        self.xp += xp

        if ((self.level == 1 and self.xp >= 300) or (self.level == 2 and self.xp >= 900) or
                (self.level == 3 and self.xp >= 2700) or (self.level == 4 and self.xp >= 6500) or
                (self.level == 5 and self.xp >= 14000) or (self.level == 6 and self.xp >= 23000) or
                (self.level == 7 and self.xp >= 34000) or (self.level == 8 and self.xp >= 48000) or
                (self.level == 9 and self.xp >= 64000) or (self.level == 10 and self.xp >= 85000) or
                (self.level == 11 and self.xp >= 100000) or (self.level == 12 and self.xp >= 120000) or
                (self.level == 13 and self.xp >= 140000) or (self.level == 14 and self.xp >= 165000) or
                (self.level == 15 and self.xp >= 195000) or (self.level == 16 and self.xp >= 225000) or
                (self.level == 17 and self.xp >= 265000) or (self.level == 18 and self.xp >= 305000) or
                (self.level == 19 and self.xp >= 355000)):
            self.level_up()

    def level_up(self):
        self.level += 1

        self.hitPoints += max(1, self.adv_class.get_hit_dice().throw() + self.stats_modifiers[2])

        self.proficiency_bonus = (self.level - 1) // 4 + 2

        self.update_armor_class()

    def update_max_inventory_weight(self):
        self.max_inventory_weight = 15 * self.total_stats[0]

    def update_curr_inventory_weight(self):
        for item in self.inventory.keys():
            self.curr_inventory_weight += item.weight * self.inventory.get(item)

    def update_total_speed(self):
        self.total_speed = self.race_speed - self.speed_debuff
