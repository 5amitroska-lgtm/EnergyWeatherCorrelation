import requests
import sqlite3
from datetime import date, timedelta, datetime
import os
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import threading

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

ZONES = {
    "CZE": "Česko",
    "DE-LU": "Nemecko + Luxembursko",
    "AT": "Rakúsko",
    "CH": "Švajčiarsko",
    "FR": "Francúzsko",
    "NL": "Holandsko",
    "BE": "Belgicko",
    "DK1": "Dánsko – západ",
    "DK2": "Dánsko – východ",
    "SE1": "Švédsko – SE1",
    "NO1": "Nórsko – NO1",
    "FI": "Fínsko",
    "PL": "Poľsko",
    "IT-NORD": "Taliansko – sever",
    "IT-CNOR": "Taliansko – stred sever",
    "IT-CSUD": "Taliansko – stred juh",
    "IT-SUD": "Taliansko – juh",
    "IT-SARD": "Taliansko – Sardínia",
    "IT-SICI": "Taliansko – Sicília",
    "ES": "Španielsko",
    "PT": "Portugalsko",
    "HU": "Maďarsko",
}

API_ZONES = {
    "CZE": ("CZ", None),
    "DE-LU": (None, "DE-LU"),
    "AT": ("AT", "AT"),
    "CH": ("CH", "CH"),
    "FR": ("FR", "FR"),
    "NL": ("NL", "NL"),
    "BE": ("BE", "BE"),
    "DK1": (None, "DK1"),
    "DK2": (None, "DK2"),
    "SE1": (None, "SE1"),
    "NO1": (None, "NO1"),
    "FI": ("FI", "FI"),
    "PL": ("PL", "PL"),
    "IT-NORD": (None, "IT-NORD"),
    "IT-CNOR": (None, "IT-CNOR"),
    "IT-CSUD": (None, "IT-CSUD"),
    "IT-SUD": (None, "IT-SUD"),
    "IT-SARD": (None, "IT-SARD"),
    "IT-SICI": (None, "IT-SICI"),
    "ES": ("ES", "ES"),
    "PT": ("PT", "PT"),
    "HU": ("HU", "HU"),
}

END = date.today()
START = END - timedelta(days=365)

write_queue = Queue()

def db_writer():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    while True:
        item = write_queue.get()
        if item is None:
            break

        cursor.executemany(
            "INSERT INTO electricity_price_data (timestamp, zone, value, source) VALUES (?, ?, ?, ?)",
            item
        )
        conn.commit()

    conn.close()  # 🔥 TOTO JE KRITICKÉ – ZATVORÍ DB SPOJENIE


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS electricity_price_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            zone TEXT,
            value REAL,
            source TEXT
        )
    """)

    conn.commit()
    conn.close()


def fetch_prices(zone):
    country, bzn = API_ZONES[zone]

    if country:
        url = f"https://api.energy-charts.info/price?country={country}&start={START}&end={END}"
        r = requests.get(url)
        if r.status_code == 200 and "unix_seconds" in r.json():
            return r.json()

    if bzn:
        url = f"https://api.energy-charts.info/price?bzn={bzn}&start={START}&end={END}"
        r = requests.get(url)
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

        # 🔥 preskočíme neplatné hodnoty
        if price is None:
            continue

        dt = datetime.fromtimestamp(ts).isoformat()
        batch.append((dt, zone, price, name))

    if batch:
        write_queue.put(batch)
        print(f"   ✔️ Pripravených {len(batch)} záznamov.")
    else:
        print(f"   ❌ Žiadne platné dáta pre {zone}.")

def db_writer():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    while True:
        item = write_queue.get()
        if item is None:
            break

        try:
            cursor.executemany(
                "INSERT INTO electricity_price_data (timestamp, zone, value, source) VALUES (?, ?, ?, ?)",
                item
            )
            conn.commit()
        except Exception as e:
            print("❌ Chyba pri zápise do DB:", e)
            # 🔥 pokračujeme ďalej, nenecháme thread spadnúť
            continue

    conn.close()

def fetch_and_store_all_prices():
    print(f"Sťahujem dáta od {START} do {END} (365 dní)...")

    writer_thread = threading.Thread(target=db_writer)
    writer_thread.start()

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(fetch_and_store_by_zone, ZONES.keys())

    write_queue.put(None)
    writer_thread.join()

    # 🔥 Vynútime uvoľnenie SQLite locku
    sqlite3.connect(DB_PATH).close()

    print("✔️ Hotovo – všetky ceny uložené.")

