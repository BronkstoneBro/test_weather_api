import pytest
import requests
from unittest.mock import Mock, patch
from core.weather_api import WeatherAPI


class TestWeatherAPI:
    """Test cases for WeatherAPI class"""

    def setup_method(self):
        """Setup test instance"""
        self.api_key = "test_api_key"
        self.weather_api = WeatherAPI(self.api_key)

    def test_init(self):
        """Test WeatherAPI initialization"""
        assert self.weather_api.api_key == "test_api_key"
        assert self.weather_api.base_url == "https://api.weatherapi.com/v1/forecast.json"

    @patch('core.weather_api.requests.get')
    def test_get_tomorrow_forecast_success(self, mock_get):
        """Test successful API call"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "forecast": {
                "forecastday": [
                    {"date": "2025-09-02"},
                    {
                        "date": "2025-09-03",
                        "day": {
                            "mintemp_c": 15.0,
                            "maxtemp_c": 25.0,
                            "avghumidity": 65,
                            "maxwind_kph": 12.5
                        },
                        "hour": [
                            {"wind_dir": "N"}, {"wind_dir": "NE"}, {"wind_dir": "E"}
                        ]
                    }
                ]
            }
        }
        mock_get.return_value = mock_response

        result = self.weather_api.get_tomorrow_forecast("Madrid")

        assert result is not None
        assert result["date"] == "2025-09-03"
        assert result["min_temp"] == 15.0
        assert result["max_temp"] == 25.0
        assert result["humidity"] == 65
        assert result["wind_speed"] == 12.5
        assert result["wind_direction"] == "NE"

        mock_get.assert_called_once_with(
            "https://api.weatherapi.com/v1/forecast.json",
            params={
                "key": "test_api_key",
                "q": "Madrid",
                "days": 2,
                "aqi": "no",
                "alerts": "no",
            },
            timeout=10,
        )

    @patch('core.weather_api.requests.get')
    def test_get_tomorrow_forecast_http_error(self, mock_get):
        """Test HTTP error handling"""
        mock_get.side_effect = requests.HTTPError("API Error")

        result = self.weather_api.get_tomorrow_forecast("Madrid")

        assert result is None

    @patch('core.weather_api.requests.get')
    def test_get_tomorrow_forecast_insufficient_data(self, mock_get):
        """Test handling of insufficient forecast data"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "forecast": {
                "forecastday": [{"date": "2025-09-02"}]
            }
        }
        mock_get.return_value = mock_response

        result = self.weather_api.get_tomorrow_forecast("Madrid")

        assert result is None

    @patch('core.weather_api.requests.get')
    def test_get_tomorrow_forecast_no_hours_data(self, mock_get):
        """Test handling when no hourly data available"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "forecast": {
                "forecastday": [
                    {"date": "2025-09-02"},
                    {
                        "date": "2025-09-03",
                        "day": {
                            "mintemp_c": 15.0,
                            "maxtemp_c": 25.0,
                            "avghumidity": 65,
                            "maxwind_kph": 12.5
                        },
                        "hour": []
                    }
                ]
            }
        }
        mock_get.return_value = mock_response

        result = self.weather_api.get_tomorrow_forecast("Madrid")

        assert result is not None
        assert result["wind_direction"] == "N/A"

    @patch('core.weather_api.requests.get')
    def test_get_tomorrow_forecast_json_error(self, mock_get):
        """Test JSON parsing error handling"""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        result = self.weather_api.get_tomorrow_forecast("Madrid")

        assert result is None