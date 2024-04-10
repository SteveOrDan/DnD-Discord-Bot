import discord
from discord.ext import commands
import CampaignRoleView
from Campaign import Campaign, CampaignState
from ClassView import ClassView
from RaceView import RaceView, RaceTypeEnum
from CampaignMember import CampaignMember, StatTypeEnum
import random
import data.Names as namesGenerator

import costants
from data import Transactions
from data.Dice import D4
from data.Items import ItemsDataBase
from data.Items.Items import Item
from data.Purse import Purse, enum_from_str


def get_user(member: discord.Member):
    for user in costants.curr_campaign.campaign_member_list:
        if user.member.id == member.id:
            return user
    return None


async def send_char_embed(ctx, member: CampaignMember):
    embed = discord.Embed(title=member.member.nick, description="Character sheet", color=0x00ff00)
    embed.add_field(name="Strength", value=f"{member.total_stats[0]}", inline=True)
    embed.add_field(name="Dexterity", value=f"{member.total_stats[1]}", inline=True)
    embed.add_field(name="Constitution", value=f"{member.total_stats[2]}", inline=True)
    embed.add_field(name="Intelligence", value=f"{member.total_stats[3]}", inline=True)
    embed.add_field(name="Wisdom", value=f"{member.total_stats[4]}", inline=True)
    embed.add_field(name="Charisma", value=f"{member.total_stats[5]}", inline=True)

    embed.add_field(name="Armor Class", value=f"{member.armor_class}", inline=False)

    embed.add_field(name="Alignment", value=f"{member.alignment}", inline=False)

    embed.add_field(name="Bonds", value=f"{member.bonds}", inline=False)

    embed.add_field(name="Flaws", value=f"{member.flaws}", inline=False)

    embed.add_field(name="Ideals", value=f"{member.ideals}", inline=False)

    embed.add_field(name="Traits", value=f"{member.traits}", inline=False)

    embed.add_field(name="Background", value=f"{member.background}", inline=False)

    embed.add_field(name="Purse", value=f"{member.purse.toString()}", inline=False)

    await ctx.send(embed=embed)


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="# Quick 2 players set up. Testing purposes only.")
    async def qps(self, ctx, dm: discord.Member, adv: discord.Member, char_class: str, char_race: str,
                  str_stat: int, dex_stat: int, con_stat: int, int_stat: int, wis_stat: int, cha_stat: int):
        guild = ctx.guild

        # Set campaign object
        costants.curr_campaign = Campaign(user_num=2, guild_id=guild.id)

        # Assign campaign and user roles
        await dm.add_roles(guild.get_role(costants.CAMPAIGN_ROLE_ID))
        await self.add_member_to_campaign(member=dm)

        await adv.add_roles(guild.get_role(costants.CAMPAIGN_ROLE_ID))
        await self.add_member_to_campaign(member=adv)

        # Assign DM role
        await dm.add_roles(guild.get_role(costants.DM_ROLE_ID))

        # Assign Adventurers role
        await adv.add_roles(guild.get_role(costants.ADVENTURER_ROLE_ID))

        # Quick character creation
        max_stat_points = 27

        scores_costs = {
            8: 0,
            9: 1,
            10: 2,
            11: 3,
            12: 4,
            13: 5,
            14: 7,
            15: 9
        }

        races = {
            "dwarf": RaceTypeEnum.DWARF,
            "mountain dwarf": RaceTypeEnum.MOUNTAIN_DWARF,
            "hill dwarf": RaceTypeEnum.HILL_DWARF,
            "elf": RaceTypeEnum.ELF,
            "high elf": RaceTypeEnum.HIGH_ELF,
            "wood elf": RaceTypeEnum.WOOD_ELF,
            "halfling": RaceTypeEnum.HALFLING,
            "lightfoot": RaceTypeEnum.LIGHTFOOT,
            "stout": RaceTypeEnum.STOUT,
            "human": RaceTypeEnum.HUMAN
        }

        classes = {
            "cleric": costants.CLERIC_ROLE_ID,
            "fighter": costants.FIGHTER_ROLE_ID,
            "rogue": costants.ROGUE_ROLE_ID,
            "wizard": costants.WIZARD_ROLE_ID
        }

        char_race = char_race.lower()
        char_class = char_class.lower()

        total_cost = scores_costs[str_stat] + scores_costs[dex_stat] + scores_costs[con_stat] + scores_costs[int_stat] + scores_costs[wis_stat] + scores_costs[cha_stat]

        if total_cost > max_stat_points:
            await ctx.send(f"Total cost of stats ({total_cost}) is greater than the maximum allowed (27).")
            return

        if not races.__contains__(char_race):
            await ctx.send("Invalid race.")
            return

        if not classes.__contains__(char_class):
            await ctx.send("Invalid class.")
            return

        curr_user = get_user(adv)

        if curr_user is None:
            await ctx.send("No user found")
            return

        curr_user.stats_set_num = 6

        curr_user.race = char_race
        curr_user.char_class = char_class

        curr_user.rolled_stats = [str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat]

        _race = races.get(char_race)
        curr_user.race_stats = [_race.get_str(), _race.get_dex(), _race.get_con(), _race.get_int(), _race.get_wis(),
                                _race.get_cha()]

        curr_user.update_all_total_stat()
        curr_user.update_stats_modifiers()

        if curr_user.char_class == "fighter" or curr_user.char_class == "cleric":
            curr_user.purse = Purse([0, D4().throw_n(5) * 10, 0, 0])
        else:
            curr_user.purse = Purse([0, D4().throw_n(4) * 10, 0, 0])

        await curr_user.member.add_roles(ctx.guild.get_role(classes.get(char_class)))
        await curr_user.member.add_roles(ctx.guild.get_role(_race.get_role_id()))

        curr_user.alignment = "N"
        curr_user.member.add_roles(ctx.guild.get_role(costants.NEUTRAL_ROLE_ID))
        curr_user.background = "Background"
        curr_user.traits = "Traits"
        curr_user.ideals = "Ideals"
        curr_user.bonds = "Bonds"
        curr_user.flaws = "Flaws"

        await send_char_embed(ctx, curr_user)

    # Create campaign
    @commands.command(help="# Create campaign (at least 3 members)")
    async def cc(self, ctx, *arr: discord.Member):
        if ctx.message.channel.id == costants.GENERAL_CHAT_ID:
            if len(arr) < 3 or len(arr) > 6:
                await ctx.send("Need at least 3 and less than 7 people to create a campaign")
                return

            guild = ctx.guild

            # Set campaign object
            costants.curr_campaign = Campaign(user_num=len(arr), guild_id=guild.id)

            # Assign campaign and user roles
            for user in arr:
                await user.add_roles(guild.get_role(costants.CAMPAIGN_ROLE_ID))
                await user.add_roles(guild.get_role(costants.CHOOSING_ROLE_ROLE_ID))
                await self.add_member_to_campaign(member=user)

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
    async def add_member_to_campaign(member: discord.Member):
        new_user = CampaignMember()

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
                    user.player_num = i + 1
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
    @commands.command(help="# Rolls stats for character build")
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

            await ctx.send(f"Use !set <STAT_NAME> to set each stat when you get asked.\n"
                           "You can also use !swap <STAT_NAME_1> <STAT_NAME_2> to swap the value of two stats\n"
                           "STAT_NAME must be one of the 6 shown on the left.\n"
                           f"Which skill would you like to set to {curr_user.roll_list[curr_user.stats_set_num]}?")

        else:
            await ctx.channel.send("You can roll for stats only in the roll-stats channel")

    @commands.has_role("Adventurer")
    @commands.command(help="# Use default stats for character build. [15, 14, 13, 12, 10, 8]")
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

            await ctx.send(f"Use !set <STAT_NAME> to set each stat when you get asked.\n"
                           "You can also use !swap <STAT_NAME_1> <STAT_NAME_2> to swap the value of two stats\n"
                           "STAT_NAME must be one of the 6 shown on the left.\n"
                           f"Which skill would you like to set to {curr_user.roll_list[curr_user.stats_set_num]}?")

        else:
            await ctx.channel.send("You can roll for stats only in the roll-stats channel")

    @commands.has_role("Adventurer")
    @commands.command(help="# Set a stat to a specified value")
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

                curr_user.stats_set_num += 1

                if curr_user.stats_set_num >= 6:
                    await ctx.send("You have set all stats")
                else:
                    await ctx.send(
                        f"Which skill would you like to set to {curr_user.roll_list[curr_user.stats_set_num]}?")
            else:
                await ctx.channel.send("You have already set all stats")

    @commands.has_role("Adventurer")
    @commands.command(help="# Swap two stats value")
    async def swap(self, ctx, stat_1: str, stat_2: str):
        curr_user = None
        for member in costants.curr_campaign.campaign_member_list:
            if member.member.id == ctx.message.author.id:
                curr_user = member

        if curr_user is None:
            return

        stat_enum_1 = None
        stat_enum_2 = None

        for statEnum1 in StatTypeEnum:
            if stat_1.__eq__(statEnum1.fullname):
                stat_enum_1 = statEnum1

        for statEnum2 in StatTypeEnum:
            if stat_2.__eq__(statEnum2.fullname):
                stat_enum_2 = statEnum2

        if stat_enum_1 is None or stat_enum_2 is None:
            await ctx.channel.send("At least one of the stats has not been recognised")
            return

        if curr_user.stats_set_bools[stat_enum_1.value] and curr_user.stats_set_bools[stat_enum_2.value]:
            swap_temp = curr_user.rolled_stats[stat_enum_1.value]
            curr_user.rolled_stats[stat_enum_1.value] = curr_user.rolled_stats[stat_enum_2.value]
            curr_user.rolled_stats[stat_enum_2.value] = swap_temp

            curr_user.update_total_stat(stat_enum_1.value)
            curr_user.update_total_stat(stat_enum_2.value)

            await curr_user.update_stat_ch(stat_enum_1.value)
            await curr_user.update_stat_ch(stat_enum_2.value)

            await ctx.channel.send(f"Swapped {stat_1} and {stat_2}")
        else:
            await ctx.channel.send("One of the stats is not set")
            return

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

    @commands.command(help="# ADMINISTRATOR ONLY: Reset server")
    @commands.has_permissions(administrator=True)
    async def reset_server(self, ctx):
        guild = ctx.guild

        for ch_id in costants.CAMPAIGN_CHANNELS:
            await guild.get_channel(ch_id).purge()

        for ch_id in costants.PLAYERS_ROLL_STATS_CH_ID:
            await guild.get_channel(ch_id).purge()

        for ch_id in costants.PLAYERS_STR_STAT_CH_ID:
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
    @commands.has_role("Adventurer")
    async def set_name(self, ctx, charName: str):
        if ctx.channel.name == costants.CHARACTER_FEATURES_CH_NAME:
            await ctx.author.edit(nick=charName)
            await ctx.message.delete()

    @commands.command()
    @commands.has_role("Adventurer")
    async def set_alignment(self, ctx, alignment: str):
        if ctx.channel.name == costants.CHARACTER_FEATURES_CH_NAME:
            curr_user = None
            for member in costants.curr_campaign.campaign_member_list:
                if member.member.id == ctx.message.author.id:
                    curr_user = member

            if curr_user is None:
                return

            alignment_roles = {
                "LG": costants.LAWFUL_GOOD_ROLE_ID,
                "NG": costants.NEUTRAL_GOOD_ROLE_ID,
                "CG": costants.CHAOTIC_GOOD_ROLE_ID,
                "LN": costants.LAWFUL_NEUTRAL_ROLE_ID,
                "N": costants.NEUTRAL_ROLE_ID,
                "CN": costants.CHAOTIC_NEUTRAL_ROLE_ID,
                "LE": costants.LAWFUL_EVIL_ROLE_ID,
                "NE": costants.NEUTRAL_EVIL_ROLE_ID,
                "CE": costants.CHAOTIC_EVIL_ROLE_ID
            }

            role_id = alignment_roles.get(alignment)

            if role_id is None:
                await ctx.channel.send(f"{alignment} alignment not recognized.")
                return

            if curr_user.alignment:
                await curr_user.member.remove_roles(ctx.guild.get_role(role_id))

            await curr_user.member.add_roles(ctx.guild.get_role(role_id))
            curr_user.alignment = alignment
            await ctx.message.delete()

    @commands.command()
    @commands.has_role("Adventurer")
    async def set_bg(self, ctx, bg: str):
        if ctx.channel.name == costants.CHARACTER_FEATURES_CH_NAME:
            curr_user = None
            for member in costants.curr_campaign.campaign_member_list:
                if member.member.id == ctx.message.author.id:
                    curr_user = member

            if curr_user is None:
                return

            curr_user.background = bg
            await ctx.message.delete()
        else:
            await ctx.channel.send("Cannot use the command in this channel.")

    @commands.command()
    @commands.has_role("Adventurer")
    async def set_traits(self, ctx, traits: str):
        if ctx.channel.name == costants.CHARACTER_FEATURES_CH_NAME:
            curr_user = None
            for member in costants.curr_campaign.campaign_member_list:
                if member.member.id == ctx.message.author.id:
                    curr_user = member

            if curr_user is None:
                return

            curr_user.traits = traits
            await ctx.message.delete()

    @commands.command()
    @commands.has_role("Adventurer")
    async def set_ideals(self, ctx, ideals: str):
        if ctx.channel.name == costants.CHARACTER_FEATURES_CH_NAME:
            curr_user = None
            for member in costants.curr_campaign.campaign_member_list:
                if member.member.id == ctx.message.author.id:
                    curr_user = member

            if curr_user is None:
                return

            curr_user.ideals = ideals
            await ctx.message.delete()

    @commands.command()
    @commands.has_role("Adventurer")
    async def set_bonds(self, ctx, bonds: str):
        if ctx.channel.name == costants.CHARACTER_FEATURES_CH_NAME:
            curr_user = None
            for member in costants.curr_campaign.campaign_member_list:
                if member.member.id == ctx.message.author.id:
                    curr_user = member

            if curr_user is None:
                return

            curr_user.bonds = bonds
            await ctx.message.delete()

    @commands.command()
    @commands.has_role("Adventurer")
    async def set_flaws(self, ctx, flaws: str):
        if ctx.channel.name == costants.CHARACTER_FEATURES_CH_NAME:
            curr_user = None
            for member in costants.curr_campaign.campaign_member_list:
                if member.member.id == ctx.message.author.id:
                    curr_user = member

            if curr_user is None:
                return

            curr_user.flaws = flaws
            await ctx.message.delete()

    @commands.command()
    async def get_bg(self, ctx, targetMember: discord.Member = -1):
        if ctx.channel.name == costants.CHARACTER_FEATURES_CH_NAME:
            curr_user = None

            if targetMember == -1:
                for member in costants.curr_campaign.campaign_member_list:
                    if member.member.id == ctx.author.id:
                        curr_user = member
            else:
                for member in costants.curr_campaign.campaign_member_list:
                    if member.member.id == targetMember.id:
                        curr_user = member

            if curr_user is None:
                return

            await ctx.channel.send(curr_user.background)

    @commands.command()
    async def random_name(self, ctx, race: str, gender: str, clan: str = None):
        await ctx.channel.send(namesGenerator.rand(race, gender, clan))

    @commands.command()
    @commands.has_role("Adventurer")
    async def complete_char(self, ctx):
        curr_user = None
        for member in costants.curr_campaign.campaign_member_list:
            if member.member.id == ctx.message.author.id:
                curr_user = member

        if curr_user is None:
            return

        if curr_user.race is None:
            await ctx.send("You must choose a race first.")
            return

        if curr_user.char_class is None:
            await ctx.send("You must choose a class first.")
            return

        if curr_user.alignment is None:
            await ctx.send("You must choose an alignment first.")
            return

        curr_user.update_all_total_stat()

        if curr_user.stats_set_num < 6:
            await ctx.send("You must set all stats first.")
            return

        await curr_user.remove_roles(ctx.guild.get_role(costants.BUILDING_CHARACTER_ROLE_ID))

        player_roles = {
            1: costants.P1_ROLE_ID,
            2: costants.P2_ROLE_ID,
            3: costants.P3_ROLE_ID,
            4: costants.P4_ROLE_ID,
            5: costants.P5_ROLE_ID
        }

        curr_user.member.remove_roles(ctx.guild.get_role(player_roles.get(curr_user.player_num)))

        await send_char_embed(ctx, curr_user)

        if curr_user.char_class == "fighter" or curr_user.char_class == "cleric":
            curr_user.purse = Purse([0, D4().throw_n(5) * 10, 0, 0])
        else:
            curr_user.purse = Purse([0, D4().throw_n(4) * 10, 0, 0])

    @commands.command(help="# Quick character creation. "
                           "Template: !quick_char_create <class> <race> STR DEX CON INT WIS CHA")
    @commands.has_role("Adventurer")
    async def quick_char_create(self, ctx, char_class: str, char_race: str, str_stat: int, dex_stat: int, con_stat: int,
                                int_stat: int, wis_stat: int, cha_stat: int):
        max_stat_points = 27

        scores_costs = {
            8: 0,
            9: 1,
            10: 2,
            11: 3,
            12: 4,
            13: 5,
            14: 7,
            15: 9
        }

        races = {
            "dwarf": RaceTypeEnum.DWARF,
            "mountain dwarf": RaceTypeEnum.MOUNTAIN_DWARF,
            "hill dwarf": RaceTypeEnum.HILL_DWARF,
            "elf": RaceTypeEnum.ELF,
            "high elf": RaceTypeEnum.HIGH_ELF,
            "wood elf": RaceTypeEnum.WOOD_ELF,
            "halfling": RaceTypeEnum.HALFLING,
            "lightfoot": RaceTypeEnum.LIGHTFOOT,
            "stout": RaceTypeEnum.STOUT,
            "human": RaceTypeEnum.HUMAN
        }

        classes = {
            "cleric": costants.CLERIC_ROLE_ID,
            "fighter": costants.FIGHTER_ROLE_ID,
            "rogue": costants.ROGUE_ROLE_ID,
            "wizard": costants.WIZARD_ROLE_ID
        }

        total_cost = scores_costs[str_stat] + scores_costs[dex_stat] + scores_costs[con_stat] + scores_costs[int_stat] + \
                     scores_costs[wis_stat] + scores_costs[cha_stat]

        if total_cost > max_stat_points:
            await ctx.send(f"Total cost of stats ({total_cost}) is greater than the maximum allowed (27).")
            return

        if not races.__contains__(char_race):
            await ctx.send("Invalid race.")
            return

        if not classes.__contains__(char_class):
            await ctx.send("Invalid class.")
            return

        curr_user = None
        for member in costants.curr_campaign.campaign_member_list:
            if member.member.id == ctx.author.id:
                curr_user = member

        curr_user.stats_set_num = 6

        curr_user.race = char_race

        curr_user.rolled_stats = [str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat]

        _race = races.get(char_race)
        curr_user.race_stats = [_race.get_str(), _race.get_dex(), _race.get_con(), _race.get_int(), _race.get_wis(),
                                _race.get_cha()]

        curr_user.update_all_total_stat()
        curr_user.update_stats_modifiers()

        if curr_user.char_class == "fighter" or curr_user.char_class == "cleric":
            curr_user.purse = Purse([0, D4().throw_n(5) * 10, 0, 0])
        else:
            curr_user.purse = Purse([0, D4().throw_n(4) * 10, 0, 0])

        await curr_user.member.add_roles(ctx.guild.get_role(classes.get(char_class)))
        await curr_user.member.add_roles(ctx.guild.get_role(_race.get_role_id()))
        await curr_user.member.remove_roles(ctx.guild.get_role(costants.BUILDING_CHARACTER_ROLE_ID))

    @commands.command(help="# Send DM request to buy an item")
    @commands.has_role("Adventurer")
    async def request_buy(self, ctx, item: str):
        if Transactions.contains(ctx.author.display_name, item):
            await ctx.send("Transaction already exists")
            return

        Transactions.add(ctx.author.display_name, item)

        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        _item: Item = ItemsDataBase.get_item(item)

        await ctx.guild.get_channel(costants.DM_CHAT_ID).send(f"{ctx.author.display_name} request to buy {item}.\n"
                                                              f"{item} default price: {_item.cost}.\n"
                                                              f"{ctx.author.display_name} purse: {curr_user.purse.toString()}.\n"
                                                              f"Type !set_price <@user> <item> <price> <currency> to set the price."
                                                              f"You can also use !set_price <@user> <item> \"default\" to set the default price.\n"
                                                              f"===============================================================================")

    @commands.command(help="# Send the adventurer the price of the requested item")
    @commands.has_role("DM")
    async def set_price(self, ctx, member: str, item: str, price: str, currency: str = None):
        transaction = Transactions.get(member, item)

        if transaction is None:
            await ctx.send("Transaction not found")
            return

        if price == "default":
            _item: Item = ItemsDataBase.get_item(item)
            price = _item.cost.value
            currency = _item.cost.coinType

        transaction.price = int(price)
        transaction.coin_type = enum_from_str(currency)

        transaction.state = Transactions.TransactionState.PRICE_SET

        await ctx.guild.get_channel(costants.CAMPAIGN_CHAT_ID).send(f"DM has set the price of {item} to {price} {currency}")

    @commands.command(help="# Accept item price and buy it")
    @commands.has_role("Adventurer")
    async def accept_trade(self, ctx, item: str):
        transaction = Transactions.get(ctx.author.display_name, item)

        if transaction is None:
            await ctx.send("Transaction not found")
            return

        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        if curr_user.purse.remove(transaction.price, transaction.coin_type.value):
            await ctx.send(f"{item} bought for {transaction.price} {transaction.coin_type}")
            curr_user.inventory.append(item)
        else:
            await ctx.send("Not enough money")

        Transactions.remove(ctx.author.display_name, item)

    @commands.command(help="# Refuse item price and close transaction")
    @commands.has_role("Adventurer")
    async def refuse_trade(self, ctx, item: str):
        transaction = Transactions.get(ctx.author.display_name, item)

        if transaction is None:
            await ctx.send("Transaction not found")
            return

        Transactions.remove(ctx.author.display_name, item)
        await ctx.send(f"{item} transaction closed")

    @commands.command()
    @commands.has_role("DM")
    async def get_all_transactions(self, ctx):
        await ctx.send(Transactions.transaction_list_to_str())

    @commands.command()
    async def get_purse(self, ctx, member: discord.Member):
        curr_user = get_user(member)

        if curr_user is None:
            return

        await ctx.send(f"{curr_user.member.display_name}'s purse: {curr_user.purse.toString()}")


async def setup(bot):
    await bot.add_cog(Game(bot))

# TODO: Roll for:
#  - ability checks: STRENGTH: ATHLETICS
#               DEXTERITY: ACROBATICS, SLEIGHT OF HAND, STEALTH
#               INTELLIGENCE: ARCANA, HISTORY, INVESTIGATION, NATURE, RELIGION
#               WISDOM: ANIMAL HANDLING, INSIGHT, MEDICINE, PERCEPTION, SURVIVAL
#               CHARISMA: DECEPTION, INTIMIDATION, PERFORMANCE, PERSUASION
#  - initiative: D20 + DEX -> create attack queue
#  - attack: D20 + STR/DEX + proficiency bonus
#       - 20: Success
#       - 1: Critical failure
#  - damage: Weapon damage (Dice)
#  - saving throws: D20 + STR/DEX/CON/INT/WIS/CHA + proficiency bonus
