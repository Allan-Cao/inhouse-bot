import discord
from discord.ext import commands
from inhouse_bot.db_system.db_helper import reset_queue, lookup_by_ign, lookup_by_id, add_user
from inhouse_bot.utils.formatter import sql_role_map, secondary_roles_lowercase, all_roles_lowercase
from discord.commands import Option

class admin_cog(commands.Cog):
    def __init__(
        self, bot
    ):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @discord.slash_command(
        name="reset", description="Resets the queue (removes everyone from the queue)"
    )
    async def reset(self, ctx: discord.ApplicationContext):
        reset_queue()
        await ctx.respond("Queue has been reset")

    @discord.slash_command(
        name="add", description="Adds a new player into the system!"
    )
    async def add(
        self, ctx, ign: str, primary_role: str, elo: float,  secondary_role: Option(str, "Optional Secondary Role", required = False, default=""),   discord_id: Option(str, "Discord account id", required = False, default="0")):
        ### Check Inputs ##
        print(discord_id)
        
        if discord_id == "0":
            discord_id = 0
        else:
            try:
                discord_id = int(discord_id)
            except:
                await ctx.respond("Unknown Discord ID receieved")
                return
            if lookup_by_id(discord_id) != None:
                await ctx.respond("That discord user is already registered!")
                return
        if lookup_by_ign(ign) != None:
            await ctx.respond("That IGN has already been registered")
            return
        if secondary_role == "":
            if (primary_role.lower() not in all_roles_lowercase):
                await ctx.respond("Unknown primary role receieved.")
                return
        else:
            if (primary_role.lower() not in all_roles_lowercase) or (secondary_role.lower() not in secondary_roles_lowercase):
                await ctx.respond("Unknown role received")
                return
        primary_role = sql_role_map[primary_role.lower()]
        secondary_role = sql_role_map[secondary_role.lower()]
        user_information = (ign, discord_id, primary_role, secondary_role, elo, 0)
        add_user(user_information)
        await ctx.respond(f"User with ign {ign} has been added!")

    # @discord.slash_command(name = "populate", description = "Resets the queue (removes everyone from the queue)")
    # async def populate(self, ctx: discord.ApplicationContext):
    #     reset_queue()
    #     await ctx.respond("Queue has been reset")


def setup(bot):
    bot.add_cog(admin_cog(bot))
