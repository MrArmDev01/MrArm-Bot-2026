import discord
from discord import app_commands
from discord.ext import commands

class PaginatorView(discord.ui.View):
    def __init__(self, pages):
        super().__init__(timeout=60) # Buttons will expire after 60 seconds of inactivity
        self.pages = pages
        self.current_page = 0

    async def update_message(self, interaction: discord.Interaction):
        # Update the existing message with the new page and the same view (buttons)
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

    @discord.ui.button(label="⬅️ Previous", style=discord.ButtonStyle.gray)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_message(interaction)
        else:
            await interaction.response.send_message("You are already on the first page.", ephemeral=True)

    @discord.ui.button(label="Next ➡️", style=discord.ButtonStyle.gray)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await self.update_message(interaction)
        else:
            await interaction.response.send_message("You are already on the last page.", ephemeral=True)

class InfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="info_cmd", description="Shows a paginated manual for all bot commands")
    @app_commands.checks.has_permissions(administrator=True)
    async def info_cmd(self, interaction: discord.Interaction):
        # Get all registered slash commands
        all_commands = self.bot.tree.get_commands()
        
        if not all_commands:
            return await interaction.response.send_message("No commands found in the system.", ephemeral=True)

        # Split commands into chunks (8 commands per page to stay within Discord limits)
        commands_per_page = 8
        pages = []
        
        for i in range(0, len(all_commands), commands_per_page):
            chunk = all_commands[i:i + commands_per_page]
            embed = discord.Embed(
                title="📖 Bot Command Manual",
                description=f"Listing all available commands (Page {len(pages)+1})",
                color=0x2b2d31
            )
            
            if self.bot.user.avatar:
                embed.set_thumbnail(url=self.bot.user.avatar.url)

            for cmd in chunk:
                # Build parameter display
                params = []
                if hasattr(cmd, 'parameters'):
                    for p in cmd.parameters:
                        star = "*" if p.required else ""
                        params.append(f"[{p.name}{star}]")
                
                param_str = " ".join(params)
                cmd_usage = f"**`/{cmd.name} {param_str}`**"
                cmd_desc = cmd.description or "No description provided."
                
                embed.add_field(
                    name=f"🔹 {cmd.name.upper()}",
                    value=f"{cmd_usage}\n{cmd_desc}",
                    inline=False
                )
            
            embed.set_footer(text=f"Page {len(pages)+1} | Total Commands: {len(all_commands)} | * = Required")
            pages.append(embed)

        # Create the view and send the first page
        view = PaginatorView(pages)
        await interaction.response.send_message(embed=pages[0], view=view)

async def setup(bot):
    await bot.add_cog(InfoCommands(bot))
