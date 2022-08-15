# -*- coding: utf-8 -*-
### Setup Fresh Database and Import from .csv file (export from google sheets)

import os
from dotenv import load_dotenv
import csv
load_dotenv() # Loads .env variables
#from inhouse_bot.inhouse import *

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

# Create Initial Database

cursor.execute("""CREATE TABLE queue (
    ign TEXT,
    id BIGINT,
    primary_role ENUM('Top','Jungle','Mid','ADC','Support', 'Fill'),
    secondary_role ENUM('Top','Jungle','Mid','ADC','Support'),
    elo FLOAT(1),
    in_ready_check BOOLEAN,
    ready_check BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
""")

# ### Test Users

# user_insert_query = """
# INSERT INTO users
# (ign, id, main_role, secondary_role, fill_queue, elo, timeout)
# VALUES ( %s, %s, %s, %s, %s, %s, %s )
# """

# cursor.execute("""CREATE TABLE ready_check (
#     ign TEXT,
#     id BIGINT,
#     role ENUM('Top','Jungle','Mid','ADC','Support'),
#     elo FLOAT(1),
#     game_id INT,
#     status BOOLEAN)
# """)

test_users = [
#    ("TauPiPhi", 645940845245104130, 'Support', None, False, 1000, 0),
#    ("DravenMain1", 0, 'ADC', None, False, 1000, 0),
#    ("Âzîr", 0, 'Mid', None, False, 1000, 0)
    # ("Manì", 0, 'ADC', None, False, 1000, 0)
]


# with connection.cursor() as cursor:
#     cursor.executemany(user_insert_query, users)
#     connection.commit()

# lookup_by_ign("TauPiPhi")