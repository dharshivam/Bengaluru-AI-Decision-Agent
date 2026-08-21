"""
Decision Agent
--------------

Combines:
1. OSRM baseline travel time
2. Traffic Intelligence Agent
3. ML travel-time prediction
4. Weather Intelligence

Returns:
- Final estimated travel time
- Traffic condition
- Weather condition
- Recommended departure time
- Explanation
"""

from datetime import datetime, timedelta

from agents.traffic_agent import get_traffic_summary


# =========================================================
# WEATHER IMPACT
# =========================================================

def calculate_weather_impact(weather_data):
    """
    Estimate additional travel-time impact based on
    current weather conditions.

    Returns:
        weather_multiplier
        weather_extra_minutes
        weather_level
        weather_message
    """

    # -----------------------------------------------------
    # DEFAULT WEATHER
    # -----------------------------------------------------

    if not weather_data or "error" in weather_data:

        return {
            "weather_multiplier": 1.00,
            "weather_extra_minutes": 0,
            "weather_level": "Unavailable",
            "weather_message":
                "Weather information is currently unavailable."
        }

    rain = float(
        weather_data.get("rain") or 0
    )

    precipitation = float(
        weather_data.get("precipitation") or 0
    )

    wind_speed = float(
        weather_data.get("wind_speed") or 0
    )

    weather_code = weather_data.get(
        "weather_code"
    )

    # -----------------------------------------------------
    # WEATHER IMPACT
    # -----------------------------------------------------

    weather_multiplier = 1.00
    weather_level = "Clear"
    weather_message = (
        "Weather conditions are favorable for travel."
    )

    # Heavy rain
    if rain >= 5 or precipitation >= 5:

        weather_multiplier = 1.20

        weather_level = "Heavy Rain"

        weather_message = (
            "Heavy rain may slow traffic and increase "
            "travel time. Extra caution is recommended."
        )

    # Moderate rain
    elif rain > 0 or precipitation > 0:

        weather_multiplier = 1.10

        weather_level = "Rain"

        weather_message = (
            "Rain may slightly increase travel time "
            "and road congestion."
        )

    # Strong wind
    elif wind_speed >= 30:

        weather_multiplier = 1.08

        weather_level = "Strong Wind"

        weather_message = (
            "Strong winds may slightly affect driving "
            "conditions."
        )

    # Cloudy / overcast weather codes
    elif weather_code in [
        1,
        2,
        3
    ]:

        weather_multiplier = 1.02

        weather_level = "Cloudy"

        weather_message = (
            "Cloudy weather conditions are generally "
            "suitable for travel."
        )

    # Thunderstorm
    elif weather_code in [
        95,
        96,
        99
    ]:

        weather_multiplier = 1.25

        weather_level = "Thunderstorm"

        weather_message = (
            "Thunderstorm conditions may significantly "
            "affect travel time and road safety."
        )

    # -----------------------------------------------------
    # RETURN
    # -----------------------------------------------------

    return {

        "weather_multiplier":
            weather_multiplier,

        "weather_extra_minutes":
            0,

        "weather_level":
            weather_level,

        "weather_message":
            weather_message
    }


# =========================================================
# FINAL TRAVEL-TIME ESTIMATION
# =========================================================

def calculate_final_travel_time(
    distance_km,
    baseline_minutes,
    hour,
    day_of_week,
    ml_prediction=None,
    weather_data=None
):
    """
    Combine:

    OSRM baseline
        +
    Traffic Intelligence
        +
    ML prediction
        +
    Weather impact
    """

    # -----------------------------------------------------
    # TRAFFIC INTELLIGENCE
    # -----------------------------------------------------

    traffic = get_traffic_summary(
        baseline_minutes=baseline_minutes,
        hour=hour,
        day_of_week=day_of_week
    )

    traffic_time = float(
        traffic["estimated_minutes"]
    )

    # -----------------------------------------------------
    # WEATHER INTELLIGENCE
    # -----------------------------------------------------

    weather = calculate_weather_impact(
        weather_data
    )

    weather_multiplier = float(
        weather["weather_multiplier"]
    )

    weather_level = weather[
        "weather_level"
    ]

    weather_message = weather[
        "weather_message"
    ]

    # -----------------------------------------------------
    # ML + TRAFFIC COMBINATION
    # -----------------------------------------------------

    if ml_prediction is not None:

        ml_prediction = float(
            ml_prediction
        )

        # Traffic = 60%
        # ML = 40%

        base_final_minutes = (
            traffic_time * 0.60
            +
            ml_prediction * 0.40
        )

        prediction_source = (
            "Traffic Intelligence + ML + Weather"
        )

    else:

        base_final_minutes = (
            traffic_time
        )

        prediction_source = (
            "Traffic Intelligence + Weather"
        )

    # -----------------------------------------------------
    # APPLY WEATHER
    # -----------------------------------------------------

    final_minutes = (
        base_final_minutes
        *
        weather_multiplier
    )

    # -----------------------------------------------------
    # WEATHER EXTRA TIME
    # -----------------------------------------------------

    weather_extra_minutes = (
        final_minutes
        -
        base_final_minutes
    )

    # -----------------------------------------------------
    # SANITY CHECK
    # -----------------------------------------------------

    minimum_time = float(
        baseline_minutes
    )

    if final_minutes < minimum_time:

        final_minutes = minimum_time

    # -----------------------------------------------------
    # BUILD EXPLANATION
    # -----------------------------------------------------

    traffic_message = traffic.get(
        "message",
        "Traffic intelligence analyzed the route."
    )

    explanation = (
        f"{traffic_message} "
        f"{weather_message}"
    )

    # -----------------------------------------------------
    # RETURN RESULT
    # -----------------------------------------------------

    return {

        "distance_km":
            round(
                distance_km,
                2
            ),

        "baseline_minutes":
            round(
                baseline_minutes,
                2
            ),

        # -----------------------------
        # TRAFFIC
        # -----------------------------

        "traffic_level":
            traffic["traffic_level"],

        "traffic_multiplier":
            traffic["traffic_multiplier"],

        "traffic_estimated_minutes":
            round(
                traffic_time,
                2
            ),

        # -----------------------------
        # ML
        # -----------------------------

        "ml_prediction":
            (
                round(
                    ml_prediction,
                    2
                )
                if ml_prediction is not None
                else None
            ),

        # -----------------------------
        # WEATHER
        # -----------------------------

        "weather_level":
            weather_level,

        "weather_multiplier":
            round(
                weather_multiplier,
                2
            ),

        "weather_extra_minutes":
            round(
                weather_extra_minutes,
                2
            ),

        "weather_message":
            weather_message,

        # -----------------------------
        # FINAL
        # -----------------------------

        "final_minutes":
            round(
                final_minutes,
                2
            ),

        "prediction_source":
            prediction_source,

        "explanation":
            explanation
    }


# =========================================================
# DEPARTURE TIME
# =========================================================

def calculate_recommended_departure(
    arrival_time,
    travel_minutes,
    safety_buffer=10
):
    """
    Calculate recommended departure time.
    """

    today = datetime.today().date()

    arrival_datetime = datetime.combine(
        today,
        arrival_time
    )

    departure_datetime = (
        arrival_datetime
        -
        timedelta(
            minutes=
            travel_minutes
            +
            safety_buffer
        )
    )

    return departure_datetime


# =========================================================
# COMPLETE JOURNEY DECISION
# =========================================================

def make_journey_decision(
    distance_km,
    baseline_minutes,
    arrival_time,
    hour,
    day_of_week,
    ml_prediction=None,
    weather_data=None,
    safety_buffer=10
):
    """
    Complete AI journey decision pipeline.

    Flow:

    Location
        ↓
    OSRM Route
        ↓
    Traffic Intelligence
        ↓
    ML Prediction
        ↓
    Weather Intelligence
        ↓
    Weighted Final Travel Time
        ↓
    Safety Buffer
        ↓
    Recommended Departure
    """

    # -----------------------------------------------------
    # FINAL TRAVEL-TIME PREDICTION
    # -----------------------------------------------------

    prediction = calculate_final_travel_time(

        distance_km=distance_km,

        baseline_minutes=
            baseline_minutes,

        hour=hour,

        day_of_week=
            day_of_week,

        ml_prediction=
            ml_prediction,

        weather_data=
            weather_data
    )

    # -----------------------------------------------------
    # RECOMMENDED DEPARTURE
    # -----------------------------------------------------

    departure_time = (
        calculate_recommended_departure(

            arrival_time=
                arrival_time,

            travel_minutes=
                prediction[
                    "final_minutes"
                ],

            safety_buffer=
                safety_buffer
        )
    )

    # -----------------------------------------------------
    # FINAL DECISION
    # -----------------------------------------------------

    return {

        **prediction,

        "recommended_departure":
            departure_time,

        "required_arrival":
            arrival_time,

        "safety_buffer":
            safety_buffer
    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    from datetime import time

    # Sample weather data
    sample_weather = {

        "temperature": 24.5,

        "humidity": 82,

        "apparent_temperature": 25.1,

        "precipitation": 2.0,

        "rain": 2.0,

        "weather_code": 61,

        "wind_speed": 12,

        "time":
            "2026-08-21T18:00"
    }

    result = make_journey_decision(

        distance_km=30,

        baseline_minutes=34,

        arrival_time=
            time(19, 0),

        hour=18,

        day_of_week=4,

        ml_prediction=42,

        weather_data=
            sample_weather,

        safety_buffer=10
    )

    print("\n===================================")
    print("       JOURNEY DECISION TEST")
    print("===================================")

    print(
        "Distance:",
        result["distance_km"],
        "km"
    )

    print(
        "Baseline:",
        result["baseline_minutes"],
        "minutes"
    )

    print(
        "Traffic:",
        result["traffic_level"]
    )

    print(
        "Traffic Time:",
        result["traffic_estimated_minutes"],
        "minutes"
    )

    print(
        "ML Prediction:",
        result["ml_prediction"],
        "minutes"
    )

    print(
        "Weather:",
        result["weather_level"]
    )

    print(
        "Weather Multiplier:",
        result["weather_multiplier"]
    )

    print(
        "Weather Extra Time:",
        result["weather_extra_minutes"],
        "minutes"
    )

    print(
        "FINAL ETA:",
        result["final_minutes"],
        "minutes"
    )

    print(
        "Prediction Source:",
        result["prediction_source"]
    )

    print(
        "Leave By:",
        result[
            "recommended_departure"
        ].strftime("%I:%M %p")
    )

    print(
        "\nReason:",
        result["explanation"]
    )

    print("===================================\n")