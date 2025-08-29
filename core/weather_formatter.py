from typing import Any
from tabulate import tabulate

CITIES = ["Chisinau", "Madrid", "Kyiv", "Amsterdam"]


class WeatherFormatter:
    """Class for formatting weather data into table"""

    HEADERS = [
        "City",
        "Min Temp",
        "Max Temp",
        "Humidity",
        "Wind Speed",
        "Wind Direction",
    ]

    @staticmethod
    def format_weather_table(weather_data: dict[str, dict[str, Any]]) -> str:
        """Format weather data into table"""
        if not weather_data:
            return "No data to display"

        date = next((data.get("date") for data in weather_data.values() if data), None)
        if not date:
            return "No data to display"

        table_data = []
        for city in CITIES:
            data = weather_data.get(city)
            if data:
                table_data.append(
                    [
                        city,
                        f"{data['min_temp']:.1f}°C",
                        f"{data['max_temp']:.1f}°C",
                        f"{data['humidity']:.0f}%",
                        f"{data['wind_speed']:.1f} kph",
                        data["wind_direction"],
                    ]
                )
            else:
                table_data.append([city, "N/A", "N/A", "N/A", "N/A", "N/A"])

        table = tabulate(table_data, headers=WeatherFormatter.HEADERS, tablefmt="grid")
        return f"Weather Forecast for {date}\n\n{table}"
