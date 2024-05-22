from discord.ext import commands
import CampaignRoleView
from Campaign import Campaign, CampaignState
from ClassView import ClassView
from RaceView import RaceView
from CampaignMember import *
import random
import data.Names as namesGenerator

import costants
from data import Transactions, MonstersDataBase, SpellDataBase
from data.Dice import D4, D20
from data.Encounter import Encounter
from data.Items import ItemsDataBase
from data.Items.Items import Item, ArmorStr
from data.MonstersDataBase import Monster
from data.Purse import Purse, enum_from_str
from data.Transactions import TransactionType


def get_user(member: discord.Member) -> CampaignMember | None:
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

    embed.add_field(name="Speed", value=f"{member.total_speed}", inline=False)

    embed.add_field(name="Armor Class", value=f"{member.armor_class}", inline=False)

    embed.add_field(name="Hit Points", value=f"{member.maxHitPoints}", inline=False)

    embed.add_field(name="Alignment", value=f"{member.alignment}", inline=False)

    embed.add_field(name="Bonds", value=f"{member.bonds}", inline=False)

    embed.add_field(name="Flaws", value=f"{member.flaws}", inline=False)

    embed.add_field(name="Ideals", value=f"{member.ideals}", inline=False)

    embed.add_field(name="Traits", value=f"{member.traits}", inline=False)

    embed.add_field(name="Background", value=f"{member.background}", inline=False)

    embed.add_field(name="Purse", value=f"{member.purse.toString()}", inline=False)

    await ctx.send(embed=embed)


class Game(commands.Cog):

    CAMPAIGN_ROLE: discord.Role = None
    CHOOSING_ROLE: discord.Role = None
    ADVENTURER_ROLE: discord.Role = None
    DM_ROLE: discord.Role = None
    BUILDING_CHARACTER_ROLE: discord.Role = None

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
            costants.curr_campaign = Campaign(user_num=len(arr), guild_id=guild.id)

            self.CAMPAIGN_ROLE = guild.get_role(costants.CAMPAIGN_ROLE_ID)
            self.CHOOSING_ROLE = guild.get_role(costants.CHOOSING_ROLE_ROLE_ID)

            # Assign campaign and user roles
            for user in arr:
                await asyncio.sleep(1)
                await user.add_roles(self.CAMPAIGN_ROLE)
                await user.add_roles(self.CHOOSING_ROLE)
                self.add_member_to_campaign(member=user)

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
    def add_member_to_campaign(member: discord.Member):
        new_user = CampaignMember()

        new_user.member = member

        costants.curr_campaign.campaign_member_list.append(new_user)

    @commands.command(help="# Start campaign")
    async def sc(self, ctx):
        if costants.curr_campaign is not None and costants.curr_campaign.check_if_can_start_campaign():
            await ctx.send("Preparing character creation...\n")

            costants.curr_campaign.campaign_state = CampaignState.BUILDING_CHARACTER

            guild = ctx.guild

            self.DM_ROLE = guild.get_role(costants.DM_ROLE_ID)
            self.ADVENTURER_ROLE = guild.get_role(costants.ADVENTURER_ROLE_ID)
            self.BUILDING_CHARACTER_ROLE = guild.get_role(costants.BUILDING_CHARACTER_ROLE_ID)

            for campaignMember in costants.curr_campaign.campaign_member_list:
                await campaignMember.member.remove_roles(self.CHOOSING_ROLE)
                if campaignMember.isAdventurer:
                    await campaignMember.member.add_roles(self.ADVENTURER_ROLE)
                    await campaignMember.member.add_roles(self.BUILDING_CHARACTER_ROLE)
                elif campaignMember.isDM:
                    await campaignMember.member.add_roles(self.DM_ROLE)
                else:
                    await ctx.channel.send(f"Error: User {campaignMember.member} is neither Adventurer nor DM.")

            await asyncio.sleep(1)
            # Fill race-info channel
            await guild.get_channel(costants.RACE_INFO_CHAT_ID).send(
                "There are 4 core races available. Some of them also have subraces.\n"
                "Type !<race_name> or !<subrace_name> to get more info about them.\n"
                "Type !info to get access to the rulebook.")

            await asyncio.sleep(1)
            # Fill class-info channel
            await guild.get_channel(costants.CLASS_INFO_CHAT_ID).send(
                "There are 4 classes available. Type !<class_name> to get the handbook references to that class")

            await asyncio.sleep(1)
            race_view = RaceView()
            await guild.get_channel(costants.SET_RACE_CHAT_ID).send("Choose your race", view=race_view)

            await asyncio.sleep(1)
            class_view = ClassView(ctx.guild)
            await guild.get_channel(costants.SET_CLASS_CHAT_ID).send("Choose your class", view=class_view)

            # Give players role
            i = 0
            for user in costants.curr_campaign.campaign_member_list:
                if user.isAdventurer:
                    await asyncio.sleep(1)
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
    def roll_stat() -> int:
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
    async def roll_stats(self, ctx):
        if ctx.channel.name == "roll-stats":
            stats = []
            for i in range(6):
                await asyncio.sleep(0.5)
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

            curr_user.roll_list.clear()

            curr_user.roll_list = [15, 14, 13, 12, 10, 8]

            for i in range(6):
                await asyncio.sleep(0.5)
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
                            await asyncio.sleep(1)
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
            general_ch = ctx.guild.get_channel(costants.CAMPAIGN_CHAT_ID)

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

        await asyncio.sleep(1)
        for ch_id in costants.PLAYERS_ROLL_STATS_CH_ID:
            await guild.get_channel(ch_id).purge()

        await asyncio.sleep(1)
        for ch_id in costants.PLAYERS_STR_STAT_CH_ID:
            await guild.get_channel(ch_id).edit(name="STR = 0")

        await asyncio.sleep(1)
        for ch_id in costants.PLAYERS_DEX_STAT_CH_ID:
            await guild.get_channel(ch_id).edit(name="DEX = 0")

        await asyncio.sleep(1)
        for ch_id in costants.PLAYERS_CON_STAT_CH_ID:
            await guild.get_channel(ch_id).edit(name="CON = 0")

        await asyncio.sleep(1)
        for ch_id in costants.PLAYERS_INT_STAT_CH_ID:
            await guild.get_channel(ch_id).edit(name="INT = 0")

        await asyncio.sleep(1)
        for ch_id in costants.PLAYERS_WIS_STAT_CH_ID:
            await guild.get_channel(ch_id).edit(name="WIS = 0")

        await asyncio.sleep(1)
        for ch_id in costants.PLAYERS_CHA_STAT_CH_ID:
            await guild.get_channel(ch_id).edit(name="CHA = 0")

        await asyncio.sleep(1)
        for campaign_member in costants.curr_campaign.campaign_member_list:
            for role in campaign_member.member.roles:
                if role.id not in costants.DEFAULT_ROLES:
                    await asyncio.sleep(0.2)
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
    async def get_bg(self, ctx):
        if ctx.channel.name == costants.CHARACTER_FEATURES_CH_NAME:
            curr_user = get_user(ctx.author)

            if curr_user is None:
                ctx.send("No user found")
                return

            await ctx.send(curr_user.background)

    @commands.command()
    async def random_name(self, ctx, race: str, gender: str, clan: str = None):
        await ctx.channel.send(namesGenerator.rand(race, gender, clan))

    @commands.command()
    @commands.has_role("Adventurer")
    async def complete_char(self, ctx):
        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        if curr_user.adv_class is None:
            await ctx.send("You must choose a class first.")
            return

        if curr_user.alignment == "None":
            await ctx.send("You must choose an alignment first.")
            return

        if curr_user.stats_set_num < 6:
            await ctx.send("You must set all stats first.")
            return

        if curr_user.race is None:
            await ctx.send("You must choose a race first.")
            return

        await curr_user.member.remove_roles(self.BUILDING_CHARACTER_ROLE)

        curr_user.confirm_race()

        await curr_user.member.add_roles(ctx.guild.get_role(curr_user.race.get_role_id()))
        await curr_user.member.add_roles(ctx.guild.get_role(curr_user.adv_class.get_role_id()))

        curr_user.race_speed = curr_user.race.get_speed()

        curr_user.update_total_speed()

        curr_user.update_all_total_stat()
        curr_user.update_stats_modifiers()

        curr_user.confirm_class()

        if curr_user.adv_class == AdvClass.FIGHTER or curr_user.adv_class == AdvClass.CLERIC:
            curr_user.purse = Purse([0, D4().throw_n(5) * 10, 0, 0])
        else:
            curr_user.purse = Purse([0, D4().throw_n(4) * 10, 0, 0])

        curr_user.hit_points = curr_user.adv_class.get_hit_dice().throw() + curr_user.stats_modifiers[2]
        curr_user.update_armor_class()
        curr_user.update_max_hit_points()

        await send_char_embed(ctx, curr_user)

    @commands.command(help="# Quick character creation. "
                           "Template: !quick_char_create <class> <race> STR DEX CON INT WIS CHA")
    @commands.has_role("Adventurer")
    async def quick_char_create(self, ctx, adv_class: str, char_race: str, str_stat: int, dex_stat: int, con_stat: int,
                                int_stat: int, wis_stat: int, cha_stat: int, alignment: str = "N"):
        await ctx.send("Creating character. Please wait a moment...")
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
            "cleric": AdvClass.CLERIC,
            "fighter": AdvClass.FIGHTER,
            "rogue": AdvClass.ROGUE,
            "wizard": AdvClass.WIZARD
        }

        alignments = ["LG", "NG", "CG", "LN", "N", "CN", "LE", "NE", "CE"]

        total_cost = scores_costs[str_stat] + scores_costs[dex_stat] + scores_costs[con_stat] + scores_costs[int_stat] + scores_costs[wis_stat] + scores_costs[cha_stat]

        if total_cost > max_stat_points:
            await ctx.send(f"Total cost of stats ({total_cost}) is greater than the maximum allowed (27).")
            return

        char_race = char_race.lower()

        if not races.__contains__(char_race):
            await ctx.send("Invalid race.")
            return

        adv_class = adv_class.lower()

        if not classes.__contains__(adv_class):
            await ctx.send("Invalid class.")
            return

        curr_user = get_user(ctx.author)

        if curr_user is None:
            await ctx.send("No user found")
            return

        if not alignments.__contains__(alignment):
            await ctx.send("Invalid alignment.")
            return

        curr_user.alignment = alignment

        curr_user.stats_set_num = 6

        curr_user.rolled_stats = [str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat]

        curr_user.adv_class = classes.get(adv_class)

        _race = races.get(char_race)
        curr_user.race = _race
        curr_user.race_stats = [_race.get_str(), _race.get_dex(), _race.get_con(), _race.get_int(), _race.get_wis(),
                                _race.get_cha()]

        curr_user.race_speed = _race.get_speed()

        curr_user.update_total_speed()

        curr_user.update_all_total_stat()
        curr_user.update_stats_modifiers()

        await curr_user.update_all_stat_ch()

        if curr_user.adv_class == AdvClass.FIGHTER or curr_user.adv_class == AdvClass.CLERIC:
            curr_user.purse = Purse([0, D4().throw_n(5) * 10, 0, 0])
        else:
            curr_user.purse = Purse([0, D4().throw_n(4) * 10, 0, 0])

        curr_user.hit_points = curr_user.adv_class.get_hit_dice().throw() + curr_user.stats_modifiers[2]

        await curr_user.member.add_roles(ctx.guild.get_role(classes.get(adv_class).get_role_id()))
        await curr_user.member.add_roles(ctx.guild.get_role(_race.get_role_id()))
        await curr_user.member.remove_roles(self.BUILDING_CHARACTER_ROLE)

        await ctx.send("Character created. You can add more info about your character using the following commands:\n"
                       "- !set_name <name>\n"
                       "- !set_bg <background>\n"
                       "- !set_traits <traits>\n"
                       "- !set_ideals <ideals>\n"
                       "- !set_bonds <bonds>\n"
                       "- !set_flaws <flaws>")
        await ctx.send("You can also use !complete_char to finish the character creation.")

    @commands.command(help="# Send DM request to buy an item")
    @commands.has_role("Adventurer")
    async def request_buy(self, ctx, item: str, amount: int = 1):
        if Transactions.contains(ctx.author.display_name, item, TransactionType.BUY):
            await ctx.send("Transaction already exists")
            return

        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        _item: Item = ItemsDataBase.get_item(item)

        if _item is None:
            await ctx.send("Item not found")
            return

        if curr_user.curr_inventory_weight + (_item.weight * amount) > curr_user.max_inventory_weight:
            await ctx.send("Not enough space in inventory")
            return

        Transactions.add(ctx.author.display_name, item, amount, TransactionType.BUY)

        await ctx.guild.get_channel(costants.DM_CHAT_ID).send(f"{ctx.author.display_name} request to buy {amount} {item}.\n"
                                                              f"{item} default price: {_item.cost.times(amount)}.\n"
                                                              f"{ctx.author.display_name} purse: {curr_user.purse.toString()}.\n"
                                                              f"Type !set_buy_price <@user> <item> <price> <currency> to set the price."
                                                              f"You can also use !set_buy_price <@user> <item> \"default\" to set the default price.\n"
                                                              f"=================================================================================================================================================")

    @commands.command(help="# Send the adventurer the price of the requested item to buy")
    @commands.has_role("DM")
    async def set_buy_price(self, ctx, member: str, item: str, price: str, currency: str = None):
        transaction = Transactions.get(member, item, TransactionType.BUY)

        if transaction is None:
            await ctx.send("Transaction not found")
            return

        if price == "default":
            _item: Item = ItemsDataBase.get_item(item)
            transaction.price = _item.cost.value * transaction.amount
            transaction.coin_type = _item.cost.coinType
        else:
            transaction.price = int(price)
            transaction.coin_type = enum_from_str(currency)

        transaction.state = Transactions.TransactionState.PRICE_SET

        await ctx.guild.get_channel(costants.CAMPAIGN_CHAT_ID).send(f"DM has set the price of {transaction.amount} {item} to {transaction.price} {transaction.coin_type}.\n"
                                                                    f"Type !accept_buy <item> to accept the trade or !refuse_buy <item> to refuse it.")

    @commands.command(help="# Send the adventurer the price of the requested item to sell")
    @commands.has_role("DM")
    async def set_sell_price(self, ctx, member: str, item: str, price: str, currency: str = None):
        transaction = Transactions.get(member, item, TransactionType.SELL)

        if transaction is None:
            await ctx.send("Transaction not found")
            return

        if price == "default":
            _item: Item = ItemsDataBase.get_item(item)
            transaction.price = _item.cost.value * transaction.amount
            transaction.coin_type = _item.cost.coinType
        else:
            transaction.price = int(price)
            transaction.coin_type = enum_from_str(currency)

        transaction.state = Transactions.TransactionState.PRICE_SET

        await ctx.guild.get_channel(costants.CAMPAIGN_CHAT_ID).send(
            f"DM has set the price of {transaction.amount} {item} to {transaction.price} {transaction.coin_type}.\n"
            f"Type !accept_sell <item> to accept the trade or !refuse_sell <item> to refuse it.")

    @commands.command(help="# Accept item price and buy it")
    @commands.has_role("Adventurer")
    async def accept_buy(self, ctx, item: str):
        transaction = Transactions.get(ctx.author.display_name, item, TransactionType.BUY)

        if transaction is None:
            await ctx.send("Transaction not found")
            return

        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        if curr_user.purse.remove(transaction.price, transaction.coin_type.value):
            await ctx.send(f"{transaction.amount} {item} bought for {transaction.price} {transaction.coin_type}")

            curr_user.add_item_to_inv(item, transaction.amount)
        else:
            await ctx.send("Not enough money")

        Transactions.remove(ctx.author.display_name, item, TransactionType.BUY)

    @commands.command(help="# Accept item price and sell it")
    @commands.has_role("Adventurer")
    async def accept_sell(self, ctx, item: str):
        transaction = Transactions.get(ctx.author.display_name, item, TransactionType.SELL)

        if transaction is None:
            await ctx.send("Transaction not found")
            return

        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        curr_user.purse.add(transaction.price, transaction.coin_type.value)

        await ctx.send(f"{transaction.amount} {item} sold for {transaction.price} {transaction.coin_type}")

        curr_user.remove_item_from_inv(item, transaction.amount)

        Transactions.remove(ctx.author.display_name, item, TransactionType.SELL)

    @commands.command(help="# Refuse item price and close transaction")
    @commands.has_role("Adventurer")
    async def refuse_buy(self, ctx, item: str):
        transaction = Transactions.get(ctx.author.display_name, item, TransactionType.BUY)

        if transaction is None:
            await ctx.send("Transaction not found")
            return

        Transactions.remove(ctx.author.display_name, item, TransactionType.BUY)
        await ctx.send(f"{transaction.amount} {item} transaction closed")

    @commands.command(help="# Send DM request to sell an item")
    @commands.has_role("Adventurer")
    async def request_sell(self, ctx, item: str, amount: int = 1):
        if Transactions.contains(ctx.author.display_name, item, TransactionType.SELL):
            await ctx.send("Transaction already exists")
            return

        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        if item not in curr_user.inventory:
            await ctx.send(f"{item} not found in inventory")
            return

        _item: Item = ItemsDataBase.get_item(item)

        if _item is None:
            await ctx.send("Item not found")
            return

        if curr_user.inventory.get(item) < amount:
            await ctx.send(f"Not enough items in inventory. You only have {curr_user.inventory.get(item)} {item}")
            return

        Transactions.add(ctx.author.display_name, item, amount, TransactionType.SELL)

        await ctx.guild.get_channel(costants.DM_CHAT_ID).send(f"{ctx.author.display_name} request to sell {amount} {item}.\n"
                                                              f"{item} default price: {_item.cost.times(amount)}.\n"
                                                              f"{ctx.author.display_name} purse: {curr_user.purse.toString()}.\n"
                                                              f"Type !set_sell_price <@user> <item> <price> <currency> to set the price."
                                                              f"You can also use !set_sell_price <@user> <item> \"default\" to set the default price.\n"
                                                              f"=================================================================================================================================================")





    @commands.command(help="# Refuse item price and close transaction")
    @commands.has_role("Adventurer")
    async def refuse_sell(self, ctx, item: str):
        transaction = Transactions.get(ctx.author.display_name, item, TransactionType.SELL)

        if transaction is None:
            await ctx.send("Transaction not found")
            return

        Transactions.remove(ctx.author.display_name, item, TransactionType.SELL)
        await ctx.send(f"{transaction.amount} {item} transaction closed")

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

    @commands.command()
    async def equip(self, ctx, item: str):
        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        # Check if item is in inventory
        if item not in curr_user.inventory:
            await ctx.send(f"{item} not found in inventory")
            return

        # Check if item is a weapon, armor or shield
        # Invalid items are never added to the inventory
        if item in ItemsDataBase.weapons:
            if curr_user.equipped_weapon is not None:
                curr_user.add_item_to_inv(curr_user.equipped_weapon.name, 1)

            curr_user.equipped_weapon = ItemsDataBase.get_item(item)
        elif item in ItemsDataBase.armors:
            if curr_user.equipped_armor is not None:
                curr_user.add_item_to_inv(curr_user.equipped_armor.name, 1)

            curr_user.equipped_armor = ItemsDataBase.get_item(item)
            curr_user.update_armor_class()
            if ((curr_user.equipped_armor.str_value == ArmorStr.STR13 and curr_user.total_stats[0] < 13) or
                    (curr_user.equipped_armor.str_value == ArmorStr.STR15 and curr_user.total_stats[0] < 15)):
                curr_user.speed_debuff = 10
            else:
                curr_user.speed_debuff = 0
            curr_user.update_total_speed()
        else:
            curr_user.has_shield = True
            curr_user.update_armor_class()

        curr_user.remove_item_from_inv(item, 1)
        await ctx.send(f"{item} equipped")

    @commands.command()
    async def unequip(self, ctx, item: str):
        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        item = item.lower()

        if item == "weapon":
            if curr_user.equipped_weapon is not None:
                curr_user.add_item_to_inv(curr_user.equipped_weapon.name, 1)
                curr_user.equipped_weapon = None
        elif item == "armor":
            if curr_user.equipped_armor is not None:
                curr_user.add_item_to_inv(curr_user.equipped_armor.name, 1)
                curr_user.equipped_armor = None
                curr_user.update_armor_class()
                curr_user.speed_debuff = 0
                curr_user.update_total_speed()
        else:
            curr_user.has_shield = False
            curr_user.update_armor_class()

        await ctx.send(f"{item} unequipped")

    @commands.command()
    async def ability_check(self, ctx, ability: str):
        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        # Get stat type
        stat = StatTypeEnum.str_to_enum(ability)

        # Roll a D20
        roll = D20().throw() + curr_user.stats_modifiers[stat.value]

        if roll == 20:
            await ctx.send(f"{curr_user.member.display_name}'s {ability} check: Critical hit!")
            return
        elif roll == 1:
            await ctx.send(f"{curr_user.member.display_name}'s {ability} check: Critical failure!")
            return

        # Add proficiency bonus if user is proficient with the ability
        if self.check_other_proficiencies(curr_user, ability):
            roll += curr_user.proficiency_bonus

        await ctx.send(f"{curr_user.member.display_name}'s {ability} check: {roll}")

    @commands.command(help="# Roll a dice. Template: !roll_dice <dice> (e.g. 1d6)")
    async def roll_dice(self, ctx, dice: str):
        if dice.__contains__("d"):
            dice_arr = dice.split("d")
            dice_num = int(dice_arr[0])
            dice_type = int(dice_arr[1])

            res = 0

            for i in range(dice_num):
                res += random.randint(1, dice_type)

            await ctx.send(f"{ctx.author.display_name} rolled {dice}: {res}")
        else:
            await ctx.send("Invalid dice format")

    @commands.command()
    @commands.has_role("DM")
    async def roll_initiatives(self, ctx):
        user_initiatives = {}

        for user in costants.curr_campaign.campaign_member_list:
            if user.isAdventurer:
                initiative = D20().throw() + user.stats_modifiers[StatTypeEnum.DEX.value]

                user_initiatives.update({user: initiative})

        queue = ""

        # Create the queue of initiatives
        for key in user_initiatives:
            queue += f"{key.member.display_name}: {user_initiatives.get(key)}  ;  "

        await ctx.guild.get_channel(costants.CAMPAIGN_CHAT_ID).send(f"Initiative rolls:  {queue}")

    @commands.command()
    async def roll_attack(self, ctx, ability: str):
        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        # Roll a D20
        roll = D20().throw()

        # Check for critical hit or failure
        if roll == 20:
            await ctx.send(f"{curr_user.member.display_name}'s attack rolled: Critical hit!")
            return
        elif roll == 1:
            await ctx.send(f"{curr_user.member.display_name}'s attack rolled: Critical failure!")
            return

        stat = StatTypeEnum.str_to_enum(ability)

        if stat is None:
            await ctx.send("Invalid ability")
            return

        # Add stat modifier
        roll += curr_user.stats_modifiers[stat.value]

        # Add proficiency bonus if user is proficient with the weapon
        if curr_user.weapon_proficiencies.__contains__(curr_user.equipped_weapon.weaponType) or self.check_other_proficiencies(curr_user, curr_user.equipped_weapon.name):
            roll += curr_user.proficiency_bonus

        await ctx.send(f"{curr_user.member.display_name}'s attack rolled: {roll}")

    @commands.command()
    async def roll_damage(self, ctx):
        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        damage = curr_user.equipped_weapon.damage.throw()

        await ctx.send(f"{curr_user.member.display_name}'s damage: {damage}")

    @commands.command()
    async def saving_throw(self, ctx, ability: str):
        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        stat = StatTypeEnum.str_to_enum(ability)

        proficiency = 0

        if curr_user.saving_throw_proficiencies.__contains__(ability.upper()):
            proficiency = curr_user.proficiency_bonus

        roll = D20().throw() + curr_user.stats_modifiers[stat.value] + proficiency

        await ctx.send(f"{curr_user.member.display_name}'s {ability} saving throw: {roll}")

    @staticmethod
    def check_other_proficiencies(user: CampaignMember, proficiency: str) -> bool:
        if user.class_proficiencies.__contains__(proficiency) or user.race_proficiencies.__contains__(proficiency):
            return True
        return False

    @commands.command()
    async def get_member_info(self, ctx, member: discord.Member):
        curr_user = get_user(member)

        if curr_user is None:
            return

        await ctx.send(curr_user.get_info())

    @commands.command(help="# Create a new monster. Template: !create_monster <name> <AC> <HP> <STR> <DEX> <CON> <INT> <WIS> <CHA> <attack_bonus> <dice_num> <damage_dice> <damage_bonus>")
    @commands.has_role("DM")
    async def create_monster(self, ctx, name: str, AC: int, HP: int,
                             STR: int, DEX: int, CON: int, INT: int, WIS: int, CHA: int,
                             attack_bonus: int, dice_num: int, damage_dice: int, damage_bonus: int):
        if MonstersDataBase.monsters.__contains__(name):
            await ctx.send(f"Monster {name} already exists in the database.")
            return

        monster: Monster = Monster(name, AC, HP,
                                   STR, DEX, CON, INT, WIS, CHA,
                                   attack_bonus, dice_num, damage_dice, damage_bonus)

        MonstersDataBase.monsters.update({name: monster})

        if MonstersDataBase.monsters.__contains__(name):
            await ctx.send(f"Monster {name} created and added to the database.")
        else:
            await ctx.send("Monster creation failed")

    @commands.command(help="# Set the current campaign's encounter."
                           "Template: !set_encounter <monster_name_1>:<count>, <monster_name_2>:<count>, ...")
    @commands.has_role("DM")
    async def set_encounter(self, ctx, monster_arr: str):
        # Encounter constructor automatically sets the monsters' dictionary
        costants.curr_campaign.curr_encounter = Encounter(monster_arr)

        await ctx.send(costants.curr_campaign.curr_encounter.toString())
        await ctx.send(costants.curr_campaign.curr_encounter.initiative_order_to_string())
        await ctx.send("It's " + costants.curr_campaign.curr_encounter.get_first_in_order() + "'s turn")

    @commands.command(help="# Attack a monster in the current encounter. Template: !attack_monster <ability> <monster_id>")
    async def attack_monster(self, ctx, ability: str, monster_id: str):
        curr_user = get_user(ctx.author)

        monster = costants.curr_campaign.curr_encounter.get_by_id(monster_id)

        if curr_user is None or monster is None:
            await ctx.send("User or monster not found")
            return

        if curr_user.equipped_weapon is None:
            await ctx.send("No weapon equipped")
            return

        # Roll a D20
        roll = D20().throw()

        # Check for critical hit or failure
        if roll == 1:
            await ctx.send(f"{curr_user.member.display_name}'s attack rolled: Critical failure!")
        else:
            doesHit: bool
            if roll == 20:
                await ctx.send(f"{curr_user.member.display_name}'s attack rolled: Critical hit!")
                doesHit = True
            else:
                stat = StatTypeEnum.str_to_enum(ability)

                if stat is None:
                    await ctx.send("Invalid ability")
                    return

                # Add stat modifier
                roll += curr_user.stats_modifiers[stat.value]

                # Add proficiency bonus if user is proficient with the weapon
                if curr_user.equipped_weapon is not None:
                    if (curr_user.weapon_proficiencies.__contains__(curr_user.equipped_weapon.weaponType) or
                            self.check_other_proficiencies(curr_user, curr_user.equipped_weapon.name)):
                        roll += curr_user.proficiency_bonus

                doesHit = roll >= monster.AC

            if doesHit:
                damage = curr_user.equipped_weapon.damage.throw_n(curr_user.equipped_weapon.dice_num)

                res = costants.curr_campaign.curr_encounter.damage(monster_id, damage)

                await ctx.send(res)

                if costants.curr_campaign.curr_encounter.check_if_encounter_over():
                    await ctx.send("The encounter has been cleared.")
                else:
                    await ctx.send("It's " + costants.curr_campaign.curr_encounter.get_next_in_order() + "'s turn.")
            else:
                await ctx.send(f"{curr_user.member.display_name}'s attack missed.")
                await ctx.send("It's " + costants.curr_campaign.curr_encounter.get_next_in_order() + "'s turn.")

    @commands.command()
    @commands.has_role("DM")
    async def attack_player(self, ctx, member: discord.Member, attacking_monster: str):
        curr_user = get_user(member)

        monster = MonstersDataBase.get_monster(attacking_monster)

        if curr_user is None or monster is None:
            await ctx.send("User or monster not found")
            return

        damage = monster.attack(curr_user.armor_class)
        curr_user.currHitPoints -= damage

        if curr_user.currHitPoints <= 0:
            await ctx.send(f"{curr_user.member.display_name} has been defeated.")
        else:
            await ctx.send(f"{curr_user.member.display_name} took {damage} damage. Remaining hit points: {curr_user.currHitPoints}")

        await ctx.send("It's " + costants.curr_campaign.curr_encounter.get_next_in_order() + "'s turn.")

    @commands.command()
    async def get_all_monsters(self, ctx):
        await ctx.send(MonstersDataBase.get_all_monsters())

    @commands.command()
    async def prepare(self, ctx, spell_name: str):
        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        spell_name = spell_name.lower()

        if SpellDataBase.get_spell(spell_name) is None:
            await ctx.send("Spell not found")
            return

        if curr_user.adv_class == AdvClass.WIZARD or curr_user.adv_class == AdvClass.CLERIC:
            if SpellDataBase.get_spell(spell_name).level == 0:
                await ctx.send("Cannot prepare cantrips")
                return

            if len(curr_user.prepared_spells) >= curr_user.max_preparable_spells:
                await ctx.send("No more spell slots available")
                return

            if spell_name in curr_user.prepared_spells:
                await ctx.send("Spell already prepared")
                return

            if spell_name not in curr_user.spells_known_list:
                await ctx.send("Spell not known")
                return

            curr_user.prepared_spells.append(spell_name)
            await ctx.send(f"{spell_name} prepared. Remaining spell slots: {curr_user.max_preparable_spells - len(curr_user.prepared_spells)}")
        else:
            await ctx.send("You cannot prepare spells")
            return

    @commands.command()
    async def unprepare(self, ctx, spell_name: str):
        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        spell_name = spell_name.lower()

        if spell_name in curr_user.prepared_spells:
            curr_user.prepared_spells.remove(spell_name)
            await ctx.send(f"{spell_name} unprepared. Remaining spell slots: {curr_user.max_preparable_spells - len(curr_user.prepared_spells)}")
        else:
            await ctx.send("Spell was never prepared")

    @commands.command()
    async def cast(self, ctx, spell_name: str, params: str = None):
        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        spell_name = spell_name.lower()

        if spell_name in SpellDataBase.spell_dic:
            if SpellDataBase.spell_dic.get(spell_name).level == 0:
                if spell_name in curr_user.spells_known_list:
                    res = SpellDataBase.spell_dic.get(spell_name).cast(curr_user, params)
                    await ctx.send(res)
                else:
                    await ctx.send("Spell not known")
            else:
                if spell_name in curr_user.prepared_spells and curr_user.curr_spell_slots > 0:
                    res = SpellDataBase.spell_dic.get(spell_name).cast(curr_user, params)
                    await ctx.send(res)
                else:
                    if curr_user.curr_spell_slots <= 0:
                        await ctx.send("No slot available")
                    else:
                        await ctx.send("Spell not prepared")
        else:
            await ctx.send("Spell not found")

    @commands.command()
    async def rest(self, ctx):
        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        curr_user.curr_spell_slots = curr_user.max_spell_slots
        await ctx.send("Spell slots restored. You have now " + str(curr_user.curr_spell_slots) + " spell slots.")

    @commands.command()
    async def get_from_name(self, ctx, name: str):
        curr_user = None
        for user in costants.curr_campaign.campaign_member_list:
            if user.member.display_name == name:
                curr_user = user

        await ctx.send("Mention: " + curr_user.member.mention)

    @commands.command()
    async def get_prepared_spells(self, ctx):
        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        await ctx.send(curr_user.get_prepared_spells_str())

    @commands.command()
    async def get_inventory(self, ctx):
        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        await ctx.send(curr_user.get_inventory_str())

    @commands.command()
    async def get_equipment(self, ctx):
        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        await ctx.send(curr_user.get_equipment_str())

    @commands.command()
    async def get_known_spells(self, ctx):
        curr_user = get_user(ctx.author)

        if curr_user is None:
            return

        await ctx.send(curr_user.get_known_spells_str())


async def setup(bot):
    await bot.add_cog(Game(bot))
