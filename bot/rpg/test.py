from discord import Interaction, app_commands
from discord.ext import commands
from discord.ext.commands import Cog


class Test(Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----------------------------------------------------------------------------------------------------
    # * New Syle Commands (/)
    # ----------------------------------------------------------------------------------------------------

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="admin", description="Checks if you are administrator")
    async def admin_new_style_cmd(self, interaction: Interaction):
        await interaction.response.send_message(
            f"[New / Command]\n✅ YOU ({interaction.user}) ARE ADMIN !"
        )

    @admin_new_style_cmd.error
    async def sadmin_error(
        self, interaction: Interaction, error: app_commands.AppCommandError
    ):
        await interaction.response.send_message(
            f"[New / Command]\n❌ you ({interaction.user}) are NOT admin."
        )

    # ----------------------------------------------------------------------------------------------------
    # * Old Style Commands (*)
    # ----------------------------------------------------------------------------------------------------
    @commands.has_guild_permissions(administrator=True)
    @commands.command(name="admin")
    async def admin_old_style_cmd(self, ctx: commands.Context):
        """Checks if you are administrator"""
        await ctx.send(f"[Old ! Command]\n✔ YOU ({ctx.author}) ARE ADMIN !")

    @admin_old_style_cmd.error
    async def admin_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"[Old ! Command]\n❌ you ({ctx.author}) are NOT admin.")
