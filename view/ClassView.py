from data.CampaignMember import *


def get_user(member: discord.Member) -> CampaignMember | None:
    for user in costants.curr_campaign.campaign_member_list:
        if user.member.id == member.id:
            return user
    return None


def select(adv_class: AdvClass, interaction: discord.Interaction):
    curr_user = get_user(interaction.user)

    if curr_user is None:
        interaction.response.send_message("User not found", ephemeral=True, delete_after=5)
        return

    curr_user.adv_class = adv_class


class ClassView(discord.ui.View):
    def __init__(self, guild: discord.Guild):
        super().__init__(timeout=None)
        self.guild = guild

    @discord.ui.button(label="Cleric", style=discord.ButtonStyle.green, custom_id='cleric_button')
    async def cleric(self, interaction: discord.Interaction, button: discord.Button):
        select(adv_class=AdvClass.CLERIC, interaction=interaction)

        await interaction.response.send_message(f"You selected Cleric class", ephemeral=True)

        # self.stop()

    @discord.ui.button(label="Fighter", style=discord.ButtonStyle.red, custom_id='fighter_button')
    async def fighter(self, interaction: discord.Interaction, button: discord.Button):
        select(adv_class=AdvClass.FIGHTER, interaction=interaction)

        await interaction.response.send_message(f"You selected Fighter class", ephemeral=True)

        # self.stop()

    @discord.ui.button(label="Rogue", style=discord.ButtonStyle.gray, custom_id='rogue_button')
    async def rogue(self, interaction: discord.Interaction, button: discord.Button):
        select(adv_class=AdvClass.ROGUE, interaction=interaction)

        await interaction.response.send_message(f"You selected Rogue class", ephemeral=True)

        # self.stop()

    @discord.ui.button(label="Wizard", style=discord.ButtonStyle.blurple, custom_id='wizard_button')
    async def wizard(self, interaction: discord.Interaction, button: discord.Button):
        select(adv_class=AdvClass.WIZARD, interaction=interaction)

        await interaction.response.send_message(f"You selected Wizard class", ephemeral=True)

        # self.stop()
