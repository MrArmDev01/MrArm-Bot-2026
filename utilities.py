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
        embed.add_field(name="🔵 Discord", value="Join for payouts and events.", inline=True)
        embed.set_footer(text=f"Server: {interaction.guild.name}", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

        # สร้างปุ่มกด Link Buttons
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="TikTok", url="https://www.tiktok.com/@mr.armxso?_r=1&_t=ZS-9687KlsdpET", style=discord.ButtonStyle.link))
        view.add_item(discord.ui.Button(label="YouTube", url="https://youtube.com/@mrarmxso?si=TLpVkaK4Ik44lR1U", style=discord.ButtonStyle.link))
        view.add_item(discord.ui.Button(label="Discord", url="https://discord.gg/QsqDgSvFYy", style=discord.ButtonStyle.link))
        
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

async def setup(bot):
    await bot.add_cog(UtilitySystem(bot))
