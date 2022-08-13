# -*- coding: utf-8 -*-
### Setup Fresh Database and Import from .csv file (export from google sheets)

import os
from dotenv import load_dotenv
import csv
load_dotenv() # Loads .env variables
from inhouse import *

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

cursor.execute("""CREATE TABLE users (
    ign TEXT,
    id BIGINT,
    main_role ENUM('Top','Jungle','Mid','ADC','Support'),
    secondary_role ENUM('Top','Jungle','Mid','ADC','Support'),
    fill_queue BOOLEAN,
    elo FLOAT(1),
    timeout INTEGER)
""")

users = []

player_csv = open('players.csv', newline='',encoding="utf-8")
csvreader = csv.reader(player_csv)
header = next(csvreader)
for row in csvreader:
    if row[0] != "":
        users.append((row[0], 0, row[2], None, False, row[3], 0))

### Test Users

user_insert_query = """
INSERT INTO users
(ign, id, main_role, secondary_role, fill_queue, elo, timeout)
VALUES ( %s, %s, %s, %s, %s, %s, %s )
"""


test_users = [
#    ("TauPiPhi", 645940845245104130, 'Support', None, False, 1000, 0),
#    ("DravenMain1", 0, 'ADC', None, False, 1000, 0),
#    ("Âzîr", 0, 'Mid', None, False, 1000, 0)
    # ("Manì", 0, 'ADC', None, False, 1000, 0)
]


with connection.cursor() as cursor:
    cursor.executemany(user_insert_query, users)
    connection.commit()

# lookup_by_ign("TauPiPhi")