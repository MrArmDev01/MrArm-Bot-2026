import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random

class CrashPrank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="crash_pc", description="Execute a spam-based system corruption sequence")
    @app_commands.describe(target="The target user to attack with fake errors")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def crash_pc(self, interaction: discord.Interaction, target: discord.Member):
        # Admin confirmation
        await interaction.response.send_message(f"☣️ Viral spam sequence engaged on {target.display_name}...", ephemeral=True)

        # List of scary error messages to spam
        errors = [
            f"⚠️ **DIRECTORY_CORRUPTION_DETECTED** in `{target.name}/System32`",
            "💉 `INJECTING_PAYLOAD.EXE` ... [OK]",
            "🔓 **SECURITY_BREACH:** Firewall bypassed for target: " + target.mention,
            "🔥 `OVERHEATING_WARNING:` CPU Core 0 temperature at 105°C",
            "💾 `WIPING_DRIVE_C:` [▓▓▓▓░░░░░░] 40% Complete",
            "📡 **REMOTE_ACCESS_GRANTED** to unknown_user@darknet",
            "🌑 `BIOS_OVERRIDE_INITIATED` ... Goodbye.",
            "🚫 **FATAL_EXCEPTION_0x000F4:** Memory cannot be read.",
            "💀 `SYSTEM_ENCRYPTION:` Your files are being locked.",
            f"🛑 **EMERGENCY_SHUTDOWN_REQUESTED** by {target.display_name}"
        ]

        # 1. Start the spamming phase (Sound alerts will go crazy)
        for error in errors:
            await interaction.channel.send(error)
            # Random fast delay to make it look like a real glitching software
            await asyncio.sleep(random.uniform(0.3, 0.8))

        # 2. Final scary summary message
        final_msg = await interaction.channel.send(
            f"❌ **[CRITICAL SYSTEM FAILURE]** ❌\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Target: {target.mention}\n"
            f"Status: `HARDWARE_LOCKDOWN`\n"
            f"Error Code: `0x8004210B` (VIRAL_INFECTION_DETECTED)\n\n"
            f"The device has been locked to prevent a total data breach. "
            f"System recovery will be available in **5 minutes**.\n"
            f"**DO NOT ATTEMPT TO REBOOT OR UNPLUG THE DEVICE.**"
        )

        # 3. Wait for 5 minutes in absolute silence
        await asyncio.sleep(300)

async def setup(bot):
    await bot.add_cog(CrashPrank(bot))
