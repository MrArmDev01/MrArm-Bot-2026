import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class BotAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. Change Bot Name
    @app_commands.command(name="set_bot_name", description="Change the bot's username")
    @app_commands.describe(name="New username for the bot")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_bot_name(self, interaction: discord.Interaction, name: str):
        try:
            await self.bot.user.edit(username=name)
            await interaction.response.send_message(f"✅ Bot name changed to: **{name}**", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed: {e}", ephemeral=True)

    # 2. Change Bot Avatar
    @app_commands.command(name="set_bot_avatar", description="Change the bot's avatar")
    @app_commands.describe(image_url="Direct URL of the image")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_bot_avatar(self, interaction: discord.Interaction, image_url: str):
        await interaction.response.defer(ephemeral=True)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    if resp.status != 200:
                        return await interaction.followup.send("❌ Could not download image.")
                    data = await resp.read()
                    await self.bot.user.edit(avatar=data)
                    await interaction.followup.send("✅ Avatar updated successfully!")
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {e}")

    # 3. Change Bot Banner (Requires Nitro on some bots or specific conditions)
    @app_commands.command(name="set_bot_banner", description="Change the bot's banner image")
    @app_commands.describe(image_url="Direct URL of the image")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_bot_banner(self, interaction: discord.Interaction, image_url: str):
        await interaction.response.defer(ephemeral=True)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    if resp.status != 200:
                        return await interaction.followup.send("❌ Could not download image.")
                    data = await resp.read()
                    await self.bot.user.edit(banner=data)
                    await interaction.followup.send("✅ Banner updated successfully!")
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {e} (Note: Bots might need specific setup for banners)")

async def setup(bot):
    await bot.add_cog(BotAdmin(bot))
