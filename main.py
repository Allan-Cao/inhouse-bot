import discord
import os
from dotenv import load_dotenv
import sqlite3
load_dotenv() # Loads .env variables
import cassiopeia as cass
from inhouse import *

### Setup SQL (sqlite3 for now but could use something better in the future)
DATABASE_FILE = os.getenv('DB_FILE')
connection = sqlite3.connect(DATABASE_FILE, isolation_level=None)
cursor = connection.cursor()

### Setup Discord Bot
#intents = discord.Intents.default()
bot = discord.Bot(debug_guilds=[821109702162907158])
#bot = discord.Client(intents = intents) # Most functions require intents (will require discord approval at 100 members)
#bot = interactions.Client(BOT_TOKEN)

### Setup Riot API
RIOT_API = os.getenv('RIOT_API')
cass.set_riot_api_key(RIOT_API)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("Managing Inhouse Queues"))

@bot.slash_command(name = "register", description = "Link your discord with already registered summoner")
async def register(ctx):
    await ctx.respond("Hey!")
    #summoner = cass.get_summoner(name="Perkz", region="NA")

# @bot.command(
#     name="link",
#     brief="Links discord account with a solo queue account",
# )
# async def link(ctx, *args):

@bot.command(
    name="lobby",
    brief="Creates lobby",
)
async def lobby(ctx):
    embed = generate_queue()
    await ctx.respond("Hello! Here's a cool embed.", embed=embed) # Send the embed with some text

bot.run(os.getenv('SERA_TOKEN'))