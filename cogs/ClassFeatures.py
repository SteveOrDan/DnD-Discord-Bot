import discord
from discord.ext import commands
import costants


class ClassFeatures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cleric(self, ctx):
        if ctx.channel.id == costants.curr_campaign.CLASS_INFO_TEXT_CH.id:
            await ctx.channel.send(embed=embed_cleric)

    @commands.command()
    async def fighter(self, ctx):
        if ctx.channel.id == costants.curr_campaign.CLASS_INFO_TEXT_CH.id:
            await ctx.channel.send(embed=embed_fighter)

    @commands.command()
    async def rogue(self, ctx):
        if ctx.channel.id == costants.curr_campaign.CLASS_INFO_TEXT_CH.id:
            await ctx.channel.send(embed=embed_rogue)

    @commands.command()
    async def wizard(self, ctx):
        if ctx.channel.id == costants.curr_campaign.CLASS_INFO_TEXT_CH.id:
            await ctx.channel.send(embed=embed_wizard)


async def setup(bot):
    await bot.add_cog(ClassFeatures(bot))


# Cleric
embed_cleric = discord.Embed(title="Cleric",
                             description="Pages from 22 to 25",
                             colour=0xd33bf5)
embed_cleric.add_field(name="Info",
                       value="Basic Rules book download link: https://dnd.wizards.com/what-is-dnd/basic-rules")

# Fighter
embed_fighter = discord.Embed(title="Fighter",
                              description="Pages from 26 to 28",
                              colour=0xfcc600)
embed_fighter.add_field(name="Info",
                        value="Basic Rules book download link: https://dnd.wizards.com/what-is-dnd/basic-rules")

# Rogue
embed_rogue = discord.Embed(title="Rogue",
                            description="Pages from 28 to 30",
                            colour=0x525252)
embed_rogue.add_field(name="Info",
                      value="Basic Rules book download link: https://dnd.wizards.com/what-is-dnd/basic-rules")

# Wizard
embed_wizard = discord.Embed(title="Wizard",
                             description="Pages from 31 to 34",
                             colour=0x0a81f7)
embed_wizard.add_field(name="Info",
                       value="Basic Rules book download link: https://dnd.wizards.com/what-is-dnd/basic-rules")
