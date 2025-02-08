import asyncio
import random
import re

from discord import Member, Message, TextChannel, User, utils
from discord.ext.commands import Bot, Cog

from core.user import DbUser


class Farm(Cog):
    """Allows players to gain stats and roles."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        member = message.author
        if member.bot or not isinstance(member, Member):
            return
        db_user = DbUser.load(member.id)

        if db_user:
            # gain xp per message sent
            xp_reward = Farm.calculate_xp_reward(message)
            db_user.xp += xp_reward
            print(f"👤 @{member.name} earned {xp_reward} xp.")

            # log xp gain to a "log" named channel
            # log_channel = utils.find(
            #     lambda c: "log" in c.name.lower(), message.guild.text_channels
            # )
            # if log_channel:
            #     await log_channel.send(
            #         f"👤 {user.display_name} earned **⏫ {xp_reward} Experience**."
            #     )

            # try level-up
            if db_user.try_level_up():
                gold_reward = random.randint(1, 500) * db_user.level
                db_user.gold += gold_reward
                await message.channel.send(
                    f"🎉 {member.mention}! You have reached **🏅 Level {db_user.level}** and earned **💰 {gold_reward} Gold**."
                )

            # try role-up
            awarded_role = await Farm.award_role(member, db_user.role_name)
            if awarded_role:
                gold_reward = random.randint(1, 1000) * db_user.level
                db_user.gold += gold_reward
                await message.channel.send(
                    f"🎉 {member.mention}! You have been awarded **{awarded_role.name} Role** and earned **💰 {gold_reward} Gold**."
                )

            # apply database changes
            db_user.save()

        # ensure other commands can still run
        # await self.bot.process_commands(message)

    # ----------------------------------------------------------------------------------------------------

    @staticmethod
    def calculate_xp_reward(message: Message):
        word_count = 0
        message_content = message.content

        # Exclude URLs
        message_content = re.sub(r"https?://\S+", "", message_content)  # Remove URLs
        word_count += len(message_content.split())

        # Handle embeds
        if message.embeds:
            word_count += len(message.embeds)  # Each embed counts as 1 word

        # Handle attachments (including GIFs, images, files)
        if message.attachments:
            word_count += len(message.attachments)  # Each attachment counts as 1 word

        # Minimum word count (to avoid 0 XP rewards)
        word_count = max(1, word_count)  # Ensure at least 1 word is counted

        return random.randint(1, word_count)

    @staticmethod
    async def award_role(user: Member, role_name: str):
        if role_name:
            role = utils.get(user.guild.roles, name=role_name)
            if role and role not in user.roles:
                await user.add_roles(role)
                return role
        return None

    @Warning
    @staticmethod
    async def run_random_xp_drop_listener(channel: TextChannel):
        """
        WARNING: Infinite Loop!\n
        Where are you planning to run this ? :O
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
