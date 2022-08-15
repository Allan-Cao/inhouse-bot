from inhouse_bot.db_system.db_helper import lookup_queue_id
class QueuePlayer():
    def __init__(self, discord_id):
        player_queue_data = lookup_queue_id(discord_id)
        if player_queue_data == None:
            role = None
            queue_time = None
            in_ready_check = None
            is_ready = None
        else:
            role = player_queue_data[2]
            queue_time = player_queue_data[7]
            in_ready_check = player_queue_data[5]
            is_ready = player_queue_data[6]
    def __str__(self):
        return f"{self.player.name} - {self.role}"