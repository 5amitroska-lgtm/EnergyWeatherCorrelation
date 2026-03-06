import database
import sqlite3
import os

print("DB PATH:", os.path.abspath("data.db"))
database.init_db()

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM api_data")
rows = cursor.fetchall()

for row in rows:
    print(row)