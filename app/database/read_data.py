import sqlite3

DB_PATH = "data.db"

def show_all():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, value
        FROM api_data
        ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    print("\n--- Všetky uložené dáta ---")
    for row in rows:
        print(row)


def show_today():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, value
        FROM api_data
        WHERE date(timestamp) = date('now')
        ORDER BY timestamp
    """)

    rows = cursor.fetchall()
    conn.close()

    print("\n--- Dáta za dnešný deň ---")
    for row in rows:
        print(row)


def show_last_24h():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, value
        FROM api_data
        WHERE timestamp >= datetime('now', '-1 day')
        ORDER BY timestamp
    """)

    rows = cursor.fetchall()
    conn.close()

    print("\n--- Posledných 24 hodín ---")
    for row in rows:
        print(row)


def show_daily_avg():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date(timestamp) AS day, AVG(value) AS avg_price
        FROM api_data
        GROUP BY day
        ORDER BY day DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    print("\n--- Priemerná cena za deň ---")
    for row in rows:
        print(row)


if __name__ == "__main__":
    show_all()
    show_today()
    show_last_24h()
    show_daily_avg()
