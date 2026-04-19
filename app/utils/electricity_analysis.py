import pandas as pd
from app.utils.enums import Zone
from datetime import datetime
from sqlalchemy import create_engine

#IN PROGRESS - TO DO

engine = create_engine('sqlite:///C:/Users/TUF/PythonLekcie/EnergyWeatherCorrelation/app/database/data.db', echo=False)

def find_highest_prices(fromDate: datetime, toDate: datetime, zone: Zone, limit: int):
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

def find_lowest_prices(fromDate: datetime, toDate: datetime, zone: Zone, limit: int):
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

if __name__ == "__main__":
    find_highest_prices("2026-01-02T00:00:00", "2026-01-03T23:00:00", "FR", 30)
    find_lowest_prices("2026-01-02T00:00:00", "2026-01-03T23:00:00", "FR", 30)