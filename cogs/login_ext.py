import discord
from discord.ext import commands
from discord import app_commands

import sqlite3
import coc
from coc import utils

import typing

class loginCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clashaddbase")
    async def clashaddbase_command(self, interaction: discord.Interaction, playertag: str):
        # Stores the player tag input in a temperary variable
        tempTag = playertag
        
        # Check if the player tag is a valid tag
        if not utils.is_valid_tag(tempTag):
            await interaction.response.send_message(f"Please supply a proper tag", ephemeral=True)
            return
        else:
            # Connects to SQLite Database
            SQLiteConnect = sqlite3.connect("storage.db")
            SQLiteCursor = SQLiteConnect.cursor()

            # Checks if PlayerTag already exists in the database
            SQLiteCursor.execute("SELECT 1 FROM PlayerTags WHERE playerTag = ?", (tempTag,))
            result = SQLiteCursor.fetchone()

            if result:
                await interaction.response.send_message(f"playerTag Already Exists for the tag **{tempTag}**", ephemeral=True)
            else:
                SQLiteCursor.execute("INSERT INTO PlayerTags (discordID, playerTag) VALUES (?, ?)" , (interaction.user.id, tempTag))
                SQLiteConnect.commit()
                SQLiteConnect.close()
                await interaction.response.send_message(f"You have logged in under the tag {tempTag}", ephemeral=True)

            # await interaction.response.send_message(f'Tag is Valid: {tempTag}', ephemeral=True)

# Autocompletes playertag option (TO BE USED ELSEWHERE)
playerTagAutocomplete = '''
    @clashaddbase_command.autocomplete("playertag")
    async def clashaddbase_autocomplete(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        testvar = ['opt1', 'opt2', 'opt3']
        print(testvar)
        for playertag_choice in testvar:
            data.append(app_commands.Choice(name=playertag_choice, value=playertag_choice))
        return data
'''

async def setup(bot: commands.Bot):
    await bot.add_cog(loginCog(bot))

# It is reccommended that you use this as a template for your cogs, make sure to change anything that is all caps to make it unique
    