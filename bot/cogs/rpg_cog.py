import asyncio
import random

import discord
from discord import (
    Color,
    Embed,
    Interaction,
    Member,
    Message,
    TextChannel,
    app_commands,
)
from discord.ext.commands import Bot, Cog

from core.db.user import DbUser


# ----------------------------------------------------------------------------------------------------
# * RPG Cog
# ----------------------------------------------------------------------------------------------------
class RpgCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(description="Get your or another member's infos")
    async def infos(self, interaction: Interaction, user: Member = None):
        user = user or interaction.user
        db_user = DbUser.load(user.id)
        embed = Embed(
            title=f"{user.display_name}",
            description=", ".join(
                [role.name for role in user.roles if role != user.guild.default_role]
            ),
            color=Color.blue(),
        )
        embed.add_field(name="", value="\n\n", inline=False)
        embed.add_field(name="Level", value=f"🏅 **{db_user.level}**")
        # embed.add_field(name="", value="\n")
        embed.add_field(
            name="XP",
            value=f"💰 **{db_user.xp}** / {db_user.next_level_xp}",
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @Cog.listener()
    async def on_message(self, message: Message):
        user = message.author
        if user.bot:
            return  # Ignore bot messages
        db_user = DbUser.load(user.id)

        # gain xp per message sent
        xp_reward = random.randint(5, 100)
        db_user.xp += xp_reward
        print(f"👤 User '{user.name}' earned {xp_reward} XP!")

        # try update role
        awarded_role = await db_user.award_role(user)
        if awarded_role:
            xp_reward = random.randint(5, 1000)
            db_user.xp += xp_reward
            await message.channel.send(
                f"🎉🎉🎉 **Role UP** \n{user.mention} has been awarded the **{awarded_role.name}** role and has been awarded **{xp_reward}**XPs!"
            )

        # try level-up
        if db_user.try_level_up():
            print(f"👤 User '{user}' leveled up to {user.level}!, with {user.xp} XPs.")

        # apply database changes
        db_user.save()

        # ensure other commands can still run
        await self.bot.process_commands(message)

    async def run_random_xp_drop_listener(channel: TextChannel):
        """
        WARNING: Infinite Loop!
        where are you planning to run this ? :O
        """
        while True:
            await asyncio.sleep(random.randint(3600, 7200))  # 1-2 hours
            user = random.choice(channel.members)
            db_user = DbUser.load(user.id)
            xp_reward = random.randint(50, 1500)
            db_user.xp += xp_reward
            db_user.save()
            await channel.send(
                f"🎉 Surprise! {user.mention} just earned {xp_reward} XP!"
            )
