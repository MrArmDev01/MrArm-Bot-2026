import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class GhostPing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="fake_pings", description="Send invisible pings to a user (Ghost Ping)")
    @app_commands.describe(target="The victim of the ghost pings", amount="How many pings? (Max 20)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def fake_pings(self, interaction: discord.Interaction, target: discord.Member, amount: int = 5):
        # Limit to 20 pings to prevent bot being flagged for spam
        if amount > 20:
            amount = 20

        # Admin confirmation (only you see this)
        await interaction.response.send_message(f"👻 Sending {amount} ghost pings to {target.display_name}...", ephemeral=True)

        for _ in range(amount):
            # 1. Send the mention
            ping_msg = await interaction.channel.send(target.mention)
            # 2. Delete it immediately (0.1 seconds)
            await ping_msg.delete()
            # 3. Small delay to make sure the notification pops up on their device
            await asyncio.sleep(0.5)

async def setup(bot):
    await bot.add_cog(GhostPing(bot))
    