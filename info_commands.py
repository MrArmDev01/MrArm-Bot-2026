import discord
from discord import app_commands
from discord.ext import commands
import datetime

# สร้างคลาส Cog เพื่อให้บอทโหลดได้
class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ย้ายคำสั่งมาไว้ในคลาส และเปลี่ยน @tree.command เป็น @app_commands.command
    @app_commands.command(name="user_info", description="View all available information about a member")
    @app_commands.describe(member="Select the member you want to inspect")
    async def user_info(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        
        # --- ส่วนการดึงข้อมูล (เหมือนเดิมที่คุณต้องการ) ---
        roles = [role.mention for role in member.roles[1:]]
        roles.reverse()
        roles_display = ", ".join(roles) if roles else "No Roles"
        
        created_at = member.created_at.strftime("%A, %B %d, %Y")
        joined_at = member.joined_at.strftime("%A, %B %d, %Y")
        
        perms = []
        if member.guild_permissions.administrator: perms.append("🛡️ Administrator")
        if member.guild_permissions.manage_guild: perms.append("⚙️ Manage Server")
        perms_display = ", ".join(perms) if perms else "General Member"

        embed = discord.Embed(title=f"User Profile: {member.name}", color=member.color)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="🆔 User ID", value=f"`{member.id}`", inline=True)
        embed.add_field(name="🌐 Status", value=str(member.status).title(), inline=True)
        embed.add_field(name="📅 Account Created", value=created_at, inline=False)
        embed.add_field(name="📥 Joined Server", value=joined_at, inline=False)
        embed.add_field(name=f"🎭 Roles [{len(roles)}]", value=roles_display[:1024], inline=False)
        embed.add_field(name="⚔️ Key Permissions", value=perms_display, inline=False)
        
        embed.timestamp = datetime.datetime.now()
        await interaction.response.send_message(embed=embed)

# --- ส่วนสำคัญที่สุด: ฟังก์ชัน setup สำหรับโหลดไฟล์ ---
async def setup(bot):
    await bot.add_cog(UserInfo(bot))
