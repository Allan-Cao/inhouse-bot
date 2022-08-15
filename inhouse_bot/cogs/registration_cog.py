import discord
from discord.ext import commands
from inhouse_bot.inhouse import *
sql_role_map = {
    "top": "Top",
    "jungle": "Jungle",
    "mid": "Mid",
    "adc": "ADC",
    "support": "Support"
}
class registration_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @discord.slash_command(name = "link", description = "Link your discord with an already registered summoner")
    async def register(self, ctx, ign: str):
        
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

    @discord.slash_command(name = "secondary", description = "Set a secondary role")
    async def secondary(self, ctx, role: str):
        if role.lower() not in ["top","jungle","mid","support","adc"]:
            await ctx.respond("Unknown role entered.")
            return
        discord_id = ctx.user.id
        player_info = lookup_by_id(discord_id)
        player_in_queue = lookup_queue_id(discord_id)
        if player_info == None:
            await ctx.respond(f"Your discord account is not linked to any account. Please register yourself into the system before running this command.")
            return
        else:
            if player_in_queue != None:
                await ctx.respond("You are currently in queue, please leave the queue before making role changes")
                return
            role = sql_role_map[role.lower()]
            if role == player_info[2]:
                await ctx.respond("Your secondary role must be different from your primary role.")
                return
            elif role == player_info[3]:
                await ctx.respond(f"Your secondary role is already {player_info[3]}.")
            elif player_info[3] != None:
                change_secondary_role(role,discord_id)
                await ctx.respond(f"Your secondary role has been changed from {player_info[2]} to {role}")
            else:
                change_secondary_role(role,discord_id)
                await ctx.respond("Secondary role has been changed!")
def setup(bot):
    bot.add_cog(registration_cog(bot))