from inhouse_bot.db_system.db_helper import get_current_queue
from collections import defaultdict
from inhouse_bot.utils.formatter import secondary_roles, ping_user_by_id
from typing import Dict, List
import discord 
import time

class GameQueue():
    def __init__(self):
        queue_query = get_current_queue()
        if queue_query == None: # Empty Queue
            self.queue_players = []
            self.game_id = None
            return
        in_ready_check_player_ids = [r[1] for r in queue_query if r[5] is not None or r[6] is not None] # I REALLY NEED AN ORM DONT I HAHA 
        self.queue_players = [
                qp for qp in queue_query if qp[1] not in in_ready_check_player_ids
            ]
        starting_queue = defaultdict(secondary_roles)
        for role in secondary_roles:
            for qp in self.queue_players_dict[role]:
                # If we already have 2 players in that role, we continue
                if len(starting_queue[role]) >= 2:
                    continue
                else:
                    starting_queue[role].append(qp)
                    self.queue_players.append(qp)
        for role_queue in self.queue_players_dict.values():
            if len(role_queue) < 2:
                self.queue_players = []
            else:
                self.game_id = time.time()
                
    def make_queue_embed(self):
        embed = discord.Embed(
            title=f"🚨🚨🚨 Queue Found! 🚨🚨🚨",
            description=f"Game ID: {self.game_id}",
            color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
        )
        for role in secondary_roles:
            embed_text = ""
            for qp in self.queue_players[role]:
                embed_text += ping_user_by_id(qp[0]) + " "
            embed.add_field(name=role, value=f"Players: {embed_text}", inline=False)
        embed.set_footer(text="Queue generated by Seraphine Bot") 
        return embed
    def player_ping(self):
        text = ""
        for qp in self.queue_players:
            text += ping_user_by_id(qp[0])
        return text
    @property
    def queue_players_dict(self) -> Dict[str, List]:
        return {role: [player for player in self.queue_players if player.role == role] for role in secondary_roles}
    @property
    def player_ids_list(self):
        return [qp[1] for qp in self.queue_players]

    def __len__(self):
        return len(self.queue_players)