import discord
from discord import app_commands
from discord.ext import commands

class DashboardView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # ปุ่มจะไม่หายไปแม้บอทจะรีสตาร์ท (ถ้าโหลด View ใหม่)

    @discord.ui.button(label="🔒 Lock", style=discord.ButtonStyle.danger)
    async def lock_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        # ปิดการส่งข้อความสำหรับทุกคน (@everyone)
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message(f"✅ {interaction.channel.mention} is now **LOCKED**.", ephemeral=True)

    @discord.ui.button(label="🔓 Unlock", style=discord.ButtonStyle.success)
    async def unlock_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        # เปิดการส่งข้อความ
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = True
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message(f"✅ {interaction.channel.mention} is now **UNLOCKED**.", ephemeral=True)

    @discord.ui.button(label="👻 Hide", style=discord.ButtonStyle.secondary)
    async def hide_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        # ซ่อนห้องจากทุกคน
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.view_channel = False
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message(f"✅ {interaction.channel.mention} is now **HIDDEN**.", ephemeral=True)

    @discord.ui.button(label="👁️ Show", style=discord.ButtonStyle.primary)
    async def show_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        # แสดงห้องให้ทุกคนเห็น
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.view_channel = True
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message(f"✅ {interaction.channel.mention} is now **VISIBLE**.", ephemeral=True)

class ChannelDashboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="send_dashboard", description="Sends a channel control dashboard to this channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def send_dashboard(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎮 Channel Control Dashboard",
            description=(
                "Use the buttons below to manage this channel's permissions quickly.\n\n"
                "🔒 **Lock:** Nobody can send messages\n"
                "🔓 **Unlock:** Everyone can send messages\n"
                "👻 **Hide:** Nobody can see this channel\n"
                "👁️ **Show:** Everyone can see this channel"
            ),
            color=0x2b2d31
        )
        embed.set_footer(text="Admin Only Tools")
        
        # ส่ง Dashboard พร้อมปุ่มกด
        await interaction.response.send_message(embed=embed, view=DashboardView())

async def setup(bot):
    await bot.add_cog(ChannelDashboard(bot))
