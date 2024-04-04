import os

import discord
import asyncio
import logging

from discord.ext import commands

import costants
from CampaignRoleView import CampaignRoleView
from ClassView import ClassView
from RaceView import RaceView


class PersistentViewBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), status=discord.Status.online, activity=discord.Game(name="DnD 5e"))

    async def setup_hook(self) -> None:
        self.add_view(CampaignRoleView(None))
        self.add_view(ClassView(guild=self.get_guild(costants.GUILD_ID)))
        self.add_view(RaceView(guild=self.get_guild(costants.GUILD_ID)))


# bot = PersistentViewBot()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), status=discord.Status.online, activity=discord.Game(name="DnD 5e"))
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


@bot.event
async def on_ready():
    print("Hello! The bot is ready!")


async def main():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


asyncio.run(main())
discord.utils.setup_logging()
bot.run(costants.BOT_TOKEN, log_handler=handler, log_level=logging.DEBUG)
