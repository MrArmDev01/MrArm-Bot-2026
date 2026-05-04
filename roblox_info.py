import discord
from discord import app_commands
from discord.ext import commands
import requests
from datetime import datetime

class RobloxInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roblox_info", description="Get detailed info, online status, and current game of a Roblox user")
    @app_commands.describe(username="The Roblox username to look up")
    async def roblox_info(self, interaction: discord.Interaction, username: str):
        await interaction.response.defer()

        try:
            # 1. Fetch User ID
            user_res = requests.post("https://users.roblox.com/v1/usernames/users", json={
                "usernames": [username],
                "excludeBannedUsers": False
            })
            user_data = user_res.json()

            if not user_data.get('data'):
                await interaction.followup.send(f"❌ User `{username}` not found.", ephemeral=True)
                return

            user_id = user_data['data'][0]['id']
            display_name = user_data['data'][0]['displayName']
            actual_username = user_data['data'][0]['name']

            # 2. Fetch User Details & Presence (Online Status)
            detail_res = requests.get(f"https://users.roblox.com/v1/users/{user_id}")
            detail_data = detail_res.json()
            
            # Presence API for Online Status and Game Activity
            presence_res = requests.post("https://presence.roblox.com/v1/presence/users", json={"userIds": [user_id]})
            presence_data = presence_res.json()['userPresences'][0]

            # 3. Process Data
            created_at = detail_data.get('created', '')
            date_obj = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            formatted_join_date = date_obj.strftime("%B %d, %Y")

            # Online Status Mapping
            # 0: Offline, 1: Online, 2: InGame, 3: Studio
            status_code = presence_data.get('userPresenceType', 0)
            last_online = presence_data.get('lastOnline', 'Unknown')
            
            status_text = "⚪ Offline"
            current_activity = "None"
            embed_color = discord.Color.light_grey()

            if status_code == 1:
                status_text = "🟢 Online (Website)"
                embed_color = discord.Color.green()
            elif status_code == 2:
                status_text = "🔵 Playing a Game"
                game_name = presence_data.get('lastLocation', 'Private Game')
                current_activity = f"🎮 Playing: **{game_name}**"
                embed_color = discord.Color.blue()
            elif status_code == 3:
                status_text = "🟠 Developing (Studio)"
                embed_color = discord.Color.orange()

            # Format Last Online Date
            if last_online != 'Unknown':
                lo_obj = datetime.strptime(last_online, "%Y-%m-%dT%H:%M:%S.%fZ")
                last_online_str = lo_obj.strftime("%B %d, %Y | %H:%M")
            else:
                last_online_str = "Hidden by Privacy"

            # 4. Fetch Avatar Headshot
            thumb_res = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png&isCircular=false")
            thumb_url = thumb_res.json()['data'][0]['imageUrl']

            # 5. Create Embed
            embed = discord.Embed(title=f"{display_name}'s Profile", url=f"https://www.roblox.com/users/{user_id}/profile", color=embed_color)
            embed.set_thumbnail(url=thumb_url)
            
            embed.add_field(name="Username", value=f"`{actual_username}`", inline=True)
            embed.add_field(name="User ID", value=f"`{user_id}`", inline=True)
            embed.add_field(name="Join Date", value=f"{formatted_join_date}", inline=True)
            
            embed.add_field(name="Current Status", value=f"**{status_text}**", inline=True)
            embed.add_field(name="Last Online", value=f"{last_online_str}", inline=True)
            embed.add_field(name="Activity", value=current_activity, inline=True)

            description = detail_data.get('description') or "No Bio Provided."
            embed.add_field(name="About Me", value=f"```\n{description[:300]}\n```", inline=False)
            
            embed.set_footer(text="Powered by Roblox API • Mr.Arm")
            embed.timestamp = discord.utils.utcnow()

            view = discord.ui.View()
            view.add_item(discord.ui.Button(label="Open Roblox Profile", url=f"https://www.roblox.com/users/{user_id}/profile"))

            await interaction.followup.send(embed=embed, view=view)

        except Exception as e:
            print(f"Error in roblox_info: {e}")
            await interaction.followup.send("⚠️ Could not fetch user data. They might be private or banned.")

async def setup(bot):
    await bot.add_cog(RobloxInfo(bot))
    