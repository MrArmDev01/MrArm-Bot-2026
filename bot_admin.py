import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class BotAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. เปลี่ยนชื่อเฉพาะในเซิร์ฟนี้ (Nickname)
    @app_commands.command(name="server_set_name", description="Change bot's name in THIS server only")
    @app_commands.describe(new_name="Enter nickname for this server")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def server_set_name(self, interaction: discord.Interaction, new_name: str):
        try:
            # แก้ไขข้อมูลสมาชิก (Member) ในเซิร์ฟเวอร์ที่เรียกคำสั่งเท่านั้น
            await interaction.guild.me.edit(nick=new_name)
            await interaction.response.send_message(f"✅ Nickname updated to **{new_name}** for this server!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to change nickname: {e}", ephemeral=True)

    # 2. เปลี่ยนรูปเฉพาะในเซิร์ฟนี้ (Server Avatar)
    @app_commands.command(name="server_set_avatar", description="Change bot's avatar in THIS server only (Requires Boost Level 2)")
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
                    
                    # แก้ไข Avatar เฉพาะใน Guild (เซิร์ฟเวอร์) นี้
                    await interaction.guild.me.edit(avatar=data)
                    await interaction.followup.send("✅ Server-specific avatar updated!")
        except discord.Forbidden:
            await interaction.followup.send("❌ Error: I cannot change server avatar. Either this server is not **Boost Level 2** or I lack 'Manage Nicknames/Manage Webhooks' permission.")
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {e}")

async def setup(bot):
    await bot.add_cog(BotAdmin(bot))
