import discord
from discord import app_commands
from discord.ext import commands

class FakeNitro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class NitroView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
        async def accept_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
            # The ultimate Rickroll prank
            rickroll_url = "https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713"

            await interaction.response.send_message(
                f"**You've been Rickrolled!** 🎸\n{rickroll_url}\n\n*System: Nitro claim failed. Reason: Skill Issue.*", 
                ephemeral=True
            )

    @app_commands.command(name="fake_nitro", description="Send a fake Discord Nitro gift to Rickroll your friends")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def fake_nitro(self, interaction: discord.Interaction):
        # Professional-looking Nitro Embed
        embed = discord.Embed(
            title="You've been gifted Nitro!",
            description="**Mr.Arm** has sent you a gift of **Discord Nitro** for 1 month!\n\nClick the button below to claim your gift and enjoy the perks.",
            color=discord.Color.from_str("#7289da") # Discord Original Blue
        )
        # Official-looking Nitro Gift Icon
        embed.set_thumbnail(url="https://i.imgur.com/w9O8A6J.png") 
        embed.set_footer(text="Offer expires in 24 hours • Official Discord Promotion")

        # Confirm to the admin only
        await interaction.response.send_message("✅ Fake Nitro gift deployed! Watch them fall for it.", ephemeral=True)

        # Send the prank to the channel
        await interaction.channel.send(embed=embed, view=self.NitroView())

async def setup(bot):
    await bot.add_cog(FakeNitro(bot))
