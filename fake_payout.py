import discord
from discord import app_commands
from discord.ext import commands
import random

class FakePayout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class PayoutView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Check Transaction Status", style=discord.ButtonStyle.secondary, emoji="📋")
        async def check_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
            # The prank reveal
            await interaction.response.send_message(
                "⚠️ **Transaction Error:** This payout was a simulated prank. No Robux were actually sent to your account. Gotcha! 😂", 
                ephemeral=True
            )

    @app_commands.command(name="fake_payout", description="Send a fake Roblox Robux payout to a friend")
    @app_commands.describe(target="The user to receive the fake Robux", amount="Amount of Robux (e.g. 1000)")
    @app_commands.checks.has_permissions(administrator=True)
    async def fake_payout(self, interaction: discord.Interaction, target: discord.Member, amount: int):
        # Professional-looking Roblox Payout Embed
        embed = discord.Embed(
            title="💰 Roblox Group Payout Successful",
            description=(
                f"The group owner has successfully sent Robux to **{target.display_name}**.\n\n"
                f"**Transaction Details:**\n"
                f"• **Amount:** `{amount:,} Robux`\n"
                f"• **Recipient:** `{target.name}`\n"
                f"• **Status:** `Completed`\n"
                f"• **Transaction ID:** `{random.randint(10000000, 99999999)}`"
            ),
            color=discord.Color.from_str("#00b06f") # Roblox Green
        )
        # Roblox Gold/Robux Icon
        embed.set_thumbnail(url="https://images.rbxcdn.com/f7528a4be46b1464c185bb5e30b135c3.png")
        embed.set_footer(text="Funds may take 3-5 business days to appear in your account pending balance.")

        # Confirm to you
        await interaction.response.send_message(f"✅ Payout prank sent to {target.mention}!", ephemeral=True)
        
        # Send the prank to the channel
        await interaction.channel.send(content=f"{target.mention}", embed=embed, view=self.PayoutView())

async def setup(bot):
    await bot.add_cog(FakePayout(bot))