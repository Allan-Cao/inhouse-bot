#######################################################################################################
#  I'm really stupid and didn't know that SQLAlchemy existed until AFTER writing all this code so.... #
#######################################################################################################
### Library Imports ###
import os
### Env Setup ###
from dotenv import load_dotenv
load_dotenv() # Loads .env variables
### SQL Queries ###
user_insert_query = """
INSERT INTO users
(ign, id, main_role, secondary_role, elo, timeout)
VALUES ( %s, %s, %s, %s, %s, %s)
"""
ign_lookup_query = "SELECT * FROM users WHERE ign = %s"
id_lookup_query = "SELECT * FROM users WHERE id = %s"
update_discord_id_query = "UPDATE users SET id = %s WHERE ign = %s"
update_secondary_role_by_id = "UPDATE users SET secondary_role = %s WHERE id = %s"

queue_lookup_ign_query = "SELECT * FROM queue WHERE id = %s"
queue_lookup_id_query = "SELECT * FROM queue WHERE id = %s"
remove_from_queue_id_query = "DELETE FROM queue WHERE id = %s"
remove_from_queue_ign_query = "DELETE FROM queue WHERE ign = %s"
reset_queue_query = "DELETE FROM queue;"
queue_row_count_query = "SELECT COUNT(1) FROM queue;"
update_in_ready_check_query = "UPDATE queue SET in_ready_check = %s WHERE id = %s"
update_readyd_query = "UPDATE queue SET ready_check = %s WHERE id = %s"
queue_insert_query = """
INSERT INTO queue
(ign, id, primary_role, secondary_role, elo, in_ready_check, ready_check, ready_check_id)
VALUES ( %s, %s, %s, %s, %s, False, Null, Null)
"""
get_current_queue_query = "SELECT * FROM queue"
get_primary_queue_query = "SELECT * FROM queue WHERE primary_role = %s"
get_role_queue_query = "SELECT * FROM queue WHERE primary_role = %s OR secondary_role = %s"
get_role_sorted_query = "SELECT * from queue WHERE primary_role = %s ORDER BY created_at;"
reset_ready_check_id_query = "UPDATE queue SET ready_check = None WHERE ready_check_id = %s"
update_ready_check_id_query = "UPDATE queue SET ready_check_id = %s WHERE id = %s"

### Setup SQL
import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host=os.getenv('SQL_URL'),
                                         database='inhouse', #CREATE DATABASE inhouse
                                         user=os.getenv('SQL_USER'),
                                         password=os.getenv('SQL_PWD'))
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
except Error as e:
    print("Error while connecting to MySQL", e)
def check_lobby_made():
    with connection.cursor() as cursor:
        lobby_users = []
        for role in ["Top", "Jungle", "Mid", "ADC", "Support"]:
            cursor.execute(get_role_sorted_query, (role,))
            myresult = cursor.fetchone()
            if len(myresult < 2):
                return False
            else:
                lobby_users.append([player[:5] for player in myresult[0:2]])
    print(lobby_users)
    for player in lobby_users:
        ...
    return True
def remove_from_queue_id(id):
    with connection.cursor() as cursor:
        cursor.execute(remove_from_queue_id_query, (id,))
        connection.commit()
def join_queue_id(id):
    player_info = lookup_by_id(id)
    with connection.cursor() as cursor:
        cursor.execute(queue_insert_query, (player_info[:5]))
        connection.commit()
def lookup_queue_id(id):
    with connection.cursor() as cursor:
        cursor.execute(queue_lookup_id_query, (id,))
        myresult = cursor.fetchone()
    return myresult
def add_user(user):
    with connection.cursor() as cursor:
        cursor.execute(user_insert_query, user)
        connection.commit()
def lookup_by_ign(ign):
    with connection.cursor() as cursor:
        cursor.execute(ign_lookup_query, (ign,))
        myresult = cursor.fetchone()
    return myresult
def change_secondary_role(new_role, id):
    with connection.cursor() as cursor:
        cursor.execute(update_secondary_role_by_id, (new_role, id,))
        connection.commit()
def lookup_by_id(id):
    with connection.cursor() as cursor:
        cursor.execute(id_lookup_query, (id,))
        myresult = cursor.fetchone()
    return myresult

def update_discord_id(id, ign):
    with connection.cursor() as cursor:
        cursor.execute(update_discord_id_query, (id, ign,))
        connection.commit()
def stop_sql():
    with connection.cursor() as cursor:
        cursor.close()
        connection.close()
def reset_queue():
    with connection.cursor() as cursor:
        cursor.execute(reset_queue_query)
        connection.commit()
def update_elo(id, elo_update):
    player_info = lookup_by_id(id)
    current_elo = player_info[4]
    updated_elo = current_elo + elo_update
    if updated_elo <= 600:
        return True
    if updated_elo >= 1500:
        return "Fill"
    elif updated_elo >= 1250:
        return "Secondary Role"
def get_current_queue():
    with connection.cursor() as cursor:
        cursor.execute(get_current_queue_query)
        return cursor.fetchall()
def update_in_ready_check(in_ready_check, id):
    with connection.cursor() as cursor:
        cursor.execute(update_in_ready_check_query, (in_ready_check, id))
        connection.commit()
def update_readyd_queue(ready_check, id):
    with connection.cursor() as cursor:
        cursor.execute(update_readyd_query, (ready_check, id))
        connection.commit()
def update_ready_check_id(ready_check_id, id):
    with connection.cursor() as cursor:
        cursor.execute(update_ready_check_id_query, (ready_check_id, id))
        connection.commit()
def reset_ready_check_id(ready_check_id):
    with connection.cursor() as cursor:
        cursor.execute(reset_ready_check_id_query, (ready_check_id))
        connection.commit()