
from app.database.read_data import remove_duplicates
from app.modules.modul1 import plot_data,plot_by_source,plot_interactive


from database import init_db, fetch_and_store_weather, fetch_and_store_electricity_price

if __name__ == "__main__":
    init_db()
    fetch_and_store_weather()
    fetch_and_store_electricity_price()
    remove_duplicates()
    plot_interactive()
