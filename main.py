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

### Set Global Variables
# top = discord.SelectOption(label="Top", value="Top")
# jungle = discord.SelectOption(label="Jungle", value="Jungle")
# mid = discord.SelectOption(label="Mid", value="Mid")
# adc = discord.SelectOption(label="ADC", value="ADC")
# support = discord.SelectOption(label="Support",value="Support")
# role_select = discord.SelectMenu(1,1,[top,jungle,mid,adc,support])
global_roles = ["top","jungle","mid","support","adc"]

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("Managing Inhouse Queues"))

############################################# User Registration ##########################################################
registration = bot.create_group("register", "Inhouse queue system")

@registration.command(name = "link", description = "Link your discord with an already registered summoner")
async def register(ctx, ign: str):
    discord_id = ctx.user.id
    user_register = lookup_by_id(discord_id)
    if user_register != None:
        await ctx.respond(f"Your discord account is already connected to the IGN {user_register[0]}. If this is an error, please contact a moderator.")
        return
    else:
        player_lookup = lookup_by_ign(ign)
        if player_lookup == None:
            await ctx.respond(f"The IGN {ign} is not in the system yet. Please contact a moderator if you think this is an error.")
        else:
            update_discord_id(discord_id, ign)
            await ctx.respond(f"Your discord account has been linked to the IGN {ign}")

class MyView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content="Timed-out editing secondary role.", view=self)
    @discord.ui.button(label="Confirm", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, secondary, interaction):
        await interaction.response.send_message("You pressed me!")

    @discord.ui.button(label="Cancel", row=1, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, secondary, interaction):
        await interaction.response.send_message("Canceled")

@registration.command(name = "secondary", description = "Set a secondary role")
async def secondary(ctx, role: str):
    if role.lower() not in global_roles:
        await ctx.respond("Unknown role entered.")
        return
    discord_id = ctx.user.id
    player_info = lookup_by_id(discord_id)
    if player_info == None:
        await ctx.respond(f"Your discord account is not linked to any account. Please register yourself into the system before running this command.")
        return
    else:
        role = role.capitalize()
        if role == player_info[2]:
            await ctx.respond("Your secondary role must be different from your primary role.")
            return
        elif role == player_info[3]:
            await ctx.respond(f"Your secondary role is already {player_info[3]}.")
        elif player_info[3] != None:
            await ctx.respond(f"Confirm that you want to switch your secondary role from {player_info[2]} to {role}", view=MyView(timeout=30))
        else:
            change_secondary_role(role,discord_id)
            await ctx.respond("Secondary role has been changed!")
            
################################################# Queue System ##############################################################
queue_system = bot.create_group("queue", "Inhouse queue system")

@queue_system.command(name = "join", description = "Joins the queue")
async def join(ctx):
  await ctx.respond(f"Hello, {ctx.author}!")

@queue_system.command(name = "leave", description = "Leaves the queue")
async def leave(ctx):
  await ctx.respond(f"Bye, {ctx.author}!")
  await ctx.respond("You have left the queue!")

@bot.slash_command(name = "profile", description = "Your profile")
async def profile(ctx: discord.ApplicationContext):
    player_info = lookup_by_id(ctx.author.id)
    if player_info == None:
        await ctx.respond(f"Your user profile could not be found. Are you sure you are registered?")
        return
    else:
        embed = format_playercard_embed(player_info)
        await ctx.respond(embed=embed)

@bot.slash_command(name = "search", description = "Lookup user")
async def search(ctx: discord.ApplicationContext, ign: str):
    player_info = lookup_by_ign(ign)
    if player_info == None:
        await ctx.respond(f"User with the IGN {ign} could not be found")
        return
    else:
        embed = format_playercard_embed(player_info)
        await ctx.respond(embed=embed)

############################## ADMIN COMMANDS ############################## 

bot.run(os.getenv('SERA_TOKEN'))