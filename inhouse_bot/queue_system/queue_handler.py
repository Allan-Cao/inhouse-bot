from inhouse_bot.db_system.db_helper import update_ready_check_id, reset_ready_check_id, remove_from_queue_id

def start_ready_check(player_ids, ready_check_message_id: int):
    # Checking to make sure everything is fine
    for player in player_ids:
        update_ready_check_id(ready_check_message_id, player[0])
def update_ready_check_id(ready_check_id: int, id: int):
    with connection.cursor() as cursor:
        cursor.execute(update_ready_check_id_query, (ready_check_id, id,))
        connection.commit()
def cancel_ready_check(ready_check_id: int, ids_to_drop):

def reset_ready_check_id(ready_check_id)
    for id in ids_to_drop:
        remove_from_queue_id(id)