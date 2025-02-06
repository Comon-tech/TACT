from colorama import Fore, Style
from discord import Message, Status
from discord.ext.commands import Bot, Cog, CommandError, Context

from pyproject import PROJECT


class Monitor(Cog):
    """Checks and reports system status."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        bot = self.bot
        print(
            f"{Fore.GREEN}[👤{bot.user}] 🤖 {PROJECT["name"]} v{PROJECT["version"]} bot launched.{Style.RESET_ALL}\n"
        )
        try:
            await bot.change_presence(status=Status.online)
            print("⏳ Syncing commands...")
            all_cmds = bot.tree.get_commands()
            synced_cmds = await bot.tree.sync()
            for cmd in synced_cmds:
                print(f"✔  {cmd} command synced.")
            print(f"✅ {len(synced_cmds)}/{len(all_cmds)} commands synced.\n")
        except Exception as e:
            print(f"⛔ Error in '{self.on_ready.__name__}':\n\t{e}")

    @Cog.listener()
    async def on_message(self, message: Message):
        time = message.created_at.strftime("%Y-%m-%d %X")
        server = message.guild.name
        channel = message.channel.name
        author = message.author
        content = message.content
        print(f"✉  [{time}][{server}][{channel}] {author}: { content}")

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        pass

    @Cog.listener()
    async def on_error(self, event: str, *args, **kwargs):
        pass
