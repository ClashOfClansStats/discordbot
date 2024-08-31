# For Discord
import discord
from discord.ext import commands

# For Clash of Clans API
import coc
from coc import utils
# For Secrets and API Keys
import os
from dotenv import load_dotenv
from pathlib import Path

# For SQLite
import sqlite3

# For Time
import time
import schedule

# For Asyncio
import asyncio

# SQLite Conection and Curson Creation
SQLiteConnect = sqlite3.connect("test.db")
SQLiteCursor = SQLiteConnect.cursor()

# Execute commands with cursor, create a schema
SQLiteCursor.execute("CREATE TABLE IF NOT EXISTS tags(discordID, playerTag)")
SQLiteCursor.execute("CREATE TABLE IF NOT EXISTS farmed(discordID, playerTag, gold, elixer, time)")

# Time Converter
def timeConvert(time):
    days = time // 86400
    hours = (time % 86400) // 3600
    minutes = (time % 3600) // 60
    seconds = time % 60

    return [int(days), int(hours), int(minutes), seconds]

# Loads Secrets and API Keys
load_dotenv()

# Discord Bot
discord_token = (os.getenv('discordBotToken'))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

cocBotToken=os.getenv('cocBotToken')
cocEmail = os.getenv('cocEmail')
cocPassword = os.getenv('cocPassword')

async def init_coc_client():
    """
    Initializes the Clash of Clans client asynchronously using the token.
    """
    global coc_client
    coc_client = coc.Client()
    await coc_client.login(email=cocEmail, password=cocPassword)
    print("Clash of Clans client initialized.")

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name='clashlogin')
async def clashlogin(interaction: discord.Interaction, playertag: str):
    tempTag = playertag
    if not utils.is_valid_tag(tempTag):
        await interaction.response.send_message(f"Please supply a proper tag", ephemeral=True)
        return
    else:
        # Checks if user already has an account
        SQLiteCursor.execute(f"SELECT 1 FROM tags WHERE playerTag = ?", (tempTag,))
        result = SQLiteCursor.fetchone()

        if result:
            await interaction.response.send_message(f"playerTag Already Exists for the tag {tempTag}", ephemeral=True)
        else:
            SQLiteCursor.execute("INSERT INTO tags (discordID, playerTag) VALUES (?, ?)" , (interaction.user.id, tempTag))
            SQLiteConnect.commit()
            await interaction.response.send_message(f"You have logged in under the tag {tempTag}", ephemeral=True)

@bot.tree.command(name='clashfarmed')
async def clashfarmed(interaction: discord.Interaction):
    SQLiteCursor.execute(f"SELECT playerTag FROM tags WHERE discordID = ?", (interaction.user.id,))
    result = SQLiteCursor.fetchone()
    tempTag = result[0]

    print (f"The result of the query is {tempTag}")
    if result:
         player = await coc_client.get_player(player_tag=tempTag)
         print(f'Gathering info for: {player}')

         player = await coc_client.get_player(player_tag=tempTag)
         print(f'Gathering info for: {player}')

         # Gets the player's total gold farmed
         achievement_name = "Gold Grab"
         achievements = player.achievements
         # Sorts all the acheivements for Gold Grab
         achievements = next((ach for ach in achievements if ach.name == achievement_name), None)
         # sets the acheivement to the value (gold farmed)
         achievements = achievements.value
         print(f'You have farmed {achievements} Gold!')

         # Gets the player's total elixer farmed
         achievement_name = "Elixir Escapade"
         achievements = player.achievements
         # Sorts all the acheivements for Elixir Escapade
         achievements = next((ach for ach in achievements if ach.name == achievement_name), None)
         # sets the acheivement to the value (elixir farmed)
         achievements = achievements.value
         print(f'You have farmed {achievements} Elixer!')
    else:
         await interaction.response.send_message(f"You must first login with /clashlogin before you can use this commands", ephemeral=True)

@bot.tree.command(name='clashrecentlyfarmed')
async def recentlyfarmed(interaction: discord.Interaction):
    SQLiteCursor.execute(f"SELECT playerTag FROM tags WHERE discordID = ?", (interaction.user.id,))
    result = SQLiteCursor.fetchone()
    tempTag = result[0]
    if result:
        player = await coc_client.get_player(player_tag=tempTag)
        print(f'Gathering info for: {player}')

        # Gets the player's total gold farmed
        achievement_name = "Gold Grab"
        achievements = player.achievements
        # Sorts all the acheivements for Gold Grab
        achievements = next((ach for ach in achievements if ach.name == achievement_name), None)
        # sets the acheivement to the value (gold farmed)
        achievements = achievements.value
        # Stores the current gold farmed to a variable
        currentGold=achievements

        # Gets the player's total elixer farmed
        achievement_name = "Elixir Escapade"
        achievements = player.achievements
        # Sorts all the acheivements for Elixir Escapade
        achievements = next((ach for ach in achievements if ach.name == achievement_name), None)
        # sets the acheivement to the value (elixir farmed)
        achievements = achievements.value
        # Stores the current elixer farmed to a variable
        currentElixer=achievements

        currentTime=time.time()
        print (f"The current time is {currentTime}")
        print (f"The current gold for {player} is {currentGold}")
        print (f"The current elixer for {player} is {currentElixer}")
        convertedTime = timeConvert(currentTime)
        print (convertedTime[0], "days,", convertedTime[1], "hours,", convertedTime[2], "minutes, and", int (convertedTime[3]), "seconds")
        print ("Sending message to Discord")
        await interaction.response.send_message(f"{player} has farmed **{currentGold}** gold and **{currentElixer}** elixir in the last {convertedTime[0]} days, {convertedTime[1]} hours, {convertedTime[2]} minutes, and {int(convertedTime[3])} seconds")
        

    else:
        await interaction.response.send_message(f"You must first login with /clashlogin before you can use this commands", ephemeral=True)

async def main():
    # Initialize the Clash of Clans client
    await init_coc_client()
    # Run the Discord bot
    await bot.start(discord_token)

asyncio.run(main())