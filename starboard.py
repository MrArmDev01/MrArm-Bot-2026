import discord
from discord.ext import commands
from discord import app_commands
import json
import os

# ไฟล์สำหรับเก็บค่าการตั้งค่า
CONFIG_FILE = 'starboard_config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()

    @app_commands.command(name="set_starboard", description="ตั้งค่าระบบ Starboard สำหรับ Forum")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_starboard(self, interaction: discord.Interaction, forum_channel: discord.ForumChannel, target_channel: discord.TextChannel):
        guild_id = str(interaction.guild_id)
        if guild_id not in self.config:
            self.config[guild_id] = {}
            
        self.config[guild_id][str(forum_channel.id)] = target_channel.id
        save_config(self.config)
        
        await interaction.response.send_message(f"✅ ตั้งค่าเรียบร้อย! เมื่อมีโพสต์ใหม่ใน {forum_channel.mention} บอทจะส่งไปที่ {target_channel.mention}", ephemeral=True)

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        guild_id = str(thread.guild.id)
        parent_id = str(thread.parent_id)

        # ตรวจสอบว่าห้อง Forum นี้ถูกตั้งค่าไว้หรือไม่
        if guild_id in self.config and parent_id in self.config[guild_id]:
            target_channel_id = self.config[guild_id][parent_id]
            target_channel = self.bot.get_channel(target_channel_id)

            if not target_channel:
                return

            # รอข้อความแรก (เพื่อให้แน่ใจว่ารูปภาพและเนื้อหามาครบ)
            await asyncio.sleep(2) 
            
            first_message = None
            async for message in thread.history(limit=1, oldest_first=True):
                first_message = message

            if first_message:
                embed = discord.Embed(
                    title=f"📌 {thread.name}",
                    description=first_message.content[:2000] if first_message.content else "*(ไม่มีเนื้อหาข้อความ)*",
                    color=discord.Color.blue(),
                    url=thread.jump_url
                )
                embed.set_author(name=thread.owner.display_name, icon_url=thread.owner.display_avatar.url)
                embed.set_footer(text=f"โพสต์จากห้อง Forum: {thread.parent.name}")

                # ดึงรูปภาพถ้ามี
                if first_message.attachments:
                    embed.set_image(url=first_message.attachments[0].url)

                await target_channel.send(embed=embed)

import asyncio
async def setup(bot):
    await bot.add_cog(Starboard(bot))
