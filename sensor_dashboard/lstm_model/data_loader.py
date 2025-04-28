import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# lstm_model/data_loader.py
import pandas as pd
import mysql.connector

def load_weather_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Radha@969",
        database="weather_db"
    )
    df = pd.read_sql("SELECT timestamp, temperature, humidity FROM weather_data ORDER BY timestamp", conn)
    conn.close()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    return df
