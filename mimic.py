import discord
from discord import app_commands
from discord.ext import commands

class Mimic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mimic", description="Impersonate someone and send a message as them")
    @app_commands.describe(target="The user you want to mimic", message="The message you want to say as them")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def mimic(self, interaction: discord.Interaction, target: discord.Member, message: str):
        # 1. Defer the response so it's hidden (ephemeral)
        await interaction.response.defer(ephemeral=True)

        # 2. Get or Create a Webhook for the channel
        # We check if there's already a webhook named 'MimicBot' to reuse it
        webhooks = await interaction.channel.webhooks()
        webhook = discord.utils.get(webhooks, name="MimicBot")
        
        if not webhook:
            webhook = await interaction.channel.create_webhook(name="MimicBot")

        # 3. Send the message using the target's Name and Avatar
        await webhook.send(
            content=message,
            username=target.display_name,
            avatar_url=target.display_avatar.url
        )

        # 4. Confirmation for you only
        await interaction.followup.send(f"✅ Successfully mimicked **{target.display_name}**!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Mimic(bot))
    