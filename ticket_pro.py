import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import io
from datetime import datetime

# Global config storage
ticket_config = {
    "admin_role_id": None,
    "category_id": None,
    "log_channel_id": None
}

class TicketControl(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Claim Ticket", style=discord.ButtonStyle.secondary, emoji="🙋‍♂️", custom_id="claim_ticket")
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        admin_role = interaction.guild.get_role(ticket_config["admin_role_id"])
        if admin_role not in interaction.user.roles and not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ Only Staff can claim tickets!", ephemeral=True)

        button.disabled = True
        button.label = "Ticket Claimed"
        button.style = discord.ButtonStyle.success

        # --- ปรับปรุง Embed เมื่อมีการ Claim ---
        embed = interaction.message.embeds[0]
        embed.color = discord.Color.gold()
        embed.set_author(name=f"Claimed by {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="🛡️ Staff in Charge", value=f"{interaction.user.mention}", inline=False)
        embed.description = "A staff member is now looking into your request. Please prepare any necessary information."

        await interaction.response.edit_message(embed=embed, view=self)
        await interaction.followup.send(f"✅ {interaction.user.mention} has taken responsibility for this ticket.")

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, emoji="🔒", custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        admin_role = interaction.guild.get_role(ticket_config["admin_role_id"])
        if admin_role not in interaction.user.roles and not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ Only Staff can close tickets!", ephemeral=True)

        await interaction.response.send_message("⌛ **Archiving conversation and closing ticket in 5 seconds...**", ephemeral=False)

        # --- Transcript Generation ---
        transcript = f"Ticket Transcript: {interaction.channel.name}\n"
        transcript += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        transcript += "-"*40 + "\n"

        async for msg in interaction.channel.history(limit=None, oldest_first=True):
            time = msg.created_at.strftime("%H:%M:%S")
            transcript += f"[{time}] {msg.author.display_name}: {msg.content}\n"

        # --- Send to Log Channel (สวยขึ้น) ---
        if ticket_config["log_channel_id"]:
            log_channel = interaction.guild.get_channel(ticket_config["log_channel_id"])
            if log_channel:
                file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{interaction.channel.name}.txt")
                log_embed = discord.Embed(
                    title="📂 Ticket Log Archived",
                    color=discord.Color.dark_grey(),
                    timestamp=datetime.now()
                )
                log_embed.add_field(name="Channel", value=f"`{interaction.channel.name}`", inline=True)
                log_embed.add_field(name="Closed By", value=interaction.user.mention, inline=True)
                log_embed.set_footer(text="System Transcript Service")
                await log_channel.send(embed=log_embed, file=file)

        await asyncio.sleep(5)
        await interaction.channel.delete()

class TicketLauncher(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.success, emoji="🎫", custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        if not ticket_config["category_id"]:
            return await interaction.response.send_message("❌ System not configured.", ephemeral=True)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        admin_role = guild.get_role(ticket_config["admin_role_id"])
        if admin_role:
            overwrites[admin_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        category = guild.get_channel(ticket_config["category_id"])
        ticket_channel = await guild.create_text_channel(name=f"🎫-{user.name}", category=category, overwrites=overwrites)

        await interaction.response.send_message(f"✅ Ticket opened: {ticket_channel.mention}", ephemeral=True)

        # --- ปรับปรุง Embed ในห้อง Ticket ใหม่ ---
        embed = discord.Embed(
            title="Support Request",
            description=f"Welcome {user.mention},\nOur support team will be with you shortly. While you wait, please provide a detailed description of your issue.",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
        embed.set_footer(text="Awaiting Staff Claim • Ticket ID: " + str(ticket_channel.id)[-6:])

        admin_mention = admin_role.mention if admin_role else "@Staff"
        await ticket_channel.send(content=f"{user.mention} | {admin_mention}", embed=embed, view=TicketControl())

class TicketPro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket_setup_pro", description="Full pro setup for Ticket System")
    @app_commands.describe(panel_channel="Where to put the button", category="Where to create tickets", admin_role="Staff role", log_channel="Where to send transcripts")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_pro(self, interaction: discord.Interaction, panel_channel: discord.TextChannel, category: discord.CategoryChannel, admin_role: discord.Role, log_channel: discord.TextChannel):
        ticket_config["role_id"] = admin_role.id
        ticket_config["category_id"] = category.id
        ticket_config["log_channel_id"] = log_channel.id

        # --- ปรับปรุง Embed หน้าแรก (Panel) ---
        panel_embed = discord.Embed(
            title="📩 Server Support Desk",
            description=(
                "Need assistance or want to report an issue?\n"
                "Click the button below to start a private conversation with our staff.\n\n"
                "**Guidelines:**\n"
                "• Be descriptive and patient.\n"
                "• All transcripts are saved for security.\n"
                "• No spamming tickets."
            ),
            color=0x2b2d31 # Dark theme color
        )
        if interaction.guild.icon:
            panel_embed.set_thumbnail(url=interaction.guild.icon.url)
        panel_embed.set_footer(text=f"{interaction.guild.name} | Support System", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

        await panel_channel.send(embed=panel_embed, view=TicketLauncher())
        await interaction.response.send_message("✅ Professional Ticket Panel has been deployed!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(TicketPro(bot))
