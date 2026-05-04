import discord
from discord import app_commands, ui
from discord.ext import commands

# --- กล่องข้อความสำหรับพิมพ์ตอบกลับ ---
class ReplyModal(ui.Modal, title='Reply to Message'):
    answer = ui.TextInput(label='Your Message', style=discord.TextStyle.paragraph, placeholder='Type your reply here...', max_length=500)

    def __init__(self, original_sender):
        super().__init__()
        self.original_sender = original_sender

    async def on_submit(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title="📨 New Reply Received!", description=self.answer.value, color=discord.Color.green())
            embed.set_footer(text=f"Reply from: {interaction.user.name}")

            # ส่งกลับไปหาคนส่งคนแรก
            await self.original_sender.send(embed=embed)
            await interaction.response.send_message("✅ Your reply has been sent!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Could not send reply: {e}", ephemeral=True)

# --- ปุ่มกดสำหรับหน้า DM ---
class DMView(ui.View):
    def __init__(self, original_sender):
        super().__init__(timeout=None) # ปุ่มอยู่ได้ตลอดกาล
        self.original_sender = original_sender

    @ui.button(label="Reply Back", style=discord.ButtonStyle.primary, emoji="✍️")
    async def reply_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(ReplyModal(self.original_sender))

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dm_user", description="Send a DM with a reply button")
    @app_commands.describe(user="Who to send to?", message="What to say?")
    async def dm_user(self, interaction: discord.Interaction, user: discord.User, message: str):
        await interaction.response.send_message(f"📤 Sending message to {user.name}...", ephemeral=True)

        try:
            # สร้าง Embed สำหรับคนรับ
            embed = discord.Embed(
                title="📩 You've got a message!",
                description=message,
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"You can reply using the button below.")

            # ส่งไปพร้อมกับปุ่ม View
            view = DMView(original_sender=interaction.user)
            await user.send(embed=embed, view=view)

            await interaction.edit_original_response(content=f"✅ Sent! {user.name} can now reply back to you.")

        except discord.Forbidden:
            await interaction.edit_original_response(content="❌ Failed: This user has their DMs closed.")
        except Exception as e:
            await interaction.edit_original_response(content=f"⚠️ Error: {e}")

async def setup(bot):
    await bot.add_cog(FunCommands(bot))
