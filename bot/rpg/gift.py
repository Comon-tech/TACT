from discord import Color, Embed, Interaction, Member, app_commands
from discord.ext.commands import Bot, Cog

from core.user import DbUser


class Gift(Cog):
    """Allows players to gift eachother."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.guild_only()
    @app_commands.command(description="Give gold to someone")
    async def donate(self, interaction: Interaction, member: Member, gold: int):
        interaction.response.defer()

        # Validate input
        if gold <= 0:
            await interaction.response.send_message(
                f"Your gold input value of **{gold}** is wrong.\nDid you mean **{-gold}** ?",
                ephemeral=True,
            )
            return

        # Retrieve donor user
        donor = interaction.user
        db_donor = DbUser.load(donor.id)
        if not db_donor:
            await interaction.response.send_message(
                f"There is a problem with {donor.display_name} data.", ephemeral=True
            )
            return

        # Retrieve recipient user
        recipient = member
        db_recipient = DbUser.load(recipient.id)
        if not db_recipient:
            await interaction.response.send_message(
                f"There is a problem with {recipient.display_name} data.",
                ephemeral=True,
            )
            return

        # Check if user is trying to donate to themselves
        if donor == recipient:
            await interaction.response.send_message(
                f"You can't donate to yourself.", ephemeral=True
            )
            return

        # Chek if donor has the gold
        if db_donor.gold < gold:
            await interaction.response.send_message(
                f"You don't enough to donate **💰 {gold} Gold**.\nYou have **💰 {db_donor.gold} Gold**.",
                ephemeral=True,
            )
            return

        # Add gold and update user data
        db_donor.gold = max(0, db_donor.gold - gold)
        db_recipient.gold += gold
        db_donor.save()
        db_recipient.save()

        # Create the response embed
        embed = Embed(
            title="💛 Gold Donation",
            description=(
                f"{recipient.mention} received **💰 {gold} Gold** from {donor.display_name}."
            ),
            color=Color.green(),
        )
        embed.set_author(name=donor.display_name, icon_url=donor.display_avatar)
        embed.set_thumbnail(url=recipient.display_avatar)

        # Respond with confirmation
        await interaction.response.send_message(embed=embed)
