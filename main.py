import discord
import os
from dotenv import load_dotenv
import sqlite3

connection = sqlite3.connect("userbase.db", isolation_level=None)
cursor = connection.cursor()

load_dotenv()
BOT_TOKEN = os.environ.get('SERA_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

client.run(BOT_TOKEN)