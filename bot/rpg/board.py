from datetime import datetime, timedelta

from discord import Color, Embed, Interaction, Member, app_commands
from discord.ext.commands import Bot, Cog
from humanize import apnumber, naturaltime

from core.user import DbUser


class Board(Cog):
    """Allows players to view their data."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.guild_only()
    @app_commands.command(description="Get your or another member's information")
    async def info(self, interaction: Interaction, user: Member = None):
        user = user or interaction.user
        db_user = DbUser.load(user.id)
        embed = Embed(
            title=f"{user.display_name}",
            description=" ".join(
                [
                    f"`{role.name}`"
                    for role in user.roles
                    if role != user.guild.default_role
                ]
            ),
            color=Color.blue(),
        )
        if db_user:
            embed.add_field(name="", value="", inline=False)
            embed.add_field(
                name="Level",
                value=f"🏅 **{apnumber(db_user.level)}**\n{db_user.draw_level_progress_bar()}",
            )
            embed.add_field(
                name="XP",
                value=f"💰 **{db_user.xp}** / {db_user.next_level_xp}",
            )
            embed.add_field(
                name="Inventory",
                value=f"📦 **{apnumber(len(db_user.inventory))}** _items_",
                inline=False,
            )
            embed.add_field(name="", value="", inline=False)
            embed.add_field(
                name="",
                value=f"-# ⌚ _Joined_ {user.guild.name} **{naturaltime(user.joined_at)}**\n-# ⌚ _Joined_ Discord **{naturaltime(user.created_at)}**",
            )
            embed.set_thumbnail(url=user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.guild_only()
    @app_commands.command(description="View leaderboard")
    async def leaderboard(self, interaction: Interaction):
        await interaction.response.defer()
        raw_db_users = DbUser.COLLECTION.find()
        if not raw_db_users:
            await interaction.followup.send("No members found for the leaderboard.")
            return
        raw_db_users = raw_db_users.sort([("level", -1), ("xp", -1)])
        embed = Embed(title="🏆 Leaderboard", color=Color.blue())
        for i, raw_db_user in enumerate(raw_db_users[:10]):
            db_user = DbUser.create(raw_db_user)
            if not db_user:
                continue
            user = interaction.guild.get_member(
                db_user.id
            ) or await interaction.guild.fetch_member(db_user.id)
            user_name = user.display_name if user else f"Unknown User ({db_user.id})"
            embed.add_field(
                name="",
                value=10 * "➖",
                inline=False,
            )
            embed.add_field(
                name="Player",
                value=f"✨ **{i + 1}** 👤 {user_name}",
            )
            embed.add_field(
                name=f"Level",
                value=f"🏅 **{apnumber(db_user.level)}**",
            )
            embed.add_field(
                name=f"XP",
                value=f"💰 **{db_user.xp}** / {db_user.next_level_xp}",
            )
        await interaction.followup.send(embed=embed)
