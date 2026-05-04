import discord
from discord import app_commands
from discord.ext import commands

class InfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="info_cmd", description="ดูรายละเอียดวิธีใช้งานทุกคำสั่งของบอทแบบเจาะลึก")
    async def info_cmd(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📖 คู่มือการใช้งานคำสั่งบอท (Command Manual)",
            description="นี่คือรายละเอียดของคำสั่งทั้งหมดที่คุณสามารถใช้ได้ในตอนนี้:",
            color=0x2b2d31
        )

        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        # ดึงคำสั่งทั้งหมดจาก Bot Tree
        all_commands = self.bot.tree.get_commands()

        for cmd in all_commands:
            # 1. รวบรวมข้อมูล Parameter (สิ่งที่ต้องกรอกหลังคำสั่ง)
            params = []
            if hasattr(cmd, 'parameters'):
                for p in cmd.parameters:
                    # แสดงชื่อตัวแปร และบอกว่าเป็นแบบบังคับ (Required) หรือไม่
                    star = "*" if p.required else ""
                    params.append(f"[{p.name}{star}]")
            
            param_str = " ".join(params) if params else ""
            
            # 2. จัดรูปแบบการแสดงผล
            # ตัวอย่าง: /dm_user [user*] [message*]
            cmd_usage = f"**`/{cmd.name} {param_str}`**"
            
            # รายละเอียดของคำสั่ง
            cmd_desc = cmd.description if cmd.description else "ไม่มีคำอธิบาย"
            
            # รายละเอียดของแต่ละ Parameter (ถ้ามี)
            param_details = ""
            if hasattr(cmd, 'parameters') and cmd.parameters:
                param_details = "\n> *รายละเอียดตัวแปร:*"
                for p in cmd.parameters:
                    param_details += f"\n> • `{p.name}`: {p.description}"

            # เพิ่มข้อมูลลงใน Embed Field
            embed.add_field(
                name=f"🔹 {cmd.name.upper()}",
                value=f"{cmd_usage}\n{cmd_desc}{param_details}",
                inline=False
            )

        embed.set_footer(text="หมายเหตุ: ตัวแปรที่มีเครื่องหมาย * คือจำเป็นต้องกรอก")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(InfoCommands(bot))
