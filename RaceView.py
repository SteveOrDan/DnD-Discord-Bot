import discord
import costants
import CampaignMember
from data.StatTypeEnum import StatTypeEnum


class RaceView(discord.ui.View):
    def __init__(self, guild: discord.Guild):
        super().__init__()
        self.guild = guild

    @staticmethod
    async def get_campaign_member(interaction: discord.Interaction):
        for member in costants.curr_campaign.campaign_member_list:
            if member.member.id == interaction.user.id:
                return member

        return None

    @staticmethod
    async def reset_race_stats(campaign_member: CampaignMember):
        for stat in campaign_member.race_stats:
            stat = 0

    async def select(self, role: discord.Role, interaction: discord.Interaction):
        if interaction.user.id in costants.curr_campaign.players_selected_race:
            race_roles = [self.guild.get_role(costants.DWARF_ROLE_ID),
                          self.guild.get_role(costants.HILL_DWARF_ROLE_ID),
                          self.guild.get_role(costants.MOUNTAIN_DWARF_ROLE_ID),
                          self.guild.get_role(costants.ELF_ROLE_ID),
                          self.guild.get_role(costants.HIGH_ELF_ROLE_ID),
                          self.guild.get_role(costants.WOOD_ELF_ROLE_ID),
                          self.guild.get_role(costants.HALFLING_ROLE_ID),
                          self.guild.get_role(costants.STOUT_ROLE_ID),
                          self.guild.get_role(costants.LIGHTFOOT_ROLE_ID),
                          self.guild.get_role(costants.HUMAN_ROLE_ID)]

            for old_role in race_roles:
                if old_role in interaction.user.roles:
                    await interaction.user.remove_roles(old_role)

            await interaction.user.add_roles(role)

        else:
            costants.curr_campaign.players_selected_race.append(interaction.user.id)
            await interaction.user.add_roles(role)

    @discord.ui.button(label="Dwarf", style=discord.ButtonStyle.red)
    async def dwarf(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected dwarf", ephemeral=True, delete_after=5)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            await self.reset_race_stats(curr_user)
            curr_user.race_stats[StatTypeEnum.CON.value] = 2

            curr_user.update_total_stat(StatTypeEnum.CON.value)
            await curr_user.update_stat_ch(StatTypeEnum.CON.value)

        await self.select(role=self.guild.get_role(costants.DWARF_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="Hill Dwarf", style=discord.ButtonStyle.red)
    async def hill_dwarf(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected hill dwarf", ephemeral=True, delete_after=5)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            await self.reset_race_stats(curr_user)
            curr_user.race_stats[StatTypeEnum.CON.value] = 2
            curr_user.race_stats[StatTypeEnum.WIS.value] = 1

            curr_user.update_total_stat(StatTypeEnum.CON.value)
            await curr_user.update_stat_ch(StatTypeEnum.CON.value)

            curr_user.update_total_stat(StatTypeEnum.WIS.value)
            await curr_user.update_stat_ch(StatTypeEnum.WIS.value)

        await self.select(role=self.guild.get_role(costants.HILL_DWARF_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="Mountain Dwarf", style=discord.ButtonStyle.red)
    async def mountain_dwarf(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected mountain dwarf", ephemeral=True)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            await self.reset_race_stats(curr_user)
            curr_user.race_stats[StatTypeEnum.CON.value] = 2
            curr_user.race_stats[StatTypeEnum.STR.value] = 2

            curr_user.update_total_stat(StatTypeEnum.CON.value)
            await curr_user.update_stat_ch(StatTypeEnum.CON.value)

            curr_user.update_total_stat(StatTypeEnum.STR.value)
            await curr_user.update_stat_ch(StatTypeEnum.STR.value)

        await self.select(role=self.guild.get_role(costants.MOUNTAIN_DWARF_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="Elf", style=discord.ButtonStyle.green)
    async def elf(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected elf", ephemeral=True)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            await self.reset_race_stats(curr_user)
            curr_user.race_stats[StatTypeEnum.DEX.value] = 2

            curr_user.update_total_stat(StatTypeEnum.DEX.value)
            await curr_user.update_stat_ch(StatTypeEnum.DEX.value)

        await self.select(role=self.guild.get_role(costants.ELF_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="High Elf", style=discord.ButtonStyle.green)
    async def high_elf(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected high elf", ephemeral=True)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            await self.reset_race_stats(curr_user)
            curr_user.race_stats[StatTypeEnum.DEX.value] = 2
            curr_user.race_stats[StatTypeEnum.INT.value] = 1

            curr_user.update_total_stat(StatTypeEnum.DEX.value)
            await curr_user.update_stat_ch(StatTypeEnum.DEX.value)

            curr_user.update_total_stat(StatTypeEnum.INT.value)
            await curr_user.update_stat_ch(StatTypeEnum.INT.value)

        await self.select(role=self.guild.get_role(costants.HIGH_ELF_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="Wood Elf", style=discord.ButtonStyle.green)
    async def wood_elf(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected wood elf", ephemeral=True)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            await self.reset_race_stats(curr_user)
            curr_user.race_stats[StatTypeEnum.DEX.value] = 2
            curr_user.race_stats[StatTypeEnum.WIS.value] = 1

            curr_user.update_total_stat(StatTypeEnum.DEX.value)
            await curr_user.update_stat_ch(StatTypeEnum.DEX.value)

            curr_user.update_total_stat(StatTypeEnum.WIS.value)
            await curr_user.update_stat_ch(StatTypeEnum.WIS.value)

        await self.select(role=self.guild.get_role(costants.WOOD_ELF_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="Halfling", style=discord.ButtonStyle.grey)
    async def halfling(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected halfling", ephemeral=True)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            await self.reset_race_stats(curr_user)
            curr_user.race_stats[StatTypeEnum.DEX.value] = 2

            curr_user.update_total_stat(StatTypeEnum.DEX.value)
            await curr_user.update_stat_ch(StatTypeEnum.DEX.value)

        await self.select(role=self.guild.get_role(costants.HALFLING_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="Stout", style=discord.ButtonStyle.grey)
    async def stout(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected stout", ephemeral=True)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            await self.reset_race_stats(curr_user)
            curr_user.race_stats[StatTypeEnum.DEX.value] = 2
            curr_user.race_stats[StatTypeEnum.CON.value] = 1

            curr_user.update_total_stat(StatTypeEnum.DEX.value)
            await curr_user.update_stat_ch(StatTypeEnum.DEX.value)

            curr_user.update_total_stat(StatTypeEnum.CON.value)
            await curr_user.update_stat_ch(StatTypeEnum.CON.value)

        await self.select(role=self.guild.get_role(costants.STOUT_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="Lightfoot", style=discord.ButtonStyle.grey)
    async def lightfoot(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected lightfoot", ephemeral=True)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            await self.reset_race_stats(curr_user)
            curr_user.race_stats[StatTypeEnum.DEX.value] = 2
            curr_user.race_stats[StatTypeEnum.CHA.value] = 1

            curr_user.update_total_stat(StatTypeEnum.DEX.value)
            await curr_user.update_stat_ch(StatTypeEnum.DEX.value)

            curr_user.update_total_stat(StatTypeEnum.CHA.value)
            await curr_user.update_stat_ch(StatTypeEnum.CHA.value)

        await self.select(role=self.guild.get_role(costants.LIGHTFOOT_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="Human", style=discord.ButtonStyle.blurple)
    async def human(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected human", ephemeral=True)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            await self.reset_race_stats(curr_user)
            curr_user.race_stats[StatTypeEnum.STR.value] = 1
            curr_user.race_stats[StatTypeEnum.DEX.value] = 1
            curr_user.race_stats[StatTypeEnum.CON.value] = 1
            curr_user.race_stats[StatTypeEnum.INT.value] = 1
            curr_user.race_stats[StatTypeEnum.WIS.value] = 1
            curr_user.race_stats[StatTypeEnum.CHA.value] = 1

            curr_user.update_all_total_stat()
            await curr_user.update_all_stat_ch()

        await self.select(role=self.guild.get_role(costants.HUMAN_ROLE_ID), interaction=interaction)
        