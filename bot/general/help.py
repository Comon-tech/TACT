from colorama import Fore, Style
from discord import Color, Embed, Interaction, Status, app_commands
from discord.ext.commands import Bot, Cog

from pyproject import PROJECT


class Help(Cog):
    """Provides help and informations."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(description="Get help with the commands")
    async def help(self, interaction: Interaction):
        all_cmds = self.bot.tree.get_commands()
        embed = Embed(
            title=f"🤖 {PROJECT["name"]} v{PROJECT["version"]}",
            description=(f"{PROJECT["description"]}\n\n"),
            color=Color.blue(),
        )
        for cmd in all_cmds:
            embed.add_field(
                name=f"{self.bot.command_prefix}{cmd.name}",
                value=cmd.description,
                inline=False,
            )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)
