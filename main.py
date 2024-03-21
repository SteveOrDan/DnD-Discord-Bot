import os
import discord
import asyncio
import logging

from discord.ext import commands
import costants

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), status=discord.Status.online, activity=discord.Game(name="Minecraft"))
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


@bot.event
async def on_ready():
    print("Hello! The bot is ready!")


# @bot.command()
# async def reload_ext(ext):
#     await bot.reload_extension(f"cogs.{ext}")


async def main():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

asyncio.run(main())
discord.utils.setup_logging()
bot.run(costants.BOT_TOKEN, log_handler=handler, log_level=logging.DEBUG)