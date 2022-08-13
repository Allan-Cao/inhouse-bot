# -*- coding: utf-8 -*-
### Setup Fresh Database and Import from .csv file (export from google sheets)

import os
from dotenv import load_dotenv
import sqlite3
load_dotenv() # Loads .env variables
import csv

### Setup SQL (sqlite3 for now but could use something better in the future)
DATABASE_FILE = os.environ.get('DB_FILE')
connection = sqlite3.connect('DATABASE_FILE', isolation_level=None)
cursor = connection.cursor()

# Create Initial Database
#cursor.execute("CREATE TABLE users (ign TEXT, id INTEGER, main_role INTEGER, secondary_role INTEGER, fill_queue BOOLEAN, elo INTEGER, timeout INTEGER)")

file1 = open('role_signup.csv', newline='',encoding="utf-8")
csvreader = csv.reader(file1)
header = next(csvreader)
for row in csvreader:

file2 = open('playerbase.csv', newline='',encoding="utf-8")
csvreader = csv.reader(file2)
header = next(csvreader)
for row in csvreader:
    if row[0] != "":
        print(row)