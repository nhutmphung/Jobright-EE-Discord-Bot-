import discord
from discord.ext import commands, tasks

import parse_jobs

from fetch_jobs import fetch_jobs
from discord_embed import createEmbedMsg
import logging
from dotenv import load_dotenv
import os
import asyncio
import json

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
jobs = parse_jobs.parse_jobs(raw_data)

filename = "posted_jobs.json"



#turns on the bot 
@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")
    sendJob.start()

@tasks.loop(seconds = 20)
async def sendJob():
    channelID = 1404228130633158676
    channel = bot.get_channel(channelID)

    if channel:

        for job in jobs:
            hashed_jobs = parse_jobs.job_id(job)
            parse_jobs.posted_jobs(hashed_jobs)
            await channel.send(embed=createEmbedMsg(job))

        
        # This will send a message for *every* job listing
bot.run(token)
