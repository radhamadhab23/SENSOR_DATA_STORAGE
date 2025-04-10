import mysql.connector
import time
from datetime import datetime
import random  # For simulating sensor data

# Connect to MySQL once
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Radha@969",
    database="SensorDataDB"
)
cursor = conn.cursor()

print("⏳ Starting sensor data logging every 1 minute...")

try:
    while True:
        # Simulate sensor data (replace this with actual sensor readings later)
        temperature = round(random.uniform(25, 35), 2)  # Simulate 25°C to 35°C
        humidity = round(random.uniform(50, 80), 2)     # Simulate 50% to 80%
        timestamp = datetime.now()

        # Insert into database
        query = "INSERT INTO SensorReadings (temperature, humidity, timestamp) VALUES (%s, %s, %s)"
        cursor.execute(query, (temperature, humidity, timestamp))
        conn.commit()

        print(f"✅ {timestamp}: Temp={temperature}°C, Humidity={humidity}% → Stored in DB")

        time.sleep(60)  # Wait for 1 minute

except KeyboardInterrupt:
    print("\n🛑 Logging stopped by user.")

finally:
    cursor.close()
    conn.close()
