import os
import joblib
import pandas as pd


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "travel_time_model.pkl"
)


def load_model():
    return joblib.load(MODEL_PATH)


def predict_travel_time(
    distance_km,
    baseline_minutes,
    hour,
    day_of_week
):
    """
    Predict travel time using the trained prototype model.
    """

    model = load_model()

    peak_hour = int(
        (7 <= hour <= 10) or
        (17 <= hour <= 21)
    )

    features = pd.DataFrame([{
        "distance_km": distance_km,
        "hour": hour,
        "day_of_week": day_of_week,
        "peak_hour": peak_hour,
        "baseline_minutes": baseline_minutes
    }])

    prediction = model.predict(features)[0]

    return max(
        round(prediction, 1),
        baseline_minutes
    )