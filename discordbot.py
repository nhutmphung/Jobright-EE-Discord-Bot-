import discord
from discord.ext import commandsimport
import logging
from dotenv import load_dotenv
import os

#getting specific token from .env 
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename = 'discord.log', encodings = 'utf-8', mode = 'w')

#Bot settup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefit = '!', intents = intents)

#idfk what this does lol
@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

bot.run(token, log_handlers = handler, log_levels = logging.DEBUG)
