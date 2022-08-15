import asyncio
from typing import Tuple, Optional, List, Set

import discord
from discord.ext.commands import Bot

async def checkmark_validation(
    bot: Bot,
    message: discord.Message,
    validating_players_ids: List[int],
    validation_threshold: int = 10,
    timeout=120,
):

    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def check(received_reaction: discord.Reaction, sending_user: discord.User):
        # This check is simply used to see if a player in the game responded to the message.
        return (
            received_reaction.message.id == message.id
            and sending_user.id in validating_players_ids
            and str(received_reaction.emoji) in ["✅", "❌"]
        )

    ids_of_players_who_validated = set()

    # Default values that will be output in case of success
    result = True
    ids_to_drop = None
    try:
        while len(ids_of_players_who_validated) < validation_threshold:
            reaction, user = await bot.wait_for("reaction_add", timeout=timeout, check=check)

            # A player accepted, we keep him in memory
            if str(reaction.emoji) == "✅":
                ids_of_players_who_validated.add(user.id)

            # A player cancels, we return it and will drop him
            elif str(reaction.emoji) == "❌":
                result, ids_to_drop = False, {user.id}
                break

    # We get there if no player accepted in the last x minutes
    except asyncio.TimeoutError:
        result, ids_to_drop = (
            None,
            set(i for i in validating_players_ids if i not in ids_of_players_who_validated),
        )

    return result, ids_to_drop