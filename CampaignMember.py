import discord


class CampaignMember:
    member: discord.Member

    isAdventurer: bool = False
    isDM: bool = False

    # Display only stats channels
    STR_ch: discord.VoiceChannel = None
    DEX_ch: discord.VoiceChannel = None
    CON_ch: discord.VoiceChannel = None
    INT_ch: discord.VoiceChannel = None
    WIS_ch: discord.VoiceChannel = None
    CHA_ch: discord.VoiceChannel = None

    # Stats
    total_stats: [int] = [0, 0, 0, 0, 0, 0]

    rolled_stats: [int] = [0, 0, 0, 0, 0, 0]

    race_stats: [int] = [0, 0, 0, 0, 0, 0]

    class_stats: [int] = [0, 0, 0, 0, 0, 0]

    equip_stats: [int] = [0, 0, 0, 0, 0, 0]

    stats_set_num: int = -1
    stats_set_bools = [False, False, False, False, False, False]

    roll_list = []

    def update_total_stat(self, stat_index: int):
        self.total_stats[stat_index] = self.rolled_stats[stat_index] + self.race_stats[stat_index] + self.class_stats[stat_index] + self.equip_stats[stat_index]

    def update_all_total_stat(self):
        for stat_index in range(len(self.total_stats)):
            self.total_stats[stat_index] = self.rolled_stats[stat_index] + self.race_stats[stat_index] + self.class_stats[stat_index] + self.equip_stats[stat_index]

    async def update_stat_ch(self, stat_index: int):
        if stat_index == 0:
            await self.STR_ch.edit(name=f'STR = {self.total_stats[stat_index]}')
        elif stat_index == 1:
            await self.DEX_ch.edit(name=f'DEX = {self.total_stats[stat_index]}')
        elif stat_index == 2:
            await self.CON_ch.edit(name=f'CON = {self.total_stats[stat_index]}')
        elif stat_index == 3:
            await self.INT_ch.edit(name=f'INT = {self.total_stats[stat_index]}')
        elif stat_index == 4:
            await self.WIS_ch.edit(name=f'WIS = {self.total_stats[stat_index]}')
        elif stat_index == 5:
            await self.CHA_ch.edit(name=f'CHA = {self.total_stats[stat_index]}')

    async def update_all_stat_ch(self):
        await self.update_stat_ch(0)
        await self.update_stat_ch(1)
        await self.update_stat_ch(2)
        await self.update_stat_ch(3)
        await self.update_stat_ch(4)
        await self.update_stat_ch(5)
