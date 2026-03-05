import sqlite3

def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            value TEXT
        )
    """)

    conn.commit()
    conn.close()