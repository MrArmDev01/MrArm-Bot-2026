import discord
from discord import app_commands, ui
from discord.ext import commands

# --- ส่วนของเมนู Dropdown ---
class RulesDropdown(ui.Select):
    def __init__(self, guild_name, manager, admin, mod):
        self.guild_name = guild_name
        self.manager = manager
        self.admin = admin
        self.mod = mod
        
        options = [
            discord.SelectOption(label='Main Rules & Hierarchy', description='General info and Staff roles', emoji='🛡️'),
            discord.SelectOption(label='Minor Infractions', description='Rules for safety and community', emoji='🟢'),
            discord.SelectOption(label='Moderate Infractions', description='Rules for conduct and behavior', emoji='🟡'),
            discord.SelectOption(label='Major Infractions', description='Strict rules - Zero Tolerance', emoji='🔴'),
        ]
        super().__init__(placeholder='Select a category to read the rules...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # 1. Main Rules
        if self.values[0] == 'Main Rules & Hierarchy':
            embed = discord.Embed(title=f"{self.guild_name} Rules", color=0x2f3136)
            embed.add_field(name="🛡️ Main Rules", value=(
                "• All members must abide by both the Discord TOS & server's rules.\n"
                "• Finding or attempting to find loopholes in the rules will result in punishment.\n"
                "• Everybody must follow the rules including staff members; no one is above the rules.\n"
                "• Staff have the final saying in any predicament."
            ), inline=False)
            embed.add_field(name="⚠️ Warning System", value=(
                "• **Verbal Warning**\n"
                "• **1st Logged Warning:** Nothing\n"
                "• **2nd Logged Warning:** 1 Hour Mute\n"
                "• **3rd Logged Warning:** 4 Hour Mute\n"
                "• **4th Logged Warning:** 1 Day Ban"
            ), inline=False)
            embed.add_field(name="👥 Chain Of Command", value=f"• {self.manager}\n• {self.admin}\n• {self.mod}", inline=False)

        # 2. Minor
        elif self.values[0] == 'Minor Infractions':
            embed = discord.Embed(title="🟢 Minor Infractions", description=(
                "**1. Spreading False Information:** Spreading false info about updates, codes, etc.\n"
                "**2. Flooding/Spamming:** Sending messages that result in covering the chat.\n"
                "**3. Chaining:** When multiple members send the same message or GIF.\n"
                "**4. Channel Misuse:** Using a channel not for its intended purpose.\n"
                "**5. Toxicity/Ragebait:** Causing drama in the community or being toxic."
            ), color=0x2ecc71)
            embed.set_footer(text="Violations result in a verbal warning or temporary mute.")

        # 3. Moderate
        elif self.values[0] == 'Moderate Infractions':
            embed = discord.Embed(title="🟡 Moderate Infractions", description=(
                "**1. NSFW Comments:** Sending sexual comments or references.\n"
                "**2. Bypassing:** Attempting to bypass banned words through creative spelling.\n"
                "**3. Public Disputes with Staff:** Arguing with staff over punishments in public.\n"
                "**4. Mass Pinging:** Pinging someone repeatedly or multiple people (6+).\n"
                "**5. Sensitive Topics:** Discussing subjects like religion, gender, or politics."
            ), color=0xf1c40f)
            embed.set_footer(text="Violations result in a warning, a mute, or a combination of both.")

        # 4. Major
        else:
            embed = discord.Embed(title="🔴 Major Infractions", description=(
                "**1. Suicide Encouragement:** Requesting or encouraging self-harm.\n"
                "**2. Doxxing:** Attempting to dox or any threats of Doxxing.\n"
                "**3. NSFW Contents:** Explicit images, videos, or messages.\n"
                "**4. Black Marketing:** Buying/Selling products for real currency.\n"
                "**5. Phishing Links:** Sending malicious or scam links.\n"
                "**6. Discrimination:** Attacks against specific groups, race, or religion."
            ), color=0xe74c3c)
            embed.set_footer(text="Violations in this category result in an IMMEDIATE BAN.")

        await interaction.response.send_message(embed=embed, ephemeral=True)

class RulesView(ui.View):
    def __init__(self, guild_name, manager, admin, mod):
        super().__init__(timeout=None)
        self.add_item(RulesDropdown(guild_name, manager, admin, mod))

class RulesSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="set_rules", description="Post professional server rules with a dropdown menu")
    @app_commands.describe(
        manager_role="The Manager role to display", 
        admin_role="The Administrator role to display", 
        mod_role="The Moderator role to display"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def set_rules(self, interaction: discord.Interaction, manager_role: discord.Role, admin_role: discord.Role, mod_role: discord.Role):
        guild = interaction.guild
        
        # Embed หลักที่แสดงคู่กับ Dropdown
        main_embed = discord.Embed(
            title=f"📖 {guild.name} | Rules & Guidelines",
            description=(
                "Welcome to our community! To ensure a safe environment for everyone, "
                "please read and follow our rules.\n\n"
                "**Please select a category from the menu below to view the details.**"
            ),
            color=0x2f3136
        )
        main_embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        main_embed.set_footer(text="Compliance with these rules is mandatory.")
        
        await interaction.response.send_message("✅ Rules menu has been posted!", ephemeral=True)
        
        # ส่ง Embed พร้อม View ที่มี Dropdown
        await interaction.channel.send(
            embed=main_embed, 
            view=RulesView(guild.name, manager_role.mention, admin_role.mention, mod_role.mention)
        )

async def setup(bot):
    await bot.add_cog(RulesSystem(bot))
