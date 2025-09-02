from typing import Dict, Optional, List
from tabulate import tabulate

from .models import WeatherForecastResult

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
    def format_weather_table(weather_results: Dict[str, WeatherForecastResult]) -> str:
        """Format weather data into table"""
        if not weather_results:
            return "No data to display"

        date: Optional[str] = None
        for result in weather_results.values():
            if result.success and result.data:
                date = result.data.date
                break

        if not date:
            return "No data to display"

        table_data: List[List[str]] = []
        for city in CITIES:
            result = weather_results.get(city)
            if result and result.success and result.data:
                data = result.data
                table_data.append(
                    [
                        city,
                        f"{data.min_temp:.1f}°C",
                        f"{data.max_temp:.1f}°C",
                        f"{data.humidity:.0f}%",
                        f"{data.wind_speed:.1f} kph",
                        data.wind_direction,
                    ]
                )
            else:
                table_data.append([city, "N/A", "N/A", "N/A", "N/A", "N/A"])

        table = tabulate(table_data, headers=WeatherFormatter.HEADERS, tablefmt="grid")
        return f"Weather Forecast for {date}\n\n{table}"
