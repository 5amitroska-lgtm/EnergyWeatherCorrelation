
from app.database.read_data import remove_duplicates
from app.modules.modul1 import plot_zone,plot_correlation
from database import init_db, fetch_and_store_weather, fetch_and_store_electricity_price
from database.fetch_all_prices import fetch_and_store_by_zone
from database.fetch_all_weather import fetch_weather_for_zone

if __name__ == "__main__":
    init_db()
    # fetch_and_store_weather()
    #fetch_and_store_electricity_price()
    zone='CZE'
    fetch_weather_for_zone(zone)

    fetch_and_store_by_zone(zone)

    plot_zone(zone)