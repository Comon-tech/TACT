import asyncio
import os

import discord
import dotenv
from discord.ext.commands import Bot, Cog

from core.dynamic_import import import_classes
from pyproject import PROJECT


def run_bot():
    dotenv.load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True
    bot = Bot(command_prefix="/", intents=intents)
    cogs = import_classes("bot/cogs", Cog)

    async def load_cogs():
        try:
            print("⏳ Loading cogs...")
            for Class in cogs:
                await bot.add_cog(Class(bot))
                print(f"✔ '{Class.__cog_name__}' cog loaded from '{Class.__module__}'.")
            print(f"✅ {len(bot.cogs)}/{len(cogs)} cogs loaded.")
        except Exception as e:
            print(f"⛔⚙  Error when loading cog from '{Class.__module__}':\n\t{e}\n")

    @bot.event
    async def on_ready():
        try:
            await bot.change_presence(status=discord.Status.online)
            print("⏳ Syncing commands...")
            all_cmds = bot.tree.get_commands()
            synced_cmds = await bot.tree.sync()
            for cmd in synced_cmds:
                print(f"✔ '{cmd}' command synced.")
            print(f"✅ {len(synced_cmds)}/{len(all_cmds)} commands synced.")
        except Exception as e:
            print(f"⛔ Error in '{on_ready.__name__}':\n\t{e}")
        print(
            f"🤖 {PROJECT["name"]} v{PROJECT["version"]} Bot is ready! [👤{bot.user}]\n"
        )

    asyncio.run(load_cogs())
    bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    run_bot()
