import requests


# =========================================================
# WEATHER CODE DESCRIPTION
# =========================================================

def get_weather_description(weather_code):

    weather_codes = {
        0: "Clear sky",

        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",

        45: "Fog",
        48: "Depositing rime fog",

        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",

        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",

        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",

        66: "Light freezing rain",
        67: "Heavy freezing rain",

        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",

        77: "Snow grains",

        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",

        85: "Slight snow showers",
        86: "Heavy snow showers",

        95: "Thunderstorm",

        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }

    return weather_codes.get(
        weather_code,
        "Unknown weather"
    )


# =========================================================
# WEATHER IMPACT ANALYSIS
# =========================================================

def analyze_weather_impact(
    precipitation,
    rain,
    wind_speed,
    weather_code
):

    precipitation = precipitation or 0
    rain = rain or 0
    wind_speed = wind_speed or 0

    description = get_weather_description(
        weather_code
    )

    # -----------------------------------------------------
    # SEVERE WEATHER
    # -----------------------------------------------------

    if weather_code in [95, 96, 99]:

        return {
            "severity": "Severe",
            "impact": "High",
            "buffer_minutes": 15,
            "message": (
                "Thunderstorm conditions detected. "
                "Travel may take significantly longer."
            )
        }

    # -----------------------------------------------------
    # HEAVY RAIN
    # -----------------------------------------------------

    if (
        rain >= 4
        or precipitation >= 4
        or weather_code in [65, 67, 82]
    ):

        return {
            "severity": "Heavy Rain",
            "impact": "High",
            "buffer_minutes": 15,
            "message": (
                "Heavy rain detected. "
                "Road conditions may reduce travel speed."
            )
        }

    # -----------------------------------------------------
    # MODERATE RAIN
    # -----------------------------------------------------

    if (
        rain >= 1
        or precipitation >= 1
        or weather_code in [
            51,
            53,
            55,
            61,
            63,
            80,
            81
        ]
    ):

        return {
            "severity": "Rain",
            "impact": "Medium",
            "buffer_minutes": 10,
            "message": (
                "Rain detected. "
                "Additional travel time is recommended."
            )
        }

    # -----------------------------------------------------
    # HIGH WIND
    # -----------------------------------------------------

    if wind_speed >= 35:

        return {
            "severity": "High Wind",
            "impact": "Medium",
            "buffer_minutes": 10,
            "message": (
                "Strong winds detected. "
                "Travel conditions may be affected."
            )
        }

    # -----------------------------------------------------
    # FOG
    # -----------------------------------------------------

    if weather_code in [45, 48]:

        return {
            "severity": "Fog",
            "impact": "Medium",
            "buffer_minutes": 10,
            "message": (
                "Fog detected. "
                "Reduced visibility may increase travel time."
            )
        }

    # -----------------------------------------------------
    # NORMAL WEATHER
    # -----------------------------------------------------

    return {
        "severity": "Normal",
        "impact": "Low",
        "buffer_minutes": 0,
        "message": (
            "Weather conditions are suitable for normal travel."
        )
    }


# =========================================================
# MAIN WEATHER AGENT
# =========================================================

def get_weather(latitude, longitude):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current="
        "temperature_2m,"
        "relative_humidity_2m,"
        "apparent_temperature,"
        "precipitation,"
        "rain,"
        "weather_code,"
        "wind_speed_10m"
        "&timezone=Asia%2FKolkata"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        current = data.get(
            "current",
            {}
        )

        temperature = current.get(
            "temperature_2m"
        )

        humidity = current.get(
            "relative_humidity_2m"
        )

        apparent_temperature = current.get(
            "apparent_temperature"
        )

        precipitation = current.get(
            "precipitation"
        ) or 0

        rain = current.get(
            "rain"
        ) or 0

        weather_code = current.get(
            "weather_code"
        )

        wind_speed = current.get(
            "wind_speed_10m"
        ) or 0

        # -------------------------------------------------
        # WEATHER ANALYSIS
        # -------------------------------------------------

        weather_impact = analyze_weather_impact(

            precipitation=precipitation,

            rain=rain,

            wind_speed=wind_speed,

            weather_code=weather_code
        )

        # -------------------------------------------------
        # FINAL WEATHER RESULT
        # -------------------------------------------------

        return {

            "temperature": temperature,

            "humidity": humidity,

            "apparent_temperature": (
                apparent_temperature
            ),

            "precipitation": precipitation,

            "rain": rain,

            "weather_code": weather_code,

            "weather_description": (
                get_weather_description(
                    weather_code
                )
            ),

            "wind_speed": wind_speed,

            "time": current.get(
                "time"
            ),

            # AI weather intelligence
            "weather_severity": (
                weather_impact["severity"]
            ),

            "weather_impact": (
                weather_impact["impact"]
            ),

            "weather_buffer_minutes": (
                weather_impact["buffer_minutes"]
            ),

            "weather_message": (
                weather_impact["message"]
            )
        }

    except Exception as e:

        return {
            "error": str(e)
        }