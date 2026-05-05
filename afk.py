import discord
from discord import app_commands
from discord.ext import commands
import datetime

class AfkSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {} # เก็บข้อมูล {user_id: reason}

    # 1. คำสั่งสำหรับตั้งค่า AFK
    @app_commands.command(name="afk", description="Set an AFK status to notify others")
    @app_commands.describe(reason="Reason for being away")
    async def afk(self, interaction: discord.Interaction, reason: str = "Away from keyboard"):
        self.afk_users[interaction.user.id] = reason
        
        embed = discord.Embed(color=0x2f3136)
        embed.set_author(name=f"Status Update: {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
        embed.description = (
            f"**Current Status:** AFK\n"
            f"**Reason:** {reason}\n\n"
            f"Your status has been recorded. I will notify others when they mention you. "
            f"Simply send a message to remove your AFK status."
        )
        embed.set_footer(text="Auto-Response System Active")
        
        await interaction.response.send_message(embed=embed)

    # 2. ระบบตรวจจับการพิมพ์เพื่อยกเลิก AFK และการโดน Tag
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # --- ส่วนที่ 1: ยกเลิก AFK เมื่อกลับมาพิมพ์ ---
        if message.author.id in self.afk_users:
            del self.afk_users[message.author.id]
            
            embed = discord.Embed(color=0x2f3136, description=f"Welcome back {message.author.mention}, your AFK status has been removed.")
            await message.channel.send(embed=embed, delete_after=5) # ลบข้อความแจ้งเตือนเองใน 5 วินาทีเพื่อไม่ให้รก

        # --- ส่วนที่ 2: แจ้งเตือนเมื่อมีคนโดน Tag ---
        if message.mentions:
            for mention in message.mentions:
                if mention.id in self.afk_users:
                    reason = self.afk_users[mention.id]
                    
                    embed = discord.Embed(color=0x2f3136)
                    embed.set_author(name=f"{mention.display_name} is currently away", icon_url=mention.display_avatar.url)
                    embed.add_field(name="Reason", value=f"```\n{reason}\n```")
                    embed.set_footer(text="This is an automated notification")
                    
                    await message.reply(embed=embed, delete_after=10) # ลบเองใน 10 วินาที

async def setup(bot):
    await bot.add_cog(AfkSystem(bot))
