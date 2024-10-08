# Discord Imports
import discord
from discord.ext import commands
from discord import app_commands

# For Clash of Clans API
import coc
from coc import utils

# For Secrets
import os
from dotenv import load_dotenv

# for Asynchronous
import asyncio

# For Time
import time
import schedule

# for SQLite
import sqlite3

# Sets up SQLite
SQLiteConnect = sqlite3.connect("Storage.db")
SQLiteCursor = SQLiteConnect.cursor()

# Set Up Schema for SQLite
SQLiteConnect.execute('''
                      CREATE TABLE IF NOT EXISTS PlayerTags (
                      
                      id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      discordID TEXT NOT NULL,
                      
                      PlayerTag TEXT NOT NULL
                      )''')

SQLiteConnect.execute('''
                      CREATE TABLE IF NOT EXISTS ClanTags (

                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      discordID TEXT NOT NULL,
                      ClanTag TEXT NOT NULL
                      )''')

# Close connection to SQLite
SQLiteConnect.close()

# Sets intents for Bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# Loads Secrets
load_dotenv()
discordToken = (os.getenv('discordBotToken'))
cocToken=os.getenv('cocBotToken')
cocEmail = os.getenv('cocEmail')
cocPassword = os.getenv('cocPassword')

# Finds Extensions with other commands
initial_extensions = [
                      'cogs.login_ext',
                      'cogs.recourceTracker_ext'
                      ]

# Coc Client Initilization
async def cocClientInitizalize():
    global cocClient
    cocClient = coc.Client()
    await cocClient.login(email=cocEmail, password=cocPassword)
    print("Clash of Clans client initialized.")

# On Ready
@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')
    try:
        synced = await bot.tree.sync()  # Sync the commands after the bot is ready
        print(f'Commands synced successfully, synced {len(synced)} commands.')
    except Exception as e:
        print(f"Error syncing commands: {e}")

async def main():
    # Load Bot Extensions
    for extension in initial_extensions:
        await bot.load_extension(extension)
    # Initializes the Clash of Clans client
    await cocClientInitizalize()
    # Start the discord bot
    await bot.start(discordToken)

asyncio.run(main())