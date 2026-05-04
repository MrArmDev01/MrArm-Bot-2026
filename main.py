import discord 
from discord.ext import commands
import os
import asyncio

class MyBot(commands.Bot):
    def __init__(self):
        # Setup Intents
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.guilds = True 
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        print("--- Loading Cogs ---")
        # ระบบ Auto-load: วนลูปหาไฟล์ทุกไฟล์ในโฟลเดอร์ cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    # ตัดนามสกุล .py ออกแล้วโหลด
                    cog_name = f'cogs.{filename[:-3]}'
                    await self.load_extension(cog_name)
                    print(f'✅ Loaded: {filename}')
                except Exception as e:
                    print(f'❌ Failed to load {filename}: {e}')

        print("--- Syncing Commands ---")
        # Sync Slash Commands เข้ากับ Discord
        try:
            await self.tree.sync()
            print("✅ Synced Slash Commands!")
        except Exception as e:
            print(f"❌ Failed to sync commands: {e}")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'🚀 Bot is online as: {bot.user}')
    print(f'Running in {len(bot.guilds)} servers')

# Run Bot
try:
    # สำหรับ Replit ใช้ os.getenv('TOKEN') หรือ os.environ.get('TOKEN')
    token = os.environ.get('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ Error: TOKEN not found in Replit Secrets")
except Exception as e:
    print(f"❌ Startup Error: {e}")

