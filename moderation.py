import discord
from discord import app_commands, ui
from discord.ext import commands
import datetime

# --- Configuration สำหรับเก็บข้อมูล Warn ---
# (หมายเหตุ: ข้อมูลจะหายถ้าบอท Restart หากต้องการให้จำตลอดไปต้องใช้ Database ครับ)
warn_data = {} 

# --- 1. ระบบ Rules (เมนูเลือกกฎ) ---
class RulesDropdown(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label='Minor Moderator', 
                description='General rules and behavior guidelines.', 
                emoji='📜'
            ),
            discord.SelectOption(
                label='Moderator', 
                description='Rules for staff conduct and moderation.', 
                emoji='🛡️'
            ),
            discord.SelectOption(
                label='Major Moderator', 
                description='Severe violations and strict community rules.', 
                emoji='🚫'
            ),
        ]
        super().__init__(placeholder='Select a rule category to read...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # ตั้งค่าเนื้อหากฎแต่ละประเภท
        if self.values[0] == 'Minor Moderator':
            title, desc, color = "📜 Minor Moderator Rules", "1. No spamming or flooding chat.\n2. Be respectful to all members.\n3. No excessive use of CAPS.", 0x3498db
        elif self.values[0] == 'Moderator':
            title, desc, color = "🛡️ Moderator Rules", "1. Do not abuse staff permissions.\n2. Always log moderation actions.\n3. Stay neutral during conflicts.", 0x2ecc71
        else:
            title, desc, color = "🚫 Major Moderator Rules", "1. No raiding or malicious activities.\n2. No NSFW content allowed.\n3. No illegal content or harassment.", 0xe74c3c
        
        embed = discord.Embed(title=title, description=desc, color=color)
        embed.set_footer(text="Please follow the rules to keep the community safe.")
        # ส่งแบบ Ephemeral (เห็นเฉพาะคนที่กด) เพื่อไม่ให้รกห้อง
        await interaction.response.send_message(embed=embed, ephemeral=True)

class RulesView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RulesDropdown())

# --- 2. ระบบ Cog (คำสั่ง set_rules และ warn) ---
class ModerationSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # คำสั่งส่งกฎ (Embed + Dropdown)
    @app_commands.command(name="set_rules", description="Post the server rules with a dropdown menu")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_rules(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📖 Server Rules & Guidelines",
            description=(
                "Welcome to our community! To ensure a safe environment for everyone, "
                "please read and follow our rules.\n\n"
                "**Please select a category below to view the specific rules.**"
            ),
            color=0x2f3136
        )
        embed.set_footer(text="Compliance with these rules is mandatory.")
        
        await interaction.response.send_message("✅ Rules menu has been posted!", ephemeral=True)
        await interaction.channel.send(embed=embed, view=RulesView())

    # คำสั่งเตือน (Warn)
    @app_commands.command(name="warn", description="Warn a member for a rule violation")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        if member.bot:
            return await interaction.response.send_message("❌ You cannot warn a bot.", ephemeral=True)

        user_id = str(member.id)
        if user_id not in warn_data:
            warn_data[user_id] = []
        
        warn_data[user_id].append({
            "reason": reason,
            "admin": interaction.user.name,
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        count = len(warn_data[user_id])
        
        embed = discord.Embed(title="⚠️ Member Warned", color=0xf1c40f)
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="Total Warnings", value=str(count), inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Warned by {interaction.user.name}")
        
        await interaction.response.send_message(embed=embed)

        # ส่งข้อความไปบอกผู้ที่โดนเตือน
        try:
            await member.send(f"⚠️ You have been warned in **{interaction.guild.name}**\n**Reason:** {reason}\n**Total Warnings:** {count}")
        except:
            pass # ถ้าผู้ใช้ปิด DM บอทจะข้ามไป

    # คำสั่งเช็กประวัติการเตือน
    @app_commands.command(name="warns", description="Check warning history of a member")
    async def check_warns(self, interaction: discord.Interaction, member: discord.Member):
        user_id = str(member.id)
        if user_id not in warn_data or not warn_data[user_id]:
            return await interaction.response.send_message(f"✅ **{member.display_name}** has no warning history.", ephemeral=True)

        history = ""
        for i, entry in enumerate(warn_data[user_id], 1):
            history += f"**{i}.** {entry['reason']} (by {entry['admin']} on {entry['time']})\n"

        embed = discord.Embed(title=f"📋 Warn History: {member.display_name}", description=history, color=0xe74c3c)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ModerationSystem(bot))
