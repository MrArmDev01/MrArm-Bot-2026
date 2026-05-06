import discord
from discord import app_commands
from discord.ext import commands
import json
import os

DATA_FILE = "goals.json"

class GoalTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.goals = self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "member_goal": {"current": 0, "target": 1000, "title": "Member Milestone"},
            "boost_goal": {"current": 0, "target": 15, "title": "Server Boost Level"},
            "message_goal": {"current": 0, "target": 5000, "title": "Activity Peak"}
        }

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.goals, f, indent=4)

    def create_bar(self, current, target, length=20):
        percent = min(current / target, 1.0)
        filled = int(length * percent)
        bar = '█' * filled + '░' * (length - filled)
        return f"`{bar}` {int(percent * 100)}%"

    @app_commands.command(name="server_goals", description="View current community goals for this server")
    async def server_goals(self, interaction: discord.Interaction):
        # ดึงข้อมูลล่าสุดจากเซิร์ฟเวอร์ที่เรียกใช้คำสั่ง
        guild = interaction.guild
        self.goals["member_goal"]["current"] = guild.member_count
        self.goals["boost_goal"]["current"] = guild.premium_subscription_count
        self.save_data()

        # สร้าง Embed โดยใช้ชื่อเซิร์ฟเวอร์อัตโนมัติ
        embed = discord.Embed(
            title=f"{guild.name} | Achievement Dashboard", # เปลี่ยนตามชื่อเซิร์ฟเวอร์
            description=f"Our collective goals and current progress towards unlocking new features in **{guild.name}**.",
            color=0x2b2d31
        )

        # ใส่รูปไอคอนเซิร์ฟเวอร์ (ถ้ามี)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        for key, goal in self.goals.items():
            bar = self.create_bar(goal["current"], goal["target"])
            status = "COMPLETED" if goal["current"] >= goal["target"] else "IN PROGRESS"
            
            embed.add_field(
                name=f"{goal['title']} ({status})",
                value=f"Progress: `{goal['current']} / {goal['target']}`\n{bar}",
                inline=False
            )

        embed.set_footer(text=f"Live System Analysis • {guild.name}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="set_goal", description="Admin only: Set a specific target for a goal")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_goal(self, interaction: discord.Interaction, goal_type: str, target: int):
        valid_types = ["member_goal", "boost_goal", "message_goal"]
        if goal_type not in valid_types:
            await interaction.response.send_message(f"Invalid type. Use: {', '.join(valid_types)}", ephemeral=True)
            return

        self.goals[goal_type]["target"] = target
        self.save_data()
        await interaction.response.send_message(f"✅ Updated {goal_type} target to {target}", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        
        self.goals["message_goal"]["current"] += 1
        if self.goals["message_goal"]["current"] % 10 == 0:
            self.save_data()

async def setup(bot):
    await bot.add_cog(GoalTracker(bot))
