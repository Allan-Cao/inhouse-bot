from inhouse_bot.db_system.db_helper import get_current_queue
from collections import defaultdict
from inhouse_bot.utils.formatter import secondary_roles
from typing import Dict, List

class GameQueue():
    def __init__(self):
        queue_query = get_current_queue()
        if queue_query == None: # Empty Queue
            self.queue_players = []
            return
        potential_queue_ids = [player_id[1] for player_id in queue_query]
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
    @property
    def queue_players_dict(self) -> Dict[str, List]:
        return {role: [player for player in self.queue_players if player.role == role] for role in secondary_roles}

    def __len__(self):
        return len(self.queue_players)