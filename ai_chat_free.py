import discord
from discord import app_commands
from discord.ext import commands
import g4f
import asyncio

class FreeAIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ask", description="Ask AI anything")
    @app_commands.describe(prompt="Type the question you want to ask")
    async def ask(self, interaction: discord.Interaction, prompt: str):
        # แจ้งบอทกำลังคิด
        await interaction.response.defer(thinking=True)
        
        try:
            # ใช้ระบบสุ่มหา Provider ที่ทำงานได้ในตอนนั้นโดยอัตโนมัติ
            response = await g4f.ChatCompletion.create_async(
                model=g4f.models.default,
                messages=[{"role": "user", "content": prompt}],
            )
            
            if not response or len(str(response).strip()) == 0:
                response = "Sorry, the AI server is currently overloaded. Please try again in 1-2 minutes"

            # ตรวจสอบความยาวข้อความ
            response_text = str(response)
            if len(response_text) > 2000:
                response_text = response_text[:1990] + "..."

            embed = discord.Embed(
                title="🤖 Nena AI Assistant",
                description=response_text,
                color=0x2ecc71
            )
            embed.set_footer(text=f"Asked by {interaction.user.display_name} | AI Mode: Auto-Select")
            
            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"AI Error Detail: {e}")
            await interaction.followup.send("❌ The AI system is experiencing a connection congestion issue. Please try a different question or try again later")

    # ระบบตอบกลับเมื่อมีการ Tag บอท
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mentioned_in(message) and not message.author.bot:
            async with message.channel.typing():
                clean_content = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
                if not clean_content: return
                
                try:
                    response = await g4f.ChatCompletion.create_async(
                        model=g4f.models.default,
                        messages=[{"role": "user", "content": clean_content}],
                    )
                    if response:
                        await message.reply(response)
                except:
                    pass

async def setup(bot):
    await bot.add_cog(FreeAIChat(bot))
