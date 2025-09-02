import os
import sys
import logging
from typing import Dict
from dotenv import load_dotenv

from core.weather_api import WeatherAPI
from core.weather_formatter import CITIES, WeatherFormatter
from core.models import WeatherForecastResult

logging.basicConfig(level=logging.INFO, format="%(message)s")
load_dotenv()


def get_api_key() -> str:
    """Retrieve API key from environment variables"""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        logging.error("WEATHER_API_KEY not found in environment variables.")
        logging.info("Setup options:")
        logging.info("1. Create .env file and add: WEATHER_API_KEY=your_api_key_here")
        logging.info(
            "2. Set environment variable: export WEATHER_API_KEY='your_api_key_here'"
        )
        logging.info("Get API key at: https://www.weatherapi.com/signup.aspx")
        raise RuntimeError("Missing WEATHER_API_KEY")
    return api_key


def main() -> None:
    """Main application function"""
    try:
        api_key = get_api_key()
        weather_api = WeatherAPI(api_key)

        logging.info("Getting tomorrow's weather forecast...")

        weather_results: Dict[str, WeatherForecastResult] = {
            city: weather_api.get_tomorrow_forecast(city) for city in CITIES
        }

        formatter = WeatherFormatter()
        result = formatter.format_weather_table(weather_results)

        print(result)

    except RuntimeError as e:
        logging.critical(e)
        sys.exit(1)

    except Exception as e:
        logging.exception("Unexpected error occurred")
        sys.exit(1)


if __name__ == "__main__":
    main()
