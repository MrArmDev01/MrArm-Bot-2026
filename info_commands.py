import discord
from discord import app_commands
from discord.ext import commands
import datetime

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="user_info", description="Detailed member profile overview")
    @app_commands.describe(member="Select the member you want to inspect")
    async def user_info(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        
        # จัดการข้อมูลยศ
        roles = [role.mention for role in member.roles[1:]]
        roles.reverse()
        roles_display = " ".join(roles) if roles else "None"
        
        # แปลงวันที่เป็น Discord Timestamp (สวยกว่า text ธรรมดา)
        created_ts = int(member.created_at.timestamp())
        joined_ts = int(member.joined_at.timestamp())
        
        # ตรวจสอบสิทธิ์การใช้งาน
        perms = []
        if member.guild_permissions.administrator: perms.append("Administrator")
        if member.guild_permissions.manage_guild: perms.append("Manage Server")
        if member.guild_permissions.manage_roles: perms.append("Manage Roles")
        if member.guild_permissions.ban_members: perms.append("Ban Members")
        perms_display = " • ".join(perms) if perms else "General Member"

        # ดีไซน์ Embed
        embed = discord.Embed(color=member.color if member.color.value != 0 else 0x2f3136)
        embed.set_author(name=f"User Information | {member.name}", icon_url=member.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar.url)

        # ส่วนที่ 1: ข้อมูลบัญชี (ใส่ Code Block ให้ดูเป็นระเบียบ)
        embed.add_field(
            name="── Identification ──", 
            value=f"**ID:** `{member.id}`\n**Status:** {str(member.status).upper()}\n**Nickname:** {member.nick or 'None'}", 
            inline=False
        )

        # ส่วนที่ 2: วันที่สำคัญ (ใช้ Timestamp แสดงผลแบบ Full Date และ Relative Time)
        embed.add_field(
            name="── Registration ──",
            value=f"**Created:** <t:{created_ts}:D> (<t:{created_ts}:R>)\n**Joined:** <t:{joined_ts}:D> (<t:{joined_ts}:R>)",
            inline=False
        )

        # ส่วนที่ 3: ยศและสิทธิ์
        embed.add_field(name=f"── Roles [{len(roles)}] ──", value=roles_display[:1024], inline=False)
        embed.add_field(name="── Permissions ──", value=f"*{perms_display}*", inline=False)

        # ส่วนท้าย
        embed.set_footer(text=f"Requested by {interaction.user.display_name}")
        embed.timestamp = datetime.datetime.now()

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(UserInfo(bot))
