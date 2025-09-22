import discord 
import hashlib
from parse_jobs import parse_jobs

def createEmbedMsg(job):
    embed = discord.Embed(
        title=job["title"],
        url=job["url"],
        description=f"Company: {job['company']}\nLocation: {job['location']}",
        color=discord.Color.blue()
    )
    return embed
