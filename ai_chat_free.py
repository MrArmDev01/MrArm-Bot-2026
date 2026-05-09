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
        await interaction.response.defer(thinking=True)
        
        try:
            response = await g4f.ChatCompletion.create_async(
                model=g4f.models.default,
                messages=[{"role": "user", "content": prompt}],
            )
            
            if not response or len(str(response).strip()) == 0:
                response = "Sorry, the AI server is currently overloaded. Please try again in 1-2 minutes"

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
            await interaction.followup.send("❌ The AI system is experiencing a connection congestion issue.")

    # ระบบตอบกลับเมื่อมีการ Tag บอท (ปรับปรุงใหม่)
    @commands.Cog.listener()
    async def on_message(self, message):
        # 1. เช็กว่าเป็นบอทพิมพ์เองไหม
        if message.author.bot:
            return

        # 2. เช็กว่ามีการ Mention @everyone หรือ @here ไหม (ถ้ามีจะไม่ตอบ)
        if message.mention_everyone:
            return

        # 3. เช็กว่าเป็นการแท็กชื่อบอทโดยตรง (Direct Mention) เท่านั้น
        if self.bot.user in message.mentions:
            async with message.channel.typing():
                clean_content = message.content.replace(f'<@{self.bot.user.id}>', '').replace(f'<@!{self.bot.user.id}>', '').strip()
                
                # ถ้าแท็กเปล่าๆ ไม่พิมพ์อะไรต่อ ก็ไม่ต้องตอบ
                if not clean_content: 
                    return
                
                try:
                    response = await g4f.ChatCompletion.create_async(
                        model=g4f.models.default,
                        messages=[{"role": "user", "content": clean_content}],
                    )
                    if response:
                        # ตัดข้อความถ้าเกินลิมิต Discord
                        final_response = str(response)
                        if len(final_response) > 2000:
                            final_response = final_response[:1990] + "..."
                        await message.reply(final_response)
                except Exception as e:
                    print(f"Mention AI Error: {e}")
                    pass

async def setup(bot):
    await bot.add_cog(FreeAIChat(bot))
