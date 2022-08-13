import discord
import asyncio
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
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

############################################# User Registration ##########################################################
@bot.slash_command(name = "link", description = "Link your discord with an already registered summoner")
async def register(ctx, ign: str):
    discord_id = ctx.user.id
    user_register = lookup_by_discord_id(discord_id)
    if user_register != None:
        await ctx.respond(f"Your discord account is already connected to the IGN {user_register[0]}. If this is an error, please contact a moderator.") # NEEDS TO TEST
        return
    else:
        player_lookup = lookup_by_ign(ign)
        if player_lookup == None:
            await ctx.respond(f"The IGN {ign} is not in the system yet. Please contact a moderator if you think this is an error.")
        else:
            update_discord_id(discord_id, ign)
            await ctx.respond(f"Your discord account has been linked to the IGN {ign}")
################################################# Queue System ##############################################################
@bot.slash_command(name = "queue", description = "Joins the queue")
async def queue(ctx, role: discord.selectMenu(options=["Top","Jungle","Mid","ADC","Support","Fill"])):
    await ctx.respond(role)

@bot.slash_command(name = "search", description = "Lookup user")
async def search(ctx: discord.ApplicationContext, ign: str):
    player_info = lookup_by_ign(ign)
    if player_info == None:
        await ctx.respond(f"User with the IGN {ign} could not be found")
        return
    else:
        embed = format_playercard_embed(player_info)
        await ctx.respond(embed=embed)

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

############################## ADMIN COMMANDS ############################## 

bot.run(os.getenv('SERA_TOKEN'))