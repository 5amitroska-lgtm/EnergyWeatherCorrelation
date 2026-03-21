import sqlite3
from datetime import date, datetime
import os
class Electricity:
    def __init__(self,date):
        datetime = date.strftime('%Y-%m-%dT%H:00:00')
        DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
                SELECT value
                FROM electricity_price_data WHERE timestamp == ?
            """, (datetime,))

        row = cursor.fetchone()
        self.timestamp = datetime
        self.price = row[0] if row else None
        conn.close()

    def speak(self):
        print(f"Ahoj ja som cena elektriny pre timestamp {self.timestamp} a cena je {self.price}")

temp=Electricity(datetime(2026,2,3, 10, 0,0))
temp.speak()