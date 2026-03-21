from app.database.fetch_all_prices import fetch_and_store_all_prices
from app.database.read_data import remove_duplicates
from database import init_db
from database.fetch_all_weather import fetch_weather_all
from app.utils.timestamps import Timestamp
from app.database.read_data import select_by_timestamp
from app.modules.graf import Graf
from datetime import date

if __name__ == "__main__":
    init_db()
    fetch_and_store_all_prices()
    fetch_weather_all()
    timestamp = Timestamp(2026,3,20).convert_to_datetime()
    print(timestamp)
    remove_duplicates()
    select_by_timestamp(timestamp)
    graf= Graf(1,"1h", date(2026, 1, 1), date(2026, 1, 31))
    zone = "CH"
    graf.plot_zone(zone)
    zone = "AT"
    graf.plot_zone(zone)
