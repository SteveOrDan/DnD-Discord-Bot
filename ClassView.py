import discord
import Campaign
import costants


class ClassView(discord.ui.View):
    def __init__(self, guild: discord.Guild):
        super().__init__(timeout=None)
        self.guild = guild

    @discord.ui.button(label="Cleric", style=discord.ButtonStyle.green)
    async def cleric(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.channel.send(f"You selected Cleric class")

        await self.select(role_id=costants.CLERIC_ROLE_ID, interaction=interaction)

        # self.stop()

    @discord.ui.button(label="Fighter", style=discord.ButtonStyle.red)
    async def fighter(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.channel.send(f"You selected Fighter class")

        await self.select(role_id=costants.FIGHTER_ROLE_ID, interaction=interaction)

        # self.stop()

    @discord.ui.button(label="Rogue", style=discord.ButtonStyle.gray)
    async def rogue(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.channel.send(f"You selected Rogue class")

        await self.select(role_id=costants.ROGUE_ROLE_ID, interaction=interaction)

        # self.stop()

    @discord.ui.button(label="Wizard", style=discord.ButtonStyle.blurple)
    async def wizard(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.channel.send(f"You selected Wizard class")

        await self.select(role_id=costants.WIZARD_ROLE_ID, interaction=interaction)

        # self.stop()

    async def select(self, role_id: int, interaction: discord.Interaction):
        if interaction.user.id in costants.curr_campaign.players_selected_class:
            class_roles = [self.guild.get_role(costants.CLERIC_ROLE_ID),
                           self.guild.get_role(costants.FIGHTER_ROLE_ID),
                           self.guild.get_role(costants.ROGUE_ROLE_ID),
                           self.guild.get_role(costants.WIZARD_ROLE_ID)]

            for old_role in class_roles:
                if old_role in interaction.user.roles:
                    await interaction.user.remove_roles(old_role)

            await interaction.user.add_roles(self.guild.get_role(role_id))

        else:
            costants.curr_campaign.players_selected_class.append(interaction.user.id)
            await interaction.user.add_roles(self.guild.get_role(role_id))
            