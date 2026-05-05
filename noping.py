import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import datetime

class EliteProtection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "config_noping.json"
        self.data = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except:
                return {"roles": [], "users": []}
        return {"roles": [], "users": []}

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.data, f, indent=4)

    # --- Setup Commands (Admin Only) ---
    
    @app_commands.command(name="noping_add_role", description="Add a role to the protection list")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_role(self, interaction: discord.Interaction, role: discord.Role):
        if role.id not in self.data["roles"]:
            self.data["roles"].append(role.id)
            self.save_config()
            await interaction.response.send_message(f"✅ Role {role.name} is now under elite protection.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ This role is already protected.", ephemeral=True)

    @app_commands.command(name="noping_add_user", description="Add a specific user to the protection list")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_user(self, interaction: discord.Interaction, member: discord.Member):
        if member.id not in self.data["users"]:
            self.data["users"].append(member.id)
            self.save_config()
            await interaction.response.send_message(f"✅ User {member.display_name} is now under elite protection.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ This user is already protected.", ephemeral=True)

    @app_commands.command(name="noping_list", description="View all protected roles and users")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def show_list(self, interaction: discord.Interaction):
        roles_mentions = [f"<@&{rid}>" for rid in self.data["roles"]]
        users_mentions = [f"<@{uid}>" for uid in self.data["users"]]
        
        embed = discord.Embed(title="🛡️ Elite Protection Registry", color=0x2f3136)
        embed.add_field(name="Protected Roles", value=", ".join(roles_mentions) if roles_mentions else "None", inline=False)
        embed.add_field(name="Protected Users", value=", ".join(users_mentions) if users_mentions else "None", inline=False)
        embed.set_footer(text="Confidential Information")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # --- Anti-Ping Logic ---

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bots and Staff (People with Manage Messages permission)
        if message.author.bot or message.author.guild_permissions.manage_messages:
            return

        is_forbidden = False
        
        # Check Role Pings
        for role in message.role_mentions:
            if role.id in self.data["roles"]:
                is_forbidden = True
                break
        
        # Check User Pings
        if not is_forbidden:
            for user in message.mentions:
                if user.id in self.data["users"]:
                    is_forbidden = True
                    break

        if is_forbidden:
            try:
                await message.delete()
                
                embed = discord.Embed(
                    description=(
                        f"⚠️ **Security Notice**\n"
                        f"{message.author.mention}, mentioning high-ranking officials or "
                        f"protected roles is restricted"
                    ),
                    color=0x2f3136
                )
                embed.set_author(name="System Protocol")
                
                # Delete warning after 5 seconds to keep channel clean
                await message.channel.send(embed=embed, delete_after=5)
                
            except discord.Forbidden:
                pass

async def setup(bot):
    await bot.add_cog(EliteProtection(bot))
