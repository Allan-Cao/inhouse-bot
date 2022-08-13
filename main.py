import discord
import asyncio
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from pandas import describe_option
load_dotenv() # Loads .env variables
import cassiopeia as cass
from inhouse import *

### Note that all SQL queries will be handled in the inhouse.py file

### Setup Discord Bot
intents = discord.Intents.default()
bot = discord.Bot(debug_guilds=[821109702162907158], intents=intents)# Most functions require intents (will require discord approval at 100 members)

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

@bot.slash_command(name = "search", description = "Lookup user")
async def search(ctx: discord.ApplicationContext, ign: str):
    embed = lookup_by_ign(ign)
    if embed == None:
        await ctx.respond(f"User with the IGN {ign} could not be found")
        return
    await ctx.respond("Ah found them! Here's their information", embed=embed)
@bot.slash_command(name = "stop")
async def stop(ctx):
    stop_sql()
    await ctx.respond("SQL connection stopped")

@bot.slash_command(description="Gets some feedback.")
@discord.option("name", description="Enter your name.")
async def feedback(ctx: discord.ApplicationContext, name: str):
    try:
        await ctx.respond(f"Hey, {name}! Send your feedback within the next 30 seconds please!")

        def is_author(m: discord.Message):
            return m.author.id == ctx.author.id

        feedback_message = await bot.wait_for("message", check=is_author, timeout=30.0) 
        await ctx.send(f"Thanks for the feedback!\nReceived feedback: `{feedback_message.content}`")
    except asyncio.TimeoutError:
        await ctx.send("Timed out, please try again!")

bot.run(os.getenv('SERA_TOKEN'))