# lstm_model/predict.py
import numpy as np
from datetime import timedelta

def predict_future_values(model, last_seq, scaler, days=5):
    predictions = []
    seq_len = len(last_seq)

    for _ in range(days):
        pred_input = last_seq.reshape(1, seq_len, 1)
        pred = model.predict(pred_input, verbose=0)[0][0]
        predictions.append(pred)
        last_seq = np.append(last_seq[1:], [[pred]], axis=0)

    predicted_values = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
    return predicted_values
