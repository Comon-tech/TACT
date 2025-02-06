import asyncio
import logging
import os
import sys

import discord
import dotenv
from discord.ext.commands import Bot, Cog

from core.importx import import_classes


def run_bot():
    dotenv.load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True
    bot = Bot(command_prefix="/", intents=intents)
    cogs = import_classes("./bot/", Cog)

    async def load_cogs():
        try:
            print("⏳ Loading cogs...")
            for Class in cogs:
                await bot.add_cog(Class(bot))
                print(f"✔  {Class.__cog_name__} cog loaded from {Class.__module__}.")
            print(f"✅ {len(bot.cogs)}/{len(cogs)} cogs loaded.")
        except Exception as e:
            print(f"⛔⚙  Error when loading cog from '{Class.__module__}':\n\t{e}\n")

    asyncio.run(load_cogs())

    try:
        bot.run(os.getenv("DISCORD_TOKEN"), log_level=logging.ERROR)
    except Exception as e:
        logging.exception(f"Fatal error: {e}")
        print(f"Fatal error: {e}", file=sys.stderr)
