import requests
import sqlite3
from datetime import datetime, date, timedelta
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

# Súradnice pre všetky krajiny/zóny
COUNTRY_COORDS = {
    "CZE": (50.1, 14.4),
    "DE-LU": (51.0, 10.0),
    "AT": (48.2, 16.3),
    "CH": (46.8, 8.3),
    "FR": (48.8, 2.3),
    "NL": (52.4, 4.9),
    "BE": (50.8, 4.3),
    "DK1": (56.2, 9.5),
    "DK2": (55.7, 12.6),
    "SE1": (66.0, 20.0),
    "SE2": (63.0, 18.0),
    "SE3": (59.3, 18.0),
    "SE4": (55.6, 13.0),
    "NO1": (59.9, 10.7),
    "NO2": (60.4, 5.3),
    "NO3": (63.4, 10.4),
    "NO4": (69.6, 18.9),
    "NO5": (58.9, 5.7),
    "FI": (60.2, 24.9),
    "PL": (52.2, 21.0),
    "IT-NORD": (45.5, 9.2),
    "IT-CNOR": (43.8, 11.2),
    "IT-CSUD": (41.9, 12.5),
    "IT-SUD": (40.8, 14.3),
    "IT-SARD": (40.1, 9.0),
    "IT-SICI": (37.5, 14.0),
    "ES": (40.4, -3.7),
    "PT": (38.7, -9.1),
    "HU": (47.5, 19.0),
    "SK": (48.1, 17.1),
    "SI": (46.0, 14.5),
    "HR": (45.8, 16.0)
}

# Rozsah – celý rok dozadu
END = date.today()
START = END - timedelta(days=365)


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


def save_to_db(timestamp, value, source):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO weather_data (timestamp, value, source) VALUES (?, ?, ?)",
        (timestamp, value, source)
    )

    conn.commit()
    conn.close()

def save_many(rows):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.executemany(
        "INSERT INTO weather_data (timestamp, value, source) VALUES (?, ?, ?)",
        rows
    )

    conn.commit()
    conn.close()

def fetch_weather_for_zone(zone):
    lat, lon = COUNTRY_COORDS[zone]

    url = (
        "https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={START}&end_date={END}"
        "&hourly=temperature_2m,cloudcover,precipitation,precipitation_probability,weathercode"
        "&timezone=UTC"
    )

    r = requests.get(url)
    data = r.json()

    # Bezpečnostná kontrola
    if "hourly" not in data:
        print(f"❌ API nevrátilo hourly dáta pre {zone}. Odpoveď:")
        print(data)
        return

    timestamps = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]
    clouds = data["hourly"]["cloudcover"]
    rain = data["hourly"]["precipitation"]
    rain_prob = data["hourly"]["precipitation_probability"]
    weathercodes = data["hourly"]["weathercode"]

    batch = []

    for ts, t, c, r_, rp, wc in zip(timestamps, temps, clouds, rain, rain_prob, weathercodes):
        dt = ts  # nemusíš konvertovať

        if t is not None:
            batch.append((dt, t, f"{zone}_temperature"))

        if c is not None:
            batch.append((dt, c, f"{zone}_cloudcover"))

        if r_ is not None:
            batch.append((dt, r_, f"{zone}_precipitation"))

        if rp is not None:
            batch.append((dt, rp, f"{zone}_precip_prob"))

        if wc is not None:
            batch.append((dt, wc, f"{zone}_weathercode"))
            batch.append((dt, decode_weathercode(wc), f"{zone}_weather_text"))
    save_many(batch)
    print(f"✔️ Uložené počasie pre {zone}")



def fetch_weather_all():
    for zone in COUNTRY_COORDS.keys():
        print(f"➡️ Sťahujem počasie pre {zone}...")
        fetch_weather_for_zone(zone)


if __name__ == "__main__":
    fetch_weather_for_zone('CZE')
