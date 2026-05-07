import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random
import json
import os
from datetime import datetime, timedelta

DATA_FILE = "giveaways_pro.json"

class GiveawayView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Join Giveaway 🎉", style=discord.ButtonStyle.primary, custom_id="join_pro_giveaway")
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        msg_id = str(interaction.message.id)
        if msg_id not in data:
            return await interaction.response.send_message("❌ This giveaway is no longer active.", ephemeral=True)
        
        giveaway = data[msg_id]
        user = interaction.user

        if user.id in giveaway["participants"]:
            return await interaction.response.send_message("⚠️ You have already joined!", ephemeral=True)

        if giveaway.get("role_id"):
            required_role = interaction.guild.get_role(giveaway["role_id"])
            if required_role not in user.roles:
                return await interaction.response.send_message(f"🚫 You need the {required_role.mention} role to join!", ephemeral=True)

        giveaway["participants"].append(user.id)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            
        await interaction.response.send_message(f"✅ Registered for **{giveaway['prize']}**!", ephemeral=True)

class GiveawayPro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump({}, f)

    @app_commands.command(name="giveaway", description="Start a professional giveaway")
    @app_commands.describe(
        prize="What is the prize?",
        duration_mins="Duration in minutes",
        winners="Number of winners",
        role_required="Role needed to join (Optional)",
        invite_required="Number of invites needed (Optional)",
        image_url="Link to an image of the prize (Optional)"
    )
    async def giveaway(
        self, 
        interaction: discord.Interaction, 
        prize: str, 
        duration_mins: int, 
        winners: int = 1,
        role_required: discord.Role = None,
        invite_required: int = 0,
        image_url: str = None
    ):
        end_time = datetime.now() + timedelta(minutes=duration_mins)
        timestamp = int(end_time.timestamp())

        # ปรับแต่ง Embed ตามบรีฟ: ลบ "Server", ลบประโยคแนะนำ, ลบอีโมจิหน้าฟิลด์
        embed = discord.Embed(
            title="🎊 GIVEAWAY 🎊",
            description=f"Participate to win a **{prize}**",
            color=0x5865F2
        )
        
        embed.add_field(name="Prize", value=f"**{prize}**", inline=True)
        embed.add_field(name="Winners", value=f"`{winners}`", inline=True)
        embed.add_field(name="Host", value=interaction.user.mention, inline=True)

        # คงความสวยงามของลูกศร/กระสุนไว้ในส่วนเงื่อนไข
        reqs = []
        if role_required: reqs.append(f"• Role: {role_required.mention}")
        if invite_required > 0: reqs.append(f"• Invites: `{invite_required}`")
        if reqs:
            embed.add_field(name="Required", value="\n".join(reqs), inline=False)

        embed.add_field(name="End In", value=f"<t:{timestamp}:R> (<t:{timestamp}:f>)", inline=False)

        if image_url and image_url.startswith("http"):
            embed.set_image(url=image_url)
        
        if interaction.guild.icon:
            embed.set_thumbnail(url=interaction.guild.icon.url)

        embed.set_footer(text=f"Giveaway ID: {interaction.id}")

        await interaction.response.send_message("Giveaway started!", ephemeral=True)
        msg = await interaction.channel.send(embed=embed, view=GiveawayView())

        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        data[str(msg.id)] = {
            "prize": prize,
            "winners_count": winners,
            "participants": [],
            "role_id": role_required.id if role_required else None,
            "channel_id": interaction.channel_id,
            "host_id": interaction.user.id
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

        await asyncio.sleep(duration_mins * 60)
        await self.process_winner(msg.id)

    async def process_winner(self, msg_id):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        if str(msg_id) not in data: return
        
        giveaway = data[str(msg_id)]
        channel = self.bot.get_channel(giveaway["channel_id"])
        if not channel: return
        
        try:
            msg = await channel.fetch_message(msg_id)
        except: return

        participants = giveaway["participants"]
        if len(participants) < giveaway["winners_count"]:
            winner_text = "Not enough participants."
        else:
            winners = random.sample(participants, min(len(participants), giveaway["winners_count"]))
            winner_text = ", ".join([f"<@{w}>" for w in winners])

        end_embed = discord.Embed(
            title="🎊 GIVEAWAY ENDED 🎊",
            description=f"Prize: **{giveaway['prize']}**\nWinners: {winner_text}\nHost: <@{giveaway['host_id']}>",
            color=0x2b2d31
        )
        if msg.embeds[0].image:
            end_embed.set_image(url=msg.embeds[0].image.url)

        await msg.edit(embed=end_embed, view=None)
        if winner_text != "Not enough participants.":
            await channel.send(f"Congratulations {winner_text}! You won the **{giveaway['prize']}**! 🎉")

async def setup(bot):
    await bot.add_cog(GiveawayPro(bot))
    bot.add_view(GiveawayView())
