from flask import Flask, render_template, jsonify
import mysql.connector
from datetime import datetime
import pytz

# Use your local timezone, e.g., Asia/Kolkata
local_tz = pytz.timezone("Asia/Kolkata")
timestamp = datetime.now(local_tz)


app = Flask(__name__)

def get_latest_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Radha@969",
        database="SensorDataDB"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM SensorReadings ORDER BY timestamp DESC LIMIT 10")
    result = cursor.fetchall()
    conn.close()
    return result[::-1]  # reverse for chronological order

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(get_latest_data())

if __name__ == '__main__':
    app.run(debug=True)
