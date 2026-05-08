import discord
from discord import app_commands, ui
from discord.ext import commands

class StaffInfoDropdown(ui.Select):
    def __init__(self, guild, roles_dict):
        self.guild = guild
        self.roles = roles_dict
        
        options = [
            discord.SelectOption(label='Management Team', description='Manager & Administrator', emoji='👑'),
            discord.SelectOption(label='High Staff', description='Head of Staff & Senior Moderator', emoji='🛡️'),
            discord.SelectOption(label='Standard Staff', description='Moderator & Junior Moderator', emoji='⚔️'),
        ]
        super().__init__(placeholder='Choose a staff division to view...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        def get_members(role):
            if not role: return "Role not configured."
            members = [m.mention for m in role.members]
            return ", ".join(members) if members else "No members assigned."

        embed = discord.Embed(color=0x2f3136)
        
        # ดึงชื่อเซิร์ฟเวอร์ (self.guild.name) มาใช้ในหัวข้อของ Dropdown ด้วย
        if self.values[0] == 'Management Team':
            embed.title = f"👑 Management Team | {self.guild.name}"
            embed.add_field(name="Manager", value=get_members(self.roles['manager']), inline=False)
            embed.add_field(name="Administrator", value=get_members(self.roles['admin']), inline=False)
            
        elif self.values[0] == 'High Staff':
            embed.title = f"🛡️ High Staff Team | {self.guild.name}"
            embed.add_field(name="Head Of Staff", value=get_members(self.roles['hos']), inline=False)
            embed.add_field(name="Senior Moderator", value=get_members(self.roles['srmod']), inline=False)
            
        else:
            embed.title = f"⚔️ Standard Staff Team | {self.guild.name}"
            embed.add_field(name="Moderator", value=get_members(self.roles['mod']), inline=False)
            embed.add_field(name="Junior Moderator", value=get_members(self.roles['jrmod']), inline=False)

        embed.set_footer(text=f"{self.guild.name} Official Staff Structure")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class StaffInfoView(ui.View):
    def __init__(self, guild, roles_dict):
        super().__init__(timeout=None)
        self.add_item(StaffInfoDropdown(guild, roles_dict))

class StaffSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="staff_info", description="Display all 6 staff ranks and members")
    @app_commands.describe(
        manager="Manager Role",
        administrator="Administrator Role",
        head_of_staff="Head Of Staff Role",
        senior_mod="Senior Moderator Role",
        moderator="Moderator Role",
        junior_mod="Junior Moderator Role"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def staff_info(self, interaction: discord.Interaction, 
                         manager: discord.Role, 
                         administrator: discord.Role, 
                         head_of_staff: discord.Role, 
                         senior_mod: discord.Role, 
                         moderator: discord.Role, 
                         junior_mod: discord.Role):
        
        guild = interaction.guild # ดึงข้อมูลเซิร์ฟเวอร์ปัจจุบัน
        roles_dict = {
            'manager': manager,
            'admin': administrator,
            'hos': head_of_staff,
            'srmod': senior_mod,
            'mod': moderator,
            'jrmod': junior_mod
        }
        
        # ใช้ f"{guild.name.upper()}" เพื่อให้ชื่อเปลี่ยนตามเซิร์ฟเวอร์ที่ใช้คำสั่ง
        embed = discord.Embed(
            title=f"{guild.name.upper()} STAFF DIRECTORY",
            description=(
                "Our staff team is divided into different divisions to ensure "
                "the best management and safety for our community.\n\n"
                "**Select a division from the dropdown menu to see the members.**"
            ),
            color=0x2f3136
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await interaction.response.send_message("✅ Staff Information posted!", ephemeral=True)
        await interaction.channel.send(embed=embed, view=StaffInfoView(guild, roles_dict))

async def setup(bot):
    await bot.add_cog(StaffSystem(bot))
