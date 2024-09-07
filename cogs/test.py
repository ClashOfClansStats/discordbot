import discord
from discord.ext import tasks, commands
from discord import app_commands

import sqlite3
import coc
from coc import utils

import os
from dotenv import load_dotenv

from table2ascii import table2ascii as t2a, PresetStyle

import asyncio

async def dailyTask():
    print("Starting daily task...")
    # Gets the parent direcotry
    currentDir = os.path.dirname(__file__)
    tempPath = os.path.split(currentDir)[0]
    print(currentDir)
    print(tempPath)
    # Load .env file
    load_dotenv(dotenv_path=f'{tempPath}/.env')

    # Fetches login info
    tempEmail = os.getenv('cocEmail')
    tempPassword = os.getenv('cocPassword')
    print(tempEmail, tempPassword)

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
        
    tableData = list(zip(playerNames, allGoldGathered, allElixerGathered))

    finalOutput = (t2a(
        header=['Player Name', 'Gold Gathered', 'Elixer Gathered'],
        body=tableData,
        style=PresetStyle.ascii_borderless
    ))

    print (finalOutput)




asyncio.run(dailyTask())