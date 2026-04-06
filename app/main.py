from app.database.fetch_all_prices import fetch_and_store_all_prices
from app.database.read_data import select_all_available_zones_for_datetime
from app.database import init_db
from app.database.fetch_all_weather import fetch_weather_all
from app.utils.timestamps import Timestamp
from app.database.read_data import select_by_timestamp
from app.modules.graf import Graf
from datetime import date
import logging
from fastapi import FastAPI
from app.routers.read_data_electricity_api import router as electricity_router
from app.routers.read_data_weather_api import router as weather_router


# Import routerov
app = FastAPI(
    title="WeatherDataCorrelation",
    version="1.0.0"
)

# Registrácia routerov
app.include_router(electricity_router)
app.include_router(weather_router)
@app.get("/")
def root():
    return {"message": "EnergyWeatherCorrelation API is running 🚀"}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    init_db()
    ZONE_CODES = [
        "CZE",
        "DE-LU",
        "AT",
        "CH",
        "FR",
        "NL",
        "BE",
        "DK1",
        "DK2",
        "SE1",
        "NO1",
        "FI",
        "PL",
        "IT-NORD",
        "IT-CNOR",
        "IT-CSUD",
        "IT-SUD",
        "IT-SARD",
        "IT-SICI",
        "ES",
        "PT",
        "HU"
        # "SK",
        # "SI",
        # "HR"
    ]
    # fetch_and_store_all_prices()
    # fetch_weather_all()
    # try:
    #     graf = Graf(1, "1h", date(2026, 1, 1), date(2026, 1, 31))
    #     available_zones = select_all_available_zones_for_datetime(Timestamp(2026,1,1).convert_to_datetime())
    #     available_zones = []
    #
    # except ValueError:
    #     raise ("Non valid timestamp")
    #
    # try:
    #     if not available_zones:
    #         raise ValueError("available_zones je prázdny – žiadne zóny na vykreslenie.")
    #
    #     else:
    #         for zone in available_zones:
    #             graf.plot_zone(zone[0])
    #             logger.info(f"graf vykresleny pre{zone[0]}")
    #
    # except Exception as e:
    #     print("Chyba:", e)
    #     logger.exception("Chyba:", e)

print(Timestamp(2026,1,1).convert_to_datetime())


