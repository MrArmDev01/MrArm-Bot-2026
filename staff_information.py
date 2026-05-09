import discord
from discord import app_commands
from discord.ext import commands

class StaffInformationDropdown(discord.ui.Select):
    def __init__(self):
        # ตั้งค่าตัวเลือกใน Dropdown
        options = [
            discord.SelectOption(
                label="Staff Hierarchy", 
                description="Official hierarchy and command authority",
                value="hierarchy"
            ),
            discord.SelectOption(
                label="Punishment Guide", 
                description="Rules and server disciplinary actions",
                value="punishment"
            ),
        ]
        super().__init__(placeholder="Make Selection...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # หน้าที่ 1: Staff Hierarchy
        if self.values[0] == "hierarchy":
            embed = discord.Embed(title="Staff Hierarchy & Authority", color=0x2b2d31)
            embed.description = (
                "This page outlines the official staff hierarchy and command authority within the server. "
                "All staff members are required to understand and strictly follow this structure.\n\n"
                "**Server Manager**\n"
                "> Holds the highest authority. Responsible for overall management and final decisions.\n\n"
                "**Community Manager**\n"
                "> Responsible for community direction, announcements, and member relations.\n\n"
                "**Head Of Staff**\n"
                "> Oversees all staff teams and ensures proper conduct across the server.\n\n"
                "**Administrator**\n"
                "> Responsible for enforcing rules and handling major moderation actions.\n\n"
                "**Head Moderator**\n"
                "> Leads the moderation team and oversees daily moderation activities.\n\n"
                "**Senior Moderator**\n"
                "> Supervises Moderators and Trial Moderators in escalated cases.\n\n"
                "**Moderator**\n"
                "> Enforces server rules, maintains order, and handles user reports.\n\n"
                "**Trial Moderator**\n"
                "> Staff member under evaluation. Assists with basic moderation tasks."
            )
            embed.set_footer(text="Staff Information • First Page Make By Mr.Arm")
            await interaction.response.edit_message(embed=embed)

        # หน้าที่ 2: Punishment Guide (ดีไซน์แบบสะอาดตา)
        elif self.values[0] == "punishment":
            embed = discord.Embed(title="Punishment Guide", color=0x2b2d31)
            embed.description = "Please read carefully and follow the professional conduct guidelines."
            
            embed.add_field(
                name="Minor Offenses", 
                value="Light Spamming, Off-Topic, Excessive Emojis, Mild Annoyance.\n*Action: Verbal Warning → Mute*", 
                inline=False
            )
            embed.add_field(
                name="Moderate Offenses", 
                value="Disrespecting Staff, Starting Arguments, Moderate Toxicity, Ping Dev.\n*Action: Logged Warning → Temp Mute*", 
                inline=False
            )
            embed.add_field(
                name="Major Offenses", 
                value="Harassment, NSFW Content, Raiding, Doxxing, Scamming, Breaking Discord TOS.\n*Action: Immediate Ban*", 
                inline=False
            )
            
            embed.set_footer(text="Moderation System Make By • Mr.Arm")
            await interaction.response.edit_message(embed=embed)

class StaffInformationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # ตั้งค่า None เพื่อให้ปุ่มใช้งานได้ตลอด
        self.add_item(StaffInformationDropdown())

class StaffInformation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="staff_info", description="Display staff hierarchy and punishment guide")
    @app_commands.checks.has_permissions(administrator=True)
    async def staff_info(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Server Information Hub",
            description="Use the dropdown menu below to navigate through the official server documentation.",
            color=0x2b2d31
        )
        embed.set_footer(text="System Developed by Mr.Arm")
        
        await interaction.response.send_message(embed=embed, view=StaffInformationView())

async def setup(bot):
    await bot.add_cog(StaffInformation(bot))
