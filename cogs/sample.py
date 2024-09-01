import discord
from discord.ext import commands
from discord import app_commands

class SAMPLECOG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="SAMPLE")
    async def SAMPLE_COMMAND(self, interaction: discord.Interaction):
        # Function goes here

        # Common lines
        await interaction.response.send_message(f'message')
        

async def setup(bot: commands.Bot):
    await bot.add_cog(SAMPLECOG(bot))

# It is reccommended that you use this as a template for your cogs, make sure to change anything that is all caps to make it unique
    