import discord
from discord.ext import commands
import os
import asyncio

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        extensions = [
            'ticket_pro',
            'roblox_info',
            'server_setup',
            'fun_commands',
            'mimic',
            'fake_payout',
            'starboard',
            'bot_admin',
            'info_cmd',
            'staff_app',
            'moderation',
            'staff_system',
            'info_commands',
            'announce',
            'afk',
            'purg',
            'noping',
            'utilities',
            'ai_chat_free',
            'booster_system',
            'staff_guidelines'
        ]
        
        for ext in extensions:
            try:
                await self.load_extension(ext)
                print(f'✅ Loaded: {ext}')
            except Exception as e:
                print(f'❌ Failed to load {ext}: {e}')
                
        await self.tree.sync()

    async def on_ready(self):
        # ตั้งค่าสถานะ Streaming โดยใช้ลิงก์ YouTube เพื่อให้ขึ้นสีม่วงและมีปุ่ม Watch
        activity = discord.Streaming(
            name="ไอ้เด็กคนนี้ - NICK KIT 🎵",
            url="https://www.youtube.com/watch?v=F07G92S_vTo" 
        )
        await self.change_presence(activity=activity)
        
        print(f'🚀 Logged in as {self.user} (Nena)')
        print(f'💜 Streaming status (YouTube) set for Nena')

bot = MyBot()

# ดึง Token จาก Railway
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ Error: DISCORD_TOKEN not found in environment variables.")

