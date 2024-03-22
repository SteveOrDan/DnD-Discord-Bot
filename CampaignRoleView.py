import discord
import Campaign
import costants


class CampaignRoleView(discord.ui.View):
    def __init__(self, campaign: Campaign):
        super().__init__(timeout=None)
        self.campaign = campaign

    @discord.ui.button(label="Dungeon Master", style=discord.ButtonStyle.blurple, custom_id='dm_button')
    async def dm_button(self, interaction: discord.Interaction, button: discord.Button):
        curr_user = None
        for campaignMember in costants.curr_campaign.campaign_member_list:
            if campaignMember.member.id == interaction.user.id:
                curr_user = campaignMember

        if curr_user is None:
            await interaction.channel.send("No user found")
            return

        if self.campaign.has_dm_already:

            if curr_user.isAdventurer:
                await interaction.response.send_message("There is already a Dungeon Master and you are an Adventurer.", ephemeral=True, delete_after=5)
                return
            elif curr_user.isDM:
                await interaction.response.send_message(f"You already are the Dungeon Master.", ephemeral=True, delete_after=5)
                return

            await interaction.response.send_message("There is already a Dungeon Master, choose the Adventurer role.", ephemeral=True, delete_after=5)

            return

        if curr_user.isAdventurer:
            curr_user.isAdventurer = False
            curr_user.isDM = True
            await interaction.response.send_message(
                "You switched from Adventurer to Dungeon Master role.",
                ephemeral=True, delete_after=5)

            self.campaign.has_dm_already = True

            return

        curr_user.isDM = True
        await interaction.response.send_message("You have selected Dungeon Master role.", ephemeral=True, delete_after=5)

        self.campaign.has_dm_already = True
        self.campaign.add_ready_player()

        msg = await interaction.channel.fetch_message(self.campaign.PLAYER_NUM_MSG_ID)
        await msg.edit(content=f"{self.campaign.ready_players_num} / {self.campaign.players_num} players are ready.")

        # self.stop()

    @discord.ui.button(label="Adventurer", style=discord.ButtonStyle.green, custom_id='adventurer_button')
    async def adventurer_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        curr_user = None
        for campaignMember in costants.curr_campaign.campaign_member_list:
            if campaignMember.member.id == interaction.user.id:
                curr_user = campaignMember

        if curr_user is None:
            await interaction.channel.send("No user found")
            return

        if curr_user.isDM:
            self.campaign.has_dm_already = False

            curr_user.isDM = False
            curr_user.isAdventurer = True

            await interaction.response.send_message("You switched from Dungeon Master to Adventurer role", ephemeral=True, delete_after=5)

            return

        elif curr_user.isAdventurer:
            await interaction.response.send_message("You have already selected the Adventurer role", ephemeral=True, delete_after=5)

            return

        await interaction.response.send_message("You have selected Adventurer role", ephemeral=True, delete_after=5)

        curr_user.isAdventurer = True

        self.campaign.add_ready_player()

        msg = await interaction.channel.fetch_message(self.campaign.PLAYER_NUM_MSG_ID)
        await msg.edit(content=f"{self.campaign.ready_players_num} / {self.campaign.players_num} players are ready.")

        # self.stop()
    