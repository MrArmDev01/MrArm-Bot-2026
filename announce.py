import discord
from discord import app_commands, ui
from discord.ext import commands
import datetime

# --- หน้าต่างกรอกข้อมูลประกาศ (Modal) ---
class AnnounceModal(ui.Modal):
    def __init__(self, channel: discord.TextChannel):
        super().__init__(title="Create Announcement")
        self.channel = channel
        
        self.ann_title = ui.TextInput(
            label="Announcement Title",
            placeholder="Enter the headline here...",
            style=discord.TextStyle.short,
            required=True
        )
        self.ann_message = ui.TextInput(
            label="Message Content",
            placeholder="Enter your detailed announcement here...",
            style=discord.TextStyle.paragraph,
            required=True
        )
        
        self.add_item(self.ann_title)
        self.add_item(self.ann_message)

    async def on_submit(self, interaction: discord.Interaction):
        # สร้าง Embed ประกาศแบบเรียบหรู
        embed = discord.Embed(
            title=self.ann_title.value,
            description=self.ann_message.value,
            color=0x2f3136, # สีเทาเข้มหรูๆ
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        embed.set_footer(text=f"Announced by {interaction.user.display_name}")
        
        # ส่งไปยังช่องที่เลือก
        await self.channel.send(embed=embed)
        await interaction.response.send_message(f"✅ Announcement sent to {self.channel.mention}", ephemeral=True)

# --- ส่วนของคำสั่งใน Class ---
class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="announce", description="Send a professional announcement embed")
    @app_commands.describe(channel="Select the channel to send the announcement")
    @app_commands.checks.has_permissions(administrator=True)
    async def announce(self, interaction: discord.Interaction, channel: discord.TextChannel):
        # เปิดหน้าต่าง Modal ให้กรอกข้อความ
        await interaction.response.send_modal(AnnounceModal(channel))

# อย่าลืมเพิ่มเข้าไปในฟังก์ชัน setup ของคุณด้วยนะครับ
async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
