import discord
from discord.ext import commands


class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx):
        await ctx.channel.purge()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! Latency:{self.bot.latency}")


async def setup(bot):
    await bot.add_cog(Utils(bot))
    