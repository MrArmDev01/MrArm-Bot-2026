import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio

class PayoutSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- View สำหรับห้องส่วนตัว (มีปุ่มปิด) ---
    class TicketControlView(discord.ui.View):
        def __init__(self, target_user: discord.Member, amount: int):
            super().__init__(timeout=None)
            self.target_user = target_user
            self.amount = amount

        @discord.ui.button(label="Close & Complete Payout", style=discord.ButtonStyle.danger, emoji="🔒")
        async def close_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
            # ตรวจสอบว่า "คนกดปิด" ต้องเป็น Admin หรือคนที่มีสิทธิ์จัดการข้อความ
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("❌ Only Administrators can close this payout session.", ephemeral=True)
                return

            await interaction.response.defer() # ป้องกันบอทค้างระหว่างส่ง DM

            # 1. ส่งข้อความยาวๆ ไปหาผู้รับทาง DM
            dm_content = (
                f"✅ **Robux Payout Completed Successfully!**\n\n"
                f"Dear **{self.target_user.display_name}**,\n"
                f"The administration has finalized your payout of **{self.amount:,} Robux**. "
                f"**Transaction Summary:**\n"
                
                f"• Amount: `{self.amount:,} Robux`\n"
                f"• Status: `Distributed`\n"
                f"• Server: `{interaction.guild.name}`\n\n"
                f"Thank you for being a part of our community! If you have any further questions, feel free to open a new support ticket."
            )

            try:
                await self.target_user.send(dm_content)
                dm_status = "✅ Successfully sent confirmation DM."
            except discord.Forbidden:
                dm_status = "⚠️ Could not DM the user (DMs are closed)."

            # 2. แจ้งสถานะในห้องก่อนลบ
            await interaction.followup.send(f"Closing room... {dm_status}\nThis channel will be deleted in 5 seconds.")
            
            # 3. รอ 5 วินาทีแล้วลบห้อง
            await asyncio.sleep(5)
            await interaction.channel.delete()

    # --- View สำหรับปุ่มแรกที่ใช้ Claim ---
    class PayoutView(discord.ui.View):
        def __init__(self, target_user: discord.Member, amount: int, parent_cog):
            super().__init__(timeout=None)
            self.target_user = target_user
            self.amount = amount
            self.parent_cog = parent_cog

        @discord.ui.button(label="Claim Robux & Open Receipt", style=discord.ButtonStyle.success, emoji="🧧")
        async def claim_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id != self.target_user.id:
                await interaction.response.send_message(f"❌ This is only for {self.target_user.mention}.", ephemeral=True)
                return

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            
            channel = await interaction.guild.create_text_channel(
                name=f"claim-{interaction.user.name}",
                overwrites=overwrites,
                category=interaction.channel.category
            )

            await interaction.response.send_message(f"✅ Private room created: {channel.mention}", ephemeral=True)
            
            embed = discord.Embed(
                title="💳 Official Payout Receipt",
                description=(
                    f"Hello {interaction.user.mention},\n"
                    f"Staff will now process your **{self.amount:,} Robux**.\n"
                    "Please wait for an administrator to finalize this session."
                ),
                color=0x00b06f
            )
            # ส่งปุ่ม "Close" ให้ Admin ในห้องลับ
            await channel.send(embed=embed, view=self.parent_cog.TicketControlView(self.target_user, self.amount))

    # --- คำสั่งหลัก ---
    @app_commands.command(name="payout", description="Send Robux payout with Admin-close & DM system")
    @app_commands.checks.has_permissions(administrator=True)
    async def payout(self, interaction: discord.Interaction, target: discord.Member, amount: int):
        embed = discord.Embed(
            title="💰 Robux Payout Successful",
            description=(
                f"has initiated a payout to **{target.display_name}**.\n\n"
                f"**Details:**\n"
                f"• Amount: `{amount:,} Robux`\n"
                f"• Status: `Pending Claim`"
            ),
            color=0x00b06f
        )
        embed.set_thumbnail(url="https://images.rbxcdn.com/f7528a4be46b1464c185bb5e30b135c3.png")
        
        await interaction.response.send_message("✅ Payout sent.", ephemeral=True)
        await interaction.channel.send(
            content=f"{target.mention}", 
            embed=embed, 
            view=self.PayoutView(target, amount, self)
        )

async def setup(bot):
    await bot.add_cog(PayoutSystem(bot))
