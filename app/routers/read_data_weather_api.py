from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
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
def select_by_timestamp(dt: datetime):
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
def select_by_zone(zone: Zone):
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
def electricity_daily_avg(zone: Zone):
    with engine.connect() as conn:
        query = """
            SELECT date(timestamp) AS day, AVG(value) AS avg_price
            FROM weather_data
            WHERE zone = ?
            GROUP BY day
            ORDER BY day DESC
        """
        rows = pd.read_sql(query, conn, params=(zone,))

        if len(rows) == 0:
            return {"message": f"No rows for timestamp {zone}"}

        return rows.to_dict(orient="records")

@router.get("/availableZones")
def select_electricity_available_zones(dt:datetime):
    iso = dt.isoformat()
    with engine.connect() as conn:
        query = """
           SELECT zone
           FROM weather_data WHERE timestamp == ?
       """
        rows = pd.read_sql(query, conn, params=(iso,))
        if len(rows) == 0:
            return {"message": f"No rows for timestamp {iso}"}
        return rows.to_dict(orient="records")

@router.get("/value")
def select_electricity_value(dt:datetime, zone: Zone):
    iso = dt.isoformat()
    with engine.connect() as conn:
        query = """
            SELECT timestamp, value, source
            FROM weather_data WHERE timestamp == ?
            AND zone = ?
        """
        rows = pd.read_sql(query, conn, params=(iso,zone,))
        if len(rows) == 0:
            return {"message": f"No rows for timestamp {iso} and zone {zone}"}
        return rows.to_dict(orient="records")


if __name__ == "__main__":

    print(select_by_zone(zone=(Zone.FR)))





