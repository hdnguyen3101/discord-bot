import discord
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.all())

#define the get_quote function to get a quote from the API
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

#Bot is ready
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

#Bot is listening for messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!quote'):
        quote = get_quote()
        await message.channel.send(quote)

#Run the bot
client.run(os.getenv('DISCORD_TOKEN'))