import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import asyncio
import re

CONFIG_FILE = 'starboard_config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"guilds": {}, "counter": {}}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()

    @app_commands.command(name="set_starboard", description="Configure Forum Starboard with custom emojis")
    @app_commands.describe(
        forum_channel="The source Forum channel", 
        target_channel="The destination news channel",
        emoji1="First reaction emoji",
        emoji2="Second reaction emoji"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def set_starboard(self, interaction: discord.Interaction, forum_channel: discord.ForumChannel, target_channel: discord.TextChannel, emoji1: str, emoji2: str):
        guild_id = str(interaction.guild_id)
        if guild_id not in self.config["guilds"]:
            self.config["guilds"][guild_id] = {}
        
        # Save settings including emojis
        self.config["guilds"][guild_id][str(forum_channel.id)] = {
            "post": post_channel.id,
            "emoji1": emoji1,
            "emoji2": emoji2
        }
        
        if str(forum_channel.id) not in self.config["counter"]:
            self.config["counter"][str(forum_channel.id)] = 0
            
        save_config(self.config)
        await interaction.response.send_message(
            f"✅ Setup Complete!\n**Forum:** {forum_channel.mention}\n**Target:** {target_channel.mention}\n**Emojis:** {emoji1} {emoji2}", 
            ephemeral=True
        )

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        guild_id = str(thread.guild.id)
        parent_id = str(thread.parent_id)

        if guild_id in self.config["guilds"] and parent_id in self.config["guilds"][guild_id]:
            settings = self.config["guilds"][guild_id][parent_id]
            target_channel = self.bot.get_channel(settings["target"])
            if not target_channel:
                return

            # Increment Suggestion Counter
            self.config["counter"][parent_id] = self.config["counter"].get(parent_id, 0) + 1
            case_num = self.config["counter"][parent_id]
            save_config(self.config)

            # Wait for content to load
            await asyncio.sleep(3)
            
            async for message in thread.history(limit=1, oldest_first=True):
                embed = discord.Embed(
                    title=f"📌 {thread.name} ┇ Suggestions #{case_num}",
                    description=message.content if message.content else "*(No description)*",
                    color=0x2b2d31,
                    url=thread.jump_url
                )
                
                embed.add_field(name="Thread", value=f"[Open Suggestion]({thread.jump_url})", inline=False)
                embed.set_footer(text=f"By {thread.owner.display_name}", icon_url=thread.owner.display_avatar.url)

                if message.attachments:
                    embed.set_image(url=message.attachments[0].url)
                else:
                    links = re.findall(r'(https?://\S+\.(?:png|jpg|jpeg|gif|webp))', message.content)
                    if links:
                        embed.set_image(url=links[0])
                
                # Send message and add custom reactions
                sent_msg = await target_channel.send(embed=embed)
                try:
                    await sent_msg.add_reaction(settings["emoji1"])
                    await sent_msg.add_reaction(settings["emoji2"])
                except Exception as e:
                    print(f"Failed to add reaction: {e}")

async def setup(bot):
    await bot.add_cog(Starboard(bot))
