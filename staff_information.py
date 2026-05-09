import discord
from discord import app_commands
from discord.ext import commands

class StaffInformationDropdown(discord.ui.Select):
    def __init__(self, role_mentions):
        self.role_mentions = role_mentions
        options = [
            discord.SelectOption(label="Staff Hierarchy", description="View official hierarchy", value="hierarchy"),
            discord.SelectOption(label="Punishment Guide", description="View rules and penalty guide", value="punishment"),
        ]
        super().__init__(placeholder="Make Selection", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "hierarchy":
            # หน้าที่ 1: เนื้อหาเป๊ะตามรูปที่ 1 (ห้ามเปลี่ยนคำ)
            embed = discord.Embed(title="⚒️ Staff Hierarchy & Authority", color=0x2b2d31)
            embed.description = (
                "This page outlines the official staff hierarchy and command authority within the server\n"
                "All staff members are required to understand and strictly follow this structure\n\n"
                f"**Server Manager**\n{self.role_mentions['manager']}\n"
                "Holds the highest authority within the server\n"
                "Responsible for overall server management, structure, systems, and final decisions\n"
                "All staff members must comply with Server Manager instructions at all times\n\n"
                f"**Community Manager**\n{self.role_mentions['community']}\n"
                "Responsible for community direction, atmosphere, announcements, and events\n"
                "Manages member relations and community feedback\n"
                "Operates under the authority of the Server Manager\n\n"
                f"**Head Of Staff**\n{self.role_mentions['head_staff']}\n"
                "Oversees all staff teams and ensures proper staff conduct\n"
                "Acts as a bridge between management and moderation teams\n"
                "Must follow instructions from Server Manager and Community Manager\n\n"
                f"**Administrator**\n{self.role_mentions['admin']}\n"
                "Responsible for enforcing rules and handling major moderation actions\n"
                "Manages staff actions and escalated cases\n"
                "Must comply with instructions from higher management\n\n"
                f"**Head Moderator**\n{self.role_mentions['head_mod']}\n"
                "Leads the moderation team and oversees moderation activities\n"
                "Ensures moderators follow guidelines and procedures\n"
                "Reports to Administrators and higher management\n\n"
                f"**Senior Moderator**\n{self.role_mentions['senior_mod']}\n"
                "Supervises Moderators and Trial Moderators\n"
                "Handles serious or escalated moderation cases\n"
                "Must follow instructions from Admins and higher staff\n\n"
                f"**Moderator**\n{self.role_mentions['mod']}\n"
                "Enforces server rules and maintains order\n"
                "Handles reports and moderates server activity\n"
                "Reports issues to Senior Moderators and above\n\n"
                f"**Trial Moderator**\n{self.role_mentions['trial_mod']}\n"
                "Staff member under evaluation\n"
                "Assists with basic moderation tasks\n"
                "Cannot make major decisions independently and must follow higher staff instructions\n\n"
                "⚠️ **Important Staff Rules**\n"
                "Failure to follow instructions from higher-ranking staff may result in disciplinary action\n"
                "Abuse of authority will lead to demotion or removal\n"
                "If unsure how to handle a situation, always consult higher staff before acting"
            )
            embed.set_footer(text="Staff Information • First Page Make By • Mr.Arm")
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "punishment":
            # หน้าที่ 2: Punishment Guide (ดีไซน์สวยงาม ข้อมูลครบ)
            embed = discord.Embed(title="📜 Punishment Guide", color=0x2b2d31)
            embed.description = "Please read carefully and follow the Punishment Guide"
            
            embed.add_field(
                name="🔰 Minor Offenses",
                value="• Light Spamming / Repeating Messages\n• Off-Topic in Channels\n• Minor Inappropriate Remarks\n• Excessive Emoji Use\n• Slightly Disruptive Behavior\n\n"
                      "*Action: Start with Verbal Warning. If continues, issue Logged Warning or Temporary Mute.*",
                inline=False
            )
            embed.add_field(
                name="🛡️ Moderate Offenses",
                value="• Disrespecting Staff\n• Starting Unnecessary Arguments\n• Attempting to Provoke Others\n• Drama That Disrupts the Server\n• Excessive Ping Usage / Moderate Toxicity\n• Don't Ping Dev",
                inline=False
            )
            embed.add_field(
                name="🚫 Major Offenses",
                value="• Repeated Moderate Offenses\n• Direct Harassment or Threats\n• Severe Toxicity / Hate Speech\n• Explicit NSFW Content\n• Raiding / Organized Disruption\n• Sharing Dangerous Links / Scamming\n• Breaking Discord TOS / Doxxing\n• Exploiting the Server / Forging Reports",
                inline=False
            )
            
            embed.add_field(
                name="💡 Staff Notice",
                value="Major offenses result in an **immediate ban without prior warning**. If unsure, always double-check with other staff.",
                inline=False
            )
            embed.set_footer(text="Moderation System Make By • Mr.Arm")
            await interaction.response.edit_message(embed=embed)

class StaffInformationView(discord.ui.View):
    def __init__(self, role_mentions):
        super().__init__(timeout=None)
        self.add_item(StaffInformationDropdown(role_mentions))

class StaffInformation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup_staff", description="Setup staff hierarchy with role mentions")
    @app_commands.describe(
        manager="Select Manager Role", community="Select Community Manager Role",
        head_staff="Select Head of Staff Role", admin="Select Admin Role",
        head_mod="Select Head Moderator Role", senior_mod="Select Senior Moderator Role",
        mod="Select Moderator Role", trial_mod="Select Trial Moderator Role"
    )
    async def setup_staff(
        self, interaction: discord.Interaction, 
        manager: discord.Role, community: discord.Role, head_staff: discord.Role,
        admin: discord.Role, head_mod: discord.Role, senior_mod: discord.Role,
        mod: discord.Role, trial_mod: discord.Role
    ):
        role_mentions = {
            "manager": manager.mention, "community": community.mention,
            "head_staff": head_staff.mention, "admin": admin.mention,
            "head_mod": head_mod.mention, "senior_mod": senior_mod.mention,
            "mod": mod.mention, "trial_mod": trial_mod.mention
        }

        embed = discord.Embed(
            title="🛡️ Server Staff Information",
            description="Select a category below to view our Staff Hierarchy or Punishment Guidelines.",
            color=0x2b2d31
        )
        embed.set_footer(text="System Developed by Mr.Arm")

        await interaction.response.send_message("✅ Staff Information setup successfully!", ephemeral=True)
        await interaction.channel.send(embed=embed, view=StaffInformationView(role_mentions))

async def setup(bot):
    await bot.add_cog(StaffInformation(bot))
