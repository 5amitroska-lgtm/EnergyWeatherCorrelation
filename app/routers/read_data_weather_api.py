from fastapi import FastAPI
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
from app.utils.enums import Zone
from fastapi import APIRouter
engine = create_engine('sqlite:///C:/Users/TUF/PythonLekcie/EnergyWeatherCorrelation/app/database/data.db', echo=False)

app = FastAPI()
router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)

@router.get("/datetime")
def select_by_timestamp(dt: datetime) -> dict:
    """select weather data from datetime"""
    iso = dt.isoformat()
    with engine.connect() as conn:

        query = """
            SELECT id, timestamp, value, source
            FROM weather_data
            WHERE timestamp = ?
        """

        rows = pd.read_sql(query, conn, params=(iso,))

        if len(rows) == 0:
            return {"message": f"No rows for timestamp {iso}"}
        return rows.to_dict(orient="records")

@router.get("/zone")
def select_by_zone(zone: Zone) -> dict:
    """select weather data for zone"""
    with engine.connect() as conn:

        query = """
            SELECT id, timestamp, value, source
            FROM weather_data
            WHERE zone = ?
        """

        rows = pd.read_sql(query, conn, params=(zone.value,))

        if len(rows) == 0:
            return {"message": f"No rows for timestamp {zone}"}
        return rows.to_dict(orient="records")


@router.get("/zone/dailyAVG")
def weather_daily_avg(zone: Zone) -> dict:
    """Return daily average for each weather source separately for given zone."""

    query = """
        SELECT 
            date(timestamp) AS day,
            source,
            AVG(value) AS avg_value
        FROM weather_data
        WHERE zone = ?
        GROUP BY day, source
        ORDER BY day DESC, source
    """

    with engine.connect() as conn:
        rows = pd.read_sql_query(query, conn, params=(zone.value,))

    if rows.empty:
        return {"message": f"No weather data for zone {zone.value}"}

    return rows.to_dict(orient="records")


@router.get("/availableZones")
def select_weather_available_zones(dt:datetime) -> list:
    """select all available zones for datetime"""
    dt_str = dt.strftime("%Y-%m-%dT%H:%M:%S")

    query = """
           SELECT zone
           FROM weather_data
           WHERE timestamp = ?
       """

    with engine.connect() as conn:
        rows = pd.read_sql_query(query, conn, params=(dt_str,))
        zones = rows["zone"].tolist()
        unique_zones = list(dict.fromkeys(zones))

    return unique_zones

@router.get("/value")
def select_weather_value(dt:datetime, zone: Zone) -> dict:
    """select weather value from datetime"""
    iso = dt.isoformat()
    with engine.connect() as conn:
        query = """
            SELECT value, source
            FROM weather_data WHERE timestamp == ?
            AND zone = ?
        """
        rows = pd.read_sql(query, conn, params=(iso,zone,))
        if len(rows) == 0:
            return {"message": f"No rows for timestamp {iso} and zone {zone}"}
        return rows.to_dict(orient="records")


if __name__ == "__main__":

    print(select_weather_value(datetime(2026,1,1),zone="FR"))





