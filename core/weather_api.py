import requests
import logging
from typing import Any

logging.basicConfig(level=logging.INFO)


class WeatherAPI:
    """Class for working with WeatherAPI.com"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.weatherapi.com/v1/forecast.json"

    def get_tomorrow_forecast(self, city: str) -> dict[str, Any] | None:
        """Get tomorrow's weather forecast for specified city"""
        try:
            response = requests.get(
                self.base_url,
                params={
                    "key": self.api_key,
                    "q": city,
                    "days": 2,
                    "aqi": "no",
                    "alerts": "no",
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            forecast_days = data.get("forecast", {}).get("forecastday", [])
            if len(forecast_days) < 2:
                logging.warning("Insufficient data for city %s", city)
                return None

            tomorrow = forecast_days[1]
            day_data = tomorrow.get("day", {})
            hours = tomorrow.get("hour", [])

            wind_direction = hours[len(hours) // 2].get("wind_dir") if hours else "N/A"

            return {
                "date": tomorrow.get("date"),
                "min_temp": day_data.get("mintemp_c"),
                "max_temp": day_data.get("maxtemp_c"),
                "humidity": day_data.get("avghumidity"),
                "wind_speed": day_data.get("maxwind_kph"),
                "wind_direction": wind_direction,
            }

        except (requests.RequestException, ValueError, KeyError) as e:
            logging.error("Error requesting data for city %s: %s", city, e)
            return None
