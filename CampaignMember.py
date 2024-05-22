import asyncio

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

    def __init__(self):
        self.member: discord.Member | None = None

        self.max_inventory_weight: int = 0
        self.curr_inventory_weight: int = 0
        self.inventory: dict = dict()  # itemName -> quantity
        self.equipped_weapon: Weapon | None = None
        self.equipped_armor: Armor | None = None
        self.has_shield: bool = False

        self.isAdventurer: bool = False
        self.isDM: bool = False

        self.player_num: int = 0

        self.race: RaceTypeEnum | None = None
        self.adv_class: AdvClass | None = None
        self.alignment: str = "None"
        self.background: str = "None"
        self.traits: str = "None"
        self.ideals: str = "None"
        self.bonds: str = "None"
        self.flaws: str = "None"

        self.max_cantrips_known: int = 0  # 3
        self.max_spell_slots: int = 0  # 2
        self.curr_spell_slots: int = 0
        self.max_preparable_spells: int = 0  # int / wis mod + level
        self.prepared_spells: [str] = []
        self.spells_known_list: [str] = []

        self.level: int = 1
        self.xp: int = 0

        self.total_speed: int = 0
        self.race_speed: int = 0
        self.speed_debuff: int = 0

        self.maxHitPoints: int = 0
        self.currHitPoints: int = 0

        self.weapon_proficiencies: [WeaponType] = []
        self.armor_proficiencies: [ArmorType] = []
        self.saving_throw_proficiencies: [str] = []
        self.race_proficiencies: [str] = []
        self.class_proficiencies: [str] = []

        self.proficiency_bonus: int = 2

        # Display only stats channels
        self.STR_ch: discord.VoiceChannel | None = None
        self.DEX_ch: discord.VoiceChannel | None = None
        self.CON_ch: discord.VoiceChannel | None = None
        self.INT_ch: discord.VoiceChannel | None = None
        self.WIS_ch: discord.VoiceChannel | None = None
        self.CHA_ch: discord.VoiceChannel | None = None

        # Stats
        self.armor_class: int = 0

        self.stats_modifiers: [int] = [0, 0, 0, 0, 0, 0]

        self.total_stats: [int] = [0, 0, 0, 0, 0, 0]

        self.rolled_stats: [int] = [0, 0, 0, 0, 0, 0]

        self.race_stats: [int] = [0, 0, 0, 0, 0, 0]

        self.equip_stats: [int] = [0, 0, 0, 0, 0, 0]

        self.stats_set_num: int = -1
        self.stats_set_bools = [False, False, False, False, False, False]

        self.roll_list: [int] = []

        self.purse: Purse | None = None

    def confirm_race(self):
        self.race_stats[0] = self.race.get_str()
        self.race_stats[1] = self.race.get_dex()
        self.race_stats[2] = self.race.get_con()
        self.race_stats[3] = self.race.get_int()
        self.race_stats[4] = self.race.get_wis()
        self.race_stats[5] = self.race.get_cha()

        self.race_speed = self.race.get_speed()

        self.race_proficiencies = self.race.get_race_proficiencies()

        self.update_all_total_stat()
        self.update_all_stat_ch()
        
    def confirm_class(self):
        self.saving_throw_proficiencies = self.adv_class.get_saving_throws()
        self.armor_proficiencies = self.adv_class.get_armor_proficiencies()
        self.weapon_proficiencies = self.adv_class.get_weapon_proficiencies()
        self.class_proficiencies = self.adv_class.get_class_proficiencies()

        if self.adv_class == AdvClass.CLERIC:
            self.max_cantrips_known = 3
            self.max_spell_slots = 2
            self.curr_spell_slots = 2
            self.max_preparable_spells = max(self.stats_modifiers[4] + self.level, 1)
            self.spells_known_list = ["light", "resistance", "spare the dying", "detect magic", "mealing word"]
        elif self.adv_class == AdvClass.WIZARD:
            self.max_cantrips_known = 3
            self.max_spell_slots = 2
            self.curr_spell_slots = 2
            self.max_preparable_spells = max(self.stats_modifiers[3] + self.level, 1)
            self.spells_known_list = ["light", "mage hand", "prestidigitation", "detect magic", "magic missile"]
        else:
            self.max_cantrips_known = 0
            self.max_spell_slots = 0
            self.curr_spell_slots = 0
            self.max_preparable_spells = 0
            self.spells_known_list = []

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
            await asyncio.sleep(1)
            await self.update_stat_ch(i)

    def update_stats_modifiers(self):
        for i in range(len(self.stats_modifiers)):
            self.stats_modifiers[i] = (self.total_stats[i] - 10) // 2

    def update_armor_class(self):
        if self.equipped_armor is None:
            self.armor_class = 10 + self.stats_modifiers[1]
        else:
            self.armor_class = self.equipped_armor.armor_class

            if self.equipped_armor.armor_type == ArmorType.LIGHT:
                self.armor_class += self.stats_modifiers[1]
            elif self.equipped_armor.armor_type == ArmorType.MEDIUM:
                self.armor_class += min(self.stats_modifiers[1], 2)

        if self.has_shield:
            self.armor_class += 2

    def update_max_hit_points(self):
        self.maxHitPoints = self.adv_class.get_hit_dice().throw() + self.stats_modifiers[2]

        self.currHitPoints = self.maxHitPoints

    def heal(self, heal_amount: int):
        self.currHitPoints += heal_amount

        if self.currHitPoints > self.maxHitPoints:
            self.currHitPoints = self.maxHitPoints

    def get_info(self) -> str:
        res = f"{self.member.mention} - {self.member.display_name}\n"

        res += f"Is adventurer: {self.isAdventurer}\n"
        res += f"Is DM: {self.isDM}\n"

        if self.isAdventurer:
            res += "Inventory: "

            for item in self.inventory:
                res += f"{item} - {self.inventory.get(item)}; "

            res += "\n"

            if self.equipped_weapon is not None:
                res += f"Equipped weapon: {self.equipped_weapon.name}\n"

            if self.equipped_armor is not None:
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

            res += f"Hit points: {self.currHitPoints}/{self.maxHitPoints}\n"

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

        self.maxHitPoints += max(1, self.adv_class.get_hit_dice().throw() + self.stats_modifiers[2])

        self.proficiency_bonus = (self.level - 1) // 4 + 2

        self.update_armor_class()

    def update_max_inventory_weight(self):
        self.max_inventory_weight = 15 * self.total_stats[0]

    def update_curr_inventory_weight(self):
        for item in self.inventory.keys():
            self.curr_inventory_weight += item.weight * self.inventory.get(item)

    def get_inventory_str(self) -> str:
        if len(self.inventory) == 0:
            return "No items in inventory"

        res = "Inventory:\n"

        for item in self.inventory.keys():
            res += f"{item} -> {self.inventory.get(item)}\n"

        return res

    def get_equipment_str(self) -> str:
        res = ""

        weapon_str = "No weapon equipped\n"
        armor_str = "No armor equipped\n"

        if self.equipped_weapon is not None:
            weapon_str = f"Weapon: {self.equipped_weapon.name}\n"

        if self.equipped_armor is not None:
            armor_str = f"Armor: {self.equipped_armor.name}\n"

        res += weapon_str
        res += armor_str

        return res

    def get_known_spells_str(self) -> str:
        if len(self.spells_known_list) == 0:
            return "No known spells"

        res = "Known spells:\n"

        for spell in self.spells_known_list:
            res += f"- {spell}\n"

        return res

    def get_prepared_spells_str(self) -> str:
        if len(self.prepared_spells) == 0:
            return "No prepared spells"

        res = "Prepared spells:\n"

        for spell in self.prepared_spells:
            res += f"- {spell}\n"

        return res

    def update_total_speed(self):
        self.total_speed = self.race_speed - self.speed_debuff

    def remove_item_from_inv(self, item_name: str, amount: int):
        if item_name in self.inventory.keys():
            self.inventory.update({item_name: self.inventory.get(item_name) - amount})

            if self.inventory[item_name] <= 0:
                self.inventory.pop(item_name)

    def add_item_to_inv(self, item_name: str, amount: int):
        if item_name in self.inventory.keys():
            self.inventory.update({item_name: self.inventory.get(item_name) + amount})
        else:
            self.inventory.update({item_name: amount})
