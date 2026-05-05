import discord
from discord import app_commands
from discord.ext import commands
import datetime

class UtilitySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- 32. Social Media Link Tree (The Hub) ---
    @app_commands.command(name="socials", description="Show all our official social media links")
    async def socials(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🔗 Connect With Us",
            description="Stay updated with our latest news, giveaways, and content!",
            color=0x2b2d31 # Dark theme color
        )
        embed.add_field(name="⚫ TikTok", value="Join our community for daily clips.", inline=True)
        embed.add_field(name="🔴 YouTube", value="Watch our full tutorials and guides.", inline=True)
        embed.add_field(name="🔵 Roblox Group", value="Join for payouts and events.", inline=True)
        embed.set_footer(text=f"Server: {interaction.guild.name}", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

        # สร้างปุ่มกด Link Buttons
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="TikTok", url="https://www.tiktok.com/", style=discord.ButtonStyle.link))
        view.add_item(discord.ui.Button(label="YouTube", url="https://www.youtube.com/", style=discord.ButtonStyle.link))
        view.add_item(discord.ui.Button(label="Roblox Group", url="https://www.roblox.com/groups/", style=discord.ButtonStyle.link))
        
        await interaction.response.send_message(embed=embed, view=view)

    # --- 33. Search Engine (Simple Browser Interface) ---
    @app_commands.command(name="search", description="Quickly find information on the web")
    @app_commands.describe(query="What do you want to search for?")
    async def search(self, interaction: discord.Interaction, query: str):
        # จำลองการค้นหา (ในระดับโปรสามารถเชื่อมต่อ Google API ได้)
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        
        embed = discord.Embed(
            title=f"🔍 Search Results: {query}",
            description=f"I found some results for your search. Click the link below to see all results on Google.",
            color=0x4285F4 # Google Blue
        )
        embed.add_field(name="Top Result", value=f"Check out the latest info for **{query}**", inline=False)
        embed.set_footer(text="Powered by Google Search Engine")

        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="View All Results", url=search_url, style=discord.ButtonStyle.link))
        
        await interaction.response.send_message(embed=embed, view=view)

    # --- 40. Shorten URL (Professional Link Format) ---
    @app_commands.command(name="shorten", description="Clean up long URLs into professional format")
    @app_commands.describe(url="Paste the long URL here")
    async def shorten(self, interaction: discord.Interaction, url: str):
        # ในที่นี้เราจะแสดงผลเป็น Embed ที่ทำให้ลิงก์ดูสะอาดและปลอดภัย
        embed = discord.Embed(
            title="🔗 URL Formatted Successfully",
            description=f"**Original Link:**\n`{url[:50]}...`" if len(url) > 50 else f"**Original Link:**\n`{url}`",
            color=0x5865F2 # Discord Blurple
        )
        embed.add_field(name="Safe Redirect", value="[Click here to open the link]( " + url + " )", inline=False)
        embed.set_footer(text="Note: Always be careful when clicking external links.")
        
        await interaction.response.send_message(embed=embed)

    # --- 31. Notification Simulator (Announcement Format) ---
    @app_commands.command(name="notify_test", description="Test how a YouTube/TikTok notification looks")
    async def notify_test(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🔴 New Video Uploaded!",
            description="**How to claim your rewards in 2026!**\nDon't forget to like and subscribe for more updates.",
            color=0xFF0000, # YouTube Red
            timestamp=datetime.datetime.now()
        )
        # ตัวอย่างรูป Thumbnail ขนาดใหญ่
        embed.set_image(url="https://images.rbxcdn.com/f7528a4be46b1464c185bb5e30b135c3.png") 
        embed.set_author(name="Your Channel Name", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        embed.set_footer(text="YouTube Notification")

        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Watch Now", url="https://youtube.com", style=discord.ButtonStyle.link))

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(UtilitySystem(bot))
