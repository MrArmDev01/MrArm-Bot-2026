import discord
from discord import app_commands
from discord.ext import commands

class ReportModal(discord.ui.Modal, title='Staff Misconduct Report'):
    def __init__(self, log_channel):
        super().__init__()
        self.log_channel = log_channel

    staff_name = discord.ui.TextInput(
        label='Name of Staff Member',
        placeholder='e.g. @StaffName',
        required=True
    )
    
    incident_details = discord.ui.TextInput(
        label='Details of Incident',
        style=discord.TextStyle.paragraph,
        placeholder='Please describe what happened in detail...',
        required=True,
        min_length=10
    )

    evidence = discord.ui.TextInput(
        label='Evidence Links (Optional)',
        placeholder='Links to screenshots or message IDs...',
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🔴 New Anonymous Staff Report",
            description="A user has submitted a report regarding staff conduct.",
            color=0xff4b4b # สีแดงแบบ Alert
        )
        embed.add_field(name="Target Staff", value=f"```\n{self.staff_name.value}\n```", inline=False)
        embed.add_field(name="Report Details", value=self.incident_details.value, inline=False)
        
        if self.evidence.value:
            embed.add_field(name="Evidence", value=self.evidence.value, inline=False)
            
        embed.set_footer(text=f"Reported at: {interaction.created_at.strftime('%Y-%m-%d %H:%M')}")
        
        await self.log_channel.send(embed=embed)
        await interaction.response.send_message("✅ Your report has been sent anonymously to the Admin team.", ephemeral=True)

class StaffReportSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.report_channel = None # ตัวแปรเก็บห้อง Log

    # คำสั่งตั้งค่าห้อง (เฉพาะ Admin)
    @app_commands.command(name="set_report_channel", description="Set the channel where anonymous reports will be sent")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_report_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        self.report_channel = channel
        await interaction.response.send_message(f"✅ Staff reports will now be sent to {channel.mention}", ephemeral=True)

    # คำสั่งแจ้งพฤติกรรม (สำหรับสมาชิกทุกคน)
    @app_commands.command(name="report_staff", description="Submit an anonymous report regarding staff misconduct")
    async def report_staff(self, interaction: discord.Interaction):
        if self.report_channel is None:
            await interaction.response.send_message("❌ The report system is not set up yet. Please ask an Admin to use `/set_report_channel`.", ephemeral=True)
            return
            
        await interaction.response.send_modal(ReportModal(self.report_channel))

async def setup(bot):
    await bot.add_cog(StaffReportSystem(bot))
