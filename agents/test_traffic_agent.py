from traffic_agent import get_traffic_summary


test_cases = [
    ("Morning Peak", 8, 1),
    ("Midday", 13, 1),
    ("Evening Peak", 18, 1),
    ("Late Night", 23, 1),
    ("Saturday Afternoon", 14, 5)
]


for name, hour, day in test_cases:

    result = get_traffic_summary(
        baseline_minutes=30,
        hour=hour,
        day_of_week=day
    )

    print("\n-----------------------------")
    print(name)
    print("-----------------------------")

    print(
        "Traffic:",
        result["traffic_level"]
    )

    print(
        "Multiplier:",
        result["traffic_multiplier"]
    )

    print(
        "Estimated Time:",
        result["estimated_minutes"],
        "minutes"
    )