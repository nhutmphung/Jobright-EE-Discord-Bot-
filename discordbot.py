import discord
from discord.ext import commands, tasks
from parse_jobs import parse_jobs
from fetch_jobs import fetch_jobs
from discord_embed import createEmbedMsg
import logging
from dotenv import load_dotenv
import os
import asyncio

#getting specific token from .env 
load_dotenv()
token = os.getenv('DISCORD_TOKEN') 

handler = logging.FileHandler(filename = 'discord.log', encoding = 'utf-8', mode = 'w')

#Bot settup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = '!', intents = intents)

#data setup
raw_data = fetch_jobs()

#process raw data into dicts
jobs = parse_jobs(raw_data)

#turns on the bot 
@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")
    sendHello.start()

@tasks.loop(seconds = 10)
async def sendHello():
    channelID = 1404228130633158676
    channel = bot.get_channel(channelID)

    if channel:
        raw_data = fetch_jobs()
        jobs = parse_jobs(raw_data)
        
        # This will send a message for *every* job listing
        for job in jobs:
            await channel.send(embed=createEmbedMsg(job))

    
bot.run(token)
