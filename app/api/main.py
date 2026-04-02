from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
engine = create_engine('sqlite:///C:/Users/TUF/PythonLekcie/EnergyWeatherCorrelation/app/database/data.db', echo=False)

app = FastAPI()

@app.get("/electricity/datetime")
def select_by_timestamp(dt: datetime):
    print(engine.url)
    with engine.connect() as conn:

        query = """
            SELECT id, timestamp, value, source
            FROM electricity_price_data
            WHERE timestamp = ?
        """

        rows = pd.read_sql(query, conn, params=(dt,))

        if len(rows) == 0:
            return {"message": f"No rows for timestamp {dt}"}

        return rows.to_dict(orient="records")

@app.get("/electricity/zone")
def select_by_zone(zone):
    print(engine.url)
    with engine.connect() as conn:

        query = """
            SELECT id, timestamp, value, source
            FROM electricity_price_data
            WHERE zone = ?
            order by timestamp DESC
        """

        rows = pd.read_sql(query, conn, params=(zone,))

        if len(rows) == 0:
            return {"message": f"No rows for timestamp {zone}"}

        return rows.to_dict(orient="records")


if __name__ == "__main__":

    select_by_timestamp("2026-03-01T09:00:00")





