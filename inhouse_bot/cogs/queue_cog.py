import discord
from discord.ext import commands
from inhouse_bot.db_system.db_helper import *
from inhouse_bot.utils.formatter import ping_user_by_id, format_time
from inhouse_bot.queue_system.queue_utils import queue_is_open
from inhouse_bot.queue_system.game_queue import GameQueue
from inhouse_bot.utils.validation_dialog import checkmark_validation
from inhouse_bot.queue_system.queue_handler import *
class queue_cog(commands.Cog):
    def __init__(
        self, bot
    ):
        self.bot = bot
    async def matchmaking_logic(self, ctx):
        queue = GameQueue()
        if len(queue.queue_players) == 10:
            embed = queue.get_embed()
            player_ping = queue.ping_queue()
            ready_check_message = await ctx.send(content=player_ping, embed=embed, delete_after=60 * 15)
            
            try:
                ready, players_to_drop = await checkmark_validation(
                    bot=self.bot,
                    message=ready_check_message,
                    validating_players_ids=queue.player_ids_list,
                    validation_threshold=10,
                )

            # We catch every error here to make sure it does not become blocking
            except Exception as e:
                self.bot.logger.error(e)
                cancel_ready_check(ids_to_drop=queue.player_ids_list)
                await ctx.send(
                    "There was a bug with the ready-check message, all players have been dropped from queue\n"
                    "Please queue again to restart the process"
                )

                return
            if ready is True:
                # We drop all 10 players from the queue 
                #validation doesn't seem to do anything (?)
                #game_queue.validate_ready_check(ready_check_message.id)

                # We commit the game to the database (without a winner)
                #game = session.merge(game)  # This gets us the game ID

                #await ctx.send(embed=game.get_embed("GAME_ACCEPTED"),)
                await ctx.send("GAME ACCEPTED (TEST)")
                # We create voice channels for each team in this game
                #await create_voice_channels(ctx, game)

            elif ready is False:
                # We remove the player who cancelled
                cancel_ready_check(ids_to_drop=players_to_drop)

                await ctx.send(
                    f"A player cancelled the game and was removed from the queue\n"
                    f"All other players have been put back in the queue",
                )

                # We restart the matchmaking logic
                # (this might cause infinite loop no?)
                await self.run_matchmaking_logic(ctx)

            elif ready is None:
                # We remove the timed out players from *all* channels (hence giving server id)
                cancel_ready_check(
                    ready_check_id=ready_check_message.id,
                    ids_to_drop=players_to_drop,
                )

                await ctx.send(
                    "The check timed out and players who did not answer have been dropped from all queues",
                )

                # We restart the matchmaking logic
                await self.run_matchmaking_logic(ctx)

    def lobby_found(self):
        ...
    def generate_queue_closed(self):
        embed = discord.Embed(
            title=f"Amateur Inhouse Queue is currently CLOSED. It will reopen at 9 am EST.",
            color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
        )
        return embed
    def generate_queue_embed(self):
        with connection.cursor() as cursor:
            cursor.execute(queue_row_count_query)
            player_count = cursor.fetchone()[0]
        embed = discord.Embed(
            title=f"{player_count} player(s) currently in queue",
            description=f"Queue as of {format_time()}",
            color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
        )
        for role in ["Top", "Jungle", "Mid", "ADC", "Support", "Fill"]:
            with connection.cursor() as cursor:
                cursor.execute(
                    get_role_queue_query,
                    (
                        role,
                        role,
                    ),
                )
                myresult = cursor.fetchall()
            player_list = ""
            for player in myresult:
                ign, player_id, primary, secondary, elo, in_ready_check, ready_check, created_at, ready_check_id = player
                if primary == role:
                    player_list += ping_user_by_id(player_id, ign) + ","
                elif secondary == role:
                    player_list += ping_user_by_id(player_id, ign) + ","
                else:
                    raise ValueError
            if player_list == "":
                player_list = f"Nobody is queued for {role}"
            embed.add_field(name=role, value=f"{player_list}", inline=False)
        embed.set_footer(
            text="Queue information generated by Seraphine Bot"
        )  # footers can have icons too
        # embed.set_author(name="Pycord Team", icon_url="https://example.com/link-to-my-image.png")
        # embed.set_thumbnail(url="https://example.com/link-to-my-thumbnail.png")
        # embed.set_image(url="https://example.com/link-to-my-banner.png")
        return embed

    @discord.slash_command(name="info", description="Current Queue")
    async def info(self, ctx: discord.ApplicationContext):
        embed = self.generate_queue_embed()
        await ctx.respond(embed=embed)

    @discord.slash_command(name="join", description="Joins the queue")
    async def join(self, ctx):
        if queue_is_open == False:
            await ctx.respond(embed = self.generate_queue_closed())
            return
        discord_id = ctx.user.id
        user_register = lookup_by_id(discord_id)
        if user_register == None:
            await ctx.respond(
                "Your discord account is not connected to any player information. Please register."
            )
            return
        player_info = lookup_queue_id(discord_id)
        if player_info != None:
            await ctx.respond("You are currently in queue")
            return
        else:
            join_queue_id(discord_id)
            await ctx.respond("You have been added to the queue!")
            await self.matchmaking_logic(ctx)

    @discord.slash_command(name="leave", description="Leaves the queue")
    async def leave(self, ctx):
        discord_id = ctx.user.id
        remove_from_queue_id(discord_id)
        await ctx.respond("You have been removed from the queue.")

def setup(bot):
    bot.add_cog(queue_cog(bot))
