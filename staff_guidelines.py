import discord
from discord import app_commands
from discord.ext import commands

class StaffDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Infractions System', description='Detailed protocols for user violations'),
            discord.SelectOption(label='Staff Rules', description='Code of conduct and expectations for staff'),
            discord.SelectOption(label='Strike System', description='Internal disciplinary actions for staff'),
            discord.SelectOption(label='Emergency Protocols', description='Procedures for severe server incidents')
        ]
        super().__init__(placeholder='Select a category to view details...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'Infractions System':
            embed = discord.Embed(
                title="Infractions System and Enforcement Protocols",
                description=(
                    "The following protocols must be followed strictly by all moderation staff to ensure fairness and consistency across the server. "
                    "All actions taken must be documented in the designated logs.\n\n"
                    "Level 1: Minor Violations\n"
                    "Includes excessive capitalization, minor spamming, and off-topic discussion in restricted channels. "
                    "Staff should issue a verbal warning before proceeding to a formal system warning. "
                    "Repeated offenses within a 24-hour window will result in a temporary mute of 1 hour.\n\n"
                    "Level 2: Moderate Violations\n"
                    "Includes directed harassment, use of prohibited language, and continuous disruption of voice channels. "
                    "These violations require an immediate formal warning and a mandatory mute of 6 to 12 hours. "
                    "Staff must provide clear evidence of the violation in the moderation log.\n\n"
                    "Level 3: Severe Violations\n"
                    "Includes hate speech, malicious links, phishing attempts, and severe harassment. "
                    "These actions warrant an immediate temporary ban ranging from 3 to 7 days. "
                    "The incident must be reported to the Senior Administration for review within 12 hours of the action taken.\n\n"
                    "Level 4: Critical Violations\n"
                    "Includes raiding, distribution of illegal content, and unauthorized advertising. "
                    "Staff are authorized to issue an immediate permanent ban and clear all recent messages. "
                    "This is the only level where action can be taken without a prior warning."
                ),
                color=0x2b2d31
            )

        elif self.values[0] == 'Staff Rules':
            embed = discord.Embed(
                title="Staff Code of Conduct and Operational Standards",
                description=(
                    "All staff members are expected to maintain the highest level of professionalism and integrity while representing the server. "
                    "Failure to adhere to these standards will lead to internal disciplinary review.\n\n"
                    "Professionalism and Neutrality\n"
                    "Staff must remain neutral during disputes and avoid taking sides based on personal relationships. "
                    "Avoid engaging in arguments with users; instead, refer to the established rules and maintain a calm demeanor.\n\n"
                    "Confidentiality Protocols\n"
                    "Information shared within the staff channels is strictly confidential. "
                    "Leaking staff discussions, internal logs, or future server plans to the general public is considered a major violation and will result in immediate dismissal.\n\n"
                    "Activity Expectations\n"
                    "While we understand real-life commitments, staff are expected to maintain a consistent presence. "
                    "If you will be unavailable for more than 48 hours, you must notify the Lead Administrator through the absence request channel.\n\n"
                    "Proper Use of Permissions\n"
                    "Staff permissions are to be used solely for the protection and maintenance of the community. "
                    "Abuse of power, including using administrative tools for personal gain or to intimidate users, is strictly prohibited."
                ),
                color=0x2b2d31
            )

        elif self.values[0] == 'Strike System':
            embed = discord.Embed(
                title="Internal Staff Strike and Disciplinary System",
                description=(
                    "To maintain accountability, we utilize a strike system for staff members who fail to meet their responsibilities or violate the code of conduct.\n\n"
                    "First Strike: Formal Notice\n"
                    "Issued for minor negligence, such as failure to log moderation actions or inactivity without prior notice. "
                    "The strike remains on record for 30 days. A meeting with a Senior Moderator may be required.\n\n"
                    "Second Strike: Final Warning\n"
                    "Issued for repeated minor violations or a single moderate violation such as unprofessional behavior towards users. "
                    "This strike results in a temporary suspension of permissions for 7 days and a formal review of the staff member's position.\n\n"
                    "Third Strike: Dismissal\n"
                    "Accumulating three strikes within a 90-day period results in immediate removal from the staff team. "
                    "The individual will be ineligible to reapply for a staff position for a minimum of 6 months.\n\n"
                    "Immediate Removal\n"
                    "Certain actions, including leaking confidential data, abuse of administrative power, or severe rule violations, "
                    "bypass the strike system and result in an immediate permanent ban from the staff team and potentially the server."
                ),
                color=0x2b2d31
            )

        elif self.values[0] == 'Emergency Protocols':
            embed = discord.Embed(
                title="Emergency Response and Crisis Management",
                description=(
                    "In the event of a server-wide emergency, such as a raid or security breach, the following protocols must be activated immediately.\n\n"
                    "Raid Response Protocol\n"
                    "1. Enable slowmode in all active text channels to 30 seconds.\n"
                    "2. If the raid persists, use the lockdown command to prevent all users from sending messages.\n"
                    "3. Identify and ban the primary accounts responsible for the disruption.\n"
                    "4. Contact the Technical Administrator to review server invite links and safety filters.\n\n"
                    "Security Breach Protocol\n"
                    "If a staff account is suspected to be compromised, notify the Server Owner through external communication immediately. "
                    "The compromised account will have its roles removed and its current session terminated.\n\n"
                    "Escalation Procedure\n"
                    "Staff should handle issues at their level whenever possible. "
                    "However, situations involving legal threats, severe harassment of staff, or technical exploits must be escalated to the Senior Admin team without delay."
                ),
                color=0x2b2d31
            )

        embed.set_footer(text="Staff Handbook | Revised May 2026")
        await interaction.response.edit_message(embed=embed)

class StaffGuidelinesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(StaffDropdown())

class StaffSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="set_staff_guidelines", description="Post the official staff handbook with dropdown navigation")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_staff_guidelines(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Official Staff Operational Guidelines",
            description=(
                "Welcome to the internal staff manual. This document contains the necessary protocols for server management and staff conduct. "
                "Please select a category from the menu below to view the detailed documentation for each system."
            ),
            color=0x2b2d31
        )
        embed.set_footer(text="Select a category below to begin")
        
        await interaction.response.send_message(embed=embed, view=StaffGuidelinesView())

async def setup(bot):
    await bot.add_cog(StaffSystem(bot))
