import discord
from discord.ext import commands
from inhouse_bot.inhouse import *
from db_system.db_helper import *
from utils.formatter import ping_user_by_id

class queue_cog(commands.Cog):
    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot
    def generate_queue_embed():
        if queue_is_open() == False:
            embed = discord.Embed(
                title=f"Amateur Inhouse Queue is currently CLOSED. It will reopen at 9 am EST.",
                color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
            )
            return embed
        with connection.cursor() as cursor:
            cursor.execute(queue_row_count_query)
            player_count = cursor.fetchone()[0]
        embed = discord.Embed(
            title=f"{player_count} player(s) currently in queue",
            description=f"Queue as of {format_time()}",
            color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
        )
        for role in ["Top","Jungle","Mid","ADC","Support","Fill"]:
            with connection.cursor() as cursor:
                cursor.execute(get_role_queue_query, (role, role,))
                myresult = cursor.fetchall()
            player_list = ""
            for player in myresult:
                ign, player_id, primary, secondary, elo, created_at = player
                if primary == role:
                    player_list += (ping_user_by_id(player_id, ign) + ",")
                elif secondary == role:
                    player_list += (ping_user_by_id(player_id, ign) + ",")
                else:
                    raise ValueError
            if player_list == "":
                player_list = f"Nobody is queued for {role}"
            embed.add_field(name=role, value=f"{player_list}", inline=False)
        embed.set_footer(text="Queue information generated by Seraphine Bot") # footers can have icons too
        #embed.set_author(name="Pycord Team", icon_url="https://example.com/link-to-my-image.png")
        #embed.set_thumbnail(url="https://example.com/link-to-my-thumbnail.png")
        #embed.set_image(url="https://example.com/link-to-my-banner.png")
        return embed

    @discord.slash_command(name = "info", description = "Current Queue")
    async def info(self, ctx: discord.ApplicationContext):
        embed = self.generate_queue_embed()
        await ctx.respond(embed=embed)
    @discord.slash_command(name = "join", description = "Joins the queue")
    async def join(self, ctx):
        discord_id = ctx.user.id
        user_register = lookup_by_id(discord_id)
        if user_register == None:
            await ctx.respond("Your discord account is not connected to any player information. Please register.")
            return
        player_info = lookup_queue_id(discord_id)
        if player_info != None:
            await ctx.respond("You are currently in queue")
            return
        else:
            join_queue_id(discord_id)
            await ctx.respond("You have been added to the queue!")
            if check_lobby_made(ctx):
                print("Lobby found?")

    @discord.slash_command(name = "leave", description = "Leaves the queue")
    async def leave(self, ctx):
        discord_id = ctx.user.id
        remove_from_queue_id(discord_id)
        await ctx.respond("You have been removed from the queue.")
def setup(bot):
    bot.add_cog(queue_cog(bot))