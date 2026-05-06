import discord
from discord import app_commands
from discord.ext import commands

class PaginatorView(discord.ui.View):
    def __init__(self, pages):
        super().__init__(timeout=60) # ปุ่มจะหายไปหลังจาก 60 วินาทีที่ไม่ใช้งาน
        self.pages = pages
        self.current_page = 0

    async def update_message(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

    @discord.ui.button(label="⬅️ ก่อนหน้า", style=discord.ButtonStyle.gray)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_message(interaction)
        else:
            await interaction.response.send_message("นี่คือหน้าแรกแล้วครับ", ephemeral=True)

    @discord.ui.button(label="ถัดไป ➡️", style=discord.ButtonStyle.gray)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await self.update_message(interaction)
        else:
            await interaction.response.send_message("นี่คือหน้าสุดท้ายแล้วครับ", ephemeral=True)

class InfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="info_cmd", description="ดูคู่มือการใช้งานคำสั่งทั้งหมด (แบบเปลี่ยนหน้าได้)")
    @app_commands.checks.has_permissions(administrator=True)
    async def info_cmd(self, interaction: discord.Interaction):
        all_commands = self.bot.tree.get_commands()
        
        if not all_commands:
            return await interaction.response.send_message("ไม่พบคำสั่งในระบบ", ephemeral=True)

        # แบ่งคำสั่งออกเป็นกลุ่มละ 8 คำสั่งต่อ 1 หน้า (เพื่อไม่ให้หน้ายาวเกินไป)
        commands_per_page = 8
        pages = []
        
        # วนลูปสร้าง Embed สำหรับแต่ละหน้า
        for i in range(0, len(all_commands), commands_per_page):
            chunk = all_commands[i:i + commands_per_page]
            embed = discord.Embed(
                title="📖 Bot Command Manual",
                description=f"แสดงรายการคำสั่งทั้งหมด (หน้า {len(pages)+1})",
                color=0x2b2d31
            )
            
            for cmd in chunk:
                params = []
                if hasattr(cmd, 'parameters'):
                    for p in cmd.parameters:
                        star = "*" if p.required else ""
                        params.append(f"[{p.name}{star}]")
                
                param_str = " ".join(params)
                cmd_usage = f"**`/{cmd.name} {param_str}`**"
                cmd_desc = cmd.description or "ไม่มีคำอธิบาย"
                
                embed.add_field(
                    name=f"🔹 {cmd.name.upper()}",
                    value=f"{cmd_usage}\n{cmd_desc}",
                    inline=False
                )
            
            embed.set_footer(text=f"Page {len(pages)+1} | ทั้งหมด {len(all_commands)} คำสั่ง")
            pages.append(embed)

        # ส่งข้อความพร้อมปุ่มเปลี่ยนหน้า
        view = PaginatorView(pages)
        await interaction.response.send_message(embed=pages[0], view=view)

async def setup(bot):
    await bot.add_cog(InfoCommands(bot))
