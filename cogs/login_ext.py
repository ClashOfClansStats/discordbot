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


    @app_commands.command(name="test")
    async def test_command(self, interaction: discord.Interaction):
        await interaction.response.defer()
        testvar = "test"
        embedTemp = discord.Embed(title="Hello World!",
                                   description=f"{testvar}", 
                                   color=0x0000FF,
                                   )
        
        await interaction.followup.send("Hello World!", embed=embedTemp)

# Add a base to your account
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

            # Closes connection to SQLite
            SQLiteCursor.close()

            if result:
                await interaction.response.send_message(f"playerTag Already Exists for the tag **{tempTag}**", ephemeral=True)
            else:
                # Reopens connection to SQLite
                SQLiteConnect = sqlite3.connect("storage.db")
                SQLiteCursor = SQLiteConnect.cursor()

                # Adds PlayerTag to the database
                SQLiteCursor.execute("INSERT INTO PlayerTags (discordID, playerTag) VALUES (?, ?)" , (interaction.user.id, tempTag))
                SQLiteConnect.commit()
                SQLiteConnect.close()
                await interaction.response.send_message(f"You have logged in under the tag {tempTag}", ephemeral=True)

# Remove a base from your account
    @app_commands.command(name="clashrembase")
    async def clashrembase_command(self, interaction: discord.Interaction, playertag: str):
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

            # Checks if PlayerTag exists in the database
            SQLiteCursor.execute("SELECT 1 FROM PlayerTags WHERE playerTag = ?", (tempTag,))
            result = SQLiteCursor.fetchone()

            # Closes connection to SQLite
            SQLiteConnect.close()

            if not result:
                await interaction.response.send_message(f"playerTag Does Not Exist for the tag **{tempTag}**", ephemeral=True)
            else:
                # Reconnects to SQLite Database
                SQLiteConnect = sqlite3.connect("storage.db")
                SQLiteCursor = SQLiteConnect.cursor()

                # Removes login for player tag
                SQLiteCursor.execute("DELETE FROM PlayerTags WHERE playerTag = ?", (tempTag,))
                SQLiteConnect.commit()
                SQLiteConnect.close()
                await interaction.response.send_message(f"You have logged out of the tag {tempTag}", ephemeral=True)


# Add a clan to your account
    @app_commands.command(name="clashaddclan")
    async def clashaddclan_command(self, interaction: discord.Interaction, clantag: str):
        # Stores the clan tag input in a temperary variable
        tempTag = clantag   
        
        # Check if the clan tag is a valid tag
        if not utils.is_valid_tag(tempTag):
            await interaction.response.send_message(f"Please supply a proper tag", ephemeral=True)
            return
        else:
            # Connects to SQLite Database
            SQLiteConnect = sqlite3.connect("storage.db")
            SQLiteCursor = SQLiteConnect.cursor()

            # Checks if ClanTag already exists in the database
            SQLiteCursor.execute("SELECT 1 FROM ClanTags WHERE ClanTag = ?", (tempTag,))
            result = SQLiteCursor.fetchone()

            # Closes connection to SQLite database
            SQLiteConnect.close()

            if result:
                await interaction.response.send_message(f"ClanTag Already Exists for the tag **{tempTag}**", ephemeral=True)
            else:
                # Reopens connection to SQLite database
                SQLiteConnect = sqlite3.connect("storage.db")
                SQLiteCursor = SQLiteConnect.cursor()

                # Adds ClanTag to the database
                SQLiteCursor.execute("INSERT INTO ClanTags (discordID, ClanTag) VALUES (?, ?)" , (interaction.user.id, tempTag))
                SQLiteConnect.commit()
                SQLiteConnect.close()
                await interaction.response.send_message(f"You have added a clan under the tag {tempTag}", ephemeral=True)

# Remove a clan from your account
    @app_commands.command(name="clashremclan")
    async def clashremclan_command(self, interaction: discord.Interaction, clantag: str):
        # Stores the clan tag input in a temperary variable
        tempTag = clantag
        
        # Check if the clan tag is a valid tag
        if not utils.is_valid_tag(tempTag):
            await interaction.response.send_message(f"Please supply a proper tag", ephemeral=True)
            return
        else:
            # Connects to SQLite Database
            SQLiteConnect = sqlite3.connect("storage.db")
            SQLiteCursor = SQLiteConnect.cursor()

            # Checks if ClanTag exists in the database
            SQLiteCursor.execute("SELECT 1 FROM ClanTags WHERE ClanTag = ?", (tempTag,))
            result = SQLiteCursor.fetchone()

            # Closes connection to SQLite
            SQLiteConnect.close()
            
            if not result:
                await interaction.response.send_message(f"ClanTag Does Not Exist for the tag **{tempTag}**", ephemeral=True)
            else:
                # Reconnects to SQLite Database
                SQLiteConnect = sqlite3.connect("storage.db")
                SQLiteCursor = SQLiteConnect.cursor()

                # Removes login for clan tag
                SQLiteCursor.execute("DELETE FROM ClanTags WHERE ClanTag = ?", (tempTag,))
                SQLiteConnect.commit()
                SQLiteConnect.close()
                await interaction.response.send_message(f"You have removed the clan {tempTag}", ephemeral=True)

            
        

### AUTOCOMPLETE FUNCTIONS ###

# Autocompletes playertag option in clashrembase command
    @clashrembase_command.autocomplete("playertag")
    async def clashaddbase_autocomplete(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        # Connects to SQLite Database
        SQLiteConnect = sqlite3.connect("storage.db")
        SQLiteCursor = SQLiteConnect.cursor()
        # Checks for all playertag choices in the database
        SQLiteCursor.execute("SELECT PlayerTag FROM PlayerTags WHERE discordID = ?", (interaction.user.id,))
        result = SQLiteCursor.fetchall()
        # Closes connection to SQLite
        SQLiteConnect.close()

        # Converts result into a list of JUST the playertags
        accountTags = [account[0] for account in result]

        # Append the choices to the list in discord
        data = []
        for playertag_choice in accountTags:
            data.append(app_commands.Choice(name=playertag_choice, value=playertag_choice))
        return data
    
# Autocompletes playertag option in clashrembase command
    @clashremclan_command.autocomplete("clantag")
    async def clashaddbase_autocomplete(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
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

# Connects cogs
async def setup(bot: commands.Bot):
    await bot.add_cog(loginCog(bot))