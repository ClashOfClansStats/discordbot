# This example requires the 'message_content' intent.

import discord
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

discord_token = (os.getenv('discordBotToken'))

print(discord_token)