import discord
from discord import app_commands
from discord.ext import commands

class RulesSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="set_rules", description="Post professional server rules based on hierarchy")
    @app_commands.describe(
        manager_role="The Manager role to display", 
        admin_role="The Administrator role to display", 
        mod_role="The Moderator role to display"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def set_rules(self, interaction: discord.Interaction, manager_role: discord.Role, admin_role: discord.Role, mod_role: discord.Role):
        guild = interaction.guild
        
        # --- Embed 1: Main Rules & Hierarchy ---
        embed1 = discord.Embed(title=f"{guild.name} Rules", color=0x2f3136)
        embed1.add_field(name=" Main Rules", value=(
            "• All members must abide by both the Discord TOS & server's rules.\n"
            "• Finding or attempting to find loopholes in the rules will result in punishment.\n"
            "• Everybody must follow the rules including staff members; no one is above the rules.\n"
            "• Staff have the final saying in any predicament."
        ), inline=False)
        
        embed1.add_field(name="⚠️ Warning System", value=(
            "• **Verbal Warning**\n"
            "• **1st Logged Warning:** Nothing\n"
            "• **3nd Logged Warning:** 2 Hour Mute\n"
            "• **5rd Logged Warning:** 6 Hour Mute\n"
            "• **7th Logged Warning:** 1 Day Ban"
        ), inline=False)
        
        embed1.add_field(name="Chain Of Command", value=(
            f"• {manager_role.mention}\n"
            f"• {admin_role.mention}\n"
            f"• {mod_role.mention}"
        ), inline=False)

        # --- Embed 2: Minor Infractions ---
        embed2 = discord.Embed(title="🟢 Minor Infractions", description=(
            "**1. Spreading False Information:** Spreading false info about updates, codes, etc.\n"
            "**2. Flooding/Spamming:** Sending messages that result in covering the chat.\n"
            "**3. Chaining:** When multiple members send the same message or GIF.\n"
            "**4. Channel Misuse:** Using a channel not for its intended purpose.\n"
            "**5. Toxicity/Ragebait:** Causing drama in the community or being toxic."
        ), color=0x2ecc71)
        embed2.set_footer(text="Violations result in a verbal warning or temporary mute.")

        # --- Embed 3: Moderate Infractions ---
        embed3 = discord.Embed(title="🟡 Moderate Infractions", description=(
            "**1. NSFW Comments:** Sending sexual comments or references.\n"
            "**2. Bypassing:** Attempting to bypass banned words through creative spelling.\n"
            "**3. Public Disputes with Staff:** Arguing with staff over punishments in public.\n"
            "**4. Mass Pinging:** Pinging someone repeatedly or multiple people (6+).\n"
            "**5. Sensitive Topics:** Discussing subjects like religion, gender, or politics."
        ), color=0xf1c40f)
        embed3.set_footer(text="Violations result in a warning, a mute, or a combination of both.")

        # --- Embed 4: Major Infractions ---
        embed4 = discord.Embed(title="🔴 Major Infractions", description=(
            "**1. Suicide Encouragement:** Requesting or encouraging self-harm.\n"
            "**2. Doxxing:** Attempting to dox or any threats of Doxxing.\n"
            "**3. NSFW Contents:** Explicit images, videos, or messages.\n"
            "**4. Black Marketing:** Buying/Selling products for real currency.\n"
            "**5. Phishing Links:** Sending malicious or scam links.\n"
            "**6. Discrimination:** Attacks against specific groups, race, or religion."
        ), color=0xe74c3c)
        embed4.set_footer(text="Violations in this category result in an IMMEDIATE BAN.")

        await interaction.response.send_message("✅ Sending Rules Embeds...", ephemeral=True)
        await interaction.channel.send(embeds=[embed1, embed2, embed3, embed4])

async def setup(bot):
    await bot.add_cog(RulesSystem(bot))
