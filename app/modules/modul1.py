import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os

# Správna cesta k databáze
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "data.db")
DB_PATH = os.path.abspath(DB_PATH)

def plot_data():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query("""
        SELECT timestamp, value, source
        FROM electricity_price_data
        ORDER BY timestamp ASC
    """, conn)

    conn.close()

    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], df["value"], marker="o")

    plt.title("Hodnoty v čase")
    plt.xlabel("Čas")
    plt.ylabel("Hodnota")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_by_source():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT timestamp, value, source
        FROM electricity_price_data
        ORDER BY timestamp ASC
    """, conn)
    conn.close()

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    plt.figure(figsize=(12, 6))

    for src in df["source"].unique():
        subset = df[df["source"] == src]
        plt.plot(subset["timestamp"], subset["value"], label=src)

    plt.title("Hodnoty podľa zdroja")
    plt.xlabel("Čas")
    plt.ylabel("Hodnota")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_interactive():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT timestamp, value, source FROM electricity_price_data", conn)
    conn.close()

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fig = px.line(df, x="timestamp", y="value", color="source", title="Interaktívny graf")
    fig.show()
