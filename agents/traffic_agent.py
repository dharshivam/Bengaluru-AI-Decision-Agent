"""
Traffic Intelligence Agent
--------------------------

Phase 2 of Bengaluru AI Urban Decision Agent.

This module estimates traffic conditions using:
- Distance
- Baseline route duration
- Departure hour
- Day of week

IMPORTANT:
This is currently a prototype traffic intelligence layer.
It does NOT claim to receive live traffic from OSRM.
A real-time traffic API can be plugged into this agent later.
"""


# =========================================================
# TRAFFIC CLASSIFICATION
# =========================================================

def classify_traffic(hour, day_of_week):
    """
    Estimate traffic level based on Bengaluru peak-hour patterns.

    Parameters
    ----------
    hour : int
        Hour of departure (0-23)

    day_of_week : int
        Monday = 0
        Sunday = 6

    Returns
    -------
    str
        LOW / MODERATE / HIGH / SEVERE
    """

    # Weekend
    if day_of_week >= 5:

        if 11 <= hour <= 21:
            return "MODERATE"

        return "LOW"


    # Weekday morning peak
    if 7 <= hour <= 10:
        return "HIGH"


    # Weekday evening peak
    if 16 <= hour <= 20:
        return "SEVERE"


    # Midday
    if 11 <= hour <= 15:
        return "MODERATE"


    # Early morning / late night
    return "LOW"


# =========================================================
# TRAFFIC MULTIPLIER
# =========================================================

def get_traffic_multiplier(traffic_level):
    """
    Convert traffic level into an estimated
    travel-time multiplier.
    """

    multipliers = {
        "LOW": 1.00,
        "MODERATE": 1.20,
        "HIGH": 1.45,
        "SEVERE": 1.80
    }

    return multipliers.get(
        traffic_level,
        1.00
    )


# =========================================================
# ESTIMATE TRAFFIC TRAVEL TIME
# =========================================================

def estimate_traffic_time(
    baseline_minutes,
    hour,
    day_of_week
):
    """
    Estimate travel time after applying
    traffic intelligence.
    """

    traffic_level = classify_traffic(
        hour,
        day_of_week
    )

    multiplier = get_traffic_multiplier(
        traffic_level
    )

    estimated_minutes = (
        baseline_minutes * multiplier
    )

    return {
        "traffic_level": traffic_level,
        "traffic_multiplier": multiplier,
        "baseline_minutes": round(
            baseline_minutes,
            2
        ),
        "estimated_minutes": round(
            estimated_minutes,
            2
        )
    }


# =========================================================
# TRAFFIC SUMMARY
# =========================================================

def get_traffic_summary(
    baseline_minutes,
    hour,
    day_of_week
):
    """
    Generate a human-readable traffic explanation.
    """

    result = estimate_traffic_time(
        baseline_minutes,
        hour,
        day_of_week
    )

    traffic_level = result["traffic_level"]
    estimated_minutes = result["estimated_minutes"]

    if traffic_level == "LOW":

        message = (
            "Traffic conditions are expected to be light. "
            "The route should remain close to the baseline "
            "routing duration."
        )

    elif traffic_level == "MODERATE":

        message = (
            "Moderate traffic is expected. "
            "Additional travel time has been added "
            "to the baseline route estimate."
        )

    elif traffic_level == "HIGH":

        message = (
            "High traffic is expected during this period. "
            "The system has increased the expected journey "
            "duration accordingly."
        )

    else:

        message = (
            "Severe traffic conditions are expected. "
            "The system has applied a significant delay "
            "factor to reduce the risk of late arrival."
        )

    return {
        **result,
        "message": message
    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    result = get_traffic_summary(
        baseline_minutes=34,
        hour=18,
        day_of_week=2
    )

    print("\n===================================")
    print("   TRAFFIC INTELLIGENCE TEST")
    print("===================================")

    print(
        f"Traffic Level     : "
        f"{result['traffic_level']}"
    )

    print(
        f"Traffic Multiplier: "
        f"{result['traffic_multiplier']}x"
    )

    print(
        f"Baseline Time     : "
        f"{result['baseline_minutes']} min"
    )

    print(
        f"Estimated Time    : "
        f"{result['estimated_minutes']} min"
    )

    print(
        f"\nExplanation:\n"
        f"{result['message']}"
    )

    print("===================================\n")