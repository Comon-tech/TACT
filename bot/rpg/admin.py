from discord import Interaction, Member, app_commands
from discord.ext.commands import Bot, Cog

from bot.rpg.board import Board
from core.user import DbUser
from core.utils import clamp


class Admin(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(description="Add an amount to a memeber's stats")
    async def add(
        self, interaction: Interaction, member: Member = None, query: str = ""
    ):
        supported_keys = ["xp", "gold", "items"]
        member = member or interaction.user
        db_user = DbUser.load(member.id)

        # Parse the query argument (e.g. "gold:-10 xp:+20 items:+potion")
        if not query:
            await interaction.response.send_message(
                f":warning: Query is required.\nQuery should contain tokens with the format `key:value` divided by space.",
                ephemeral=False,
            )
            return

        updated_db_user_raw = db_user.model_dump()
        changes = ""
        for token in query.split():
            if ":" not in token:
                await interaction.response.send_message(
                    f"⛔ Error in query: ```py\n{query}```Expected `:` in token `{token}`.\nToken format should be `key:value`",
                    ephemeral=False,
                )
                return
            key, value_to_add = token.split(":")
            if key not in supported_keys:
                await interaction.response.send_message(
                    f"⛔ Error in query ```py\n{query}```\nKey `{key}` is not supported.\nSupported keys are `{supported_keys}`.",
                    ephemeral=False,
                )
                return
            try:
                value = updated_db_user_raw[key]
                if isinstance(updated_db_user_raw[key], int):
                    new_value = value + int(value_to_add)
                    new_value = clamp(new_value, 0, abs(new_value))
                    updated_db_user_raw[key] = new_value
                    changes += (
                        f"- `{key}`: `{value} + {value_to_add}` ➡ `{new_value}`\n"
                    )
                if isinstance(updated_db_user_raw[key], list):
                    # TODO: support + sign to remove items form the list
                    new_value = value + str(value_to_add).split(",")
                    updated_db_user_raw[key] = new_value
                    changes += (
                        f"- `{key}`: `{value} + {value_to_add}` ➡ `{new_value}`\n"
                    )
            except:
                updated_db_user_raw = None
        db_user = DbUser.create(updated_db_user_raw)

        # Update database user
        if not db_user:
            await interaction.response.send_message(
                f"⛔ Could not update user data:\n```py\n# 👤 {member.display_name} ({member.name})\n# ❌```\nInvalid data.",
                ephemeral=False,
            )
        elif not db_user.save().modified_count:
            await interaction.response.send_message(
                f":information_source: No update was needed for user data:\n```py\n# 👤 {member.display_name} ({member.name})\n{db_user}\n```",
                ephemeral=False,
            )
        else:
            await interaction.response.send_message(
                f"✅ User data updated:\n```py\n# 👤 {member.display_name} ({member.name})\n{db_user}```\n{changes}",
                ephemeral=False,
            )

    # @add.error
    # async def add_error(
    #     self, interaction: Interaction, error: app_commands.AppCommandError
    # ):
    #     await interaction.response.send_message(f"❌ {error}", ephemeral=True)
