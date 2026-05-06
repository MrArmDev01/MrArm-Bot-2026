import discord
from discord import app_commands
from discord.ext import commands

class InfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="info_cmd", description="Shows detailed documentation for all bot commands")
    @app_commands.checks.has_permissions(administrator=True) # Only Admins can use this
    async def info_cmd(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📖 Bot Command Manual (Admin Access)",
            description="Detailed list of all available slash commands and their usage guides:",
            color=0x2b2d31
        )

        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        # Fetch all commands from the bot's command tree
        all_commands = self.bot.tree.get_commands()

        if not all_commands:
            embed.description = "No commands found in the system."
        else:
            for cmd in all_commands:
                # 1. Build Parameter list (e.g., [user*] [message*])
                params = []
                if hasattr(cmd, 'parameters'):
                    for p in cmd.parameters:
                        star = "*" if p.required else ""
                        params.append(f"[{p.name}{star}]")
                
                param_str = " ".join(params) if params else ""
                
                # 2. Command Usage string
                cmd_usage = f"**`/{cmd.name} {param_str}`**"
                
                # 3. Main Description
                cmd_desc = cmd.description if cmd.description else "No description available."
                
                # 4. Detailed Parameter descriptions
                param_details = ""
                if hasattr(cmd, 'parameters') and cmd.parameters:
                    param_details = "\n> *Parameter Details:*"
                    for p in cmd.parameters:
                        param_details += f"\n> • `{p.name}`: {p.description}"

                # Add to Embed
                embed.add_field(
                    name=f"🔹 {cmd.name.upper()}",
                    value=f"{cmd_usage}\n{cmd_desc}{param_details}",
                    inline=False
                )

        embed.set_footer(text="Note: Parameters marked with * are required.")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(InfoCommands(bot))

