# For Discord
import typing
from typing import Literal
import discord
from discord.ext import commands
from discord import app_commands

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

# For functions
import funcs

# SQLite Conection and Curson Creation
SQLiteConnect = sqlite3.connect("test.db")
SQLiteCursor = SQLiteConnect.cursor()

# Execute commands with cursor, create a schema
SQLiteCursor.execute("CREATE TABLE IF NOT EXISTS tags(discordID, playerTag)")
SQLiteCursor.execute("CREATE TABLE IF NOT EXISTS farmed(discordID, playerTag, goldFarmed, elixerFarmed, time)")

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
    # Initializes the Clash of Clans client asynchronously using the token.
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

@bot.tree.command(name='clashnewuser')
async def clashaddbase(interaction: discord.Interaction, playertag: str):
    tempTag = playertag
    if not utils.is_valid_tag(tempTag):
        await interaction.response.send_message(f"Please supply a proper tag", ephemeral=True)
        return
    else:
        # Checks if user already has an account
        SQLiteCursor.execute(f"SELECT 1 FROM tags WHERE playerTag = ?", (tempTag,))
        result = SQLiteCursor.fetchone()

        if result:
            await interaction.response.send_message(f"playerTag Already Exists for the tag **{tempTag}**", ephemeral=True)
        else:
            SQLiteCursor.execute("INSERT INTO tags (discordID, playerTag) VALUES (?, ?)" , (interaction.user.id, tempTag))
            SQLiteConnect.commit()
            await interaction.response.send_message(f"You have logged in under the tag {tempTag}", ephemeral=True)

@bot.tree.command(name='clashnewclan')
async def clashaddclan(interaction: discord.Interaction, clantag: str):
    tempTag = clantag
    if not utils.is_valid_tag(tempTag):
        await interaction.response.send_message(f"Please supply a proper tag", ephemeral=True)
        return
    else:
        # 
        print()

# Test Command for autofill
@bot.tree.command(name='testcommand')
async def testcommand(interaction: discord.Interaction, clantag: str):
    tempTag = clantag
    print(f'The user has selected {tempTag} as their clantag.')
    if not utils.is_valid_tag(tempTag):
        await interaction.response.send_message(f"Please supply a proper tag", ephemeral=True)
        return
    else:
        
        await interaction.response.send_message(f"You are using {playerClanTag}: {playerClan} as your selected clan!", ephemeral=True)
# Autocomplete for option "clantag"
@testcommand.autocomplete('clantag')
async def clantag_autocomplete(interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
    data = []
    testvar = ['opt1', 'opt2', 'opt3']
    print(testvar)
    for tag_choice in testvar:
        data.append(app_commands.Choice(name=tag_choice, value=tag_choice))
    return data
         
@bot.tree.command(name='clashfarmed')
async def clashfarmed(interaction: discord.Interaction):
    SQLiteCursor.execute(f"SELECT playerTag FROM tags WHERE discordID = ?", (interaction.user.id,))
    result = SQLiteCursor.fetchone()
    tempTag = result[0]
    print (f"The result of the query is {tempTag}")

    if result:
         player = await coc_client.get_player(player_tag=tempTag)
         print(f'Gathering info for: {player}')

         totalgathered = funcs.recourcesGathered(player=player, allAchievements=player.achievements)
    
         await interaction.response.send_message(f"You have gathered a total of **{format(totalgathered[0],',d')}** Gold, and **{format(totalgathered[1],',d')}** Elixer!")

    else:
         await interaction.response.send_message(f"You must first login with /clashlogin before you can use this commands", ephemeral=True)

@bot.tree.command(name='clashdailyfarmed')
async def dailyfarmed(interaction: discord.Interaction):
    SQLiteCursor.execute(f"SELECT playerTag FROM tags WHERE discordID = ?", (interaction.user.id,))
    result = SQLiteCursor.fetchone()
    tempTag = result[0]
    if result:
        player = await coc_client.get_player(player_tag=tempTag)
        print(f'Gathering info for: {player}')

        totalgathered = funcs.recourcesGathered(player=player, allAchievements=player.achievements)

        print(f'totalgathered: Gold: {totalgathered[0]} | Elixer: {totalgathered[1]}')

        currentTime=time.time()

        # Prints results to console
        print (f"The current time is {currentTime}")
        print (f"The current gold for {player} is {totalgathered[0]}")
        print (f"The current elixer for {player} is {totalgathered[1]}")

        convertedTime = funcs.timeConvert(currentTime)
        print ("Convertedtime:", convertedTime[0], "days,", convertedTime[1], "hours,", convertedTime[2], "minutes, and", int (convertedTime[3]), "seconds")
        print ("Sending message to Discord")
        await interaction.response.send_message(f"{player} has farmed **{totalgathered[0]}** gold and **{totalgathered[1]}** elixir in the last {convertedTime[0]} days, {convertedTime[1]} hours, {convertedTime[2]} minutes, and {int(convertedTime[3])} seconds")
        

    else:
        await interaction.response.send_message(f"You must first login with /clashlogin before you can use this commands", ephemeral=True)

# Daily task to run
async def daily_task():
    # Logic for daily task here
    print("Daily task running...")

    
# Schedules daily_task to run at midnight
def schedule_daily_task():
    schedule.every().day.at("00:00").do(lambda: asyncio.create_task(daily_task()))

# Checks scheduler every second
async def run_scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

async def main():
    # Schedule the daily task
    schedule_daily_task()
    # Run the scheduler in the background
    asyncio.create_task(run_scheduler())
    # Initialize the Clash of Clans client
    await init_coc_client()
    # Run the Discord bot
    await bot.start(discord_token)

asyncio.run(main())