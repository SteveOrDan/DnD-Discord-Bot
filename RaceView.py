import discord
import costants
import enum
from CampaignMember import CampaignMember, StatTypeEnum


class RaceTypeEnum(enum.Enum):
    DWARF = ("dwarf", 0, 0, 2, 0, 0, 0, costants.DWARF_ROLE_ID)
    HILL_DWARF = ("hill dwarf", 0, 0, 2, 1, 0, 0, costants.HILL_DWARF_ROLE_ID)
    MOUNTAIN_DWARF = ("mountain dwarf", 2, 0, 2, 0, 0, 0, costants.MOUNTAIN_DWARF_ROLE_ID)
    ELF = ("elf", 0, 2, 0, 0, 0, 0, costants.ELF_ROLE_ID)
    HIGH_ELF = ("high elf", 0, 2, 0, 1, 0, 0, costants.HIGH_ELF_ROLE_ID)
    WOOD_ELF = ("wood elf", 0, 2, 0, 0, 1, 0, costants.WOOD_ELF_ROLE_ID)
    HALFLING = ("halfling", 0, 2, 0, 0, 0, 0, costants.HALFLING_ROLE_ID)
    STOUT = ("stout", 0, 2, 1, 0, 0, 0, costants.STOUT_ROLE_ID)
    LIGHTFOOT = ("lightfoot", 0, 2, 0, 0, 0, 1, costants.LIGHTFOOT_ROLE_ID)
    HUMAN = ("human", 1, 1, 1, 1, 1, 1, costants.HUMAN_ROLE_ID)

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


class RaceView(discord.ui.View):
    def __init__(self, guild: discord.Guild):
        super().__init__(timeout=None)
        self.guild = guild

    @staticmethod
    async def get_campaign_member(interaction: discord.Interaction):
        for member in costants.curr_campaign.campaign_member_list:
            if member.member.id == interaction.user.id:
                return member

        return None

    @staticmethod
    def set_race(campaign_member: CampaignMember, RaceType: RaceTypeEnum):
        campaign_member.race = RaceType.get_name()

        campaign_member.race_stats[StatTypeEnum.STR.value] = RaceType.get_str()
        campaign_member.race_stats[StatTypeEnum.DEX.value] = RaceType.get_dex()
        campaign_member.race_stats[StatTypeEnum.CON.value] = RaceType.get_con()
        campaign_member.race_stats[StatTypeEnum.INT.value] = RaceType.get_int()
        campaign_member.race_stats[StatTypeEnum.WIS.value] = RaceType.get_wis()
        campaign_member.race_stats[StatTypeEnum.CHA.value] = RaceType.get_cha()

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

    @discord.ui.button(label="Dwarf", style=discord.ButtonStyle.red, custom_id='dwarf_button')
    async def dwarf(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected dwarf", ephemeral=True, delete_after=5)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            self.set_race(curr_user, RaceTypeEnum.DWARF)

            curr_user.update_all_total_stat()
            await curr_user.update_all_stat_ch()

        await self.select(role=self.guild.get_role(costants.DWARF_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="Hill Dwarf", style=discord.ButtonStyle.red, custom_id='hill_dwarf_button')
    async def hill_dwarf(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected hill dwarf", ephemeral=True, delete_after=5)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            self.set_race(curr_user, RaceTypeEnum.HILL_DWARF)

            curr_user.update_all_total_stat()
            await curr_user.update_all_stat_ch()

        await self.select(role=self.guild.get_role(costants.HILL_DWARF_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="Mountain Dwarf", style=discord.ButtonStyle.red, custom_id='mountain_dwarf_button')
    async def mountain_dwarf(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected mountain dwarf", ephemeral=True, delete_after=5)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            self.set_race(curr_user, RaceTypeEnum.MOUNTAIN_DWARF)

            curr_user.update_all_total_stat()
            await curr_user.update_all_stat_ch()

        await self.select(role=self.guild.get_role(costants.MOUNTAIN_DWARF_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="Elf", style=discord.ButtonStyle.green, custom_id='elf_button')
    async def elf(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected elf", ephemeral=True, delete_after=5)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            self.set_race(curr_user, RaceTypeEnum.ELF)

            curr_user.update_all_total_stat()
            await curr_user.update_all_stat_ch()

        await self.select(role=self.guild.get_role(costants.ELF_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="High Elf", style=discord.ButtonStyle.green, custom_id='high_elf_button')
    async def high_elf(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected high elf", ephemeral=True, delete_after=5)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            self.set_race(curr_user, RaceTypeEnum.HIGH_ELF)

            curr_user.update_all_total_stat()
            await curr_user.update_all_stat_ch()

        await self.select(role=self.guild.get_role(costants.HIGH_ELF_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="Wood Elf", style=discord.ButtonStyle.green, custom_id='wood_elf_button')
    async def wood_elf(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected wood elf", ephemeral=True, delete_after=5)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            self.set_race(curr_user, RaceTypeEnum.WOOD_ELF)

            curr_user.update_all_total_stat()
            await curr_user.update_all_stat_ch()

        await self.select(role=self.guild.get_role(costants.WOOD_ELF_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="Halfling", style=discord.ButtonStyle.grey, custom_id='halfling_button')
    async def halfling(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected halfling", ephemeral=True, delete_after=5)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            self.set_race(curr_user, RaceTypeEnum.HALFLING)

            curr_user.update_all_total_stat()
            await curr_user.update_all_stat_ch()

        await self.select(role=self.guild.get_role(costants.HALFLING_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="Stout", style=discord.ButtonStyle.grey, custom_id='stout_button')
    async def stout(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected stout", ephemeral=True, delete_after=5)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            self.set_race(curr_user, RaceTypeEnum.STOUT)

            curr_user.update_all_total_stat()
            await curr_user.update_all_stat_ch()

        await self.select(role=self.guild.get_role(costants.STOUT_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="Lightfoot", style=discord.ButtonStyle.grey, custom_id='lightfoot_button')
    async def lightfoot(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected lightfoot", ephemeral=True, delete_after=5)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            self.set_race(curr_user, RaceTypeEnum.LIGHTFOOT)

            curr_user.update_all_total_stat()
            await curr_user.update_all_stat_ch()

        await self.select(role=self.guild.get_role(costants.LIGHTFOOT_ROLE_ID), interaction=interaction)

    @discord.ui.button(label="Human", style=discord.ButtonStyle.blurple, custom_id='human_button')
    async def human(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Selected human", ephemeral=True, delete_after=5)

        curr_user = await self.get_campaign_member(interaction)

        if curr_user is not None:
            self.set_race(curr_user, RaceTypeEnum.HUMAN)

            curr_user.update_all_total_stat()
            await curr_user.update_all_stat_ch()

        await self.select(role=self.guild.get_role(costants.HUMAN_ROLE_ID), interaction=interaction)
