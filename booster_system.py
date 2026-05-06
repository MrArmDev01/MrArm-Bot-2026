import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class BoosterSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "booster_settings.json"
        self.settings = self.load_settings()

    def load_settings(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_settings(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4, ensure_ascii=False)

    # --- Commands to Set Up ---
    @app_commands.command(name="set_booster_msg", description="Set up the welcome message for Server Boosters")
    @app_commands.describe(
        channel="The channel to send the message in",
        title="Title of the Embed",
        message="The message content (Use {user} to mention the booster)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def set_booster_msg(self, interaction: discord.Interaction, channel: discord.TextChannel, title: str, message: str):
        guild_id = str(interaction.guild.id)
        self.settings[guild_id] = {
            "channel_id": channel.id,
            "title": title,
            "message": message
        }
        self.save_settings()
        
        await interaction.response.send_message(f"✅ Booster message set to {channel.mention} successfully!", ephemeral=True)

    # --- Event Listener ---
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        # Check if the member just started boosting
        if before.premium_since is None and after.premium_since is not None:
            guild_id = str(after.guild.id)
            
            if guild_id in self.settings:
                config = self.settings[guild_id]
                channel = after.guild.get_channel(config["channel_id"])
                
                if channel:
                    # Replace {user} with actual mention
                    final_msg = config["message"].replace("{user}", after.mention)
                    
                    embed = discord.Embed(
                        title=config["title"],
                        description=final_msg,
                        color=0xff73fa # Pink Booster Color
                    )
                    embed.set_thumbnail(url=after.display_avatar.url)
                    embed.set_author(name="New Server Booster!", icon_url="https://cdn.discordapp.com/emojis/825414364171010078.png")
                    embed.set_footer(text=f"Thank you for boosting {after.guild.name}!")
                    
                    await channel.send(content=after.mention, embed=embed)

async def setup(bot):
    await bot.add_cog(BoosterSystem(bot))
