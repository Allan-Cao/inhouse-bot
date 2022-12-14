from email.policy import default
from inhouse_bot.db_system.db_helper import get_current_queue
from collections import defaultdict
from inhouse_bot.utils.formatter import secondary_roles, ping_user_by_id
from typing import Dict, List
import discord 
import time

class GameQueue():
    def __init__(self):
        """
            Class to represent the current queue. game_id is the id of the lobby that can be created. If game_id is None, there is no lobby to create.
            Checks to see if there are enough players to make a lobby. If there are, it creates a lobby and sets the game_id. If there are not, it sets the game_id to None
            There is a list of players in the lobby. Each player is a tuple with the following format: (ign, discord_id, primary_role, secondary_role, elo, in_ready_check, ready_check, queue_join_time, ready_check_id)
            The ready_check_id is the id of the ready check that the player is in. If the player is not in a ready check, the ready_check_id is None.
            The ready_check_id is used to add the player to the ready check when they leave the queue.
            A lobby is created when there are enough players in the queue to make a lobby.
            There are enough players to make a lobby if there are 2 players in each role.
            A player can have multiple roles but only be in lobby once.
        """
        queue_data = get_current_queue()
        self.game_id = None
        self.queue_players = defaultdict(list)
        self.lobby_players = defaultdict(list)
        for player in queue_data:
            self.queue_players[player[2]].append(player)
        if len(queue_data) < 10:
            self.game_id = None
        else:
            self.check_lobby()
    def check_lobby(self):
        for role in secondary_roles:
            if len(self.queue_players[role]) < 2: # If there are less than 2 people in a given role, can't make a lobby
                self.lobby_players = []
                self.game_id = None
                break
            else:
                for qp in self.queue_players[role]:
                    if len(self.lobby_players[role]) < 2:
                        self.lobby_players[role].append(qp)
        self.game_id = int(time.time())

    def make_queue_embed(self):
        embed = discord.Embed(
            title=f"???????????? Queue Found! ????????????",
            description=f"Game ID: {self.game_id}",
            color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
        )
        for role in secondary_roles:
            text = ""
            for qp in self.lobby_players[role]:
                text += ping_user_by_id(qp[1], qp[0])
            embed.add_field(name=role, value=f"Players: {text}", inline=False)
        embed.set_footer(text="Queue generated by Seraphine Bot") 
        return embed
    @property
    def lobby_players_dict(self) -> Dict[str, List]:
        return {role: [player for player in self.lobby_players if player[2] == role] for role in secondary_roles}
    @property
    def player_ids_list(self):
        return [qp[1] for qp in self.lobby_players]

    def __len__(self):
        return len(self.queue_players)