import discord
import costants
from CampaignMember import AdvClass


class ClassView(discord.ui.View):
    def __init__(self, guild: discord.Guild):
        super().__init__(timeout=None)
        self.guild = guild

    @discord.ui.button(label="Cleric", style=discord.ButtonStyle.green, custom_id='cleric_button')
    async def cleric(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message(f"You selected Cleric class", ephemeral=True, delete_after=5)

        await self.select(adv_class=AdvClass.CLERIC, interaction=interaction)

        # self.stop()

    @discord.ui.button(label="Fighter", style=discord.ButtonStyle.red, custom_id='fighter_button')
    async def fighter(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message(f"You selected Fighter class", ephemeral=True, delete_after=5)

        await self.select(adv_class=AdvClass.FIGHTER, interaction=interaction)

        # self.stop()

    @discord.ui.button(label="Rogue", style=discord.ButtonStyle.gray, custom_id='rogue_button')
    async def rogue(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message(f"You selected Rogue class", ephemeral=True, delete_after=5)

        await self.select(adv_class=AdvClass.ROGUE, interaction=interaction)

        # self.stop()

    @discord.ui.button(label="Wizard", style=discord.ButtonStyle.blurple, custom_id='wizard_button')
    async def wizard(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message(f"You selected Wizard class", ephemeral=True, delete_after=5)

        await self.select(adv_class=AdvClass.WIZARD, interaction=interaction)

        # self.stop()

    async def select(self, adv_class: AdvClass, interaction: discord.Interaction):
        if interaction.user.id in costants.curr_campaign.players_selected_class:
            class_roles = [self.guild.get_role(costants.CLERIC_ROLE_ID),
                           self.guild.get_role(costants.FIGHTER_ROLE_ID),
                           self.guild.get_role(costants.ROGUE_ROLE_ID),
                           self.guild.get_role(costants.WIZARD_ROLE_ID)]

            for old_role in class_roles:
                if old_role in interaction.user.roles:
                    await interaction.user.remove_roles(old_role)

            await interaction.user.add_roles(self.guild.get_role(adv_class.get_role_id()))

        else:
            costants.curr_campaign.players_selected_class.append(interaction.user.id)
            await interaction.user.add_roles(self.guild.get_role(adv_class.get_role_id()))

        curr_user = None

        for user in costants.curr_campaign.campaign_member_list:
            if user.member.id == interaction.user.id:
                curr_user = user

        if curr_user is None:
            return

        curr_user.saving_throw_proficiencies = adv_class.get_saving_throws()
        curr_user.armor_proficiencies = adv_class.get_armor_proficiencies()
        curr_user.weapon_proficiencies = adv_class.get_weapon_proficiencies()
        curr_user.class_proficiencies = adv_class.get_class_proficiencies()

        curr_user.adv_class = adv_class
            