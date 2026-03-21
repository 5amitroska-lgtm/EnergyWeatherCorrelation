import sqlite3
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import date

# Cesta k databáze
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database", "data.db"))
class Graf:

    def __init__(self, downsample, resample, date_from, date_to):
        self.downsample = downsample  # každý 10. riadok (10)
        self.resample = resample  # "1h"  # agregácia na hodinové priemery
        self.webgl = True  # WebGL rendering
        self.date_from = date_from
        self.date_to = date_to

    def load_zone(self, zone):
        conn = sqlite3.connect(DB_PATH)

        # --- CENY ---
        q_price = f"""
            SELECT timestamp, value
            FROM electricity_price_data
            WHERE source LIKE '{zone} - %'
                AND timestamp BETWEEN '{self.date_from}' AND '{self.date_to}'
            ORDER BY timestamp
        """
        df_price = pd.read_sql_query(q_price, conn)
        df_price["timestamp"] = pd.to_datetime(df_price["timestamp"], format="ISO8601")
        df_price = df_price.rename(columns={"value": "price"})

        # --- POČASIE ---
        q_weather = f"""
            SELECT timestamp, value, source
            FROM weather_data
            WHERE source LIKE '{zone}_%'
                AND timestamp BETWEEN '{self.date_from}' AND '{self.date_to}'
            ORDER BY timestamp
        """
        df_weather = pd.read_sql_query(q_weather, conn)
        conn.close()

        if df_weather.empty:
            return df_price

        df_weather["timestamp"] = pd.to_datetime(df_weather["timestamp"], format="ISO8601")
        df_weather["variable"] = df_weather["source"].str.replace(f"{zone}_", "", regex=False)

        # odstrániť textové hodnoty (weather_text)
        df_weather = df_weather[df_weather["value"].apply(lambda x: isinstance(x, (int, float)))]

        # odstrániť duplicity
        df_weather = (
            df_weather
            .groupby(["timestamp", "variable"], as_index=False)
            .agg({"value": "mean"})
        )

        # pivot
        df_weather = df_weather.pivot(
            index="timestamp",
            columns="variable",
            values="value"
        ).reset_index()

        # --- MERGE ---
        df = df_price.merge(df_weather, on="timestamp", how="left")

        # --- RESAMPLE (1h) ---
        df = (
            df.set_index("timestamp")
            .resample(self.resample)
            .mean()
            .reset_index()
        )

        # --- DOWNSAMPLE PO MERGE (najdôležitejšie!) ---
        df = df.iloc[::self.downsample]  # každý 30. bod → 30× rýchlejšie

        return df

    # --- GRAF: CENA + POČASIE ---
    def plot_zone(self, zone):
        df = self.load_zone(zone)

        fig = go.Figure()

        # Cena elektriny
        fig.add_trace(go.Scatter(
            x=df["timestamp"], y=df["price"],
            mode="lines",
            name="Cena elektriny",
            line=dict(color="red", width=2)
        ))

        # Teplota
        if "temperature" in df:
            fig.add_trace(go.Scatter(
                x=df["timestamp"], y=df["temperature"],
                mode="lines",
                name="Teplota",
                yaxis="y2",
                line=dict(color="blue", width=1)
            ))

        # Oblačnosť
        if "cloudcover" in df:
            fig.add_trace(go.Scatter(
                x=df["timestamp"], y=df["cloudcover"],
                mode="lines",
                name="Oblačnosť",
                yaxis="y3",
                line=dict(color="gray", width=1)
            ))

        # Zrážky
        if "precipitation" in df:
            fig.add_trace(go.Scatter(
                x=df["timestamp"], y=df["precipitation"],
                mode="lines",
                name="Zrážky",
                yaxis="y4",
                line=dict(color="green", width=1)
            ))

        fig.update_layout(
            title=f"Zóna {zone}: Cena elektriny + Počasie",
            xaxis=dict(title="Čas"),
            yaxis=dict(title="Cena [€/MWh]", side="left"),
            yaxis2=dict(title="Teplota [°C]", overlaying="y", side="right"),
            yaxis3=dict(title="Oblačnosť [%]", overlaying="y", side="right", position=0.92),
            yaxis4=dict(title="Zrážky [mm]", overlaying="y", side="right", position=0.97),
            height=650,
            legend=dict(x=0.01, y=0.99)
        )

        fig.show()

# --- TEST ---
if __name__ == "__main__":
    graf= Graf(1,"1h", date(2026, 1, 1), date(2026, 1, 31))
    zone = "CH"
    graf.plot_zone(zone)
    zone = "AT"
    graf.plot_zone(zone)
