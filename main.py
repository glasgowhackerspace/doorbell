# This example requires the 'message_content' intent.

import discord
import dotenv
import os

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    keyholder_mentioned = any([role.name == "keyholder" for role in message.role_mentions])
    if keyholder_mentioned:
        if (name := message.author.nick) is None:
            name = message.author.name
        print('\007', end="") # terminal bell sound
        print(f"detected message mentioning keyholder from: {message.author.name} ({name})")
        await message.channel.send(f"keyholder was mentioned in this message from {name}: [{message.content}]")


client.run(os.getenv("DISCORD_BOT_TOKEN"))
