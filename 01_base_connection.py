import discord
import os
import requests
import json
import random
from dotenv import load_dotenv
# from keep_alive import keep_alive

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client(intents=discord.Intents.all())

# Bot is ready
@client.event
async def on_ready():
    print("{0.user} has connected to Discord!".format(client))

# keep_alive()
#Run the bot
client.run(DISCORD_TOKEN)
