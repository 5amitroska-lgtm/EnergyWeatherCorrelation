from app.database.init_db import init_db
from app.database.fetch_electricity_price_cz import fetch_and_store_electricity_price
from app.database.fetch_weather_cz import fetch_and_store_weather
from app.database.read_data import remove_duplicates
from app.modules.modul1 import plot_data,plot_by_source,plot_interactive

if __name__ == "__main__":
    print(init_db())
    fetch_and_store_electricity_price()
    fetch_and_store_weather()
    remove_duplicates()
    plot_interactive()