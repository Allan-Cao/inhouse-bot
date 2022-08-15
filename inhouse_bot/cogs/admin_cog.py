import discord
from discord.ext import commands
from inhouse_bot.inhouse import *

class admin_cog(commands.Cog):
    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot
    @commands.has_permissions(administrator=True)

    @discord.slash_command(name = "reset", description = "Resets the queue (removes everyone from the queue)")
    async def reset(self, ctx: discord.ApplicationContext):
        reset_queue()
        await ctx.respond("Queue has been reset")
    
    # @discord.slash_command(name = "populate", description = "Resets the queue (removes everyone from the queue)")
    # async def populate(self, ctx: discord.ApplicationContext):
    #     reset_queue()
    #     await ctx.respond("Queue has been reset")
def setup(bot):
    bot.add_cog(admin_cog(bot))