import discord
from discord import app_commands
from discord.ext import commands
import random

class FakeCall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class CallView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Join Call", style=discord.ButtonStyle.green, emoji="📞")
        async def join_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
            # The prank response
            await interaction.response.send_message(
                "⚠️ **Failed to join:** The call is full or has been set to private by the host.", 
                ephemeral=True
            )

        @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
        async def decline_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message(
                "You have declined the call invitation.", 
                ephemeral=True
            )

    @app_commands.command(name="fake_call", description="Start a fake group call prank")
    @app_commands.describe(topic="The topic of the call (e.g. Secret Meeting)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def fake_call(self, interaction: discord.Interaction, topic: str = "Group Call"):
        # Create a professional Call Embed
        embed = discord.Embed(
            title=f"📞 {topic}",
            description=(
                f"**{interaction.user.display_name}** started a call.\n\n"
                "**Current participants:**\n"
                f"👤 {interaction.user.mention} (Host)\n"
                "👤 [Unknown User] \n"
                "👤 [Unknown User] \n\n"
                "*Waiting for others to join...*"
            ),
            color=discord.Color.from_str("#2ecc71") # Discord Call Green
        )
        embed.set_author(name="Discord Call Service", icon_url="https://cdn0.iconfinder.com/data/icons/free-social-media-set/24/discord-512.png")
        embed.set_footer(text="ID: " + str(random.randint(100000, 999999)))

        # Confirmation to the admin
        await interaction.response.send_message("✅ Fake call invitation sent!", ephemeral=True)
        
        # Send the prank to the channel
        await interaction.channel.send(embed=embed, view=self.CallView())

async def setup(bot):
    await bot.add_cog(FakeCall(bot))
    