from discord import Color, Embed, Interaction, app_commands
from discord.ext.commands import Bot, Cog


class Help(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="help", description="Get help with the commands")
    async def help(self, interaction: Interaction):
        all_cmds = self.bot.tree.get_commands()
        # all_cmds_txt = [f"{cmd.name}: {cmd.description}\n" for cmd in all_cmds]
        embed = Embed(
            title="📚 ACT Bot Help",
            description=(f"Use these commands to explore all features!\n\n"),
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
