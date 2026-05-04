import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class BotAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. Change Nickname (Free for all servers)
    @app_commands.command(name="server_set_name", description="Change bot's nickname in THIS server only")
    @app_commands.describe(new_name="Enter nickname for this server")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def server_set_name(self, interaction: discord.Interaction, new_name: str):
        try:
            await interaction.guild.me.edit(nick=new_name)
            await interaction.response.send_message(f"✅ Nickname updated to **{new_name}**!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed: {e}", ephemeral=True)

    # 2. Change Server Avatar (Requires Boost Level 2)
    @app_commands.command(name="server_set_avatar", description="Change bot's avatar in THIS server (Needs Boost Level 2)")
    @app_commands.describe(image_url="Direct URL of the image")
    @app_commands.checks.has_permissions(administrator=True)
    async def server_set_avatar(self, interaction: discord.Interaction, image_url: str):
        await interaction.response.defer(ephemeral=True)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    if resp.status != 200:
                        return await interaction.followup.send("❌ Could not download image.")
                    data = await resp.read()
                    await interaction.guild.me.edit(avatar=data)
                    await interaction.followup.send("✅ Server avatar updated!")
        except discord.Forbidden:
            await interaction.followup.send("❌ Error: Needs **Boost Level 2** to change server avatar.")
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {e}")

    # 3. Change Server Banner (Requires Boost Level 3)
    @app_commands.command(name="server_set_banner", description="Change bot's banner in THIS server (Needs Boost Level 3)")
    @app_commands.describe(image_url="Direct URL of the image")
    @app_commands.checks.has_permissions(administrator=True)
    async def server_set_banner(self, interaction: discord.Interaction, image_url: str):
        await interaction.response.defer(ephemeral=True)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    if resp.status != 200:
                        return await interaction.followup.send("❌ Could not download image.")
                    data = await resp.read()
                    
                    # Edit member banner for this specific guild
                    await interaction.guild.me.edit(banner=data)
                    await interaction.followup.send("✅ Server banner updated!")
        except discord.Forbidden:
            await interaction.followup.send("❌ Error: Needs **Boost Level 3** to change server banner.")
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {e}")

async def setup(bot):
    await bot.add_cog(BotAdmin(bot))
