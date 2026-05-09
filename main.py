import discord
from discord.ext import commands
import os
import asyncio
from flask import Flask
from threading import Thread

# --- ระบบ Web Server สำหรับหลอก Render ให้บอทไม่หลับ ---
app = Flask('')

@app.get('/')
def home():
    return "Nena Bot is Online!"

def run():
    # Render จะส่ง Port มาให้ผ่าน Environment Variable ชื่อ PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True # สั่งให้ Thread จบพร้อมโปรแกรมหลัก
    t.start()

# --- โครงสร้างบอทเดิมของคุณ ---
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        extensions = [
            'ticket_pro', 'roblox_info', 'server_setup', 'fun_commands',
            'mimic', 'fake_payout', 'starboard', 'bot_admin',
            'info_cmd', 'staff_app', 'staff_system', 'info_commands',
            'announce', 'afk', 'purg', 'noping', 'utilities',
            'ai_chat_free', 'booster_system', 'giveaway', 'staff_information'
        ]
        
        for ext in extensions:
            try:
                await self.load_extension(ext)
                print(f'✅ Loaded: {ext}')
            except Exception as e:
                print(f'❌ Failed to load {ext}: {e}')
                
        await self.tree.sync()

    async def on_ready(self):
        # ตั้งค่าสถานะ Streaming (ตามต้นฉบับ)
        activity = discord.Streaming(
            name="ไอ้เด็กคนนี้ - NICK KIT 🎵",
            url="https://www.youtube.com/watch?v=F07G92S_vTo" 
        )
        await self.change_presence(activity=activity)
        
        print(f'🚀 Logged in as {self.user} (Nena)')
        print(f'💜 Streaming status (YouTube) set for Nena')

bot = MyBot()

# ดึง Token จาก Environment Variables (ใน Render ให้ตั้งชื่อ DISCORD_TOKEN)
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN:
    # เรียกใช้ฟังก์ชัน keep_alive ก่อนรันบอท
    keep_alive()
    bot.run(TOKEN)
else:
    print("❌ Error: DISCORD_TOKEN not found in environment variables.")
