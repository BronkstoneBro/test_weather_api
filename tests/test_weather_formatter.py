from core.weather_formatter import WeatherFormatter, CITIES


class TestWeatherFormatter:
    """Test cases for WeatherFormatter class"""

    def setup_method(self):
        """Setup test instance"""
        self.formatter = WeatherFormatter()

    def test_cities_constant(self):
        """Test CITIES constant"""
        expected_cities = ["Chisinau", "Madrid", "Kyiv", "Amsterdam"]
        assert CITIES == expected_cities

    def test_headers_constant(self):
        """Test HEADERS constant"""
        expected_headers = [
            "City",
            "Min Temp",
            "Max Temp",
            "Humidity",
            "Wind Speed",
            "Wind Direction",
        ]
        assert WeatherFormatter.HEADERS == expected_headers

    def test_format_weather_table_success(self):
        """Test successful table formatting"""
        weather_data = {
            "Chisinau": {
                "date": "2025-09-03",
                "min_temp": 12.5,
                "max_temp": 23.8,
                "humidity": 72,
                "wind_speed": 8.3,
                "wind_direction": "NW",
            },
            "Madrid": {
                "date": "2025-09-03",
                "min_temp": 18.2,
                "max_temp": 28.1,
                "humidity": 45,
                "wind_speed": 15.7,
                "wind_direction": "SW",
            },
        }

        result = self.formatter.format_weather_table(weather_data)

        assert "Weather Forecast for 2025-09-03" in result
        assert "Chisinau" in result
        assert "Madrid" in result
        assert "12.5°C" in result
        assert "23.8°C" in result
        assert "72%" in result
        assert "8.3 kph" in result
        assert "NW" in result

    def test_format_weather_table_empty_data(self):
        """Test formatting with empty data"""
        result = self.formatter.format_weather_table({})
        assert result == "No data to display"

    def test_format_weather_table_no_valid_data(self):
        """Test formatting when all city data is None"""
        weather_data = {
            "Chisinau": None,
            "Madrid": None,
            "Kyiv": None,
            "Amsterdam": None,
        }

        result = self.formatter.format_weather_table(weather_data)
        assert result == "No data to display"

    def test_format_weather_table_partial_data(self):
        """Test formatting with some cities having None data"""
        weather_data = {
            "Chisinau": {
                "date": "2025-09-03",
                "min_temp": 12.5,
                "max_temp": 23.8,
                "humidity": 72,
                "wind_speed": 8.3,
                "wind_direction": "NW",
            },
            "Madrid": None,
            "Kyiv": None,
            "Amsterdam": {
                "date": "2025-09-03",
                "min_temp": 10.1,
                "max_temp": 19.4,
                "humidity": 68,
                "wind_speed": 12.0,
                "wind_direction": "W",
            },
        }

        result = self.formatter.format_weather_table(weather_data)

        assert "Weather Forecast for 2025-09-03" in result
        assert "Chisinau" in result
        assert "Amsterdam" in result
        assert "N/A" in result

    def test_format_weather_table_temperature_formatting(self):
        """Test temperature formatting precision"""
        weather_data = {
            "Madrid": {
                "date": "2025-09-03",
                "min_temp": 15.666,
                "max_temp": 25.333,
                "humidity": 67.8,
                "wind_speed": 10.999,
                "wind_direction": "E",
            }
        }

        result = self.formatter.format_weather_table(weather_data)

        assert "15.7°C" in result
        assert "25.3°C" in result
        assert "68%" in result
        assert "11.0 kph" in result
