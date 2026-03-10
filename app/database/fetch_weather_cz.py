import requests
import sqlite3
from datetime import datetime, date, timedelta

LAT = 49.8
LON = 15.5

today = date.today()
tomorrow = today + timedelta(days=1)

url = (
    "https://api.open-meteo.com/v1/forecast?"
    f"latitude={LAT}&longitude={LON}"
    f"&start_date={today}&end_date={tomorrow}"
    "&hourly=temperature_2m"
    "&timezone=UTC"
)

def save_to_db(timestamp, value, source):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO api_data (timestamp, value, source) VALUES (?, ?, ?)",
        (timestamp, value, source)
    )

    conn.commit()
    conn.close()

def fetch_temperature_cz():
    response = requests.get(url)
    data = response.json()

    timestamps = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]

    results = []

    for ts, temp in zip(timestamps, temps):
        dt = datetime.fromisoformat(ts).isoformat()
        results.append((dt, temp))

    return results

def fetch_and_store_temperature():
    rows = fetch_temperature_cz()

    for timestamp, value in rows:
        save_to_db(timestamp, value, "temperature")
        print("Uložené (teplota):", timestamp, value)


if __name__ == "__main__":
    fetch_and_store_temperature()
