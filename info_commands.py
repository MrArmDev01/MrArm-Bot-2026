import discord
from discord import app_commands
import datetime

# --- คำสั่ง /user_info (แบบละเอียด) ---
@app_commands.command(name="user_info", description="View all available information about a member")
@app_commands.describe(member="Select the member you want to inspect")
async def user_info(interaction: discord.Interaction, member: discord.Member = None):
    # หากไม่ระบุชื่อ ให้ดึงข้อมูลของคนที่ใช้คำสั่งเอง
    member = member or interaction.user
    
    # 1. จัดการข้อมูลยศ (Roles)
    roles = [role.mention for role in member.roles[1:]] # ไม่เอา @everyone
    roles.reverse() # เรียงจากยศสูงสุดลงไป
    roles_display = ", ".join(roles) if roles else "No Roles"
    
    # 2. จัดการข้อมูลวันที่ (Dates)
    created_at = member.created_at.strftime("%A, %B %d, %Y @ %I:%M %p")
    joined_at = member.joined_at.strftime("%A, %B %d, %Y @ %I:%M %p")
    
    # 3. ตรวจสอบสิทธิ์การใช้งาน (Permissions)
    perms = []
    if member.guild_permissions.administrator: perms.append("🛡️ Administrator")
    if member.guild_permissions.manage_guild: perms.append("⚙️ Manage Server")
    if member.guild_permissions.manage_roles: perms.append("🎭 Manage Roles")
    if member.guild_permissions.manage_channels: perms.append("📁 Manage Channels")
    if member.guild_permissions.ban_members: perms.append("🚫 Ban Members")
    if member.guild_permissions.kick_members: perms.append("👢 Kick Members")
    if member.guild_permissions.mention_everyone: perms.append("📢 Mention Everyone")
    perms_display = "\n".join(perms) if perms else "✅ General Member"

    # 4. ตรวจสอบสถานะและกิจกรรม (Status & Activity)
    status = str(member.status).title()
    activity_display = "None"
    if member.activity:
        if isinstance(member.activity, discord.Spotify):
            activity_display = f"🎧 Listening to **Spotify**: {member.activity.title} by {member.activity.artist}"
        elif isinstance(member.activity, discord.Game):
            activity_display = f"🎮 Playing **{member.activity.name}**"
        else:
            activity_display = f"✨ {member.activity.name}"

    # 5. สร้าง Embed แสดงผล
    embed = discord.Embed(title=f"User Profile: {member.name}", color=member.color)
    embed.set_thumbnail(url=member.display_avatar.url)
    
    # ข้อมูลทั่วไป
    embed.add_field(name="🆔 User ID", value=f"`{member.id}`", inline=True)
    embed.add_field(name="🏷️ Nickname", value=member.nick or "None", inline=True)
    embed.add_field(name="🌐 Status", value=status, inline=True)
    
    # วันที่สำคัญ
    embed.add_field(name="📅 Account Created", value=f"{created_at}", inline=False)
    embed.add_field(name="📥 Joined Server", value=f"{joined_at}", inline=False)
    
    # กิจกรรมที่ทำอยู่
    embed.add_field(name="👾 Current Activity", value=activity_display, inline=False)
    
    # ยศ (จำกัดการแสดงผลถ้าเยอะเกินไปเพื่อไม่ให้ Embed พัง)
    if len(roles_display) > 1024:
        roles_display = f"{roles_display[:1020]}..."
    embed.add_field(name=f"🎭 Roles [{len(roles)}]", value=roles_display, inline=False)
    
    # สิทธิ์การใช้งานหลัก
    embed.add_field(name="⚔️ Key Permissions", value=perms_display, inline=False)
    
    # รูป Banner (ถ้ามี - ต้องใช้บอทที่มีสิทธิ์พิเศษหรือสมาชิกที่มี Nitro)
    if member.desktop_status == discord.Status.online: device = "Desktop 🖥️"
    elif member.mobile_status == discord.Status.online: device = "Mobile 📱"
    else: device = "Unknown/Offline"
    
    embed.set_footer(text=f"Last Device Seen: {device} | Requested by {interaction.user.name}")
    embed.timestamp = datetime.datetime.now()

    await interaction.response.send_message(embed=embed)
