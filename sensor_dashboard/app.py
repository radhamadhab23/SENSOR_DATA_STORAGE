# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import requests
from datetime import datetime, date, timedelta
import csv
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# ✅ Set up logging
logging.basicConfig(level=logging.INFO)

# ✅ Get credentials from environment
API_KEY = os.environ.get('API_KEY')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# ✅ MySQL DB connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=DB_PASSWORD,
        database="weather_db"
    )

# # ✅ Route: Get current weather from API & store in DB
# @app.route('/api/weather', methods=['GET'])
# def get_current_weather():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
        
#         # First try to get today's latest temperature
#         today = date.today().strftime('%Y-%m-%d')
#         cursor.execute("""
#             SELECT * FROM weather_data 
#             WHERE DATE(timestamp) = %s 
#             ORDER BY timestamp DESC 
#             LIMIT 1
#         """, (today,))
        
#         latest_data = cursor.fetchone()
        
#         # If no data for today, get the last valid data
#         if not latest_data:
#             cursor.execute("""
#                 SELECT * FROM weather_data 
#                 ORDER BY timestamp DESC 
#                 LIMIT 1
#             """)
#             latest_data = cursor.fetchone()
        
#         cursor.close()
#         conn.close()
        
#         if latest_data:
#             return jsonify({
#                 'temperature': latest_data['temperature'],
#                 'humidity': latest_data['humidity'],
#                 'timestamp': latest_data['timestamp']
#             })
#         else:
#             return jsonify({
#                 'temperature': 0,
#                 'humidity': 0,
#                 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             })
            
#     except Exception as e:
#         if 'conn' in locals():
#             conn.close()
#         return jsonify({
#             'temperature': 0,
#             'humidity': 0,
#             'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         })

# ✅ Route: Fetch latest 20 historical records
@app.route('/api/weather/history', methods=['GET'])
def get_weather_history():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 20")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(records)

# ✅ Route: Import CSV data to DB
@app.route('/api/weather/import_csv', methods=['POST'])
def import_csv():
    file_path = 'data1.csv'
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row = {k.strip(): v.strip() for k, v in row.items()}
                if not all(k in row for k in ('timestamp', 'temperature', 'humidity')):
                    return jsonify({"error": "CSV must contain 'timestamp', 'temperature', 'humidity'."}), 400

                cursor.execute(
                    "INSERT INTO weather_data (temperature, humidity, timestamp) VALUES (%s, %s, %s)",
                    (row['temperature'], row['humidity'], row['timestamp'])
                )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "CSV imported successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Route: Today's data
@app.route('/api/weather/today', methods=['GET'])
def get_today_weather():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        today = date.today().strftime('%Y-%m-%d')
        query = "SELECT * FROM weather_data WHERE DATE(timestamp) = %s"
        cursor.execute(query, (today,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

# ✅ Route: Yesterday's data
@app.route('/api/weather/yesterday', methods=['GET'])
def get_yesterday_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    yesterday = (datetime.now() - timedelta(days=1)).date()
    cursor.execute("""
        SELECT * FROM weather_data
        WHERE DATE(timestamp) = %s
        ORDER BY timestamp
    """, (yesterday,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# ✅ Route: Last 7 days
@app.route('/api/weather/last7days', methods=['GET'])
def get_last_7_days():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    seven_days_ago = (datetime.now() - timedelta(days=7)).date()
    cursor.execute("""
        SELECT * FROM weather_data
        WHERE DATE(timestamp) >= %s
        ORDER BY timestamp
    """, (seven_days_ago,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# ✅ Prediction (Unified)
from sensor_dashboard.lstm_model.run_lstm import run_prediction
@app.route('/api/weather/predict5days', methods=['GET'])
def predict_5_days():
    try:
        predictions = run_prediction(days=5)  # Each item = (date, temp)
        results = []

        for item in predictions:
            date_str, temp = item
            results.append({
                "date": date_str,
                "temperature": float(temp)
            })

        return jsonify({"predictions": results})
    except Exception as e:
        return jsonify({"error": str(e)})


# ✅ Run server
if __name__ == '__main__':
    app.run(debug=True)
