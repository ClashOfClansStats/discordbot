import discord
from discord.ext import commands
from discord import app_commands

class testCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="test")
    async def test_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("Test command executed successfully!")

async def setup(bot: commands.Bot):
    await bot.add_cog(testCog(bot))