from dataclasses import dataclass
from typing import Optional


@dataclass
class WeatherData:
    """Weather forecast data model"""

    city: str
    date: str
    min_temp: float
    max_temp: float
    humidity: int
    wind_speed: float
    wind_direction: str

    def __post_init__(self):
        """Validate data after initialization"""
        if self.min_temp > self.max_temp:
            raise ValueError(
                f"Min temp ({self.min_temp}) cannot be greater than max temp ({self.max_temp})"
            )
        if not (0 <= self.humidity <= 100):
            raise ValueError(f"Humidity ({self.humidity}) must be between 0 and 100")
        if self.wind_speed < 0:
            raise ValueError(f"Wind speed ({self.wind_speed}) cannot be negative")


@dataclass
class WeatherForecastResult:
    """Result of weather forecast request"""

    success: bool
    data: Optional[WeatherData] = None
    error_message: Optional[str] = None
