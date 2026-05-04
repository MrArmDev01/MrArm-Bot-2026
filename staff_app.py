import discord
from discord import app_commands, ui
from discord.ext import commands
import datetime
import random

# --- No Hardcoding Configuration ---
config = {
    "log_channel": None,
    "staff_role": None
}

# รายการสถานการณ์สำหรับสุ่ม (Scenario Response)
SCENARIOS = [
    {
        "id": "A",
        "topic": "Two members are arguing and using offensive language in General Chat.",
        "placeholder": "What are your steps to calm the situation and maintain order?"
    },
    {
        "id": "B",
        "topic": "A member is spamming suspicious phishing links or 'Free Nitro' scams.",
        "placeholder": "How would you protect the community and handle the spammer?"
    }
]

# --- 2. สิ่งที่จะเด้งมาให้ตอบ (The Modals) ---

# หน้าที่ 3: ข้อ 11-15
class AppModalPart3(ui.Modal):
    def __init__(self, scenario, part1_data, part2_data):
        super().__init__(title='Staff Application Form (3/3)')
        self.scenario = scenario
        self.part1_data = part1_data
        self.part2_data = part2_data
        
        self.scenario_input = ui.TextInput(
            label=f'11. Scenario Response ({self.scenario["id"]})',
            style=discord.TextStyle.paragraph,
            placeholder=f"Situation: {self.scenario['topic']}\n\nYour Answer...",
            required=True
        )
        self.conflict = ui.TextInput(label='12. Conflict Resolution', style=discord.TextStyle.paragraph, placeholder='How to handle disagreements with teammates?', required=True)
        self.tools = ui.TextInput(label='13. Tools/Bot Knowledge', placeholder='Experienced with Dyno, MEE6, etc?', required=True)
        self.commitment = ui.TextInput(label='14. Commitment Level', placeholder='How long do you plan to stay with us?', required=True)
        self.questions = ui.TextInput(label='15. Any Questions for us?', style=discord.TextStyle.paragraph, required=False)

        self.add_item(self.scenario_input)
        self.add_item(self.conflict)
        self.add_item(self.tools)
        self.add_item(self.commitment)
        self.add_item(self.questions)

    async def on_submit(self, interaction: discord.Interaction):
        if config["log_channel"] is None:
            return await interaction.response.send_message("❌ Log channel not set!", ephemeral=True)

        # รวมข้อมูลทั้งหมดส่งไปที่ Log
        embed = discord.Embed(title="📩 New Staff Application Received", color=0x5865F2, timestamp=datetime.datetime.now())
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.add_field(name="Applicant", value=f"{interaction.user.mention} ({interaction.user.name})", inline=True)
        embed.add_field(name="Name/Age", value=self.part1_data['name_age'], inline=True)
        embed.add_field(name="Language", value=self.part1_data['language'], inline=True)
        embed.add_field(name="TimeZone", value=self.part1_data['timezone'], inline=True)
        embed.add_field(name="3. Past Experience", value=self.part1_data['experience'], inline=False)
        embed.add_field(name="4. Why should we choose you?", value=self.part1_data['reason'], inline=False)
        embed.add_field(name="7. Strengths", value=self.part2_data['strengths'], inline=True)
        embed.add_field(name="8. Weakness", value=self.part2_data['weakness'], inline=True)
        embed.add_field(
            name=f"Scenario Response ({self.scenario['id']})", 
            value=f"**Situation:** {self.scenario['topic']}\n\n**Candidate's Answer:**\n{self.scenario_input.value}", 
            inline=False
        )
        embed.set_footer(text=f"User ID: {interaction.user.id}")
        
        await config["log_channel"].send(embed=embed, view=AdminDecisionView(interaction.user))
        await interaction.response.send_message("✅ Your application has been successfully submitted! Please wait for a DM response.", ephemeral=True)

# หน้าที่ 2: ข้อ 6-10
class AppModalPart2(ui.Modal):
    def __init__(self, scenario, part1_data):
        super().__init__(title='Staff Application Form (2/3)')
        self.scenario = scenario
        self.part1_data = part1_data
        
        self.strengths = ui.TextInput(label='6. What are your strengths?', placeholder='e.g. Patient, active', required=True)
        self.weakness = ui.TextInput(label='7. What are your weaknesses?', placeholder='e.g. perfectionist', required=True)
        self.stress = ui.TextInput(label='8. How do you handle stress?', style=discord.TextStyle.paragraph, required=True)
        self.rules = ui.TextInput(label='9. Your understanding of Rules', placeholder='Explain or rate 1-10', required=True)
        self.availability = ui.TextInput(label='10. Availability', placeholder='Hours per day/week', required=True)

        self.add_item(self.strengths)
        self.add_item(self.weakness)
        self.add_item(self.stress)
        self.add_item(self.rules)
        self.add_item(self.availability)

    async def on_submit(self, interaction: discord.Interaction):
        part2_data = {
            "strengths": self.strengths.value, "weakness": self.weakness.value,
            "stress": self.stress.value, "rules": self.rules.value, "availability": self.availability.value
        }
        await interaction.response.send_modal(AppModalPart3(self.scenario, self.part1_data, part2_data))

# หน้าที่ 1: ข้อ 1-5 (คงคำถามเดิมของคุณไว้และเพิ่ม Language)
class AppModal(ui.Modal):
    def __init__(self, scenario):
        super().__init__(title='Staff Application Form (1/3)')
        self.scenario = scenario
        
        self.name_age = ui.TextInput(label='1. Name and Age', placeholder='e.g. Nena, 20 years old', required=True)
        self.language = ui.TextInput(label='2. What Language do you use?', placeholder='Thai, English, etc.', required=True)
        self.timezone = ui.TextInput(label='3. What is your TimeZone?', placeholder='e.g. GMT+7, EST, etc.', required=True)
        self.experience = ui.TextInput(label='4. Past Experience', style=discord.TextStyle.paragraph, placeholder='Have you been staff before? If yes, where?', required=True)
        self.reason = ui.TextInput(
            label='5. Why should we choose you?', 
            style=discord.TextStyle.paragraph, 
            placeholder='Tell us about your strengths and passion for this community...', 
            required=True
        )
        
        self.add_item(self.name_age)
        self.add_item(self.language)
        self.add_item(self.timezone)
        self.add_item(self.experience)
        self.add_item(self.reason)

    async def on_submit(self, interaction: discord.Interaction):
        part1_data = {
            "name_age": self.name_age.value, "language": self.language.value,
            "timezone": self.timezone.value, "experience": self.experience.value,
            "reason": self.reason.value
        }
        await interaction.response.send_modal(AppModalPart2(self.scenario, part1_data))

# --- 3. ระบบตอบรับ/ปฏิเสธ (Manager Decision & DM) - คงเดิมตามโค้ดคุณ ---
class AdminDecisionView(ui.View):
    def __init__(self, applicant: discord.Member):
        super().__init__(timeout=None)
        self.applicant = applicant

    @ui.button(label='Accept ✅', style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: ui.Button):
        role_msg = ""
        if config["staff_role"]:
            try:
                await self.applicant.add_roles(config["staff_role"])
                role_msg = f"\n✅ Role {config['staff_role'].mention} has been assigned!"
            except:
                role_msg = "\n❌ Failed to assign role (Check Bot Permissions)."

        try:
            embed_dm = discord.Embed(
                title="🎊 Congratulations! Your Application is Approved",
                description=(
                    f"Hello **{self.applicant.name}**,\n\n"
                    f"We are thrilled to inform you that after reviewing your application, "
                    f"our Management Team has decided to **Accept** you as part of our Staff Team! 🎉\n\n"
                    f"Your answers showed great potential and we believe you will be a valuable asset to our community.\n\n"
                    f"**📌 YOUR NEXT STEPS:**\n"
                    f"1. You now have access to the **Staff-Only** channels.\n"
                    f"2. Please read the **pinned guidelines** in the staff lounge immediately.\n"
                    f"3. Introduce yourself to other team members.\n"
                    f"4. If you have any questions, feel free to ask a Senior Manager.\n\n"
                    f"Welcome aboard, we look forward to working with you!"
                ),
                color=0x2ecc71
            )
            embed_dm.set_footer(text="Best Regards, Community Management Team")
            await self.applicant.send(embed=embed_dm)
            dm_msg = "✅ Success DM Sent."
        except:
            dm_msg = "❌ DM Failed (User's DMs are closed)."

        for item in self.children: item.disabled = True
        await interaction.response.edit_message(content=f"**Status: Accepted by {interaction.user.mention}**{role_msg}\n{dm_msg}", view=self)

    @ui.button(label='Reject ❌', style=discord.ButtonStyle.danger)
    async def reject(self, interaction: discord.Interaction, button: ui.Button):
        try:
            embed_dm = discord.Embed(
                title="Staff Application Update",
                description=(
                    f"Hello **{self.applicant.name}**,\n\n"
                    f"Thank you for your interest in joining our Staff Team. After careful consideration, "
                    f"we regret to inform you that we will not be moving forward with your application at this time.\n\n"
                    f"Please don't be discouraged! This doesn't mean you aren't a great member of our community. "
                    f"We encourage you to stay active and try applying again in the future when recruitment reopens.\n\n"
                    f"Thank you for your understanding."
                ),
                color=0xe74c3c
            )
            await self.applicant.send(embed=embed_dm)
            dm_msg = "✅ Rejection DM Sent."
        except:
            dm_msg = "❌ DM Failed."

        for item in self.children: item.disabled = True
        await interaction.response.edit_message(content=f"**Status: Rejected by {interaction.user.mention}**\n{dm_msg}", view=self)

# --- 1. ใบประกาศแบบละเอียด (Recruitment Post Setup) - คงเดิมตามโค้ดคุณ ---
class StaffApp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="app_setup", description="Setup Detailed Staff Recruitment (Admin Only)")
    @app_commands.describe(log_channel="Channel where applications will be sent", staff_role="Role to give on acceptance")
    @app_commands.checks.has_permissions(administrator=True)
    async def app_setup(self, interaction: discord.Interaction, log_channel: discord.TextChannel, staff_role: discord.Role):
        config["log_channel"] = log_channel
        config["staff_role"] = staff_role
        
        guild_name = interaction.guild.name
        
        embed = discord.Embed(
            title=f"STAFF RECRUITMENT",
            description=(
                f"We are looking for dedicated, mature, and active individuals to join our "
                f"Management Team. If you have a passion for helping others and want to "
                f"contribute to the growth of **{guild_name}**, this is your chance!"
            ),
            color=0x2ecc71
        )

        embed.add_field(
            name="📋 Requirements",
            value=(
                "• Must be at least 15 years old.\n"
                "• Must be active and helpful in text/voice channels.\n"
                "• Ability to stay calm and professional under pressure.\n"
                "• Good understanding of our server rules.\n"
            ),
            inline=False
        )

        embed.add_field(
            name="🛠️ Responsibilities",
            value=(
                "• Monitor channels and maintain a friendly environment.\n"
                "• Assist members with questions or issues.\n"
                "• Host community events and keep the chat active.\n"
                "• Handle conflicts fairly according to guidelines."
            ),
            inline=False
        )

        embed.add_field(
            name="⚠️ IMPORTANT NOTE",
            value="Being a Staff member is a responsibility. We expect honesty and dedication.",
            inline=False
        )

        embed.set_footer(text=f"Community Management • Click below to apply")
        
        await interaction.response.send_message("✅ Professional Recruitment Post Created!", ephemeral=True)
        await interaction.channel.send(embed=embed, view=AppView())

class AppView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label='Apply Now 📝', style=discord.ButtonStyle.primary, custom_id='apply_btn')
    async def apply(self, interaction: discord.Interaction, button: ui.Button):
        scenario = random.choice(SCENARIOS)
        await interaction.response.send_modal(AppModal(scenario))

async def setup(bot):
    await bot.add_cog(StaffApp(bot))
