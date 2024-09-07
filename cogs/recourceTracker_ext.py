import discord
from discord.ext import tasks, commands
from discord import app_commands

import sqlite3
import coc
from coc import utils

import os
from dotenv import load_dotenv

from table2ascii import table2ascii as t2a, PresetStyle

import typing

import datetime

class recourceTrackerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clashdailyfarmed")
    async def clashdailyfarmed_command(self, interaction: discord.Interaction, clantag: str):
        tempTag = clantag
        if not coc.utils.is_valid_tag(tempTag):
            await interaction.response.send_message(f"Please supply a proper tag", ephemeral=True)
            return
        else:
            # Gets the parent direcotry
            currentDir = os.path.dirname(__file__)
            tempPath = os.path.split(currentDir)[0]

            # Load .env file
            load_dotenv(dotenv_path=tempPath)

            # Fetches login info
            cocEmail = os.getenv('cocEmail')
            cocPassword = os.getenv('cocPassword')
            print(f"cocEmail: {cocEmail} | cocPassword: {cocPassword}")

            await coc.Client.login(email=cocEmail, password=cocPassword)
            print(f"coc client logged in using email: {cocEmail} and password: {cocPassword}")
            
            # Gets clan info
            clan = coc.Client.get_clan(tempTag)

            await interaction.response.send_message(clan, ephemeral=True)

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

### TASK FUNCTIONS ### 
class loopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dailyTask.start()

# Daily task that runs at 0:00 EST
    @tasks.loop(time=datetime.time(hour=4, minute=20,second=15, tzinfo=datetime.timezone.utc))
    async def dailyTask(self):
        print("Starting daily task...")
        # Gets the parent direcotry
        currentDir = os.path.dirname(__file__)
        tempPath = os.path.split(currentDir)[0]

        # Load .env file
        load_dotenv(dotenv_path=tempPath)

        # Fetches login info
        tempEmail = os.getenv('cocEmail')
        tempPassword = os.getenv('cocPassword')

        # Initializes coc client
        coc_client=coc.Client()
        await coc_client.login(email=tempEmail, password=tempPassword)
        
        # Gets clan info
        clan = await coc_client.get_clan('#2QPUQUR9Y')

        # Creates an empty array of player tags
        playerTags = []
        playerNames = []
        async for player in clan.get_detailed_members():
            playerTags.append(player.tag)
            playerNames.append(player.name)

        allGoldGathered = []
        allElixerGathered = []
        for element in playerTags:
            tempPlayer = await coc_client.get_player(element)
            allAchievements = tempPlayer.achievements
            acheivementValues = next((ach for ach in allAchievements if ach.name == "Gold Grab"), None)
            goldGathered = acheivementValues.value
            allGoldGathered.append(goldGathered)

            acheivementValues = next((ach for ach in allAchievements if ach.name == "Elixir Escapade"), None)
            elixirGathered = acheivementValues.value
            allElixerGathered.append(elixirGathered)
        




        
        

async def setup(bot: commands.Bot):
    await bot.add_cog(recourceTrackerCog(bot))
    await bot.add_cog(loopCog(bot))

# It is reccommended that you use this as a template for your cogs, make sure to change anything that is all caps to make it unique
    