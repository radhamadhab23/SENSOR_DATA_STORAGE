# lstm_model/preprocessor.py
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def preprocess_series(df, feature, seq_len=10):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df[[feature]])
    X, y = [], []
    for i in range(len(scaled) - seq_len):
        X.append(scaled[i:i+seq_len])
        y.append(scaled[i+seq_len])
    return np.array(X), np.array(y), scaler
