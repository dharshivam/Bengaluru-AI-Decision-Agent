from weather_agent import get_weather


# Bengaluru coordinates
latitude = 12.9716
longitude = 77.5946


weather = get_weather(
    latitude,
    longitude
)


print("\n===== BENGALURU WEATHER =====")

if "error" in weather:

    print("Error:", weather["error"])

else:

    print(
        "Temperature:",
        weather["temperature"],
        "°C"
    )

    print(
        "Humidity:",
        weather["humidity"],
        "%"
    )

    print(
        "Feels Like:",
        weather["apparent_temperature"],
        "°C"
    )

    print(
        "Rain:",
        weather["rain"],
        "mm"
    )

    print(
        "Precipitation:",
        weather["precipitation"],
        "mm"
    )

    print(
        "Wind:",
        weather["wind_speed"],
        "km/h"
    )

    print(
        "Time:",
        weather["time"]
    )