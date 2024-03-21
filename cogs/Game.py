import discord
from discord.ext import commands
import CampaignRoleView
import Campaign
from ClassView import ClassView
from RaceView import RaceView
from data.CampaignState import CampaignState
import CampaignMember
import random

import costants
from data.StatTypeEnum import StatTypeEnum


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Create campaign
    @commands.command(help="# Create campaign (at least 3 members)")
    async def cc(self, ctx, *arr: discord.Member):
        if ctx.message.channel.id == costants.GENERAL_CHAT_ID:
            if len(arr) < 3 or len(arr) > 6:
                await ctx.send("Need at least 3 and less than 7 people to create a campaign")
                return

            guild = ctx.guild

            # Set campaign object
            costants.curr_campaign = Campaign.Campaign(user_num=len(arr), guild_id=guild.id)

            # Assign campaign and user roles
            for user in arr:
                await user.add_roles(guild.get_role(costants.CAMPAIGN_ROLE_ID))
                await user.add_roles(guild.get_role(costants.CHOOSING_ROLE_ROLE_ID))
                await self.add_member_to_campaign(ctx=ctx, member=user)

            set_roles_ch = guild.get_channel(costants.SET_ROLES_CHAT_ID)

            new_msg = await set_roles_ch.send(
                f"{costants.curr_campaign.ready_players_num} / {costants.curr_campaign.players_num} players are ready.")

            costants.curr_campaign.PLAYER_NUM_MSG_ID = new_msg.id

            # Set the view for the roles
            view = CampaignRoleView.CampaignRoleView(costants.curr_campaign)
            await set_roles_ch.send(
                "Choose your role in the campaign, then type !sc to begin when all players are ready.", view=view)
            await view.wait()

    @staticmethod
    # Creates CampaignMember object and adds it to the campaign's list of users and give him a special user role (saved attributes: member, member_Role)
    async def add_member_to_campaign(ctx, member: discord.Member):
        new_user = CampaignMember.CampaignMember()

        new_user.member = member

        costants.curr_campaign.campaign_member_list.append(new_user)

    @commands.command(help="# Start campaign")
    # @commands.has_role("choosing role")
    async def sc(self, ctx):
        if costants.curr_campaign is not None and costants.curr_campaign.check_if_can_start_campaign():
            await ctx.send("Preparing character creation...\n")

            costants.curr_campaign.campaign_state = CampaignState.BUILDING_CHARACTER

            guild = ctx.guild

            for campaignMember in costants.curr_campaign.campaign_member_list:
                await campaignMember.member.remove_roles(guild.get_role(costants.CHOOSING_ROLE_ROLE_ID))
                if campaignMember.isAdventurer:
                    await campaignMember.member.add_roles(guild.get_role(costants.ADVENTURER_ROLE_ID))
                    await campaignMember.member.add_roles(guild.get_role(costants.BUILDING_CHARACTER_ROLE_ID))
                elif campaignMember.isDM:
                    await campaignMember.member.add_roles(guild.get_role(costants.DM_ROLE_ID))
                else:
                    await ctx.channel.send(f"Error: User {campaignMember.member} is neither Adventurer nor DM.")

            # Fill race-info channel
            await guild.get_channel(costants.RACE_INFO_CHAT_ID).send(
                "There are 4 core races available. Some of them also have subraces.\n"
                "Type !<race_name> or !<subrace_name> to get more info about them.\n"
                "Type !info to get access to the rulebook.")

            # Fill class-info channel
            await guild.get_channel(costants.CLASS_INFO_CHAT_ID).send(
                "There are 4 classes available. Type !<class_name> to get the handbook references to that class")

            race_view = RaceView(ctx.guild)
            await guild.get_channel(costants.SET_RACE_CHAT_ID).send("Choose your race", view=race_view)

            class_view = ClassView(ctx.guild)
            await guild.get_channel(costants.SET_CLASS_CHAT_ID).send("Choose your class", view=class_view)

            # Give players role
            i = 0
            for user in costants.curr_campaign.campaign_member_list:
                if user.isAdventurer:
                    await user.member.add_roles(ctx.guild.get_role(costants.PLAYER_ROLES_ID[i]))
                    user.STR_ch = ctx.guild.get_channel(costants.PLAYERS_STR_STAT_CH_ID[i])
                    user.DEX_ch = ctx.guild.get_channel(costants.PLAYERS_DEX_STAT_CH_ID[i])
                    user.CON_ch = ctx.guild.get_channel(costants.PLAYERS_CON_STAT_CH_ID[i])
                    user.INT_ch = ctx.guild.get_channel(costants.PLAYERS_INT_STAT_CH_ID[i])
                    user.WIS_ch = ctx.guild.get_channel(costants.PLAYERS_WIS_STAT_CH_ID[i])
                    user.CHA_ch = ctx.guild.get_channel(costants.PLAYERS_CHA_STAT_CH_ID[i])
                    i += 1

        else:
            await ctx.send("Not all players are ready or there is no Dungeon Master")

    @commands.command()
    async def info(self, ctx):
        embed_info = discord.Embed(title="Basic Rules book download link",
                                    url="https://dnd.wizards.com/what-is-dnd/basic-rules")
        await ctx.channel.send(embed=embed_info)

    # Generate a random number as the sum of the 3 highest rolls of 4 d6
    @staticmethod
    def roll_stat():
        stat = []
        res = 0

        for i in range(4):
            stat.append(random.randint(1, 6))
            res += stat[i]

        res -= min(stat)
        return res

    # Generates the 6 stats for the user that uses the command, saves them and show them in the channels' name
    @commands.has_role("Adventurer")
    @commands.command()
    async def roll(self, ctx):
        if ctx.channel.name == "roll-stats":
            stats = []
            for i in range(6):
                stats.append(self.roll_stat())
                await ctx.send(f"Roll {i}: {stats[i]}")

            curr_user = None
            for campaignMember in costants.curr_campaign.campaign_member_list:
                if campaignMember.member.id == ctx.author.id:
                    curr_user = campaignMember

            if curr_user is None:
                await ctx.send("No user found")
                return
            await ctx.send("User found")

            curr_user.roll_list.clear()

            for stat in stats:
                curr_user.roll_list.append(stat)

            curr_user.stats_set_num = 0
            curr_user.stats_set_bools = [False, False, False, False, False, False]
            curr_user.stats_set_name.clear()

            await ctx.send(f"Use !set <STAT_NAME> to set each stat when you get asked.\n"
                           "STAT_NAME must be one of the 6 shown on the left.\n"
                           f"Which skill would you like to set to {curr_user.roll_list[curr_user.stats_set_num]}?")

        else:
            await ctx.channel.send("You can roll for stats only in the roll-stats channel")

    @commands.has_role("Adventurer")
    @commands.command()
    async def default_stats(self, ctx):
        if ctx.channel.name == "roll-stats":
            curr_user = None
            for campaignMember in costants.curr_campaign.campaign_member_list:
                if campaignMember.member.id == ctx.author.id:
                    curr_user = campaignMember

            if curr_user is None:
                await ctx.send("No user found")
                return
            await ctx.send("User found")

            curr_user.roll_list.clear()

            curr_user.roll_list = [15, 14, 13, 12, 10, 8]

            for i in range(6):
                await ctx.send(f"Stat {i}: {curr_user.roll_list[i]}")

            curr_user.stats_set_num = 0
            curr_user.stats_set_bools = [False, False, False, False, False, False]
            curr_user.stats_set_name.clear()

            await ctx.send(f"Use !set <STAT_NAME> to set each stat when you get asked.\n"
                           "STAT_NAME must be one of the 6 shown on the left.\n"
                           f"Which skill would you like to set to {curr_user.roll_list[curr_user.stats_set_num]}?")

        else:
            await ctx.channel.send("You can roll for stats only in the roll-stats channel")

    @commands.has_role("Adventurer")
    @commands.command()
    async def set(self, ctx, stat: str):
        if ctx.channel.name == "roll-stats":
            curr_user = None
            for campaignMember in costants.curr_campaign.campaign_member_list:
                if campaignMember.member.id == ctx.author.id:
                    curr_user = campaignMember

            if curr_user is None:
                await ctx.channel.send("User not found")
                return

            if 0 <= curr_user.stats_set_num < 6:
                foundStat: bool = False

                if stat.__eq__(StatTypeEnum.NONE.fullname):
                    await ctx.channel.send("Invalid stat NONE")
                    return

                for statEnum in StatTypeEnum:
                    if stat.__eq__(statEnum.fullname):
                        if not curr_user.stats_set_bools[statEnum.value]:
                            foundStat = True
                            curr_user.rolled_stats[statEnum.value] = curr_user.roll_list[curr_user.stats_set_num]
                            curr_user.update_total_stat(statEnum.value)
                            await curr_user.update_stat_ch(statEnum.value)
                            curr_user.stats_set_bools[statEnum.value] = True
                            await ctx.channel.send(f"Stat {stat} has been set")
                        else:
                            await ctx.channel.send("Stat already set. Choose a different stat")
                            return

                if not foundStat:
                    await ctx.channel.send(f"{stat} stat cannot be found")
                    return

                print("starting at: " + curr_user.stats_set_num)
                curr_user.stats_set_num += 1
                print(curr_user.stats_set_num)

                if curr_user.stats_set_num >= 6:
                    await ctx.send("You have set all stats")
                else:
                    await ctx.send(
                        f"Which skill would you like to set to {curr_user.roll_list[curr_user.stats_set_num]}?")
            else:
                await ctx.channel.send("You have already set all stats")

    @commands.has_role("Adventurer")
    @commands.command()
    async def swap_roll(self, ctx, stat_1: str, stat_2: str):
        curr_user: CampaignMember = None
        for member in costants.curr_campaign.campaign_member_list:
            if member.member.id == ctx.message.author.id:
                curr_user = member

        if curr_user is None:
            return

        # Get and swap values
        # ------------------------ TO DO ------------------------

    # Command to type to start a vote to delete the campaign, if all members' vote is positive the server is reset
    @commands.command(help="# Sets up a vote for deleting the campaign")
    async def dc(self, ctx):
        if costants.curr_campaign is not None and ctx.author.id not in costants.curr_campaign.player_confirm_delete:
            general_ch = costants.curr_campaign.CAMPAIGN_GENERAL_TEXT_CH

            costants.curr_campaign.player_confirm_delete.append(ctx.author.id)

            if len(costants.curr_campaign.player_confirm_delete) == 1:
                await general_ch.send(
                    f"{ctx.author.mention} wants to delete the campaign. Type !dc to confirm deletion.\n"
                    f"The campaign will be deleted only when all players confirm.")

            await general_ch.send(
                f"{len(costants.curr_campaign.player_confirm_delete)} / {costants.curr_campaign.players_num} want to delete the campaign")

        if len(costants.curr_campaign.player_confirm_delete) == costants.curr_campaign.players_num:
            costants.curr_campaign.player_confirm_delete.clear()
            await self.reset_server(ctx)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset_server(self, ctx):
        guild = ctx.guild

        for ch_id in costants.CAMPAIGN_CHANNELS:
            await guild.get_channel(ch_id).purge()

        for ch_id in costants.PLAYERS_ROLL_STATS_CH_ID:
            await guild.get_channel(ch_id).purge()

        for ch_id in costants.PLAYERS_STR_STAT_CH_ID:
            if guild.get_channel(ch_id).name is not "STR = 0":
                await guild.get_channel(ch_id).edit(name="STR = 0")

        for ch_id in costants.PLAYERS_DEX_STAT_CH_ID:
            await guild.get_channel(ch_id).edit(name="DEX = 0")

        for ch_id in costants.PLAYERS_CON_STAT_CH_ID:
            await guild.get_channel(ch_id).edit(name="CON = 0")

        for ch_id in costants.PLAYERS_INT_STAT_CH_ID:
            await guild.get_channel(ch_id).edit(name="INT = 0")

        for ch_id in costants.PLAYERS_WIS_STAT_CH_ID:
            await guild.get_channel(ch_id).edit(name="WIS = 0")

        for ch_id in costants.PLAYERS_CHA_STAT_CH_ID:
            await guild.get_channel(ch_id).edit(name="CHA = 0")

        for campaign_member in costants.curr_campaign.campaign_member_list:
            for role in campaign_member.member.roles:
                if role.id not in costants.DEFAULT_ROLES:
                    await campaign_member.member.remove_roles(role)

        costants.curr_campaign = None

    @commands.command()
    async def hello(self, ctx):
        await ctx.channel.send("Hello!")


async def setup(bot):
    await bot.add_cog(Game(bot))
    