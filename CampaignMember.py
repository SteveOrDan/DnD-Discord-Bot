import discord
import enum

from data.Items import ItemsDataBase
from data.Items.Armor import ArmorType
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


class CampaignMember:
    member: discord.Member

    isAdventurer: bool = False
    isDM: bool = False

    race: str
    alignment: str
    background: str
    traits: str
    ideals: str
    bonds: str
    flaws: str

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

    class_stats: [int] = [0, 0, 0, 0, 0, 0]

    equip_stats: [int] = [0, 0, 0, 0, 0, 0]

    stats_set_num: int = -1
    stats_set_bools = [False, False, False, False, False, False]

    roll_list: [int]

    purse: Purse

    def update_total_stat(self, stat_index: int):
        self.total_stats[stat_index] = self.rolled_stats[stat_index] + self.race_stats[stat_index] + self.class_stats[stat_index] + self.equip_stats[stat_index]

    def update_all_total_stat(self):
        for stat_index in range(len(self.total_stats)):
            self.total_stats[stat_index] = self.rolled_stats[stat_index] + self.race_stats[stat_index] + self.class_stats[stat_index] + self.equip_stats[stat_index]

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

    def equip_armor(self, armor: str):
        currArmor = ItemsDataBase.armors.get(armor)

        if currArmor is None:
            return

        self.armor_class = currArmor.armor_class

        if currArmor.armor_type == ArmorType.LIGHT:
            self.armor_class += self.stats_modifiers[1]
        elif currArmor.armor_type == ArmorType.MEDIUM:
            self.armor_class += min(self.stats_modifiers[1], 2)
