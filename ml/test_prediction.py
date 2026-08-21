from predict import predict_travel_time


distance = 30.4
baseline_minutes = 34

predicted_time = predict_travel_time(
    distance_km=distance,
    baseline_minutes=baseline_minutes,
    hour=18,
    day_of_week=4
)

print(
    f"Predicted travel time: "
    f"{predicted_time} minutes"
)