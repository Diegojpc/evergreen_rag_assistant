from pydantic import BaseModel
import datetime as dt
from typing import List
import random as rand

from app.models.weather import WeatherForecast, WeatherDailyForecast


class WeatherInformationService(BaseModel):
    """
    A service class that provides weather forecast information.

    This service generates simulated weather forecasts for a given location.
    The forecasts include daily weather data such as temperature, precipitation,
    humidity, and wind speed for a specified number of days.

    Attributes:
        total_forecast_days (int): The number of days to generate forecasts for.
                                  Defaults to 7 days.
    """

    total_forecast_days: int = 7

    def get_weather_forecast(self, location: str) -> WeatherForecast | None:
        """
        Generates a weather forecast for the specified location.

        This method creates a simulated weather forecast with random but realistic
        weather data for each day in the forecast period. The data includes
        temperature ranges, precipitation amounts, humidity levels, and wind speeds.

        Args:
            location (str): The location for which to generate the weather forecast.

        Returns:
            WeatherForecast | None: A WeatherForecast object containing:
                - created_at: The timestamp when the forecast was generated
                - location: The location the forecast is for
                - daily: A list of daily forecasts containing:
                    - date: The forecast date
                    - max_temperature_c: Maximum temperature in Celsius
                    - min_temperature_c: Minimum temperature in Celsius
                    - precipitation_mm: Precipitation amount in millimeters
                    - precipitation_prob: Probability of precipitation (0-1)
                    - humidity_relative_avg: Average relative humidity percentage
                    - wind_speed_kmh: Wind speed in kilometers per hour
        """

        if rand.randint(0, 9) >= 7:
            return None

        created_at: dt.datetime = dt.datetime.now()

        daily_forecasts: List[WeatherDailyForecast] = []

        for i in range(self.total_forecast_days):
            date: dt.date = (created_at + dt.timedelta(days=i)).date()
            max_temperature_c: float = rand.uniform(22.0, 32.0)
            min_temperature_c: float = rand.uniform(10.0, 18.0)
            precipitation_mm: float = (
                rand.uniform(0.0, 15.0) if rand.random() < 0.4 else 0.0
            )
            precipitation_prob: float = rand.random()
            humidity_relative_avg: float = rand.uniform(50.0, 90.0)
            wind_speed_kmh: float = rand.uniform(5.0, 25.0)

            daily_forecast: WeatherDailyForecast = WeatherDailyForecast(
                date=date,
                max_temperature_c=max_temperature_c,
                min_temperature_c=min_temperature_c,
                precipitation_mm=precipitation_mm,
                precipitation_prob=precipitation_prob,
                humidity_relative_avg=humidity_relative_avg,
                wind_speed_kmh=wind_speed_kmh,
            )

            daily_forecasts.append(daily_forecast)

        return WeatherForecast(
            created_at=created_at, location=location, daily=daily_forecasts
        )
