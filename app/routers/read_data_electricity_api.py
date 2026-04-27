from fastapi import FastAPI
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
from app.utils.enums import Zone
from fastapi import APIRouter
engine = create_engine('sqlite:///C:/Users/TUF/PythonLekcie/EnergyWeatherCorrelation/app/database/data.db', echo=False)

app = FastAPI()
router = APIRouter(
    prefix="/electricity",
    tags=["Electricity"]
)

@router.get("/datetime")
def select_by_timestamp(dt: datetime)-> dict:
    """select electricity prices by datetime"""
    iso = dt.isoformat()
    with engine.connect() as conn:

        query = """
            SELECT id, timestamp, value, source
            FROM electricity_price_data
            WHERE timestamp = ?
        """

        rows = pd.read_sql(query, conn, params=(iso,))

        if len(rows) == 0:
            return {"message": f"No rows for timestamp {iso}"}

        return rows.to_dict(orient="records")

@router.get("/zone")
def select_by_zone(zone: Zone) -> dict:
    """Select electricity prices by zone"""
    with engine.connect() as conn:

        query = """
            SELECT id, timestamp, value, source
            FROM electricity_price_data
            WHERE zone = ?
        """

        rows = pd.read_sql(query, conn, params=(zone.value,))

        if len(rows) == 0:
            return {"message": f"No rows for zone {zone}"}
        return rows.to_dict(orient="records")

@router.get("/zone/dailyAVG")
def electricity_daily_avg(zone: Zone) -> dict:
    """"select averaged electricity prices (one value per day) by zone"""
    with engine.connect() as conn:
        query = """
            SELECT date(timestamp) AS day, AVG(value) AS avg_price
            FROM electricity_price_data
            WHERE zone = ?
            GROUP BY day
            ORDER BY day DESC
        """
        rows = pd.read_sql(query, conn, params=(zone,))

        if len(rows) == 0:
            return {"message": f"No rows for timestamp {zone}"}

        return rows.to_dict(orient="records")

@router.get("/value")
def select_electricity_value(dt:datetime, zone: Zone) -> dict:
    """select value for timestamp and zone"""
    iso = dt.isoformat()
    with engine.connect() as conn:
        query = """
            SELECT value
            FROM electricity_price_data WHERE timestamp == ?
            AND zone = ?
        """
        rows = pd.read_sql(query, conn, params=(iso,zone,))
        if len(rows) == 0:
            return {"message": f"No rows for timestamp {iso} and zone {zone}"}
        return rows.to_dict(orient="records")

@router.get("/highestPrice")
def find_highest_prices(fromDate: datetime, toDate: datetime, zone: Zone, limit: int) -> dict:
    """select the highest prices in the range fromDate to toDate by zone
        and limit is the number how many the highest prices do you want to show"""
    with engine.connect() as conn:

        query = """
            SELECT id, timestamp, value, source
            FROM electricity_price_data
            WHERE timestamp >= ?
            AND timestamp <= ? 
            AND zone = ?
            order by value DESC
            limit ?
        """

        rows=pd.read_sql_query(query,conn, params=(fromDate, toDate, zone, limit))
        order_rows = pd.DataFrame(rows).sort_values(by=['timestamp'], ascending=False)
        print(order_rows)

@router.get("/lowestPrice")
def find_lowest_prices(fromDate: datetime, toDate: datetime, zone: Zone, limit: int) -> dict:
    """select the lowes prices in the range fromDate to toDate by zone
        and limit is the number how many the lowest prices do you want to show"""
    with engine.connect() as conn:

        query = """
            SELECT id, timestamp, value, source
            FROM electricity_price_data
            WHERE timestamp >= ?
            AND timestamp <= ? 
            AND zone = ?
            order by value ASC
            limit ?
        """

        rows=pd.read_sql_query(query,conn, params=(fromDate, toDate, zone, limit))
        order_rows = pd.DataFrame(rows).sort_values(by=['timestamp'], ascending=False)
        print(order_rows)

@router.get("/available_zones")
def select_all_available_zones_for_datetime(dt: datetime) -> list:
    """select all available zones for datetime"""
    dt_str = dt.strftime("%Y-%m-%dT%H:%M:%S")

    query = """
        SELECT zone
        FROM electricity_price_data
        WHERE timestamp = ?
    """

    with engine.connect() as conn:
        rows = pd.read_sql_query(query, conn, params=(dt_str,))

    return rows["zone"].tolist()



if __name__ == "__main__":

    print(select_all_available_zones_for_datetime(datetime(2026, 1, 1)))