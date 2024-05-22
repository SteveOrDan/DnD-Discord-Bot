from CampaignMember import *


def get_user(member: discord.Member) -> CampaignMember | None:
    for user in costants.curr_campaign.campaign_member_list:
        if user.member.id == member.id:
            return user
    return None


def select_race(interaction: discord.Interaction, race: RaceTypeEnum):
    curr_user = get_user(interaction.user)

    if curr_user is None:
        interaction.response.send_message("User not found", ephemeral=True, delete_after=5)
        return

    curr_user.race = race


class RaceView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Dwarf", style=discord.ButtonStyle.red, custom_id='dwarf_button')
    async def dwarf(self, interaction: discord.Interaction, button: discord.Button):
        select_race(interaction, RaceTypeEnum.DWARF)

        await interaction.response.send_message("Selected dwarf", ephemeral=True)

    @discord.ui.button(label="Hill Dwarf", style=discord.ButtonStyle.red, custom_id='hill_dwarf_button')
    async def hill_dwarf(self, interaction: discord.Interaction, button: discord.Button):
        select_race(interaction, RaceTypeEnum.HILL_DWARF)

        await interaction.response.send_message("Selected hill dwarf", ephemeral=True)

    @discord.ui.button(label="Mountain Dwarf", style=discord.ButtonStyle.red, custom_id='mountain_dwarf_button')
    async def mountain_dwarf(self, interaction: discord.Interaction, button: discord.Button):
        select_race(interaction, RaceTypeEnum.MOUNTAIN_DWARF)

        await interaction.response.send_message("Selected mountain dwarf", ephemeral=True)

    @discord.ui.button(label="Elf", style=discord.ButtonStyle.green, custom_id='elf_button')
    async def elf(self, interaction: discord.Interaction, button: discord.Button):
        select_race(interaction, RaceTypeEnum.ELF)

        await interaction.response.send_message("Selected elf", ephemeral=True)

    @discord.ui.button(label="High Elf", style=discord.ButtonStyle.green, custom_id='high_elf_button')
    async def high_elf(self, interaction: discord.Interaction, button: discord.Button):
        select_race(interaction, RaceTypeEnum.HIGH_ELF)

        await interaction.response.send_message("Selected high elf", ephemeral=True)

    @discord.ui.button(label="Wood Elf", style=discord.ButtonStyle.green, custom_id='wood_elf_button')
    async def wood_elf(self, interaction: discord.Interaction, button: discord.Button):
        select_race(interaction, RaceTypeEnum.WOOD_ELF)

        await interaction.response.send_message("Selected wood elf", ephemeral=True)

    @discord.ui.button(label="Halfling", style=discord.ButtonStyle.grey, custom_id='halfling_button')
    async def halfling(self, interaction: discord.Interaction, button: discord.Button):
        select_race(interaction, RaceTypeEnum.HALFLING)

        await interaction.response.send_message("Selected halfling", ephemeral=True)

    @discord.ui.button(label="Stout", style=discord.ButtonStyle.grey, custom_id='stout_button')
    async def stout(self, interaction: discord.Interaction, button: discord.Button):
        select_race(interaction, RaceTypeEnum.STOUT)

        await interaction.response.send_message("Selected stout", ephemeral=True)

    @discord.ui.button(label="Lightfoot", style=discord.ButtonStyle.grey, custom_id='lightfoot_button')
    async def lightfoot(self, interaction: discord.Interaction, button: discord.Button):
        select_race(interaction, RaceTypeEnum.LIGHTFOOT)

        await interaction.response.send_message("Selected lightfoot", ephemeral=True)

    @discord.ui.button(label="Human", style=discord.ButtonStyle.blurple, custom_id='human_button')
    async def human(self, interaction: discord.Interaction, button: discord.Button):
        select_race(interaction, RaceTypeEnum.LIGHTFOOT)

        await interaction.response.send_message("Selected human", ephemeral=True)
