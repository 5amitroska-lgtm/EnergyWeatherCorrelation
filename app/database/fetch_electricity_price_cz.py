import requests
import sqlite3
from datetime import datetime, date, timedelta
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

today = date.today()
tomorrow = today + timedelta(days=1)

url = (
    f"https://api.energy-charts.info/price?"
    f"country=CZE&start={today}&end={tomorrow}"
)

def save_to_db(timestamp, value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO electricity_price_data (timestamp, value, source) VALUES (?, ?, ?)",
        (timestamp, value, "electricity_price_cz")
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

def fetch_and_store_electricity_price():
    rows = fetch_prices_cz()

    for timestamp, value in rows:
        save_to_db(timestamp, value)
        print("Uložené:", timestamp, value)

if __name__ == "__main__":
    fetch_and_store_electricity_price()