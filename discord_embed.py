import discord 
from parse_jobs import parse_jobs

def create_embed_msg(job):
    embed = discord.Embed(
        title = job['title'],
        company = job['company'],
        location = job['location'],
        url = job['url']
    )
    return create_embed_msg