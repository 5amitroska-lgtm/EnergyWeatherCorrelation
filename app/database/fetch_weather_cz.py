import requests
import sqlite3
from datetime import datetime, date, timedelta
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")
LAT = 49.8
LON = 15.5

today = date.today()
tomorrow = today + timedelta(days=1)

# Open-Meteo API s rozšírenými údajmi
url = (
    "https://api.open-meteo.com/v1/forecast?"
    f"latitude={LAT}&longitude={LON}"
    f"&start_date={today}&end_date={tomorrow}"
    "&hourly=temperature_2m,cloudcover,precipitation,precipitation_probability,weathercode"
    "&timezone=UTC"
)

# Preklad weathercode → text
def decode_weathercode(code: int) -> str:
    if code == 0:
        return "slnecno"
    if code in (1, 2, 3):
        return "zamracene"
    if code in (51, 53, 55, 61, 63, 65, 80, 81, 82):
        return "prsi"
    if code in (71, 73, 75, 77):
        return "snezi"
    if code in (95, 96, 99):
        return "burka"
    return "nezname"


# Uloženie jedného riadku do DB
def save_to_db(timestamp, value, source):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO weather_data (timestamp, value, source) VALUES (?, ?, ?)",
        (timestamp, value, source)
    )

    conn.commit()
    conn.close()


# Stiahnutie všetkých údajov z API
def fetch_weather_data():
    response = requests.get(url)
    data = response.json()

    timestamps = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]
    clouds = data["hourly"]["cloudcover"]
    rain = data["hourly"]["precipitation"]
    rain_prob = data["hourly"]["precipitation_probability"]
    weathercodes = data["hourly"]["weathercode"]

    results = []

    for ts, t, c, r, rp, wc in zip(timestamps, temps, clouds, rain, rain_prob, weathercodes):
        dt = datetime.fromisoformat(ts).isoformat()
        results.append({
            "timestamp": dt,
            "temperature": t,
            "cloudcover": c,
            "precipitation": r,
            "precip_prob": rp,
            "weathercode": wc,
            "weather_text": decode_weathercode(wc)
        })

    return results


# Uloženie všetkých údajov do DB
def fetch_and_store_weather():
    rows = fetch_weather_data()

    for row in rows:
        ts = row["timestamp"]

        save_to_db(ts, row["temperature"], "temperature")
        save_to_db(ts, row["cloudcover"], "cloudcover")
        save_to_db(ts, row["precipitation"], "precipitation")
        save_to_db(ts, row["precip_prob"], "precipitation_probability")
        save_to_db(ts, row["weathercode"], "weathercode")
        save_to_db(ts, row["weather_text"], "weather_text")

        print("Uložené:", ts, row)


if __name__ == "__main__":
    fetch_and_store_weather()
