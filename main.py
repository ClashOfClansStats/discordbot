# For Discord
import discord
from discord.ext import commands

# For Clash of Clans API
import coc

# For Secrets and API Keys
import os
from dotenv import load_dotenv
from pathlib import Path

# For SQLite
import sqlite3

# SQLite Conection and Curson Creation
SQLiteConnect = sqlite3.connect("test.db")
SQLiteCursor = SQLiteConnect.cursor()

# Execute commands with cursor, This creates a table called "tags"
SQLiteCursor.execute("""CREATE TABLE IF NOT EXISTS tags(discordID, playerTag)""")

# Test code to create a table if it doesn't exist and check if a playerTag already existsm if not insert it
'''
discordIDVar = "213213"
playerTagVar = "AG2134"

SQLiteCursor.execute("SELECT 1 FROM tags WHERE playerTag = ?", (playerTagVar,))
result = SQLiteCursor.fetchone()

if result:
    print ("playerTag Already Exists under the value " + playerTagVar)
else:
    SQLiteCursor.execute("INSERT INTO tags (discordID, playerTag) VALUES (?, ?)" , (discordIDVar, playerTagVar))

SQLiteConnect.commit()
'''

# Loads Secrets and API Keys
load_dotenv()

# Discord Bot
discord_token = (os.getenv('discordBotToken'))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command(name='test')
async def test(ctx, arg):
    pass


bot.run(discord_token)