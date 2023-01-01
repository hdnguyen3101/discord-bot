import discord
import os
import requests
import json
import random
from replit import db
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client(intents=discord.Intents.all())

# define sad_words function to check for sad words in a message
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]

# start encouragement function to encourage the user
start_encouragements = ["Cheer up!", "Hang in there.", "You are a great person / bot!"]

# turn on or off responses
if "responding" not in db.keys():
    db["responding"] = True


# define the get_quote function to get a quote from the API
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return quote


# Update encouragements function to add new encouragements
def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


# Delete encouragements function to delete encouragements
def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


# Bot is ready
@client.event
async def on_ready():
    print("{0.user} has connected to Discord!".format(client))


# Bot is listening for messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # Bot is listening for the !quote command
    msg = message.content

    if msg.startswith("!quote"):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        # Option start encouragements
        options = start_encouragements
        if "encouragements" in db.keys():
            options = options + list(db["encouragements"])

        # Bot is listening for sad words and responding with encouragements
        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

    # Bot is listening for the !new command
    if msg.startswith("!new"):
        encouraging_message = msg.split("!new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    # Bot is listening for the !del command
    if msg.startswith("!del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("!del", 1)[1])
            delete_encouragement(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    # Bot is listening for the !list command
    if msg.startswith("!list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    # Bot is listening for the !responding command
    if msg.startswith("!responding"):
        value = msg.split("!responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")

keep_alive()
# Run the bot
client.run(os.getenv("DISCORD_TOKEN"))
