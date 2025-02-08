import dotenv
from colorama import Fore
from discord import Interaction, Message, Status, app_commands
from discord.ext.commands import Bot, Cog, CommandError, Context

from pyproject import PROJECT

dotenv.load_dotenv()


class Monitor(Cog):
    """Checks and reports system status."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(description="Sync commands.")
    async def sync(self, interaction: Interaction):
        await Monitor.sync_commands(self.bot)
        await interaction.response.send_message("Commands synced!")

    @Cog.listener()
    async def on_ready(self):
        print(
            f"{Fore.GREEN}[👤{self.bot.user}] 🤖 {PROJECT["name"]} v{PROJECT["version"]} bot launched.{Fore.RESET}\n"
        )
        Monitor.log_local_commands(self.bot)
        Monitor.log_local_old_commands(self.bot)

    @Cog.listener()
    async def on_message(self, message: Message):
        Monitor.log_message(message)

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        pass

    @Cog.listener()
    async def on_error(self, event: str, *args, **kwargs):
        pass

    # ----------------------------------------------------------------------------------------------------

    @staticmethod
    async def sync_commands(bot: Bot):
        print("⏳ Syncing commands...")
        all_cmds = bot.tree.get_commands()
        synced_cmds = await bot.tree.sync()
        for cmd in synced_cmds:
            print(f"✔  {cmd} command synced.")
        print(f"✅ {len(synced_cmds)}/{len(all_cmds)} commands synced.\n")

    @staticmethod
    def log_local_commands(bot: Bot):
        print("🔘 Local Commands:")
        for cmd in bot.tree.get_commands():
            print("\t/", cmd.name, ":", cmd.description)
        print()

    @staticmethod
    async def log_remote_commands(bot: Bot):
        print("🟢 Remote Commands:")
        for cmd in await bot.tree.fetch_commands():
            print("\t/", cmd.name, ":", cmd.description)
        print()

    @staticmethod
    def log_local_old_commands(bot: Bot):
        print("⚫ Local Old Commands:")
        for cmd in bot.commands:
            print("\t!", cmd.name, ":", cmd.description)
        print()

    @staticmethod
    def log_message(message: Message):
        time = message.created_at.strftime("%Y-%m-%d %X")
        print(
            f'✉  [{message.guild}][{message.channel}] 👤 @{message.author} sent {Fore.BLUE}"{message.content}"{Fore.RESET} on {time}.'
        )
