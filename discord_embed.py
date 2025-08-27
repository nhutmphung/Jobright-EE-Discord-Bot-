import discord 
from filter_jobs import filter_jobs

def create_embed_msg(job):
    embed = discord.Embed(
        title = job['title'],
        company = job['company'],
        location = job['location'],
        url = job['url']
    )
    return create_embed_msg