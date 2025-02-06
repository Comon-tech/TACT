import asyncio
import random

from discord import Member, Message, TextChannel, User, utils
from discord.ext.commands import Bot, Cog

from core.user import DbUser


class Farm(Cog):
    """Allows players to gain xp, level and roles."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        user = message.author
        if user.bot:
            return
        db_user = DbUser.load(user.id)

        if db_user:
            # gain xp per message sent
            xp_reward = random.randint(5, 100)
            db_user.xp += xp_reward
            print(f"👤 User '{user.name}' earned {xp_reward} XP!")

            # try update role
            awarded_role = await self.award_role(user, db_user.role_name)
            if awarded_role:
                xp_reward = random.randint(5, 1000)
                db_user.xp += xp_reward
                await message.channel.send(
                    f"🎉🎉🎉 **Role UP** \n{user.mention} has been awarded the **{awarded_role.name}** role and has been awarded **{xp_reward}**XPs!"
                )

            # try level-up
            if db_user.try_level_up():
                print(
                    f"👤 User '{user}' leveled up to {user.level}!, with {user.xp} XPs."
                )

            # apply database changes
            db_user.save()

        # ensure other commands can still run
        await self.bot.process_commands(message)

    async def award_role(self, user: User | Member, role_name: str):
        if role_name:
            role = utils.get(user.guild.roles, name=role_name)
            if role and role not in user.roles:
                await user.add_roles(role)
                return role
        return None

    # ----------------------------------------------------------------------------------------------------

    @Warning
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
