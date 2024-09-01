import discord
from discord.ext import commands
from discord import app_commands

import sqlite3
import coc
from coc import utils

import typing



class recourceTrackerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clashdailyfarmed")
    async def clashdailyfarmed_command(self, interaction: discord.Interaction, clantag: str):
        temptag = clantag

        await interaction.response.send_message(f'You have chosen the tag {temptag}')
        
### AUTOCOMPLETE FUNCTIONS ###
    @clashdailyfarmed_command.autocomplete('clantag')
    async def clashdailyfarmed_autocomplete(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        # Connects to SQLite Database
        SQLiteConnect = sqlite3.connect("storage.db")
        SQLiteCursor = SQLiteConnect.cursor()
        # Checks for all playertag choices in the database
        SQLiteCursor.execute("SELECT ClanTag FROM ClanTags WHERE discordID = ?", (interaction.user.id,))
        result = SQLiteCursor.fetchall()
        # Closes connection to SQLite
        SQLiteConnect.close()

        # Converts result into a list of JUST the playertags
        clanTags = [account[0] for account in result]

        # Append the choices to the list in discord
        data = []
        for playertag_choice in clanTags:
            data.append(app_commands.Choice(name=playertag_choice, value=playertag_choice))
        return data


async def setup(bot: commands.Bot):
    await bot.add_cog(recourceTrackerCog(bot))

# It is reccommended that you use this as a template for your cogs, make sure to change anything that is all caps to make it unique
    