import discord
from discord import app_commands
from discord.ext import commands
import g4f # ใช้ Library GPT4Free

class FreeAIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ask", description="ถาม AI ได้ทุกเรื่อง (ไม่ต้องใช้ API Key)")
    @app_commands.describe(prompt="พิมข้อความที่ต้องการถาม...")
    async def ask(self, interaction: discord.Interaction, prompt: str):
        # แจ้งว่าบอทกำลังประมวลผล
        await interaction.response.defer(thinking=True)
        
        try:
            # เรียกใช้งาน AI ผ่าน g4f (ใช้โมเดล gpt-3.5 หรืออื่นๆ)
            response = await g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_35_turbo,
                messages=[{"role": "user", "content": prompt}],
            )
            
            # ตรวจสอบความยาวข้อความ
            if len(response) > 2000:
                response = response[:1990] + "..."

            embed = discord.Embed(
                title="🤖 Free AI Assistant",
                description=response,
                color=0x2ecc71
            )
            embed.set_footer(text=f"ถามโดย {interaction.user.display_name}")
            
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"❌ บอทขัดข้องชั่วคราว: {e}")

async def setup(bot):
    await bot.add_cog(FreeAIChat(bot))

