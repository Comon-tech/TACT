import tomllib
from collections import defaultdict

from discord import Message
from discord.ext.commands import Bot, Cog

from core.db.user import DbUser

# ----------------------------------------------------------------------------------------------------
# * Blacklist
# ----------------------------------------------------------------------------------------------------
with open("bot/cogs/chat_filter_cog.toml", "rb") as file:
    BLACKLIST_WORDS = tomllib.load(file)["blacklist_words"]


# ----------------------------------------------------------------------------------------------------
# * Chat Filter Cog
# ----------------------------------------------------------------------------------------------------
class ChatFilterCog(Cog):
    max_offenses = 5
    xp_penalty = 500

    def __init__(self, bot: Bot):
        self.bot = bot
        self.offenses = defaultdict(int)  # { "user_id": offense_count }

    @Cog.listener()
    async def on_message(self, message: Message):
        user = message.author
        content = message.content
        print(f"✉  '[{message.guild.name}][{message.channel.name}] {user}: {content}'")
        if user.bot:
            return  # Ignore bot messages

        # chat filter & offense punishment
        for bl_word in BLACKLIST_WORDS:
            if bl_word not in content:
                continue

            # censor message
            await message.delete()
            await message.channel.send(f"🛑 {user.mention}: ||{content}||")

            # mark offense
            self.offenses[user.id] += 1

            # penalize abuse
            if self.offenses[user.id] < self.max_offenses:
                continue
            db_user = DbUser.load(user.id)
            db_user.xp -= self.xp_penalty
            db_user.save()
            self.offenses[user.id] = 0
            await user.send(
                f"🚨 ***You have used offensive words too many times. You have been penalized `{self.xp_penalty}` XP!***"
            )
            await message.channel.send(
                f"🚨 {user.mention} ***has been penalized `{self.xp_penalty}` XPs for using offensive words too many times!!.***"
            )
