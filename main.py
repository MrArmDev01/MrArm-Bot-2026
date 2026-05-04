import discord
from discord.ext import commands
import os
import asyncio

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # รายชื่อไฟล์ที่คุณต้องการให้บอทโหลด (ตามรูปที่คุณส่งมา)
        # เราจะไม่โหลด main.py และ requirements.txt เข้าตัวเอง
        extensions = [
            'ticket_pro',
            'verify',
            'roblox_info',
            'server_setup',
            'fun_commands',
            'ghost_ping',
            'mimic',
            'fake_nitro',
            'fake_payout',
            'fake_call',
            'crash_prank',
            'quarantine_prank',
            'starboard',
            'bot_admin'
        ]
        
        for ext in extensions:
            try:
                await self.load_extension(ext)
                print(f'✅ Loaded: {ext}')
            except Exception as e:
                print(f'❌ Failed to load {ext}: {e}')
                
        await self.tree.sync()

    async def on_ready(self):
        print(f'🚀 Logged in as {self.user}')

bot = MyBot()

# ดึง Token จาก Environment Variable ใน Railway
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
