import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

timestamp_str_now_hour_rounded = datetime.now().strftime('%Y-%m-%dT%H:00:00')

def show_all():
    """Function  prints all the rows in the database ordered by timestamp"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, value, source
        FROM electricity_price_data
        ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    print("\n--- Všetky uložené dáta ---")
    for row in rows:
        print(row)


def show_today():
    """Function  prints all rows corresponding to the current date form 00:00 to 23:00"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, value, source
        FROM electricity_price_data
        WHERE date(timestamp) = date('now')
        ORDER BY timestamp
    """)

    rows = cursor.fetchall()
    conn.close()

    print("\n--- Dáta za dnešný deň ---")
    for row in rows:
        print(row)


def show_last_24h():
    """Function  prints last 24 hour rows"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, value, source
        FROM electricity_price_data
        WHERE timestamp >= datetime('now', '-1 day')
        ORDER BY timestamp
    """)

    rows = cursor.fetchall()
    conn.close()

    print("\n--- Posledných 24 hodín ---")
    for row in rows:
        print(row)


def show_daily_avg():
    """Function  prints daily average rows"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date(timestamp) AS day, AVG(value) AS avg_price
        FROM electricity_price_data
        GROUP BY day
        ORDER BY day DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    print("\n--- Priemerná cena za deň ---")
    for row in rows:
        print(row)

def select_by_timestamp(dt: datetime):
    """Function  prints a row corresponding to the given timestamp"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, value, source
        FROM electricity_price_data WHERE timestamp == ?
    """, (dt,))

    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        print(row)

def select_by_source(source):
    """Function  prints a row corresponding to the given timestamp"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, value, source
        FROM electricity_price_data WHERE source == ?
    """, (source,))

    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        print(row)

def remove_duplicates():
    """Function removes duplicated rows in DB only if all values match"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM electricity_price_data
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM electricity_price_data
            GROUP BY timestamp, value, source
        );
    """)

    conn.commit()
    conn.close()

def check_number_of_duplicates():
    """Function checks duplicatd rows in the DB and prints a count of duplicates"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, COUNT(*) FROM electricity_price_data GROUP BY timestamp HAVING COUNT(*) > 1")
    print(len(cursor.fetchall()))

if __name__ == "__main__":
    remove_duplicates()
    #show_all()
    #show_today()
    #show_last_24h()
    #show_daily_avg()
    #print(timestamp_str_now_hour_rounded)
    select_by_source('electricity_price_cz')
    select_by_timestamp(timestamp_str_now_hour_rounded)
    check_number_of_duplicates()
