import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS electricity_price_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            value REAL NOT NULL,
            source TEXT NOT NULL            
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            value REAL NOT NULL,
            source TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()

def show_table(table_name):
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

    conn.close()
    return df