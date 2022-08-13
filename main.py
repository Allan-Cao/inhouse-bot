import discord
import os
from dotenv import load_dotenv
import sqlite3
load_dotenv() # Loads .env variables

### Setup SQL (sqlite3 for now but could use something better in the future)
DATABASE_FILE = os.environ.get('DB_FILE')
connection = sqlite3.connect(DATABASE_FILE, isolation_level=None)
cursor = connection.cursor()

### Setup Discord Bot
intents = discord.Intents.default()
BOT_TOKEN = os.environ.get('SERA_TOKEN')
bot = discord.Client(intents = intents) # Most functions require intents (will require discord approval at 100 members)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("Inhouse Queue"))

@bot.event
async def on_message(message):
    await bot.process_commands(message)

bot.run(BOT_TOKEN)