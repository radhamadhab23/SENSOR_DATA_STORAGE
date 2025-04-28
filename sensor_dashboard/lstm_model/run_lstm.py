# lstm_model/run_lstm.py
# Inside run_lstm.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sensor_dashboard.lstm_model.preprocessor import preprocess_series
from sensor_dashboard.lstm_model.data_loader import load_weather_data
from sensor_dashboard.lstm_model.model import build_lstm_model
from sensor_dashboard.lstm_model.predict import predict_future_values

from datetime import datetime, timedelta

def run_prediction(feature='temperature', days=5):
    df = load_weather_data()
    X, y, scaler = preprocess_series(df, feature)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    model = build_lstm_model((X.shape[1], 1))
    model.fit(X, y, epochs=50, verbose=0)

    last_seq = X[-1].reshape(X.shape[1], 1)
    predictions = predict_future_values(model, last_seq, scaler, days)

    last_date = df.index[-1]
    dates = [(last_date + timedelta(days=i+1)).strftime('%Y-%m-%d') for i in range(days)]

    return list(zip(dates, predictions))
