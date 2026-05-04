import discord
from discord import app_commands, ui
from discord.ext import commands
import datetime

# Configuration dictionary to avoid hardcoding
config = {
    "log_channel": None,
    "staff_role": None
}

class AppModal(ui.Modal, title='Staff Application Form'):
    name_age = ui.TextInput(label='1. Name and Age', placeholder='e.g. Nena, 20 years old', required=True)
    time_avail = ui.TextInput(label='2. Availability', placeholder='e.g. 6:00 PM - 10:00 PM Daily', required=True)
    reason = ui.TextInput(label='3. Why should we choose you?', style=discord.TextStyle.paragraph, required=True)
    experience = ui.TextInput(label='4. Past Experience', style=discord.TextStyle.paragraph, placeholder='List your previous staff roles...', required=False)
    scenario = ui.TextInput(label='5. Conflict Resolution', style=discord.TextStyle.paragraph, placeholder='How would you handle a fight between members?', required=True)

    async def on_submit(self, interaction: discord.Interaction):
        if config["log_channel"] is None:
            return await interaction.response.send_message("❌ System Error: Log channel not configured.", ephemeral=True)

        log_channel = config["log_channel"]
        
        embed = discord.Embed(title="📩 New Staff Application", color=0x5865F2, timestamp=datetime.datetime.now())
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.add_field(name="Applicant", value=f"{interaction.user.mention} ({interaction.user.name})", inline=False)
        embed.add_field(name="Name/Age", value=self.name_age.value, inline=True)
        embed.add_field(name="Time Available", value=self.time_avail.value, inline=True)
        embed.add_field(name="Reason", value=self.reason.value, inline=False)
        embed.add_field(name="Experience", value=self.experience.value or "None", inline=False)
        embed.add_field(name="Scenario Response", value=self.scenario.value, inline=False)
        
        await log_channel.send(embed=embed, view=AdminDecisionView(interaction.user))
        await interaction.response.send_message("✅ Your application has been submitted! Please wait for a DM response.", ephemeral=True)

class AdminDecisionView(ui.View):
    def __init__(self, applicant: discord.Member):
        super().__init__(timeout=None)
        self.applicant = applicant

    @ui.button(label='Accept ✅', style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: ui.Button):
        role_status = ""
        if config["staff_role"]:
            try:
                await self.applicant.add_roles(config["staff_role"])
                role_status = f"\n✅ Role {config['staff_role'].mention} assigned."
            except:
                role_status = "\n❌ Failed to assign role (Check Bot Permissions)."

        try:
            embed_dm = discord.Embed(
                title="🎊 Congratulations! Application Accepted",
                description=(
                    f"Hello **{self.applicant.name}**,\n\n"
                    f"We are excited to inform you that your application has been **Approved**! "
                    f"Our team was impressed by your answers and we believe you'll be a great fit for our community.\n\n"
                    f"**Next Steps:**\n"
                    f"1. Check the newly visible Staff-Only channels.\n"
                    f"2. Read the pinned guidelines in the staff lounge.\n"
                    f"3. Introduce yourself to the team!\n\n"
                    f"Welcome aboard!"
                ),
                color=0x2ecc71
            )
            embed_dm.set_footer(text="Community Management Team")
            await self.applicant.send(embed=embed_dm)
            dm_status = "✅ DM sent successfully."
        except:
            dm_status = "❌ DM failed (User blocked DMs)."

        for item in self.children: item.disabled = True
        await interaction.response.edit_message(content=f"**Status: Accepted by {interaction.user.mention}**{role_status}\n{dm_status}", view=self)

    @ui.button(label='Reject ❌', style=discord.ButtonStyle.danger)
    async def reject(self, interaction: discord.Interaction, button: ui.Button):
        try:
            embed_dm = discord.Embed(
                title="Staff Application Update",
                description=f"Hello **{self.applicant.name}**,\n\nThank you for applying. After careful consideration, we have decided not to proceed with your application at this time. We appreciate your interest and encourage you to keep being an active member of our community!",
                color=0xe74c3c
            )
            await self.applicant.send(embed=embed_dm)
            dm_status = "✅ Rejection DM sent."
        except:
            dm_status = "❌ DM failed."

        for item in self.children: item.disabled = True
        await interaction.response.edit_message(content=f"**Status: Rejected by {interaction.user.mention}**\n{dm_status}", view=self)

class StaffApp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="app_setup", description="Setup Staff Recruitment (Admin Only)")
    @app_commands.describe(log_channel="Where to send applications", staff_role="Role to give on acceptance")
    @app_commands.checks.has_permissions(administrator=True)
    async def app_setup(self, interaction: discord.Interaction, log_channel: discord.TextChannel, staff_role: discord.Role):
        config["log_channel"] = log_channel
        config["staff_role"] = staff_role
        
        embed = discord.Embed(
            title="💼 Staff Recruitment",
            description="Do you want to help our community grow?\nClick the button below to fill out the application form!",
            color=0x2ecc71
        )
        embed.set_footer(text="Formal Application System • Nena Bot")
        
        await interaction.response.send_message(f"✅ Setup complete! Logs will be sent to {log_channel.mention}", ephemeral=True)
        await interaction.channel.send(embed=embed, view=AppView())

class AppView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label='Apply Now 📝', style=discord.ButtonStyle.primary, custom_id='apply_btn')
    async def apply(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(AppModal())

async def setup(bot):
    await bot.add_cog(StaffApp(bot))
