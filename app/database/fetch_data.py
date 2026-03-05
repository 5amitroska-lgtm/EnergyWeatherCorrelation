import requests
import sqlite3
from datetime import datetime, date, timedelta
from database import init_db

today = date.today()
tomorrow = today + timedelta(days=1)

url = (
    f"https://api.energy-charts.info/price?"
    f"country=CZE&start={today}&end={tomorrow}"
)

def save_to_db(timestamp, value):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO api_data (timestamp, value) VALUES (?, ?)",
        (timestamp, value)
    )

    conn.commit()
    conn.close()

def fetch_prices_cz():
    response = requests.get(url)
    data = response.json()

    timestamps = data["unix_seconds"]
    prices = data["price"]

    results = []

    for ts, price in zip(timestamps, prices):
        dt = datetime.utcfromtimestamp(ts).isoformat()
        results.append((dt, price))

    return results

def fetch_and_store():
    init_db()
    rows = fetch_prices_cz()

    for timestamp, value in rows:
        save_to_db(timestamp, value)
        print("Uložené:", timestamp, value)

if __name__ == "__main__":
    fetch_and_store()