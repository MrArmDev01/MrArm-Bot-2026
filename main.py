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
            'info_cmd'
        ]
        
        for ext in extensions:
            try:
                await self.load_extension(ext)
                print(f'✅ Loaded: {ext}')
            except Exception as e:
                print(f'❌ Failed to load {ext}: {e}')
                
        await self.tree.sync()

    async def on_ready(self):
        # ตั้งค่าสถานะ Streaming สำหรับ Nena
        # ใช้ชื่อเพลง และลิงก์ที่คุณส่งมา (Discord จะแสดงเป็นสถานะสีม่วง)
        activity = discord.Streaming(
            name="Love You💕",
            url="https://www.youtube.com/watch?v=F07G92S_vTo" # ลิงก์ YouTube ของเพลงนี้        )
        await self.change_presence(activity=activity)
        
        print(f'🚀 Logged in as {self.user} (Nena)')
        print(f'💜 Streaming status set: {activity.name}')

bot = MyBot()

# ดึง Token จาก Environment Variable ใน Railway
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ Error: DISCORD_TOKEN not found in environment variables.")

