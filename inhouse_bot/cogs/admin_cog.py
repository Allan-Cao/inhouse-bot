import discord
from discord.ext import commands
from inhouse_bot.db_system.db_helper import reset_queue, lookup_by_ign, lookup_by_id, add_user
from inhouse_bot.utils.formatter import sql_role_map, secondary_roles_lowercase, all_roles_lowercase
from discord.commands import Option

class admin_cog(commands.Cog):
    # Setup admin_cog which can only be used by admininstrators
    def __init__(self, bot):
        self.bot = bot
    # Commands can only be used by admins
    @commands.has_permissions(administrator=True)
    @discord.slash_command(
        name="reset", description="Resets the queue (removes everyone from the queue)"
    )
    async def reset(self, ctx: discord.ApplicationContext):
        reset_queue()
        await ctx.respond("Queue has been reset")

    @discord.slash_command(
        name="add", description="Adds a new player into the database system!"
    )
    async def add(
        self, ctx, ign: str, primary_role: str, elo: float,  secondary_role: Option(str, "Optional Secondary Role", required = False, default=""),   discord_id: Option(str, "Discord account id", required = False, default="0")):
        # Checks if the user is already in the system
        if discord_id == "0":
            discord_id = 0
        else:
            try:
                # convert discord_id to int
                discord_id = int(discord_id)
            except:
                await ctx.respond("Discord account id must be a number")
                return
            if lookup_by_id(discord_id) != None:
                await ctx.respond("User is already in the system")
                return
        if lookup_by_ign(ign) != None:
            await ctx.respond("User is already in the system")
            return
        # Check if secondary_role is valid
        if secondary_role != "":
            if secondary_role.lower() not in secondary_roles_lowercase:
                await ctx.respond("Secondary role is not valid")
                return
        # Check if primary_role is valid
        if primary_role.lower() not in all_roles_lowercase:
            await ctx.respond("Primary role is not valid")
            return
        primary_role = sql_role_map[primary_role.lower()]
        secondary_role = sql_role_map[secondary_role.lower()]
        # format user_information into a tuple
        user_information = (ign, discord_id, primary_role, secondary_role, elo, 0)
        # Add user to the database    
        add_user(user_information)
        await ctx.respond(f"User with ign {ign} has been added!")
    # Discord command to reset queue with the reset_queue command
    @commands.has_permissions(administrator=True)
    @discord.slash_command(
        name="reset", description="Resets the queue (removes everyone from the queue)"
    )
    async def reset(self, ctx: discord.ApplicationContext):
        reset_queue()
        await ctx.respond("Queue has been reset")

def setup(bot):
    bot.add_cog(admin_cog(bot))
