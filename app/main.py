from app.database.fetch_all_prices import fetch_and_store_all_prices
from app.routers.read_data_electricity_api import select_all_available_zones_for_datetime
from app.database import init_db
from app.database.fetch_all_weather import fetch_weather_all
from app.utils.timestamps import Timestamp
from app.modules.graf import Graf
from datetime import date, datetime
import logging
from fastapi import FastAPI
from app.routers.read_data_electricity_api import router as electricity_router
from app.routers.read_data_weather_api import router as weather_router
from app.utils.enums import Zone

# Import of routers
app = FastAPI(
    title="WeatherDataCorrelation",
    version="1.0.0"
)

# Registration of routers
app.include_router(electricity_router)
app.include_router(weather_router)

print("ROUTERS:", app.routes)
@app.get("/")
def root():
    return {"message": "EnergyWeatherCorrelation API is running 🚀"}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    init_db()
    #----------------------------------------------------
    # Methods for filling empty database
    #----------------------------------------------------
    fetch_and_store_all_prices()
    fetch_weather_all()

    try:
        #------------------------------------------------------
        # Entering a date  range for thich we want to make analysis
        #------------------------------------------------------
        graf = Graf(1, "1h", date(2026, 1, 1), date(2026, 1, 31))
        available_zones = select_all_available_zones_for_datetime(datetime(2026,1,1))

    except ValueError:
        raise ("Non valid timestamp")

    try:
        if not available_zones:
            raise ValueError("available_zones je prázdny – žiadne zóny na vykreslenie.")

        else:
            #---------------------------------------------------
            # All available zones for which can be the analysis made
            # Plot in browser
            #-----------------------------------------------------
            for zone in available_zones:
                graf.plot_zone(zone)
                logger.info(f"graf vykresleny pre{zone}")

    except Exception as e:
        print("Chyba:", e)
        logger.exception("Chyba:", e)


