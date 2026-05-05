import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class ModeratorTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear_user", description="Clean up messages from a specific member")
    @app_commands.describe(
        member="The member whose messages you want to delete",
        limit="How many messages to scan (default 50)"
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear_user(self, interaction: discord.Interaction, member: discord.Member, limit: int = 50):
        # 1. ส่งการตอบรับเบื้องต้น (กันบอทค้างกรณีลบเยอะ)
        await interaction.response.defer(ephemeral=True)
        
        # 2. ฟังก์ชันตรวจสอบว่าเป็นข้อความของสมาชิกคนนั้นไหม
        def is_member(m):
            return m.author.id == member.id

        try:
            # 3. สั่งลบข้อความตามเงื่อนไข
            deleted = await interaction.channel.purge(limit=limit, check=is_member)
            
            # 4. แจ้งผลลัพธ์แบบเรียบหรู
            embed = discord.Embed(
                description=f"System has successfully removed **{len(deleted)}** messages sent by {member.mention}.",
                color=0x2f3136
            )
            embed.set_author(name="Purge Operation Complete", icon_url=member.display_avatar.url)
            embed.set_footer(text=f"Scan Limit: {limit} messages")
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except discord.Forbidden:
            await interaction.followup.send("Error: I do not have permission to delete messages.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"An unexpected error occurred: {str(e)}", ephemeral=True)

# ฟังก์ชัน setup สำหรับโหลด Cog
async def setup(bot):
    await bot.add_cog(ModeratorTools(bot))
