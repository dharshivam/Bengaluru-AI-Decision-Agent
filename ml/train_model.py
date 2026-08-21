import os
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


# =========================================================
# CREATE PROTOTYPE DATA
# =========================================================

np.random.seed(42)

rows = 2000

distance = np.random.uniform(3, 40, rows)

hour = np.random.randint(6, 23, rows)

day_of_week = np.random.randint(0, 7, rows)

baseline_minutes = (
    distance / 30 * 60
)


# Peak hour indicator
peak_hour = np.where(
    ((hour >= 7) & (hour <= 10)) |
    ((hour >= 17) & (hour <= 21)),
    1,
    0
)


# Simulated Bengaluru traffic effect
traffic_multiplier = np.where(
    peak_hour == 1,
    np.random.uniform(1.4, 2.2, rows),
    np.random.uniform(0.9, 1.3, rows)
)


# Simulated actual travel time
travel_time = (
    baseline_minutes *
    traffic_multiplier
    +
    np.random.normal(0, 5, rows)
)


travel_time = np.maximum(
    travel_time,
    baseline_minutes
)


# =========================================================
# DATAFRAME
# =========================================================

df = pd.DataFrame({

    "distance_km": distance,

    "hour": hour,

    "day_of_week": day_of_week,

    "peak_hour": peak_hour,

    "baseline_minutes": baseline_minutes,

    "travel_time_minutes": travel_time
})


print("\nDataset:")
print(df.head())


# =========================================================
# FEATURES / TARGET
# =========================================================

X = df[
    [
        "distance_km",
        "hour",
        "day_of_week",
        "peak_hour",
        "baseline_minutes"
    ]
]

y = df["travel_time_minutes"]


# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# =========================================================
# MODEL
# =========================================================

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)


print("\nTraining model...")

model.fit(
    X_train,
    y_train
)


# =========================================================
# EVALUATION
# =========================================================

predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)


print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")

print(
    f"Mean Absolute Error: "
    f"{mae:.2f} minutes"
)

print(
    f"R² Score: "
    f"{r2:.3f}"
)


# =========================================================
# SAVE MODEL
# =========================================================

model_path = os.path.join(
    os.path.dirname(__file__),
    "travel_time_model.pkl"
)

joblib.dump(
    model,
    model_path
)


print("\nModel saved to:")

print(model_path)