from collections import defaultdict

from discord import Message
from discord.ext.commands import Bot, Cog

from core.user import DbUser


class Filter(Cog):
    """Filters blacklisted message content."""

    BLACKLIST_PATH = "./bot/general/blacklist.txt"
    MAX_OFFENSES = 5
    XP_PENALTY = 500

    def __init__(self, bot: Bot):
        self.bot = bot
        self.offenses = defaultdict(int)  # { "user_id": offense_count }
        with open(self.BLACKLIST_PATH, "r") as file:
            self.blacklist_words = file.read().split("\n")

    @Cog.listener()
    async def on_message(self, message: Message):
        user = message.author
        if user.bot:
            return
        content = message.content

        for bl_word in self.blacklist_words:
            if bl_word not in content:
                continue

            # censor message
            await message.delete()
            await message.channel.send(f"🛑 {user.mention}: ||{content}||")

            # mark offense & penalize abuse
            self.offenses[user.id] += 1
            if self.offenses[user.id] < self.MAX_OFFENSES:
                continue
            db_user = DbUser.load(user.id)
            if db_user:
                db_user.xp -= self.XP_PENALTY
                db_user.save()
                self.offenses[user.id] = 0
                await user.send(
                    f"🚨 ***You have used offensive words too many times. You have been penalized `{self.XP_PENALTY}` XP!***"
                )
                await message.channel.send(
                    f"🚨 {user.mention} ***has been penalized `{self.XP_PENALTY}` XPs for using offensive words too many times!!.***"
                )
