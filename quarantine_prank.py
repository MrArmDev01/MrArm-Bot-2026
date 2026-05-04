import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class QuarantinePrank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="quarantine_user", description="Prank a user by pretending they are quarantined/invisible")
    @app_commands.describe(target="The user to quarantine")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def quarantine_user(self, interaction: discord.Interaction, target: discord.Member):
        # Admin confirmation (only you see)
        await interaction.response.send_message(f"☣️ Quarantine sequence started for {target.display_name}...", ephemeral=True)

        # 1. Create a professional system embed
        embed = discord.Embed(
            title="🛑 User Quarantine Notification",
            description=(
                f"User **{target.name}#{target.discriminator}** has been flagged by Discord Safety Systems.\n\n"
                f"**Reason:** `Potential Account Compromise / Bot-like Behavior`\n"
                f"**Status:** `Shadow-Quarantined`\n\n"
                f"Messages sent by this user will now be filtered and visible only to Discord Staff for manual review. "
                f"The user may appear 'offline' or 'invisible' to other members."
            ),
            color=discord.Color.red()
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/564/564619.png")
        embed.set_footer(text="Discord Safety Audit • ID: " + str(target.id))

        # 2. Send the "System" message to the channel
        await interaction.channel.send(embed=embed)

        # 3. Optional: Send a fake DM to the target
        try:
            await target.send(
                f"**Official Message from Discord Support:**\n"
                f"Your account in server **{interaction.guild.name}** has been restricted. "
                f"Your messages are no longer visible to other members until you complete a security audit.\n"
                f"Ref: `ERR_SHADOW_BAN_V3`"
            )
        except:
            pass # In case they have DMs closed

async def setup(bot):
    await bot.add_cog(QuarantinePrank(bot))
    