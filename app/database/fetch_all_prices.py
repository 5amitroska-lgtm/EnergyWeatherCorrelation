import requests
import sqlite3
from datetime import date, timedelta, datetime
import os
from concurrent.futures import ThreadPoolExecutor

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

ZONES = {
    "CZE": "Česko",
    "DE-LU": "Nemecko + Luxembursko",
    "AT": "Rakúsko",
    "CH": "Švajčiarsko",
    "FR": "Francúzsko",
    # "NL": "Holandsko",
    # "BE": "Belgicko",
    # "DK1": "Dánsko – západ",
    # "DK2": "Dánsko – východ",
    # "SE1": "Švédsko – SE1",
    # "SE2": "Švédsko – SE2",
    # "SE3": "Švédsko – SE3",
    # "SE4": "Švédsko – SE4",
    # "NO1": "Nórsko – NO1",
    # "NO2": "Nórsko – NO2",
    # "NO3": "Nórsko – NO3",
    # "NO4": "Nórsko – NO4",
    # "NO5": "Nórsko – NO5",
    # "FI": "Fínsko",
    # "PL": "Poľsko",
    # "IT-NORD": "Taliansko – sever",
    # "IT-CNOR": "Taliansko – stred sever",
    # "IT-CSUD": "Taliansko – stred juh",
    # "IT-SUD": "Taliansko – juh",
    # "IT-SARD": "Taliansko – Sardínia",
    # "IT-SICI": "Taliansko – Sicília",
    # "ES": "Španielsko",
    # "PT": "Portugalsko",
    # "HU": "Maďarsko",
    # "SK": "Slovensko",
    # "SI": "Slovinsko",
    # "HR": "Chorvátsko"
}

END = date.today()
START = END - timedelta(days=365)


def save_many(rows):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO electricity_price_data (timestamp, value, source) VALUES (?, ?, ?)",
        rows
    )
    conn.commit()
    conn.close()


def fetch_prices(zone):
    url_country = (
        f"https://api.energy-charts.info/price?"
        f"country={zone}&start={START}&end={END}"
    )

    url_bzn = (
        f"https://api.energy-charts.info/price?"
        f"bzn={zone}&start={START}&end={END}"
    )

    r = requests.get(url_country)
    if r.status_code == 200 and "unix_seconds" in r.json():
        return r.json()

    r = requests.get(url_bzn)
    if r.status_code == 200 and "unix_seconds" in r.json():
        return r.json()

    return None


def fetch_and_store_by_zone(zone: str):
    name = ZONES[zone]
    print(f"➡️  {zone} – {name}")

    data = fetch_prices(zone)
    if not data:
        print(f"   ❌ Dáta nie sú dostupné.")
        return

    timestamps = data["unix_seconds"]
    prices = data["price"]

    batch = []
    for ts, price in zip(timestamps, prices):
        dt = datetime.utcfromtimestamp(ts).isoformat()
        batch.append((dt, price, f"{zone} - {name}"))

    save_many(batch)

    print(f"   ✔️ Uložených {len(batch)} záznamov.")


def fetch_and_store_all_prices():
    print(f"Sťahujem dáta od {START} do {END} (365 dní)...")

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(fetch_and_store_by_zone, ZONES.keys())


if __name__ == "__main__":
    fetch_and_store_all_prices()
