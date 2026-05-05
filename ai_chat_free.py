import discord
from discord import app_commands
from discord.ext import commands
import g4f
import asyncio

class FreeAIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ask", description="ถาม AI ได้ทุกเรื่อง (ChatGPT Free - ไม่ต้องใช้ API Key)")
    @app_commands.describe(prompt="พิมพ์ข้อความที่ต้องการถามหรือสั่งให้ AI ทำ...")
    async def ask(self, interaction: discord.Interaction, prompt: str):
        # แจ้งบอทกำลังคิด (เพราะ AI ใช้เวลาประมวลผล)
        await interaction.response.defer(thinking=True)
        
        try:
            # เรียกใช้งาน AI ผ่าน g4f โดยระบุโมเดลเป็นชื่อโดยตรงเพื่อความเสถียร
            response = await g4f.ChatCompletion.create_async(
                model="gpt-4o", # ใช้ GPT-4o ที่ฉลาดและเสถียรกว่า
                messages=[{"role": "user", "content": prompt}],
            )
            
            # ตรวจสอบว่ามีคำตอบกลับมาหรือไม่
            if not response:
                response = "ขออภัยครับ AI ไม่สามารถหาคำตอบให้ได้ในขณะนี้ ลองใหม่อีกครั้งนะครับ"

            # จัดการกรณีที่คำตอบยาวเกิน 2000 ตัวอักษร
            if len(response) > 2000:
                # ถ้าคำตอบยาวเกิน ให้แบ่งส่งหรือตัดตอน
                response_text = response[:1990] + "..."
            else:
                response_text = response

            embed = discord.Embed(
                title="🤖 AI Assistant (Free Edition)",
                description=response_text,
                color=0x2ecc71 # สีเขียว
            )
            embed.set_footer(text=f"Asked by {interaction.user.display_name} | Powered by GPT-4o")
            
            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"AI Error: {e}")
            await interaction.followup.send(f"❌ เกิดข้อผิดพลาด: ระบบ AI ขัดข้องชั่วคราว กรุณาลองใหม่อีกครั้งในภายหลัง")

    # ระบบตอบกลับเมื่อมีการ Tag บอท (Optional)
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mentioned_in(message) and not message.author.bot:
            async with message.channel.typing():
                clean_content = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
                if not clean_content: 
                    return
                
                try:
                    response = await g4f.ChatCompletion.create_async(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": clean_content}],
                    )
                    await message.reply(response if response else "หือ? มีอะไรให้ช่วยหรือเปล่าครับ?")
                except Exception as e:
                    print(f"Tag AI Error: {e}")

async def setup(bot):
    await bot.add_cog(FreeAIChat(bot))
